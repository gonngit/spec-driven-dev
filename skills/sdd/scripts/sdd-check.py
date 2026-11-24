#!/usr/bin/env python3
"""Checks for sdd. Written rules turned into checks that can be run.

  trace     are the IDs of the spec, the domain and the ADR rules in the plan and in test names
  keywords  are the RFC 2119 keywords in the documents used by the rules
  journal   does the change being recorded carry the journal
  self      do sdd's index and files agree

Run it from the project root: the folder that holds docs/ (it may be a subfolder of the git repository).
Exit code: 0 pass, 1 fail, 2 could not be checked (inconclusive).
Documents are UTF-8 (a BOM and CRLF line ends are accepted). Code blocks and HTML comments in documents are ignored.
Standard library only, Python 3.10+. Project documents may be Korean or English.

Limits:
  trace     a name check only: a skipped or empty test still counts. Comments and Python docstrings are
            removed first. IDs inside backticks are not checked against the definitions (so a product
            name such as `Cloudflare R2` is safe there), but they still count as mentioned. ADR rules always
            define IDs; they need tests only when a plan that mentions them has an ADR-rule end condition
            ("All N ADR rules" / "ADR 규칙 N개"), which plans written with an older template lack.
  keywords  수 있다/없다 is read only when 수 follows a space and a word ending in ㄹ ("할 수 있다"); an
            unspaced 할수있다 is not caught, and a noun before 수 that ends in ㄹ ("파일 수 있음") is.
            A Korean double negative in a MUST NOT row ("저장하지 않아서는 안 된다") is not caught.
  journal   looks at the change set, not at each step: several uncommitted steps pass once one of them
            has a new step heading.
"""
import argparse
import datetime
import os
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

PASS, FAIL, INCONCLUSIVE = 0, 1, 2
TEST_DIRS = ["tests", "test", "src/test"]
SKIP_DIRS = {"node_modules", "venv", ".venv", "dist", "build"}
# Test files: test_*, *_test.*, *.test.*, *.spec.*, *_spec.*, and, inside a folder named test, tests or spec,
# the JVM forms *Test.*, *Tests.*, *Spec.*.
TEST_FILE = re.compile(r"^test_|_test\.|\.test\.|\.spec\.|_spec\.")
JVM_TEST_FILE = re.compile(r"(?:Tests?|Spec)\.")
TEST_FOLDER_NAMES = {"test", "tests", "spec"}


class Unreadable(Exception):
    pass


def decode(data, name):
    try:
        return unicodedata.normalize("NFC", data.decode("utf-8-sig")).replace("\r\n", "\n")
    except UnicodeDecodeError as e:
        raise Unreadable(name, f"not UTF-8 ({e.reason} at byte {e.start})")


def read(path):
    try:
        data = Path(path).read_bytes()
    except OSError as e:
        raise Unreadable(path, e.strerror or type(e).__name__)
    return decode(data, path)


def report(name, problems, summary):
    if problems:
        print(f"FAIL: {name}")
        for p in problems:
            print(f"  - {p}")
        print(f"  ({summary})")
        return FAIL
    print(f"PASS: {name} ({summary})")
    return PASS


def inconclusive(name, why):
    print(f"INCONCLUSIVE: {name}. {why}")
    return INCONCLUSIVE


def visible_lines(text):
    """The lines of a document with code blocks (``` and ~~~) and HTML comments blanked; line numbers stay."""
    text = re.sub(r"<!--.*?-->", lambda m: "\n" * m.group().count("\n"), text, flags=re.S)
    out, fence = [], None
    for line in text.splitlines():
        m = re.match(r"^\s*(```|~~~)", line)
        if fence:
            if m and m.group(1) == fence:
                fence = None
            out.append("")
        elif m:
            fence = m.group(1)
            out.append("")
        else:
            out.append(line)
    return out


CONFLICT = re.compile(r"^(<<<<<<<|>>>>>>>)(?: |$)", re.M)


def conflicts(f, text):
    """Conflict markers outside code blocks, as problems with line numbers."""
    return [f"{f}:{i} conflict marker" for i, line in enumerate(visible_lines(text), 1) if CONFLICT.match(line)]


# ---------------------------------------------------------------- trace

LEVELS = ("MUST NOT", "MUST", "SHOULD", "MAY")
GONE = ("REPLACED", "REMOVED")
ROW = re.compile(r"^\s*\|?\s*(AC-\d+\.\d+|R\d+)\s*\|\s*([^|]*?)\s*(?:\||$)")
TILDE = "[~∼～〜]"
AC_RANGE = re.compile(r"(?<![\w.-])AC-(\d+)\.(\d+)\s*" + TILDE + r"\s*(?:AC-\1\.|\1\.)?(\d+)(?!\d|\.\d)")
R_RANGE = re.compile(r"(?<![A-Za-z0-9])R(\d+)\s*" + TILDE + r"\s*R?(\d+)(?![0-9A-Za-z])")
AC_ONE = re.compile(r"(?<![\w.-])AC-\d+\.\d+(?!\d)")
R_ONE = re.compile(r"(?<![A-Za-z0-9])R\d+(?![0-9A-Za-z])")
ADR_ONE = re.compile(r"(?<![A-Za-z0-9])ADR-(\d{4})(?:\.(\d+))?(?!\d)")
DECISION = re.compile(r"^#{1,3}\s*(?:Decision|결정(?:\s*사항)?\s*(?:\(.*)?$)", re.I)
ITEM = re.compile(r"^(\d+)[.)]\s")
ADR_ROW = re.compile(r"^\s*\|\s*(\d+)\.?\s*\|\s*\**\s*(MUST NOT|MUST|SHOULD|MAY|REPLACED|REMOVED)\s*\**\s*\|")
# A replaced ADR: the status value starts with "Replaced by ADR-NNNN", "Superseded by ADR-NNNN" or "ADR-NNNN(으)로 대체".
ADR_REPLACED = re.compile(r"^\s*[-*]?\s*\**(?:Status|상태)\**\s*[:：]\s*\**\s*(?:(?:Replaced|Superseded) by \[?ADR-\d{4}"
                          r"|\[?ADR-\d{4}(?:\]\([^)]*\))?\s*으?로\s*대체)", re.I)
# A retired rule item: "1. Replaced by ADR-NNNN.k (date)." / "1. Removed (date):" / "ADR-NNNN.k으로 대체" / "삭제".
RULE_GONE = re.compile(r"^\d+[.)]\s+\**\s*(?:((?:Replaced|Superseded) by ADR-\d{4}\.\d+|ADR-\d{4}\.\d+\s*으?로\s*대체)"
                       r"|(Removed|삭제))", re.I)
BOLD = re.compile(r"\*\*(?:(?!\*\*).)+\*\*|(?<!\w)__(?:(?!__).)+__(?!\w)")
# End condition phrases: (kind, pattern). Bold around the number and any spacing are accepted.
N = r"\s*\**\s*([0-9]+)\s*\**\s*"
END = [
    ("AC", re.compile(r"\bAll" + N + r"acceptance criteri(?:a|on)\b", re.I)),
    ("R", re.compile(r"\bAll" + N + r"rules?\b", re.I)),
    ("ADR", re.compile(r"\bAll" + N + r"ADR rules?\b", re.I)),
    ("AC", re.compile(r"인수\s*조건" + N + "개")),
    ("R", re.compile(r"(?<!ADR)규칙" + N + "개")),  # "ADR  규칙" is joined to "ADR규칙" before matching
    ("ADR", re.compile(r"ADR규칙" + N + "개")),
]
FUNC_NAME = re.compile(r"\b(def|function|func|fn|fun|void)\s+(?:`([^`]+)`|([A-Za-z_$][\w$]*))\s*[(<]")
STR_NAME = re.compile(r"(?<![.\w$])(?:test|it|describe)(?:\.(?:only|skip|todo|concurrent))?\s*\(\s*(['\"`])(.*?)\1")
# Strings first, so that a # or // inside a string is not a comment. Python triple-quoted strings go with the comments.
# `#` starts a comment only in the languages listed in HASH_COMMENT (Rust #[test] and JS #private stay).
CODE_TOKEN = re.compile(r'"""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\'|"(?:\\.|[^"\\\n])*"|\'(?:\\.|[^\'\\\n])*\'|`(?:\\.|[^`\\])*`'
                        r"|/\*[\s\S]*?\*/|//[^\n]*")
CODE_TOKEN_HASH = re.compile(CODE_TOKEN.pattern + r"|#[^\n]*")
HASH_COMMENT = {".py", ".pyi", ".rb", ".sh", ".bash", ".bats", ".pl", ".r", ".ex", ".exs", ".yaml", ".yml", ".toml"}
TOKEN_IN_NAME = re.compile(r"(?<![^_])(?:ac(\d+)_(\d+)|adr(\d{4})_(\d+)|r(\d+))(?=_)")
ID_AT_START = re.compile(r"^(AC-\d+\.\d+|ADR-\d{4}\.\d+|R\d+)(?!\w)")


def kind(id_):
    return "ADR" if id_.startswith("ADR-") else "AC" if id_.startswith("AC-") else "R"


def defined_ids(folder, prefix):
    """{id: level} from the requirement tables, plus problems. Only rows whose Level cell holds a level define IDs."""
    ids, problems = {}, []
    for f in sorted(Path(folder).glob("*.md")):
        table = []  # rows of the current table block
        for no, line in enumerate(visible_lines(read(f)) + [""], 1):
            if line.lstrip().startswith("|") or ROW.match(line):
                table.append((no, line))
                continue
            if table:
                header = [c.strip().lower() for c in table[0][1].strip().strip("|").split("|")]
                rows = [(n, ROW.match(t)) for n, t in table]
                rows = [(n, m) for n, m in rows if m and m.group(1).startswith(prefix)]
                is_req = any(m.group(2) in LEVELS + GONE for _, m in rows) or (
                    len(header) > 1 and header[1] in ("level", "수준", "레벨", "등급"))
                for n, m in rows if is_req else []:
                    id_, level = m.groups()
                    if level not in LEVELS + GONE:
                        problems.append(f"{f}:{n} the Level cell of {id_} is \"{level}\". Write MUST, MUST NOT, SHOULD, MAY, REPLACED or REMOVED")
                    elif id_ in ids:
                        problems.append(f"ID defined twice: {id_}")
                    else:
                        ids[id_] = level
                table = []
    return ids, problems


def adr_rules(folder):
    """{ADR-NNNN.k: level}, files, problems, warnings. A rule is a numbered item with a bold keyword, or a row
    `| k | LEVEL | … |`, under a Decision heading (`# Decision` … `### Decision`, `## 결정`, `## 결정 사항`).
    A replaced ADR's rules are REPLACED; a rule item that starts with "Replaced by ADR-NNNN.k" or "Removed" is retired."""
    ids, files, problems, warnings = {}, {}, [], []
    for f in sorted(Path(folder).glob("*.md")):
        lines = visible_lines(read(f))
        has_bold = any(has_level(lv, " ".join(BOLD.findall(line))) for line in lines for lv in LEVELS)
        m = re.match(r"(\d{4})-", f.name)
        if not m:
            if has_bold:
                warnings.append(f"{f} has bold keywords but its name does not start with NNNN-, so it defines no rule")
            continue
        files[m.group(1)] = f
        replaced = any(ADR_REPLACED.match(line) for line in lines)
        inside, item, found, starts = 0, None, {}, []  # inside: level of the Decision heading being read
        for line in lines + ["#"]:
            if line.startswith("#"):
                level = len(line) - len(line.lstrip("#"))
                if DECISION.match(line):
                    inside = level
                elif inside and level <= inside:
                    inside = 0
                item = None
                continue
            row = ADR_ROW.match(line)
            if inside and row:
                found[row.group(1)] = row.group(2)
                continue
            im = ITEM.match(line)
            if im:
                item = im.group(1)
                if inside:
                    starts.append(item)
                    gone = RULE_GONE.match(line)
                    if gone:
                        found[item] = "REPLACED" if gone.group(1) else "REMOVED"
            elif not (line[:1].isspace() and line.strip()):
                item = None  # only indented lines continue an item
            if inside and item and any(has_level(lv, " ".join(BOLD.findall(line))) for lv in LEVELS):
                found.setdefault(item, "MUST")
        problems += [f"{f}: item {k} appears more than once under the Decision heading. Number each rule once"
                     for k in sorted(found, key=int) if starts.count(k) > 1]
        if has_bold and not found:
            warnings.append(f"{f} has bold keywords but no rule the checker can read. Write each rule as a numbered item "
                            "or a row `| k | LEVEL | … |` under `## Decision` / `## 결정`")
        for k, level in found.items():
            ids[f"ADR-{m.group(1)}.{k}"] = "REPLACED" if replaced and level not in GONE else level
    return ids, files, problems, warnings


def ids_in_text(text, adrs, skip_code=False):
    """IDs and ranges in the text. With skip_code, IDs inside backticks are left out."""
    text = "\n".join(CODE.sub("", line) if skip_code else line for line in visible_lines(text))
    found = set(AC_ONE.findall(text)) | set(R_ONE.findall(text))
    for major, a, b in AC_RANGE.findall(text):
        found |= {f"AC-{major}.{n}" for n in range(int(a), int(b) + 1)}
    for a, b in R_RANGE.findall(text):
        found |= {f"R{n}" for n in range(int(a), int(b) + 1)}
    for num, k in ADR_ONE.findall(text):
        if k:
            found.add(f"ADR-{num}.{k}")
        else:
            found.add(f"ADR-{num}")
            found |= {i for i in adrs if i.startswith(f"ADR-{num}.")}
    return found


def test_token(id_):
    if id_.startswith("ADR-"):
        return "adr" + id_[4:].replace(".", "_") + "_"
    if id_.startswith("AC-"):
        return "ac" + id_[3:].replace(".", "_") + "_"
    return id_.lower() + "_"


def test_names(text, hash_comment=True):
    """(name, IDs it carries) for each test name in a test file. Pin tests carry none.
    A name check only: comments and Python triple-quoted strings are removed first; a `def`/`func`/`function` must start with test/Test."""
    token = CODE_TOKEN_HASH if hash_comment else CODE_TOKEN
    text = token.sub(lambda m: m.group() if m.group()[0] in "\"'`" and m.group()[:3] not in ('"""', "'''") else " ", text)
    names = [(a or b, False) for kw, a, b in FUNC_NAME.findall(text)
             if kw not in ("def", "func", "function") or (a or b).startswith(("test", "Test"))]
    names += [(s, True) for _, s in STR_NAME.findall(text)]
    for name, is_string in names:
        low = name.lower()
        if low.startswith(("pin_", "test_pin_")):
            continue
        ids = set()
        for ac1, ac2, adr1, adr2, r in TOKEN_IN_NAME.findall(low):
            ids.add(f"AC-{ac1}.{ac2}" if ac1 else f"ADR-{adr1}.{adr2}" if adr1 else f"R{r}")
        if is_string:
            m = ID_AT_START.match(name.strip())
            if m:
                ids.add(m.group(1))
        yield name, ids


def test_files(folders, fallback=False):
    """Test files under the folders. The JVM forms count only inside a test folder, never in the whole-project fallback."""
    for folder in folders:
        for root, dirs, files in os.walk(folder):
            dirs[:] = sorted(d for d in dirs if not d.startswith(".") and d not in SKIP_DIRS)
            in_test_folder = not fallback and bool(
                TEST_FOLDER_NAMES & {Path(folder).name, *Path(root).relative_to(folder).parts})
            for f in sorted(files):
                if TEST_FILE.search(f) or (in_test_folder and JVM_TEST_FILE.search(f)):
                    yield Path(root) / f


def plan_tasks(text):
    """{task number: row text} from the plan's task table: the first table whose header has `#` and Task/작업.
    The first cell is `1`, `1.`, `Task 1` or `작업 1`. Other tables (Risks …) are not read."""
    tasks, table = {}, None  # table: None before a table, True inside the task table, False inside another
    for line in visible_lines(text) + [""]:
        if line.lstrip().startswith("|"):
            if table is None:
                cells = [c.strip().lower() for c in line.strip().strip("|").split("|")]
                table = "#" in cells and any(c.startswith(("task", "작업")) for c in cells)
            elif table:
                m = re.match(r"^\s*\|\s*(?:Task\s+|작업\s*)?(\d+)\.?\s*\|", line, re.I)
                if m:
                    tasks.setdefault(int(m.group(1)), line)
        elif table:
            break
        else:
            table = None
    return tasks


def cmd_trace(args):
    docs = Path(args.docs)
    if args.plan is not None and args.upto < 1:
        return inconclusive("trace", f"--upto {args.upto}: tasks start at 1")
    problems = []
    for sub in ("spec", "domain", "adr", "plan"):
        for f in sorted((docs / sub).glob("*.md")):
            problems += conflicts(f, read(f))
    acs, more = defined_ids(docs / "spec", "AC-")
    problems += more
    rules, more = defined_ids(docs / "domain", "R")
    problems += more
    adrs, adr_files, more, warnings = adr_rules(docs / "adr")
    problems += more
    for w in warnings:
        print(f"WARNING: {w}")
    every = {**acs, **rules, **adrs}
    active = [i for i, lv in every.items() if lv not in GONE]
    if not every:
        return inconclusive("trace", f"no IDs in the tables of {docs}/spec and {docs}/domain or in {docs}/adr")

    def exists(i):
        return i in every or (re.fullmatch(r"ADR-\d{4}", i) and i[4:] in adr_files)

    def dangling(f, text):
        return [f"{f} points at an ID that does not exist: {i}" for i in sorted(ids_in_text(text, adrs, True)) if not exists(i)]

    for sub in ("spec", "domain"):
        for f in sorted((docs / sub).glob("*.md")):
            problems += dangling(f, read(f))

    plans = sorted((docs / "plan").glob("*.md"))
    planned, adr_required = set(), set()
    for p in plans:
        text = read(p)
        mentioned = ids_in_text(text, adrs)
        planned |= mentioned
        problems += dangling(p, text)
        readable, counts_adr = False, False
        end_text = re.sub(r"ADR\s+규칙", "ADR규칙", "\n".join(visible_lines(text)))
        for k, pattern in END:
            want = len([i for i in mentioned if i in active and kind(i) == k])
            for n in pattern.findall(end_text):
                readable = True
                if k == "ADR":
                    counts_adr = True
                    adr_required |= {i for i in mentioned if kind(i) == "ADR"}
                if int(n) != want:
                    problems.append(f"{p} end condition says {n} for {k} IDs, but the plan mentions {want} active ones")
        if not readable:
            problems.append(f"plan {p.name.split('-')[0]} has no end condition the checker can read "
                            "(\"All N acceptance criteria\", \"All N rules\", \"All N ADR rules\", \"인수 조건 N개\", \"규칙 N개\", \"ADR 규칙 N개\")")
        elif not counts_adr:
            for adr in sorted({i[:8] for i in mentioned if kind(i) == "ADR" and i in active}):
                k = len([i for i in mentioned if i.startswith(adr + ".") and i in active])
                print(f"WARNING: plan {p.name.split('-')[0]} mentions {adr} ({k} rules) but its end condition does not "
                      "count ADR rules; their tests are not required")
    if plans:
        problems += [f"not in the plan: {i}" for i in active if i not in planned]
    elif not args.no_tests:
        problems.append(f"no documents in {docs}/plan")

    need = active
    if args.plan:
        matches = [p for p in plans if p.name.startswith(args.plan + "-")]
        if len(matches) != 1:
            return inconclusive("trace", f"{len(matches)} plans {args.plan}-… in {docs}/plan: " + ", ".join(p.name for p in matches))
        rows = [t for n, t in plan_tasks(read(matches[0])).items() if n <= args.upto]
        if not rows:
            return inconclusive("trace", f"no task row numbered {args.upto} or lower in {matches[0]}. "
                                "The first cell of a task row is `1`, `1.`, `Task 1` or `작업 1`")
        built = ids_in_text(" ".join(rows), adrs)
        need = [i for i in active if i in built]
    # Old plans have no ADR-rule end condition: their ADR rules define IDs but need no test.
    need = [i for i in need if kind(i) != "ADR" or i in adr_required]

    tested = "not looked at (--no-tests)"
    free = [i for i in active if kind(i) == "ADR" and i not in adr_required]
    if not args.no_tests:
        root, fallback = docs.parent, False
        folders = args.tests or [str(root / d) for d in TEST_DIRS if (root / d).is_dir()]
        if not folders:
            folders, fallback = [str(root)], True
        missing_dirs = [d for d in folders if not Path(d).is_dir()]
        if missing_dirs:
            return inconclusive("trace", f"no test folder: {', '.join(missing_dirs)}")
        covered, n_files = set(), 0
        for f in test_files(folders, fallback):
            try:
                data = f.read_bytes()
            except OSError as e:
                raise Unreadable(f, e.strerror or type(e).__name__)
            if b"\0" in data:
                continue  # binary fixture
            n_files += 1
            for name, ids in test_names(decode(data, f), f.suffix.lower() in HASH_COMMENT):
                for i in ids:
                    if i not in every:
                        problems.append(f"{f} test {name} names an ID that is defined nowhere: {i}")
                    elif every[i] in GONE:
                        problems.append(f"{f} test {name} names {i}, which is {every[i]}. Rename it to the new ID or delete it")
                    covered.add(i)
        if n_files == 0:
            return inconclusive("trace", f"no test files in {', '.join(folders)}. Use --tests or --no-tests")
        missing = [i for i in need if i not in covered]
        problems += [f"no test with `{test_token(i)}` in its name: {i}" for i in missing]
        tested = f"IDs with a test {len(need) - len(missing)}/{len(need)} in {n_files} test files in {', '.join(folders)}"
        if len(need) < len(active) - len(free):
            tested += f", not built yet {len(active) - len(free) - len(need)}"
    gone = len(every) - len(active)
    return report("trace", problems, f"{len(acs)} acceptance criteria, {len(rules)} rules, {len(adrs)} ADR rules"
                  + (f" ({len(free)} with no test required: no plan end condition counts ADR rules)" if free else "")
                  + (f"; {gone} of them replaced or removed" if gone else "") + f", {tested}")


# ------------------------------------------------------------- keywords

LEVEL_ROW = re.compile(r"^\s*\|?\s*([A-Za-z0-9.\-]+)\s*\|\s*(MUST NOT|MUST|SHOULD|MAY|REPLACED|REMOVED)\s*\|(.*)$")
# Korean documents use these words for the levels.
LEVEL_WORD = {"MUST": "반드시", "MUST NOT": "절대", "SHOULD": "권장한다", "MAY": "수 있다"}
# English documents use the RFC 2119 words themselves. MUST is not counted inside MUST NOT.
LEVEL_EN = {
    "MUST": re.compile(r"(?<![A-Za-z])MUST(?![A-Za-z])(?!\s+NOT(?![A-Za-z]))"),
    "MUST NOT": re.compile(r"(?<![A-Za-z])MUST\s+NOT(?![A-Za-z])"),
    "SHOULD": re.compile(r"(?<![A-Za-z])SHOULD(?![A-Za-z])"),
    "MAY": re.compile(r"(?<![A-Za-z])MAY(?![A-Za-z])"),
}
EN_KEYWORD = re.compile(r"(?<![A-Za-z])(MUST NOT|MUST|SHOULD|MAY)(?![A-Za-z])")
CODE = re.compile(r"`[^`]*`")
QUOTED = re.compile(r"\"[^\"]*\"|“[^”]*”|‘[^’]*’|「[^」]*」|『[^』]*』")
SU = re.compile(r"(?:^|([가-힣])\s+)수\s*[가도는]?\s*(있|없)")
# A prohibition in a MUST row: read from the verb ending, so 않은/금지어/보안된/NOT FOUND pass.
KO_PROHIBIT = re.compile(r"지\s*않(는다|아야|도록|습니다|게)|(서는|면)\s*(안|아니)\s*(된|돼|됩)|지\s*(마라|마세요|말\s*것|말아야)"
                         r"|금지(한다|된다|합니다)|불가(하다|합니다)")
EN_PROHIBIT = re.compile(r"(\*\*|__)\s*(?i:never)\b|MUST(\*\*|__)?\s+NOT\s+[a-z]")
KO_MUST_NOT = re.compile(r"(서는|면)\s*안\s*(된|돼|됩)")
EN_MUST_NOT_LOWER = re.compile(r"(\*\*|__)MUST\1\s*not\b|(\*\*|__)MUST not\b")
STATUS_ITEM = re.compile(r"^[-*]\s*(\*\*)?(상태|읽는\s*법|Status|How to read)(\*\*)?\s*[:：]")
HOW_TO_READ = ("how to read this document", "이 문서를 읽는 법")


def is_how_to_read(line):
    """A heading of level 2 or deeper titled "How to read this document" / "이 문서를 읽는 법"; bold, case and a trailing : or . do not matter."""
    m = re.match(r"^#{2,}\s+(.*)$", line)
    return bool(m) and re.sub(r"[*_]", "", m.group(1)).strip().rstrip(":：. ").lower() in HOW_TO_READ


def has_level(level, bold):
    """Does the bold text carry that level's keyword, in Korean or in English? Either is enough."""
    return LEVEL_WORD[level] in bold or bool(LEVEL_EN[level].search(bold))


def su_not_permission(plain):
    """수 있/없 (also 수가, 수도, 수는) where 수 follows a space and a word ending in ㄹ (할/볼/읽을). 점수, 행 수가 do not count."""
    return any(m.group(1) and (ord(m.group(1)) - 0xAC00) % 28 == 8 for m in SU.finditer(plain))


def requirement_lines(text):
    """Yield the lines that can hold a requirement. Skips the "how to read" section, status items with their
    indented list continuation, code and comments."""
    skip_level = None  # heading level of the "how to read" section being skipped
    in_status = False
    for no, line in enumerate(visible_lines(text), 1):
        h = re.match(r"^(#+)\s", line)
        if h:
            if skip_level and len(h.group(1)) > skip_level:
                continue
            skip_level = len(h.group(1)) if is_how_to_read(line) else None
            in_status = False
            if skip_level:
                continue
        if skip_level:
            continue
        if in_status and line[:1].isspace() and line.strip() and not line.lstrip().startswith("|"):
            continue
        in_status = bool(STATUS_ITEM.match(line))
        if in_status:
            continue
        yield no, line


def cmd_keywords(args):
    files = [Path(f) for f in args.files]
    if not files:
        docs = Path(args.docs)
        for sub in ("spec", "domain", "adr"):
            files += sorted((docs / sub).glob("*.md"))
    if not files:
        return inconclusive("keywords", "no documents to check")
    problems, counts = [], dict.fromkeys(LEVEL_WORD, 0)
    for f in files:
        text = read(f)
        problems += conflicts(f, text)
        for no, line in requirement_lines(text):
            where = f"{f}:{no}"
            line = CODE.sub("", line)
            m = LEVEL_ROW.match(line)
            if m and m.group(2) in GONE:
                continue  # a retired row is neither counted nor checked
            bolds = " ".join(BOLD.findall(line))
            plain = QUOTED.sub("", BOLD.sub("", line))
            for level in LEVEL_WORD:
                counts[level] += bolds.count(LEVEL_WORD[level]) + len(LEVEL_EN[level].findall(bolds))
            for word in ("반드시", "절대"):
                if word in plain:
                    problems.append(f"{where} \"{word}\" is not bold. Bold it for a requirement; use another word for explanation")
            if su_not_permission(plain):
                problems.append(f"{where} \"수 있다/없다\" that is not a permission (MAY). Use other words for ability and possibility; write a prohibition as **절대 …서는 안 된다** (MUST NOT)")
            if EN_MUST_NOT_LOWER.search(line):
                problems.append(f"{where} \"MUST not\". Write a prohibition as **MUST NOT**")
            # An English keyword is a keyword only in upper case. The Level cell and a note such as "(MAY)" beside a bold keyword are allowed.
            en = EN_KEYWORD.search(QUOTED.sub("", BOLD.sub("", m.group(3) if m else line)))
            if en and not has_level(en.group(), bolds):
                problems.append(f"{where} \"{en.group()}\" is not bold. Bold it for a requirement; write it in lower case for explanation")
            if m:
                id_, level, rest = m.groups()
                sentence = rest.split("|")[0]  # the level is read from the sentence cell only
                s_bold = " ".join(BOLD.findall(sentence))
                if not has_level(level, s_bold):
                    problems.append(f"{where} the level of {id_} is {level} but the sentence has no bold \"{level}\" or \"{LEVEL_WORD[level]}\"")
                others = [lv for lv in LEVEL_WORD if lv != level and has_level(lv, s_bold) and not (level == "MUST NOT" and lv == "MUST")]
                if level == "MUST" and (KO_PROHIBIT.search(sentence) or EN_PROHIBIT.search(sentence)
                                        or re.search(r"(?i)\bnever\b", s_bold) or "MUST NOT" in others or "절대" in s_bold):
                    problems.append(f"{where} {id_}: a MUST row states a prohibition; use MUST NOT")
                elif others:
                    problems.append(f"{where} the level of {id_} is {level} but its bold carries {', '.join(others)}")
                if level == "MUST NOT" and re.search(r"[가-힣]", sentence) and not (
                        "절대" in s_bold and KO_MUST_NOT.search(re.sub(r"\*\*|__", "", sentence))):
                    problems.append(f"{where} the level of {id_} is MUST NOT: write the prohibition as **절대 …서는 안 된다** or **절대 …면 안 된다**")
    summary = f"{len(files)} documents" + ("" if args.files else f" in {args.docs}") + ", " + ", ".join(f"{k} {v}" for k, v in counts.items())
    if not problems and not sum(counts.values()):
        return inconclusive("keywords", f"no keywords found ({summary})")
    return report("keywords", problems, summary)


# -------------------------------------------------------------- journal

STEP_HEADING = re.compile(r"^## (?:Step|스텝) \d+", re.M)
DONE = ("**Done", "**한 일")
# Harness skill and agent folders; the rules file (.omp/AGENTS.md, .claude/CLAUDE.md …) is not ignored.
IGNORED_UNTRACKED = (".omp/skills/", ".omp/agents/", ".claude/skills/", ".claude/agents/")
IGNORED_PARTS = ("__pycache__", ".pytest_cache")
EMPTY_TREE = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"


def git(*a):
    r = subprocess.run(["git", "-c", "core.quotepath=false", *a], capture_output=True)
    return r.returncode, r.stdout.decode("utf-8", "replace")


def norm(path):
    return unicodedata.normalize("NFC", Path(os.path.normpath(path)).as_posix())


def blob(rev_path, name):
    """Text of a file in git (`HEAD:./x`, `:./x`), or None if it is not there."""
    r = subprocess.run(["git", "show", rev_path], capture_output=True)
    return decode(r.stdout, name) if r.returncode == 0 else None


def steps_in(text):
    """The step headings of a journal, outside code fences."""
    return STEP_HEADING.findall("\n".join(visible_lines(text or "")))


def new_step_sections(old, new):
    """(heading, text) of each step after the old file's steps."""
    lines = visible_lines(new)
    starts = [i for i, line in enumerate(lines) if STEP_HEADING.match(line)] + [len(lines)]
    n_old = len(steps_in(old))
    return [(lines[a], "\n".join(lines[a:b])) for a, b in zip(starts[n_old:-1], starts[n_old + 1:])]


def has_rev(rev):
    return git("rev-parse", "--verify", "-q", rev)[0] == 0


def commit_changes(rev):
    """(status, path) of the project files the commit changed, against its first parent."""
    base = f"{rev}^1" if has_rev(f"{rev}^1") else EMPTY_TREE
    _, d = git("diff", "--relative", "--no-renames", "--name-status", "-z", base, rev, "--", ".")
    f = d.split("\0")
    return [(f[i][0], unicodedata.normalize("NFC", f[i + 1])) for i in range(0, len(f) - 1, 2)]


def cmd_journal(args):
    today = datetime.date.today()
    date = args.date or today.isoformat()
    try:
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date):
            raise ValueError
        if datetime.date.fromisoformat(date) > today:
            return inconclusive("journal", f"--date {date} is in the future (today is {today.isoformat()})")
    except ValueError:
        return inconclusive("journal", f"--date {date} is not a real date (YYYY-MM-DD)")
    docs_dir = norm(args.docs) + "/"
    jdir = norm(Path(args.docs) / "journal") + "/"
    journal = jdir + date + ".md"
    code, prefix = git("rev-parse", "--show-prefix")
    if code != 0:
        return inconclusive("journal", "not a git repository")
    prefix = unicodedata.normalize("NFC", prefix.strip())
    _, out = git("status", "--porcelain=v1", "-z", "--untracked-files=all", "--", ".")
    entries, renamed, parts = [], [], out.split("\0")
    while parts and parts[0]:
        e = parts.pop(0)
        xy, path = e[:2], unicodedata.normalize("NFC", e[3:])
        path = path[len(prefix):] if path.startswith(prefix) else path
        if xy[0] in "RC":
            old = unicodedata.normalize("NFC", parts.pop(0))
            old = old[len(prefix):] if old.startswith(prefix) else old
            if xy[0] == "R" and (old.startswith(jdir) or path.startswith(jdir)):
                renamed.append(f"{old} was renamed to {path}. Keep each date's journal under its own name")
        if xy == "??" and (path.startswith(IGNORED_UNTRACKED) or any(p in IGNORED_PARTS for p in path.split("/"))):
            continue
        entries.append((xy, path))
    has_head = has_rev("HEAD")

    def project_commit(rev):
        """rev if it changed the project, else the last commit before it that did (None if there is none)."""
        if not has_rev(rev) or commit_changes(rev):
            return rev if has_rev(rev) else None
        return git("log", "-1", "--format=%H", rev, "--", ".")[1].strip() or None

    last = project_commit("HEAD") if has_head else None

    def last_commit():
        return commit_changes(last) if last else []

    staged = [(xy[0], p) for xy, p in entries if xy[0] not in " ?"]
    if staged:
        mode, changes = "staged", staged
        new_of = lambda p: blob(f":./{p}", p)  # noqa: E731
        old_of = lambda p: blob(f"HEAD:./{p}", p) if has_head else None  # noqa: E731
    elif entries:
        if all(xy == "??" for xy, _ in entries) and any(p.startswith(jdir) for _, p in last_commit()):
            return inconclusive("journal", "only untracked files changed and the last commit carries the journal: "
                                + ", ".join(p for _, p in entries) + ". Not part of a step? Ask the user")
        mode, changes = "working tree", [("D" if "D" in xy else "M", p) for xy, p in entries]
        new_of = lambda p: read(p) if Path(p).is_file() else None  # noqa: E731
        old_of = lambda p: blob(f"HEAD:./{p}", p) if has_head else None  # noqa: E731
    else:
        mode, changes = "last commit", last_commit()
        if not changes:
            return report("journal", [], "the working tree is clean; the last commit changed nothing in the project")
        new_of = lambda p: blob(f"{last}:./{p}", p)  # noqa: E731
        base = f"{last}^1" if has_rev(f"{last}^1") else None
        old_of = lambda p: blob(f"{base}:./{p}", p) if base else None  # noqa: E731

    problems, counts = list(renamed), {}
    changed = [p for _, p in changes]
    journals = [(s, p) for s, p in changes if p.startswith(jdir) and p.endswith(".md")]
    for s, p in journals:
        new = new_of(p)
        if s == "D" or new is None:
            problems.append(f"{p} is deleted")
            continue
        old = old_of(p) or ""
        if conflicts(p, new):
            problems.append(f"{p} has conflict markers")
        if not new.startswith(old.rstrip()):
            problems.append(f"{p}: past steps were edited (the committed text is no longer the start of the file)")
        if mode != "last commit" and p[len(jdir):-3] < date and journal not in changed:
            problems.append(f"{p} is an earlier date's journal and {journal} did not change. Write today's step in {journal}")
        sections = new_step_sections(old, new)
        if not sections and (mode == "last commit" or p == journal):
            problems.append(f"{p} changed but has no new `## Step N` / `## 스텝 N` heading")
        problems += [f"{p}: \"{h}\" has no **Done** / **한 일**" for h, body in sections if not any(d in body for d in DONE)]
        counts[p] = len(steps_in(new))

    # During a merge, or for a merge commit, the merge step needs its own entry: a step heading neither parent has.
    parents = ("HEAD", "MERGE_HEAD") if mode != "last commit" and has_rev("MERGE_HEAD") else \
        (f"{last}^1", f"{last}^2") if mode == "last commit" and has_rev(f"{last}^2") else None
    if parents and journals and not any(
            set(steps_in(new_of(p))) - {h for rev in parents for h in steps_in(blob(f"{rev}:./{p}", p))}
            for _, p in journals if new_of(p) is not None):
        problems.append(f"merge of {parents[0]} and {parents[1]}: the journal has no step heading that neither parent has. "
                        "Write the merge step's own entry")

    if mode == "last commit":
        if not journals:
            problems.append(f"the last commit changed {len(changes)} files in the project but nothing under {jdir}. Write the journal before the commit")
        elif all(p.startswith(docs_dir) for p in changed):
            prev = project_commit(f"{last}~1")
            before = commit_changes(prev) if prev else []
            if before and not any(p.startswith(jdir) for _, p in before):
                problems.append(f"the commit before the last changed {len(before)} files in the project without the journal, "
                                f"and the last commit changed only {docs_dir}: code and journal were committed separately")
    elif journal not in changed:
        problems.append(f"{len(changes)} files changed ({mode}) but {journal} did not. Write the journal before the commit")
    shown = journal if journal in counts else (list(counts)[-1] if counts else journal)
    return report("journal", problems, f"{mode}: {len(changes)} files, {counts.get(shown, 0)} steps in {shown}")


# ----------------------------------------------------------------- self

REF = re.compile(r"`((?:playbooks|principles|references|scripts)/[A-Za-z0-9_.\-]+)`")
REVIEW_REF = re.compile(r"`(review/[A-Za-z0-9_.\-/]+)`")


def cmd_self(args):
    # Self-check of the level test: both languages count, and MUST is told apart from MUST NOT.
    assert has_level("MUST", "**MUST**") and has_level("MUST", "**반드시**")
    assert has_level("MUST NOT", "**MUST NOT**") and not has_level("MUST", "**MUST NOT**")
    assert len(STEP_HEADING.findall("## Step 1\n## 스텝 2\n### Step 3\n")) == 2
    root = Path(__file__).resolve().parent.parent
    router = root / "SKILL.md"
    problems = []
    router_text = read(router)
    indexed = set(REF.findall(router_text))
    for kind in ("playbooks", "principles"):
        on_disk = {f"{kind}/{f.name}" for f in (root / kind).glob("*.md")}
        in_index = {r for r in indexed if r.startswith(kind + "/")}
        problems += [f"not in the index: {r}" for r in sorted(on_disk - in_index)]
        problems += [f"file missing: {r}" for r in sorted(in_index - on_disk)]
    if len(router_text.splitlines()) > 150:
        problems.append("the router is over 150 lines. Move body text into a separate file")
    for f in sorted(root.rglob("*.md")):
        base = f.parent if f.parent.name in ("playbooks", "principles", "references") else None
        rel = f.relative_to(root)
        # A skill under review/ resolves its paths against its own folder.
        home = root / rel.parts[0] / rel.parts[1] if rel.parts[0] == "review" and len(rel.parts) > 2 else root
        for ref in REF.findall(read(f)):
            if not (home / ref).exists():
                problems.append(f"{rel} points at a file that does not exist: {ref}")
        for ref in REVIEW_REF.findall(read(f)):
            if not (root / ref).exists():
                problems.append(f"{rel} points at a file that does not exist: {ref}")
        if base is None:
            continue
        lines = [line for line in read(f).splitlines() if line.strip()]
        if base.name == "playbooks" and len(lines) < 2:
            problems.append(f"{rel} is empty")
        elif base.name == "playbooks":
            if not lines[0].startswith("### "):
                problems.append(f"{rel} first line is not `### Name`")
            if not lines[1].startswith("**You own"):
                problems.append(f"{rel} second line is not the ownership sentence (`**You own …`)")
            if not lines[-1].startswith("**Report:**"):
                problems.append(f"{rel} last line is not `**Report:**`")
            steps = [line for line in lines if re.match(r"^\d+\. ", line)]
            if len(steps) < 3:
                problems.append(f"{rel} has fewer than 3 numbered steps")
            if len(lines) > 25:
                problems.append(f"{rel} has {len(lines)} non-empty lines. Cut it to 25 or fewer")
            if f.name not in ("wrap-up.md",) and not any("wrap-up.md" in s for s in steps):
                problems.append(f"{rel} has no step that calls the wrap-up (`wrap-up.md`)")
        if base.name == "principles":
            for mark in ("**Why:**", "**How:**", "**Evidence:**"):
                if not any(line.startswith(mark) for line in lines):
                    problems.append(f"{rel} has no `{mark}`")
    n_pb = len(list((root / "playbooks").glob("*.md")))
    n_pr = len(list((root / "principles").glob("*.md")))
    return report("self", problems, f"{n_pb} playbooks, {n_pr} principles, router {len(router_text.splitlines())} lines")


def main():
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8", errors="replace")
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    t = sub.add_parser("trace", help="IDs in the plan and in test names. ADR rules need tests only when a plan that "
                       "mentions them has an ADR-rule end condition (\"All N ADR rules\" / \"ADR 규칙 N개\")")
    t.add_argument("--docs", default="docs", help="the docs folder; its parent is the project root")
    t.add_argument("--tests", action="append", help="test folder; may repeat. Default: every one of tests, test, src/test "
                   "under the project root that exists, else the whole project root. A name check only: skipped or empty tests count")
    t.add_argument("--no-tests", action="store_true", help="check the documents only")
    t.add_argument("--plan", help="plan number NN for a partial run (with --upto); exactly one plan NN-… must exist")
    t.add_argument("--upto", type=int, help="only the IDs in tasks 1..K of --plan need tests (K >= 1)")
    t.set_defaults(fn=cmd_trace)
    k = sub.add_parser("keywords", help="RFC 2119 keywords; default files: spec, domain and ADR documents. "
                       "수 is read only after a space: an unspaced 할수있다 is not caught")
    k.add_argument("files", nargs="*")
    k.add_argument("--docs", default="docs")
    k.set_defaults(fn=cmd_keywords)
    j = sub.add_parser("journal", help="does the change being recorded carry the journal (the change set, not each step)")
    j.add_argument("--docs", default="docs")
    j.add_argument("--date", help="YYYY-MM-DD, the day of the request; not in the future. Default: today")
    j.set_defaults(fn=cmd_journal)
    s = sub.add_parser("self", help="do sdd's index and files agree")
    s.set_defaults(fn=cmd_self)
    args = p.parse_args()
    if args.cmd == "trace" and (args.plan is None) != (args.upto is None):
        p.error("--plan and --upto go together")
    try:
        code = args.fn(args)
    except Unreadable as e:
        code = inconclusive(args.cmd, f"cannot read {e.args[0]}: {e.args[1]}")
    sys.exit(code)


if __name__ == "__main__":
    main()
