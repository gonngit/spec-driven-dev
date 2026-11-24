#!/usr/bin/env python3
"""Checks for sdd. Written rules turned into checks that can be run.

  trace     is every ID in the spec and the domain present in the plan and in the test names
  keywords  are the RFC 2119 keywords in the documents used by the rules
  journal   did today's journal change together with this change
  self      do sdd's index and files agree

Exit code: 0 pass, 1 fail, 2 could not be checked (inconclusive).
Standard library only. Project documents may be Korean or English.
"""
import argparse
import datetime
import re
import subprocess
import sys
from pathlib import Path

PASS, FAIL, INCONCLUSIVE = 0, 1, 2
TEXT_SUFFIXES = {
    ".java", ".kt", ".kts", ".groovy", ".scala", ".py", ".js", ".jsx", ".ts",
    ".tsx", ".go", ".rs", ".rb", ".cs", ".swift", ".php", ".hurl", ".feature",
}
TEST_DIRS = ["tests", "test", "src/test"]


def read(path):
    return Path(path).read_text(encoding="utf-8")


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


# ---------------------------------------------------------------- trace

AC_ROW = re.compile(r"^\|\s*(AC-\d+\.\d+)\s*\|")
R_ROW = re.compile(r"^\|\s*(R\d+)\s*\|")
AC_RANGE = re.compile(r"AC-(\d+)\.(\d+)\s*[~∼-]\s*(?:AC-)?(?:\1\.)?(\d+)")
R_RANGE = re.compile(r"\bR(\d+)\s*[~∼-]\s*R?(\d+)\b")
AC_ONE = re.compile(r"AC-\d+\.\d+")
R_ONE = re.compile(r"(?<![A-Za-z0-9])R\d+(?![0-9A-Za-z])")


def defined_ids(folder, row):
    ids, dup = [], []
    for f in sorted(Path(folder).glob("*.md")):
        for line in read(f).splitlines():
            m = row.match(line)
            if m:
                (dup if m.group(1) in ids else ids).append(m.group(1))
    return ids, dup


def ids_in_text(text):
    found = set(AC_ONE.findall(text)) | set(R_ONE.findall(text))
    for major, a, b in AC_RANGE.findall(text):
        found |= {f"AC-{major}.{n}" for n in range(int(a), int(b) + 1)}
    for a, b in R_RANGE.findall(text):
        found |= {f"R{n}" for n in range(int(a), int(b) + 1)}
    return found


def test_token(id_):
    if id_.startswith("AC-"):
        return "ac" + id_[3:].replace(".", "_") + "_"
    return id_.lower() + "_"


def cmd_trace(args):
    docs = Path(args.docs)
    acs, dup_ac = defined_ids(docs / "spec", AC_ROW)
    rules, dup_r = defined_ids(docs / "domain", R_ROW)
    ids = acs + rules
    if not ids:
        return inconclusive("trace", f"no IDs in the tables of {docs}/spec and {docs}/domain")
    problems = [f"ID defined twice: {d}" for d in dup_ac + dup_r]

    plans = sorted((docs / "plan").glob("*.md"))
    if plans:
        planned = set()
        for p in plans:
            planned |= ids_in_text(read(p))
        problems += [f"not in the plan: {i}" for i in ids if i not in planned]
        known = set(ids)
        problems += [f"the plan points at an ID that does not exist: {i}" for i in sorted(planned - known)]
    else:
        problems.append(f"no documents in {docs}/plan")

    tested = "not looked at (--no-tests)"
    if not args.no_tests:
        # shortcut: only common folder names are tried, pass --tests when tests sit beside the code.
        names = [args.tests] if args.tests else TEST_DIRS
        tests = next((Path(n) for n in names if Path(n).is_dir()), None)
        if tests is None:
            return inconclusive("trace", f"no test folder: {', '.join(names)}. Use --no-tests to check documents only")
        blob = "\n".join(
            read(f).lower() for f in tests.rglob("*")
            if f.is_file() and f.suffix in TEXT_SUFFIXES
        )
        missing = [
            i for i in ids
            if not re.search(r"(?<![a-z0-9])" + re.escape(test_token(i)), blob)
        ]
        problems += [f"no test with `{test_token(i)}` in its name: {i}" for i in missing]
        tested = f"IDs with a test {len(ids) - len(missing)}/{len(ids)}"
    return report("trace", problems, f"{len(acs)} acceptance criteria, {len(rules)} rules, {tested}")


# ------------------------------------------------------------- keywords

BOLD = re.compile(r"\*\*[^*]+\*\*")
LEVEL_ROW = re.compile(r"^\|\s*([A-Za-z0-9.\-]+)\s*\|\s*(MUST NOT|MUST|SHOULD|MAY)\s*\|(.*)$")
# Korean documents use these words for the levels.
LEVEL_WORD = {"MUST": "반드시", "MUST NOT": "절대", "SHOULD": "권장한다", "MAY": "수 있다"}
# English documents use the RFC 2119 words themselves. MUST is not counted inside MUST NOT.
LEVEL_EN = {
    "MUST": re.compile(r"\bMUST\b(?!\s+NOT\b)"),
    "MUST NOT": re.compile(r"\bMUST\s+NOT\b"),
    "SHOULD": re.compile(r"\bSHOULD\b"),
    "MAY": re.compile(r"\bMAY\b"),
}
EN_KEYWORD = re.compile(r"\b(MUST NOT|MUST|SHOULD|MAY)\b")
CODE = re.compile(r"`[^`]*`")
QUOTED = re.compile(r"\"[^\"]*\"|“[^”]*”")


def has_level(level, bold):
    """Does the bold text carry that level's keyword, in Korean or in English? Either is enough."""
    return LEVEL_WORD[level] in bold or bool(LEVEL_EN[level].search(bold))


def requirement_lines(text):
    """Yield only lines that can hold a requirement. Skips "how to read", status lines and code blocks."""
    skip_section = in_code = False
    for no, line in enumerate(text.splitlines(), 1):
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        if line.startswith("#"):
            skip_section = "읽는 법" in line or "how to read" in line.lower()
            continue
        if skip_section or re.match(r"^- (상태|읽는 법|Status|How to read)\s*:", line):
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
        for no, line in requirement_lines(read(f)):
            where = f"{f}:{no}"
            bolds = " ".join(BOLD.findall(line))
            plain = QUOTED.sub("", CODE.sub("", BOLD.sub("", line)))
            for level in LEVEL_WORD:
                counts[level] += bolds.count(LEVEL_WORD[level]) + len(LEVEL_EN[level].findall(bolds))
            for word in ("반드시", "절대"):
                if word in plain:
                    problems.append(f"{where} \"{word}\" is not bold. Bold it for a requirement; use another word for explanation")
            if re.search(r"수\s*(있|없)", plain):
                problems.append(f"{where} \"수 있다/없다\" that is not a permission (MAY). Use other words for ability and possibility")
            m = LEVEL_ROW.match(line)
            # An English keyword is a keyword only in upper case. The Level cell and a note such as "(MAY)" beside a bold keyword are allowed.
            en = EN_KEYWORD.search(QUOTED.sub("", CODE.sub("", BOLD.sub("", m.group(3) if m else line))))
            if en and not has_level(en.group(), bolds):
                problems.append(f"{where} \"{en.group()}\" is not bold. Bold it for a requirement; write it in lower case for explanation")
            if m:
                id_, level, rest = m.groups()
                rest_bold = " ".join(BOLD.findall(rest))
                if not has_level(level, rest_bold):
                    problems.append(f"{where} the level of {id_} is {level} but the sentence has no bold \"{level}\" or \"{LEVEL_WORD[level]}\"")
                if level == "MUST" and has_level("MUST NOT", rest_bold) and not has_level("MUST", rest_bold):
                    problems.append(f"{where} the level of {id_} is MUST but the sentence is a prohibition")
    summary = f"{len(files)} documents, " + ", ".join(f"{k} {v}" for k, v in counts.items())
    return report("keywords", problems, summary)


# -------------------------------------------------------------- journal

STEP_HEADING = re.compile(r"^## (?:Step|스텝) \d+", re.M)


def git(*a):
    return subprocess.run(["git", *a], capture_output=True, text=True)


def cmd_journal(args):
    date = args.date or datetime.date.today().isoformat()
    journal = f"{args.docs}/journal/{date}.md"
    status = git("status", "--porcelain", "--untracked-files=all")
    if status.returncode != 0:
        return inconclusive("journal", "not a git repository")
    changed = [line[3:].split(" -> ")[-1].strip('"') for line in status.stdout.splitlines()]
    if not changed:
        last = git("log", "-1", "--name-only", "--format=").stdout.split()
        if journal in last:
            return report("journal", [], "the working tree is clean; the last commit has today's journal")
        return report("journal", [], "the working tree is clean; there is no change to record")
    if journal in changed:
        steps = len(STEP_HEADING.findall(read(journal))) if Path(journal).exists() else 0
        return report("journal", [], f"{journal} changed. {steps} steps. {len(changed)} files changed")
    return report(
        "journal",
        [f"{len(changed)} files changed but {journal} did not. Write the journal before the commit"],
        "the journal is written for every step",
    )


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
        if base.name == "playbooks":
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
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    t = sub.add_parser("trace")
    t.add_argument("--docs", default="docs")
    t.add_argument("--tests", help="default: the first of tests, test, src/test that exists")
    t.add_argument("--no-tests", action="store_true")
    t.set_defaults(fn=cmd_trace)
    k = sub.add_parser("keywords")
    k.add_argument("files", nargs="*")
    k.add_argument("--docs", default="docs")
    k.set_defaults(fn=cmd_keywords)
    j = sub.add_parser("journal")
    j.add_argument("--docs", default="docs")
    j.add_argument("--date")
    j.set_defaults(fn=cmd_journal)
    s = sub.add_parser("self")
    s.set_defaults(fn=cmd_self)
    args = p.parse_args()
    sys.exit(args.fn(args))


if __name__ == "__main__":
    main()
