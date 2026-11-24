"""Regression tests for skills/sdd/scripts/sdd-check.py. Each test builds a throwaway project in tmp_path."""
import re
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "skills/sdd/scripts/sdd-check.py"
DATE = "2026-11-24"

SPEC = """# Spec 01. Count

- Status: Approved (2026-11-20).

| ID | Level | Sentence |
|---|---|---|
| AC-1.1 | MUST | The tool **MUST** print the count. |
| AC-1.2 | MUST NOT | The tool **MUST NOT** print a stack trace. |
"""
DOMAIN = """# Domain 01

| ID | Level | Rule |
|---|---|---|
| R1 | MUST | A count **MUST** be zero or more. |
"""
PLAN = """# Plan 01. Count

## Task order

| # | Task | What to verify |
|---|---|---|
| 1 | Count. | R1 |
| 2 | Print. | AC-1.1, AC-1.2 |

## End condition
- All 2 acceptance criteria have a passing test.
- All 1 rules have a passing test.
"""
TESTS = """def test_ac1_1_prints():
    pass

def test_ac1_2_no_trace():
    pass

def test_r1_non_negative():
    pass
"""


def write(root, files):
    for name, text in files.items():
        p = Path(root) / name
        p.parent.mkdir(parents=True, exist_ok=True)
        (p.write_bytes if isinstance(text, bytes) else p.write_text)(text)


def key_path(key):
    """docs__spec__01_count_md -> docs/spec/01-count.md: the last _ is the dot, a leading number takes a dash."""
    *folders, name = key.split("__")
    stem, suffix = name.rsplit("_", 1)
    return "/".join(folders + [re.sub(r"^(\d+)_", r"\1-", stem) + "." + suffix])


def project(tmp_path, **over):
    files = {"docs/spec/01-count.md": SPEC, "docs/domain/01-count.md": DOMAIN,
             "docs/plan/01-count.md": PLAN, "tests/test_count.py": TESTS}
    files.update({key_path(k): v for k, v in over.items()})
    write(tmp_path, {k: v for k, v in files.items() if v is not None})
    return tmp_path


def run(cwd, *args, python=sys.executable):
    r = subprocess.run([python, str(SCRIPT), *args], cwd=cwd, capture_output=True, text=True, encoding="utf-8")
    assert "Traceback" not in r.stderr, r.stderr
    return r.returncode, r.stdout


def git(cwd, *args):
    subprocess.run(["git", "-c", "user.email=t@t", "-c", "user.name=t", *args], cwd=cwd, check=True, capture_output=True)


def repo(path):
    path.mkdir(parents=True, exist_ok=True)
    git(path, "init", "-q", "-b", "main")
    return path


def commit(cwd, msg="c"):
    git(cwd, "add", "-A")
    git(cwd, "commit", "-q", "-m", msg)


# ---------------------------------------------------------------- trace

def test_trace_baseline_passes(tmp_path):
    code, out = run(project(tmp_path), "trace")
    assert code == 0, out


def test_trace_missing_test_fails(tmp_path):
    code, out = run(project(tmp_path, tests__test_count_py="def test_ac1_1_x(): pass\ndef test_r1_x(): pass\n"), "trace")
    assert code == 1 and "AC-1.2" in out


def test_trace_not_in_plan_fails(tmp_path):
    code, out = run(project(tmp_path, docs__plan__01_count_md=PLAN.replace("R1", "-")), "trace", "--no-tests")
    assert code == 1 and "not in the plan: R1" in out


def test_trace_unknown_id_in_plan_fails(tmp_path):
    code, out = run(project(tmp_path, docs__plan__01_count_md=PLAN + "\nAC-1.9\n"), "trace", "--no-tests")
    assert code == 1 and "does not exist: AC-1.9" in out


def test_trace_dangling_reference_in_spec_fails(tmp_path):
    code, out = run(project(tmp_path, docs__spec__01_count_md=SPEC + "\nSee AC-1.7.\n"), "trace", "--no-tests")
    assert code == 1 and "does not exist: AC-1.7" in out


def test_trace_duplicate_id_fails(tmp_path):
    spec = SPEC + "| AC-1.1 | MUST | Again **MUST**. |\n"
    code, out = run(project(tmp_path, docs__spec__01_count_md=spec), "trace", "--no-tests")
    assert code == 1 and "defined twice: AC-1.1" in out


def test_trace_bad_level_cell_fails(tmp_path):
    spec = SPEC.replace("| AC-1.1 | MUST |", "| AC-1.1 | must |")
    code, out = run(project(tmp_path, docs__spec__01_count_md=spec), "trace", "--no-tests")
    assert code == 1 and '"must"' in out


def test_trace_sources_table_is_not_a_definition(tmp_path):
    spec = SPEC + "\n## Sources\n\n| ID | Source |\n|---|---|\n| AC-1.1 | the user |\n| AC-1.2 | the user |\n"
    code, out = run(project(tmp_path, docs__spec__01_count_md=spec), "trace")
    assert code == 0, out


def test_trace_row_without_leading_pipe_and_bom(tmp_path):
    spec = "\ufeff" + SPEC.replace("| AC-1.2 | MUST NOT |", "AC-1.2 | MUST NOT |")
    code, out = run(project(tmp_path, docs__spec__01_count_md=spec.encode("utf-8")), "trace")
    assert code == 0, out


def test_trace_ids_in_code_blocks_are_ignored(tmp_path):
    spec = SPEC + "\n```\n| AC-1.1 | MUST | example |\n```\n~~~\nAC-1.9\n~~~\n<!-- AC-1.8 -->\n"
    code, out = run(project(tmp_path, docs__spec__01_count_md=spec), "trace")
    assert code == 0, out


def test_trace_comment_and_import_do_not_count(tmp_path):
    tests = "from sklearn.metrics import r2_score\n# covers ac1_1_ ac1_2_ r1_\ndef test_nothing(): pass\n"
    code, out = run(project(tmp_path, tests__test_count_py=tests), "trace")
    assert code == 1 and "0/3" in out


def test_trace_string_names_and_mjs(tmp_path):
    tests = "test('AC-1.1 prints', () => {});\nit('AC-1.2: no trace', () => {});\ndescribe('R1 count', () => {});\n"
    code, out = run(project(tmp_path, tests__test_count_py=None, test__count_test_mjs=tests), "trace")
    assert code == 0, out


def test_trace_jvm_test_file(tmp_path):
    java = "class CountTests {\n  @Test void ac1_1_prints() {}\n  @Test void ac1_2_x() {}\n  @Test void r1_x() {}\n}\n"
    code, out = run(project(tmp_path, tests__test_count_py=None, src__test__java__CountTests_java=java), "trace")
    assert code == 0, out


def test_trace_orphan_test_fails(tmp_path):
    code, out = run(project(tmp_path, tests__test_count_py=TESTS + "def test_ac1_4_gone(): pass\n"), "trace")
    assert code == 1 and "defined nowhere: AC-1.4" in out


def test_trace_pin_tests_are_ignored(tmp_path):
    code, out = run(project(tmp_path, tests__test_count_py=TESTS + "def test_pin_ac1_9_old(): pass\n"), "trace")
    assert code == 0, out


def test_trace_replaced_id(tmp_path):
    spec = SPEC.replace("| AC-1.2 | MUST NOT | The", "| AC-1.2 | REPLACED | Replaced by AC-1.3 (2026-11-24). The") \
        + "| AC-1.3 | MUST NOT | The tool **MUST NOT** print a trace or a path. |\n"
    plan = PLAN.replace("AC-1.1, AC-1.2", "AC-1.1, AC-1.3. AC-1.2 replaced")
    files = dict(docs__spec__01_count_md=spec, docs__plan__01_count_md=plan)
    # the old test still names the replaced ID
    code, out = run(project(tmp_path, **files), "trace")
    assert code == 1 and "AC-1.2, which is REPLACED" in out and "AC-1.3" in out
    write(tmp_path, {"tests/test_count.py": TESTS.replace("ac1_2_", "ac1_3_")})
    code, out = run(tmp_path, "trace")
    assert code == 0, out


def test_trace_removed_id_needs_no_plan_or_test(tmp_path):
    spec = SPEC.replace("| AC-1.2 | MUST NOT | The", "| AC-1.2 | REMOVED | Removed (2026-11-24): not needed. The")
    plan = PLAN.replace("AC-1.1, AC-1.2", "AC-1.1").replace("All 2 acceptance", "All 1 acceptance")
    tests = TESTS.replace("def test_ac1_2_no_trace():\n    pass\n", "")
    code, out = run(project(tmp_path, docs__spec__01_count_md=spec, docs__plan__01_count_md=plan, tests__test_count_py=tests), "trace")
    assert code == 0, out


def test_trace_end_condition_count(tmp_path):
    code, out = run(project(tmp_path, docs__plan__01_count_md=PLAN.replace("All 2 acceptance", "All 3 acceptance")), "trace")
    assert code == 1 and "end condition says 3" in out


def test_trace_korean_end_condition_and_range_with_particle(tmp_path):
    plan = PLAN.replace("AC-1.1, AC-1.2", "AC-1.1～AC-1.2를 만든다").replace("R1 |", "R1~R1을 |") \
        .replace("All 2 acceptance criteria", "인수 조건 2개").replace("All 1 rules", "규칙 1개")
    code, out = run(project(tmp_path, docs__plan__01_count_md=plan), "trace")
    assert code == 0, out


def test_trace_range_at_sentence_end(tmp_path):
    plan = PLAN.replace("AC-1.1, AC-1.2", "AC-1.1 ~ AC-1.2.")
    code, out = run(project(tmp_path, docs__plan__01_count_md=plan), "trace")
    assert code == 0, out


def test_trace_adr_rules(tmp_path):
    adr = "# ADR-0001\n\n## Decision\n\n1. The tool **MUST** be one file.\n2. Plain text, no keyword.\n\n## Consequences\n\n1. Fast **MUST**.\n"
    plan = PLAN + "- All 1 ADR rules have a passing test.\n\nInput: ADR-0001\n"
    code, out = run(project(tmp_path, docs__adr__0001_one_file_md=adr, docs__plan__01_count_md=plan), "trace")
    assert code == 1 and "adr0001_1_" in out and "ADR-0001.2" not in out
    write(tmp_path, {"tests/test_adr.py": "def test_adr0001_1_one_file(): pass\n"})
    code, out = run(tmp_path, "trace")
    assert code == 0, out


def test_trace_partial_run(tmp_path):
    tests = "def test_r1_non_negative(): pass\n"
    project(tmp_path, tests__test_count_py=tests)
    code, out = run(tmp_path, "trace", "--plan", "01", "--upto", "1")
    assert code == 0 and "not built yet 2" in out, out
    code, out = run(tmp_path, "trace", "--plan", "01", "--upto", "2")
    assert code == 1


def test_trace_no_plan_with_no_tests_is_not_a_failure(tmp_path):
    code, out = run(project(tmp_path, docs__plan__01_count_md=None), "trace", "--no-tests")
    assert code == 0, out


def test_trace_tests_folder_may_repeat(tmp_path):
    files = dict(tests__test_count_py=None, a__test_a_py="def test_ac1_1_x(): pass\ndef test_ac1_2_x(): pass\n",
                 b__test_b_py="def test_r1_x(): pass\n")
    code, out = run(project(tmp_path, **files), "trace", "--tests", "a", "--tests", "b")
    assert code == 0, out


def test_trace_whole_project_when_no_test_folder(tmp_path):
    files = dict(tests__test_count_py=None, pkg__count_test_py=TESTS, node_modules__x__test_y_py="def test_ac1_9_x(): pass\n")
    code, out = run(project(tmp_path, **files), "trace")
    assert code == 0, out


def test_trace_binary_fixture_is_skipped(tmp_path):
    code, out = run(project(tmp_path, tests__test_clip_ts=b"\x47\x00\xff\xfe"), "trace")
    assert code == 0, out


def test_trace_task_cell_forms_and_bad_upto(tmp_path):
    tests = "def test_r1_non_negative(): pass\n"
    for cell in ("1.", "Task 1", "작업 1"):
        project(tmp_path, tests__test_count_py=tests, docs__plan__01_count_md=PLAN.replace("| 1 |", f"| {cell} |"))
        code, out = run(tmp_path, "trace", "--plan", "01", "--upto", "1")
        assert code == 0 and "1/1" in out, (cell, out)
    assert run(tmp_path, "trace", "--plan", "01", "--upto", "0")[0] == 2
    write(tmp_path, {"docs/plan/01-count.md": PLAN.replace("| 1 |", "| - |").replace("| 2 |", "| - |")})
    assert run(tmp_path, "trace", "--plan", "01", "--upto", "1")[0] == 2
    write(tmp_path, {"docs/plan/01-count.md": PLAN, "docs/plan/01-old.md": PLAN})
    code, out = run(tmp_path, "trace", "--plan", "01", "--upto", "1")
    assert code == 2 and "2 plans" in out


def test_trace_comments_docstrings_helpers_and_dot_test_do_not_count(tmp_path):
    tests = ('"""\ndef test_ac1_1_x(): pass\n"""\n# def test_ac1_2_x(): pass\ndef make_r1_data(): pass\n'
             "// it('AC-1.2 later', () => {})\ncheck.test('R1 ok')\n/* test('AC-1.1 x') */\ndef test_nothing(): pass\n")
    code, out = run(project(tmp_path, tests__test_count_py=tests), "trace")
    assert code == 1 and "0/3" in out, out


def test_trace_jvm_name_outside_test_folder_does_not_count(tmp_path):
    files = dict(tests__test_count_py=None, pkg__count_test_py="def test_ac1_1_x(): pass\ndef test_ac1_2_x(): pass\n",
                 src__ApiSpec_ts="function r1_validate() {}\n")
    code, out = run(project(tmp_path, **files), "trace")
    assert code == 1 and "r1_" in out


def test_trace_pin_only_as_prefix(tmp_path):
    code, out = run(project(tmp_path, tests__test_count_py=TESTS + "def test_ac1_9_pin_x(): pass\n"), "trace")
    assert code == 1 and "defined nowhere: AC-1.9" in out


def test_trace_end_condition_forms(tmp_path):
    for ac, r in (("All **2** acceptance criteria", "All\u00a01 rules"), ("인수조건 2개", "규칙 1 개")):
        plan = PLAN.replace("All 2 acceptance criteria", ac).replace("All 1 rules", r)
        code, out = run(project(tmp_path, docs__plan__01_count_md=plan), "trace")
        assert code == 0, (ac, out)
    plan = PLAN.replace("All 2 acceptance criteria", "ADR규칙 0개")
    code, out = run(project(tmp_path, docs__plan__01_count_md=plan), "trace")
    assert code == 0, out


def test_trace_plan_without_end_condition_fails(tmp_path):
    code, out = run(project(tmp_path, docs__plan__01_count_md=PLAN.split("## End condition")[0]), "trace")
    assert code == 1 and "plan 01 has no end condition" in out


def test_trace_backtick_id_is_not_cross_checked(tmp_path):
    code, out = run(project(tmp_path, docs__plan__01_count_md=PLAN + "\nStore in `Cloudflare R2`.\n"), "trace")
    assert code == 0, out


def test_trace_conflict_marker_in_plan_fails(tmp_path):
    code, out = run(project(tmp_path, docs__plan__01_count_md=PLAN + "<<<<<<< HEAD\n=======\n>>>>>>> x\n"), "trace")
    assert code == 1 and "conflict" in out


def test_trace_docs_elsewhere_finds_tests_at_its_parent(tmp_path):
    project(tmp_path / "proj")
    code, out = run(tmp_path, "trace", "--docs", "proj/docs")
    assert code == 0 and "proj/tests" in out, out


ADR_TABLE = "# ADR-0001\n\n- Status: Accepted.\n\n## Decision Outcome\n\n| # | Level | Rule |\n|---|---|---|\n" \
            "| 1 | MUST | The tool **MUST** be one file. |\n| 2 | MUST NOT | It **MUST NOT** import x. |\n"


def test_trace_adr_table_rules_define_ids_without_adr_end_condition(tmp_path):
    files = dict(docs__adr__0001_one_md=ADR_TABLE, docs__plan__01_count_md=PLAN + "\nInput: ADR-0001\n",
                 tests__test_adr_py="def test_adr0001_2_x(): pass\n")
    code, out = run(project(tmp_path, **files), "trace")
    assert code == 0 and "2 ADR rules (2 with no test required" in out, out


def test_trace_adr_rules_need_tests_with_adr_end_condition(tmp_path):
    plan = PLAN + "- All 2 ADR rules have a passing test.\n\nInput: ADR-0001\n"
    files = dict(docs__adr__0001_one_md=ADR_TABLE.replace("## Decision Outcome", "## 결정 사항"), docs__plan__01_count_md=plan,
                 tests__test_adr_py="def test_adr0001_2_x(): pass\n")
    code, out = run(project(tmp_path, **files), "trace")
    assert code == 1 and "no test with `adr0001_1_`" in out and "ADR-0001.2" not in out, out


def test_trace_replaced_adr_retires_its_rules(tmp_path):
    plan = PLAN + "- All 0 ADR rules have a passing test.\n\nInput: ADR-0001\n"
    for status in ("Replaced by ADR-0002 (2026-11-24).", "ADR-0002로 대체 (2026-11-24)."):
        adr = ADR_TABLE.replace("Accepted.", status)
        code, out = run(project(tmp_path, docs__adr__0001_one_md=adr, docs__plan__01_count_md=plan), "trace")
        assert code == 0 and "replaced or removed" in out, (status, out)


def test_trace_adr_repeated_number_and_unreadable_rules(tmp_path):
    adr = "# ADR-0001\n\n## Decision\n\n1. The tool **MUST** be one file.\n1. It **MUST** be fast.\n"
    code, out = run(project(tmp_path, docs__adr__0001_one_md=adr), "trace", "--no-tests")
    assert code == 1 and "more than once" in out
    adr = "# ADR-0001\n\n## Decision\n\n- The tool **MUST** be one file.\n"
    code, out = run(project(tmp_path, docs__adr__0001_one_md=adr), "trace", "--no-tests")
    assert "WARNING" in out and "no rule the checker can read" in out


def test_trace_cp949_spec_is_inconclusive(tmp_path):
    spec = SPEC.replace("print the count", "개수를 출력").encode("cp949")
    code, out = run(project(tmp_path, docs__spec__01_count_md=spec), "trace")
    assert code == 2 and "cannot read" in out and "01-count.md" in out


# ------------------------------------------------------------- keywords

KO = """# 명세 01

| ID | Level | 문장 |
|---|---|---|
| AC-1.1 | MUST | 시스템은 점수를 **반드시 출력해야 한다**. 함수 있음, 인수 없이. |
| AC-1.2 | MUST NOT | 시스템은 비밀번호를 **절대 저장해서는 안 된다**. |
"""


def kw(tmp_path, text, name="docs/spec/01.md"):
    write(tmp_path, {name: text})
    return run(tmp_path, "keywords")


def test_keywords_baseline_korean_nouns_with_su(tmp_path):
    code, out = kw(tmp_path, KO)
    assert code == 0, out


def test_keywords_su_after_space_fails_and_unspaced_is_a_documented_limit(tmp_path):
    code, out = kw(tmp_path, KO + "\n입력을 읽을 수 없다.\n")
    assert code == 1 and "수 있다/없다" in out
    # behaviour changed in round 2 (C6): the ㄹ heuristic is gone, so an unspaced 읽을수 is not caught
    code, out = kw(tmp_path, KO + "\n읽을수 없다.\n")
    assert code == 0, out


def test_keywords_su_particles_fail(tmp_path):
    for s in ("볼 수가 없다", "볼 수도 있다", "볼 수는 없다"):
        assert kw(tmp_path, KO + f"\n{s}.\n")[0] == 1, s


def test_keywords_nouns_ending_in_su_pass(tmp_path):
    code, out = kw(tmp_path, KO + "\n실수 없이, 홀수 없는, 근무 일수 없음.\n")
    assert code == 0, out


def test_keywords_prohibition_forms_in_must_row_fail(tmp_path):
    for s in ("**반드시** 저장하지 않아야 한다", "**반드시 저장하면 안 된다**", "**반드시 저장을 금지한다**"):
        code, out = kw(tmp_path, KO.replace("**반드시 출력해야 한다**", s))
        assert code == 1 and "use MUST NOT" in out, s
    for s in ("**MUST never** print", "**MUST** never print", "**MUST** NOT print"):
        code, out = kw(tmp_path, SPEC.replace("**MUST** print", s))
        assert code == 1 and "use MUST NOT" in out, s


def test_keywords_korean_must_not_needs_jeoldae(tmp_path):
    code, out = kw(tmp_path, KO.replace("**절대 저장해서는 안 된다**", "**MUST NOT** 저장"))
    assert code == 1 and "절대" in out
    code, out = kw(tmp_path, KO.replace("**절대 저장해서는 안 된다**", "**절대** 저장하면 **안 된다**"))
    assert code == 0, out


def test_keywords_level_only_from_sentence_cell(tmp_path):
    code, out = kw(tmp_path, KO + "| AC-1.3 | MUST | 도구는 출력한다. | **반드시** 출처 |\n")
    assert code == 1 and "AC-1.3" in out


def test_keywords_how_to_read_heading_is_exact(tmp_path):
    for h in ("## 값을 읽는 법", "## How to read the sensor", "# 이 문서를 읽는 법"):
        code, out = kw(tmp_path, KO + f"\n{h}\n\n반드시 쓴다.\n")
        assert code == 1, h


def test_keywords_status_continuation_does_not_hide_table_rows(tmp_path):
    text = "# 명세\n\n- 상태: 승인.\n  | AC-1.2 | MUST | 도구는 저장한다. |\n" + KO.split("\n", 1)[1]
    code, out = kw(tmp_path, text)
    assert code == 1 and "AC-1.2" in out


def test_keywords_retired_rows_are_not_counted(tmp_path):
    code, out = kw(tmp_path, SPEC + "| AC-1.3 | REPLACED | Replaced by AC-1.1. The tool **MUST** x. |\n")
    assert code == 0 and "MUST 1," in out, out


def test_keywords_heading_is_checked(tmp_path):
    code, out = kw(tmp_path, KO + "\n## 계산할 수 없는 입력\n")
    assert code == 1 and ":8" in out


def test_keywords_bold_of_another_level_fails(tmp_path):
    code, out = kw(tmp_path, KO.replace("**반드시 출력해야 한다**", "**반드시 볼 수 있다**"))
    assert code == 1 and "MAY" in out


def test_keywords_korean_must_not_needs_prohibition_form(tmp_path):
    code, out = kw(tmp_path, KO.replace("**절대 저장해서는 안 된다**", "**절대 저장하지 않는다**"))
    assert code == 1 and "절대 …서는 안 된다" in out


def test_keywords_must_row_with_prohibition_fails(tmp_path):
    code, out = kw(tmp_path, KO.replace("**반드시 출력해야 한다**", "**반드시 저장하지 않아야 한다**"))
    assert code == 1 and "prohibition" in out


def test_keywords_english_must_lower_not_fails(tmp_path):
    code, out = kw(tmp_path, SPEC.replace("**MUST NOT** print", "**MUST** not print").replace("| MUST NOT |", "| MUST |"))
    assert code == 1 and "MUST not" in out


def test_keywords_particle_after_must(tmp_path):
    code, out = kw(tmp_path, KO + "\n설명: MUST를 쓴다.\n")
    assert code == 1 and '"MUST" is not bold' in out


def test_keywords_korean_quotes_exempt(tmp_path):
    code, out = kw(tmp_path, KO + "\n오류 문구는 ‘읽을 수 없다’와 「쓸 수 없다」와 『MUST』이다.\n")
    assert code == 0, out


def test_keywords_underscore_bold(tmp_path):
    code, out = kw(tmp_path, SPEC.replace("**MUST** print", "__MUST__ print"))
    assert code == 0, out


def test_keywords_status_continuation_and_how_to_read(tmp_path):
    text = KO.replace("# 명세 01\n", "# 명세 01\n\n- 상태: 승인. 수정 (2026-11-24):\n  옛 문구 '줄 수 있다'를 고쳤다. 읽을 수 없다\n\n"
                      "## 이 문서를 읽는 법\n\nMUST는 반드시다.\n\n### 키워드\n\n수 있다는 MAY다.\n\n## 요구\n")
    code, out = kw(tmp_path, text)
    assert code == 0, out


def test_keywords_comments_and_tilde_fences_skipped(tmp_path):
    code, out = kw(tmp_path, SPEC + "\n~~~\nMUST\n~~~\n<!-- this MUST\nbe split -->\n")
    assert code == 0, out


def test_keywords_zero_keywords_is_inconclusive(tmp_path):
    code, out = kw(tmp_path, "# Spec\n")
    assert code == 2


def test_keywords_conflict_markers_fail(tmp_path):
    code, out = kw(tmp_path, SPEC + "<<<<<<< HEAD\nx\n=======\ny\n>>>>>>> other\n")
    assert code == 1 and "conflict" in out


def test_keywords_nfd_hangul(tmp_path):
    import unicodedata
    code, out = kw(tmp_path, unicodedata.normalize("NFD", KO))
    assert code == 0, out


def test_keywords_missing_file_is_inconclusive(tmp_path):
    code, out = run(tmp_path, "keywords", "nope.md")
    assert code == 2 and "nope.md" in out


# -------------------------------------------------------------- journal

J1 = "# 2026-11-24\n\n## Step 1\n\nRequest: a\n**Done:** a\n"
J2 = J1 + "\n## Step 2\n\nRequest: b\n**Done:** b\n"
J3 = J2 + "\n## Step 3\n\nRequest: merge\n**Done:** merged\n"


def jrepo(path, journal=J1):
    repo(path)
    write(path, {"app.py": "x = 1\n", f"docs/journal/{DATE}.md": journal})
    commit(path)
    return path


def journal(cwd, *extra):
    return run(cwd, "journal", "--date", DATE, *extra)


def test_journal_working_tree_with_new_step_passes(tmp_path):
    p = jrepo(tmp_path)
    write(p, {"app.py": "x = 2\n", f"docs/journal/{DATE}.md": J2})
    code, out = journal(p)
    assert code == 0, out


def test_journal_working_tree_without_journal_fails(tmp_path):
    p = jrepo(tmp_path)
    write(p, {"app.py": "x = 2\n"})
    assert journal(p)[0] == 1


def test_journal_staged_set_must_hold_journal(tmp_path):
    p = jrepo(tmp_path)
    write(p, {"app.py": "x = 2\n", f"docs/journal/{DATE}.md": J2})
    git(p, "add", "app.py")
    code, out = journal(p)
    assert code == 1 and "staged" in out


def test_journal_no_new_step_fails(tmp_path):
    p = jrepo(tmp_path)
    write(p, {"app.py": "x = 2\n", f"docs/journal/{DATE}.md": J1 + "more\n"})
    code, out = journal(p)
    assert code == 1 and "no new" in out


def test_journal_edited_past_step_fails(tmp_path):
    p = jrepo(tmp_path)
    write(p, {"app.py": "x = 2\n", f"docs/journal/{DATE}.md": J2.replace("Request: a", "Request: z")})
    code, out = journal(p)
    assert code == 1 and "past steps" in out


def test_journal_earlier_date_file_alone_fails(tmp_path):
    # behaviour changed in round 2 (C9): an earlier-date file fails only when today's journal did not change
    p = jrepo(tmp_path)
    write(p, {"app.py": "x = 2\n", "docs/journal/2026-11-20.md": "# old\n"})
    code, out = journal(p)
    assert code == 1 and "earlier date" in out


def test_journal_earlier_uncommitted_step_with_today_passes(tmp_path):
    p = jrepo(tmp_path)
    write(p, {"docs/journal/2026-11-20.md": "# 2026-11-20\n\n## Step 1\n\n**Done:** x\n", f"docs/journal/{DATE}.md": J2})
    code, out = journal(p)
    assert code == 0, out


def test_journal_deleted_fails(tmp_path):
    p = jrepo(tmp_path)
    (p / f"docs/journal/{DATE}.md").unlink()
    code, out = journal(p)
    assert code == 1 and "deleted" in out


def test_journal_conflict_markers_fail(tmp_path):
    p = jrepo(tmp_path)
    write(p, {f"docs/journal/{DATE}.md": J2 + "<<<<<<< HEAD\n>>>>>>> x\n"})
    code, out = journal(p)
    assert code == 1 and "conflict" in out


def test_journal_clean_tree_commit_without_journal_fails(tmp_path):
    p = jrepo(tmp_path)
    write(p, {"app.py": "x = 2\n"})
    commit(p)
    code, out = journal(p)
    assert code == 1 and "last commit" in out


def test_journal_clean_tree_commit_with_journal_passes(tmp_path):
    p = jrepo(tmp_path)
    write(p, {"app.py": "x = 2\n", f"docs/journal/{DATE}.md": J2})
    commit(p)
    code, out = journal(p)
    assert code == 0, out


def test_journal_merge_commit_needs_its_own_step(tmp_path):
    # behaviour changed in round 2 (C10): the merge commit needs a step heading neither parent has
    p = jrepo(tmp_path)
    git(p, "checkout", "-q", "-b", "slice")
    write(p, {"app.py": "x = 2\n", f"docs/journal/{DATE}.md": J2})
    commit(p)
    git(p, "checkout", "-q", "main")
    write(p, {"other.py": "y\n"})
    commit(p)
    git(p, "merge", "-q", "--no-ff", "--no-commit", "slice")
    code, out = journal(p)
    assert code == 1 and "neither parent" in out
    write(p, {f"docs/journal/{DATE}.md": J3})
    git(p, "add", "-A")
    code, out = journal(p)
    assert code == 0, out
    git(p, "commit", "-q", "-m", "merge")
    code, out = journal(p)
    assert code == 0, out


def test_journal_merge_commit_without_own_step_fails(tmp_path):
    p = jrepo(tmp_path)
    git(p, "checkout", "-q", "-b", "slice")
    write(p, {"app.py": "x = 2\n", f"docs/journal/{DATE}.md": J2})
    commit(p)
    git(p, "checkout", "-q", "main")
    write(p, {"other.py": "y\n", f"docs/journal/{DATE}.md": J1 + "x\n"})
    commit(p)
    git(p, "merge", "-q", "--no-ff", "-m", "merge", "slice", "-X", "theirs")
    code, out = journal(p)
    assert code == 1 and "neither parent" in out


def test_journal_untracked_only_is_inconclusive(tmp_path):
    p = jrepo(tmp_path)
    write(p, {"README.md": "user's\n", ".omp/skills/x": "y", "__pycache__/a.pyc": "z"})
    code, out = journal(p)
    assert code == 2 and "README.md" in out and ".omp" not in out


def test_journal_harness_folders_are_ignored_but_not_the_rules_file(tmp_path):
    # behaviour changed in round 2 (C12): only skill and agent folders are ignored
    p = jrepo(tmp_path)
    write(p, {".omp/skills/x.md": "y", ".claude/agents/z": "w"})
    code, out = journal(p)
    assert code == 0, out
    write(p, {".omp/AGENTS.md": "rules\n"})
    code, out = journal(p)
    assert code == 2 and ".omp/AGENTS.md" in out


def test_journal_split_code_and_journal_commits_fail(tmp_path):
    p = jrepo(tmp_path)
    write(p, {"app.py": "x = 2\n"})
    commit(p)
    write(p, {f"docs/journal/{DATE}.md": J2})
    commit(p)
    code, out = journal(p)
    assert code == 1 and "committed separately" in out


def test_journal_fenced_heading_is_not_a_step(tmp_path):
    p = jrepo(tmp_path)
    write(p, {"app.py": "x = 2\n", f"docs/journal/{DATE}.md": J1 + "\n```\n## Step 2\n**Done:** x\n```\n"})
    code, out = journal(p)
    assert code == 1 and "no new" in out


def test_journal_new_step_needs_done(tmp_path):
    p = jrepo(tmp_path)
    write(p, {"app.py": "x = 2\n", f"docs/journal/{DATE}.md": J1 + "\n## 스텝 2\n\n요청: b\n"})
    code, out = journal(p)
    assert code == 1 and "**Done**" in out
    write(p, {f"docs/journal/{DATE}.md": J1 + "\n## 스텝 2\n\n**한 일:** b\n"})
    code, out = journal(p)
    assert code == 0 and f"2 steps in docs/journal/{DATE}.md" in out, out


def test_journal_rename_fails(tmp_path):
    p = jrepo(tmp_path)
    git(p, "mv", f"docs/journal/{DATE}.md", "docs/journal/2026-11-23.md")
    code, out = journal(p)
    assert code == 1 and "renamed" in out


def test_journal_crlf_rewrite_is_not_an_edit(tmp_path):
    p = jrepo(tmp_path)
    write(p, {"app.py": "x = 2\n", f"docs/journal/{DATE}.md": J2.replace("\n", "\r\n").encode()})
    code, out = journal(p)
    assert code == 0, out


def test_journal_future_date_is_inconclusive(tmp_path):
    p = jrepo(tmp_path)
    code, out = run(p, "journal", "--date", "2099-01-01")
    assert code == 2 and "future" in out


def test_journal_subfolder_project(tmp_path):
    root = repo(tmp_path / "repo")
    proj = root / "services" / "카운트"
    write(proj, {"app.py": "x\n", f"docs/journal/{DATE}.md": J1})
    write(root, {"other/a.py": "a\n"})
    commit(root)
    write(root, {"other/a.py": "b\n"})  # a change in another project is not this project's
    assert journal(proj)[0] == 0
    write(proj, {"app.py": "y\n", f"docs/journal/{DATE}.md": J2})
    code, out = journal(proj)
    assert code == 0, out
    write(proj, {f"docs/journal/{DATE}.md": J1})
    assert journal(proj)[0] == 1


def test_journal_bad_date_is_inconclusive(tmp_path):
    p = jrepo(tmp_path)
    assert run(p, "journal", "--date", "2026-13-45")[0] == 2
    assert run(p, "journal", "--date", "yesterday")[0] == 2


def test_journal_cp949_journal_is_inconclusive(tmp_path):
    p = jrepo(tmp_path)
    write(p, {f"docs/journal/{DATE}.md": (J2 + "한국어\n").encode("cp949")})
    code, out = journal(p)
    assert code == 2 and "cannot read" in out


def test_journal_not_a_repository(tmp_path):
    assert journal(tmp_path)[0] == 2


# ----------------------------------------------------------------- self

def test_self_passes():
    code, out = run(SCRIPT.parent, "self")
    assert code == 0, out


# ------------------------------------------------------- round 3 fixes


def test_trace_upto_reads_only_the_task_table(tmp_path):
    plan = PLAN + "\n## Risks\n\n| # | Risk |\n|---|---|\n| 1 | slow disk |\n"
    code, out = run(project(tmp_path, docs__plan__01_count_md=plan, tests__test_count_py="def test_ac1_1_x(): pass\n"),
                    "trace", "--plan", "01", "--upto", "1")
    assert code == 1 and "R1" in out, out


def test_trace_plan_mentions_adr_without_adr_end_condition_warns(tmp_path):
    files = dict(docs__adr__0001_one_md=ADR_TABLE, docs__plan__01_count_md=PLAN + "\nInput: ADR-0001\n")
    code, out = run(project(tmp_path, **files), "trace")
    assert code == 0 and "WARNING: plan 01 mentions ADR-0001 (2 rules)" in out, out


def test_trace_adr_heading_forms_and_bold_level_cell(tmp_path):
    plan = PLAN + "- All 1 ADR rule has a passing test.\n\nInput: ADR-0001\n"
    for h in ("# Decision", "### DECISION", "##Decision", "## 결정 (요약)"):
        adr = f"# ADR-0001\n\n{h}\n\n1. The tool **MUST** be one file.\n"
        code, out = run(project(tmp_path, docs__adr__0001_one_md=adr, docs__plan__01_count_md=plan), "trace")
        assert code == 1 and "adr0001_1_" in out, (h, out)
    adr = "# ADR-0001\n\n## 결정\n\n1. 도구는 **반드시** 한 파일이다.\n\n## 결정하지 않은 것\n\n1. **반드시** 나중에.\n"
    code, out = run(project(tmp_path, docs__adr__0001_one_md=adr), "trace", "--no-tests")
    assert "more than once" not in out and "1 ADR rules" in out, out
    adr = "# ADR-0001\n\n## The decision\n\n1. The tool **MUST** be one file.\n"
    code, out = run(project(tmp_path, docs__adr__0001_one_md=adr), "trace", "--no-tests")
    assert "WARNING" in out, out
    adr = ADR_TABLE.replace("| 1 | MUST |", "| 1 | **MUST** |")
    code, out = run(project(tmp_path, docs__adr__0001_one_md=adr), "trace", "--no-tests")
    assert "2 ADR rules" in out, out


def test_trace_adr_replaced_status_forms_and_retired_rule(tmp_path):
    plan = PLAN + "- All 0 ADR rules have a passing test.\n\nInput: ADR-0001\n"
    for status in ("Superseded by ADR-0002.", "replaced by [ADR-0002](0002-x.md)."):
        code, out = run(project(tmp_path, docs__adr__0001_one_md=ADR_TABLE.replace("Accepted.", status),
                                docs__plan__01_count_md=plan), "trace")
        assert code == 0 and "2 of them replaced" in out, (status, out)
    adr = ADR_TABLE.replace("Accepted.", "Accepted. Not replaced by ADR-0002.")
    assert run(project(tmp_path, docs__adr__0001_one_md=adr, docs__plan__01_count_md=plan), "trace")[0] == 1
    adr = "# ADR-0001\n\n## Decision\n\n1. Replaced by ADR-0002.1 (2026-11-24). The tool **MUST** be one file.\n" \
          "2. 삭제 (2026-11-24): 도구는 **반드시** 빠르다.\n3. It **MUST** log.\n"
    code, out = run(project(tmp_path, docs__adr__0001_one_md=adr), "trace", "--no-tests")
    assert "2 of them replaced" in out, out


def test_keywords_must_row_prohibition_by_verb_ending(tmp_path):
    for s in ("**반드시** 저장하지 마라", "**반드시** 저장해서는 아니 된다", "**반드시** 저장하면 안 됩니다", "**반드시** 저장이 불가하다"):
        code, out = kw(tmp_path, KO.replace("**반드시 출력해야 한다**", s))
        assert code == 1 and "use MUST NOT" in out, s
    for s in ("**반드시** 저장되지 않은 항목을 표시한다", "**반드시** 금지어 목록을 읽는다", "**반드시** 보안된 연결로 보낸다",
              "**반드시** 준비가 안 된 항목을 표시한다"):
        assert kw(tmp_path, KO.replace("**반드시 출력해야 한다**", s))[0] == 0, s
    for s in ("print NOT FOUND", "return NOT_FOUND", "reset a count that was never set"):
        assert kw(tmp_path, SPEC.replace("print the count", s))[0] == 0, s
    for s in ("**MUST** never print", "**MUST** NOT print"):
        assert kw(tmp_path, SPEC.replace("**MUST** print the count", s))[0] == 1, s


def test_keywords_korean_must_not_polite_forms(tmp_path):
    for s in ("**절대 저장해서는 안 됩니다**", "**절대 저장하면 안 돼**"):
        assert kw(tmp_path, KO.replace("**절대 저장해서는 안 된다**", s))[0] == 0, s


def test_keywords_su_only_after_rieul_word(tmp_path):
    code, out = kw(tmp_path, KO + "\n행 수가 없으면 0. 항목 수 없음. 수도 없이 재시도.\n")
    assert code == 0, out
    assert kw(tmp_path, KO + "\n볼 수가 없다.\n")[0] == 1


def test_keywords_how_to_read_heading_forms(tmp_path):
    for h in ("## 이 문서를 읽는 법:", "## How to read this document.", "## **이 문서를 읽는 법**"):
        code, out = kw(tmp_path, KO + f"\n{h}\n\n반드시 쓴다.\n")
        assert code == 0, (h, out)


def test_keywords_conflict_markers_fenced_and_bare(tmp_path):
    assert kw(tmp_path, SPEC + "\n```\n<<<<<<< HEAD\n>>>>>>> x\n```\n")[0] == 0
    assert kw(tmp_path, SPEC + "<<<<<<<\nx\n>>>>>>>\n")[0] == 1


def test_keywords_summary_names_docs_folder(tmp_path):
    code, out = kw(tmp_path, SPEC)
    assert "documents in docs" in out, out


def test_trace_end_condition_singular_and_adr_spaces(tmp_path):
    plan = PLAN.replace("AC-1.1, AC-1.2", "AC-1.1").replace("All 2 acceptance criteria", "All 1 acceptance criterion") \
        .replace("All 1 rules", "All 1 rule")
    spec = SPEC.replace("| AC-1.2 | MUST NOT | The", "| AC-1.2 | REMOVED | Removed (2026-11-24). The")
    tests = TESTS.replace("def test_ac1_2_no_trace():\n    pass\n", "")
    code, out = run(project(tmp_path, docs__plan__01_count_md=plan, docs__spec__01_count_md=spec, tests__test_count_py=tests), "trace")
    assert code == 0, out
    code, out = run(project(tmp_path, docs__plan__01_count_md=PLAN + "- ADR  규칙 0개.\n"), "trace")
    assert code == 0, out


def test_trace_hash_comment_only_in_hash_languages_and_function_prefix(tmp_path):
    rust = "#[test] fn ac1_1_x() {}\n#[test] fn ac1_2_x() {}\n#[test] fn r1_x() {}\n"
    code, out = run(project(tmp_path, tests__test_count_py=None, tests__count_test_rs=rust), "trace")
    assert code == 0, out
    js = "function make_r1_data() {}\ntest('AC-1.1 x', () => {});\ntest('AC-1.2 x', () => {});\n"
    code, out = run(project(tmp_path / "js", tests__test_count_py=None, tests__count_test_js=js), "trace")
    assert code == 1 and "R1" in out, out


def test_journal_split_commit_with_extra_doc_fails(tmp_path):
    p = jrepo(tmp_path)
    write(p, {"app.py": "x = 2\n"})
    commit(p)
    write(p, {f"docs/journal/{DATE}.md": J2, "docs/plan/01-c.md": "# p\n"})
    commit(p)
    code, out = journal(p)
    assert code == 1 and "committed separately" in out


def test_journal_uses_last_commit_that_touched_project(tmp_path):
    root = repo(tmp_path / "repo")
    proj = root / "proj"
    write(proj, {"app.py": "x\n", f"docs/journal/{DATE}.md": J1})
    commit(root)
    write(proj, {"app.py": "y\n"})
    commit(root)
    write(root, {"other/a.txt": "z\n"})
    commit(root)
    code, out = journal(proj)
    assert code == 1 and "nothing under" in out, out
