# Trace by ID

Give IDs to requirements and rules. Link source → spec → domain → plan → test names by ID.

**Why:** One answer changes several documents. With IDs you know at once where to edit. Without IDs you cannot verify that "every requirement has a test".

**How:**
- An acceptance criterion is `AC-<goal>.<number>`. A domain rule is `R<number>`. Number the rules of an ADR.
- The plan's "What to verify" points at IDs. Do not rewrite the sentences there.
- A test name starts with the ID, or has it right after an underscore (`ac1_1_…`, `test_ac1_1_…`, `r4_…`, `adr0003_…`). The check does not find `TestAC1_1_…`. The ID appears in the failure message.
- The ID in a test's name is the ID of the sentence that the test's input breaks.
- Do not renumber IDs. Append new items at the end. What an ID already in use points at does not change.
- After changing a document, run `scripts/sdd-check.py trace` (with `--no-tests` while no test exists yet).

**Stop:** Do not implement a requirement that has no ID. Create the ID in the document first.

**Evidence:** At the end of a slice the output of `sdd-check.py trace` is a pass.
