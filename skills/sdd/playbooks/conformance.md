### Conformance

**You own the list of requirements in the documents. The documents are the standard.**

"It complies today" and "a test enforces it" are different. A rule kept by being careful breaks in the next task. Conformance also finds defects in the documents. It does not go one way only.

1. List every MUST and MUST NOT in the documents (the ID or the document name, and the sentence). Run the whole test suite and record the baseline.
2. For each sentence, collect the facts: is there a test that enforces it, does the code comply. Verify with `grep` and by running.
3. Sort the sentences into four groups: complies and a test enforces it / complies but nothing enforces it / does not comply / not built yet (a later plan task).
4. Where it does not comply: if the documents hold the answer, write the test first and fix it. If it needs a new decision, do not fix it. Leave it in the list.
5. Where nothing enforces it: add a test (`principles/encode-in-checks.md`). Do not add a test that does not match the sentence exactly.
6. Inject defects one at a time and run the whole test suite. Record which test caught each. Restore (`principles/see-it-fail.md`).
7. Fix the document defects that the conformance check found. Run `scripts/sdd-check.py trace` and `scripts/sdd-check.py keywords`.
8. Do the **Wrap-up** (`wrap-up.md`).

**Report:** the table of the four groups, what was fixed, the tests added and the sentence each enforces, the defect-injection table, the non-compliance left unfixed and the decision it needs, the scope the conformance check did not cover.
