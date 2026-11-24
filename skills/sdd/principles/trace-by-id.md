# Trace by ID

Give IDs to requirements and rules. Link source → spec → domain → plan → test names by ID.

**Why:** One answer changes several documents. With IDs you know at once where to edit. Without IDs you cannot verify that "every requirement has a test".

**How:**
- IDs: `AC-<goal>.<number>`, `R<number>`, and `ADR-NNNN.k` for the k-th numbered item with a bold keyword under an ADR's `## Decision`. Only rows `| ID | LEVEL | …` define AC and R IDs; a Sources list does not. Put a product name that looks like an ID in backticks (`Cloudflare R2`); the cross-reference check skips it.
- The plan's "What to verify" points at IDs. A mention anywhere in the plan counts as covered. `ADR-NNNN` covers all of that ADR's rules. Write a range as `AC-1.1~AC-1.3` or `R1~R3` (`∼`, `～`, `〜` work too). Do not rewrite the sentences there.
- Test names: only function names (`def`, `func` and `function` names starting with `test`/`Test`; `fn`, `void`, `fun` names) and the first string argument of `test(`, `it(` and `describe(` count. Comments, docstrings and other code do not. This is a name check only: a skipped or empty test still counts.
  - A function name carries an ID when it starts with the token or has it right after `_`: `ac1_1_`, `r4_`, `adr0003_2_`. The trailing `_` is required. `TestAC1_1_…` is not found.
  - A string name carries an ID when it starts with `AC-1.1`, `R4` or `ADR-0003.2`, followed by a space or punctuation.
  - Pin tests (`pin_…`, `test_pin_…`) carry no ID and are ignored.
- Only test files are read (`test_*`, `*_test.*`, `*.test.*`, `*.spec.*`, `*_spec.*`; `*Test.*`, `*Tests.*`, `*Spec.*` only inside a test folder), in `tests`, `test` and `src/test`, or in the whole project when none of those exists; add `--tests <folder>` (repeatable) to name the folders. Run from the project root: the folder that holds `docs/`.
- The ID in a test's name is the ID of the sentence that the test's input breaks. Pin tests keep `pin_`. Other tests that carry no ID (a skeleton) are named `task<N>_` (`test_task<N>_` in Python); so is a whole-result test that breaks several rules, and each rule still needs its own test. ADR rules need tests only when the plan that mentions them has the "All N ADR rules" end condition.
- Do not renumber IDs. Append new items at the end. An ID's meaning never changes in place: mark the old row `REPLACED` or `REMOVED` (`references/doc-style.md`). `trace` fails while a test still names a REPLACED or REMOVED ID; plan references to them are allowed.
- After changing a document, run `scripts/sdd-check.py trace` (with `--no-tests` while no test exists yet). While a plan is half built, `trace --plan NN --upto K` checks only tasks 1..K.

**Stop:** Do not implement a requirement that has no ID. Create the ID in the document first.

**Evidence:** At the end of a slice the output of plain `sdd-check.py trace` is a pass. A pass is necessary, not sufficient: each plan task must also be recorded as verified in the journal.
