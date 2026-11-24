### Conformance

**You own the list of requirements in the documents. The documents are the standard.**

"It complies today" and "a check enforces it" are different. A rule kept by being careful breaks in the next task. Conformance also finds defects in the documents. It does not go one way only.

1. List every MUST and MUST NOT in the spec, domain, ADRs and the project rules file (the ID or the document name, and the sentence). Leave out REPLACED and REMOVED rows, retired numbered ADR items, and the rules of a replaced ADR. Run the whole test suite and record the baseline.
2. For each sentence, collect the facts: is there a check (a test or a script) that enforces it, does the code comply. Verify with `grep` and by running.
3. Sort the sentences into four groups: complies and a check enforces it / complies but nothing enforces it / does not comply / not built yet (a later plan task; add no test for it).
4. List the document defects found, including a MUST sentence with no ID. Show the list, the fixes and the IDs the new tests will carry, and get approval before naming any test. Write the approved document fixes now, IDs first, and run `scripts/sdd-check.py trace --no-tests` and `keywords`. A fix may be split: do the approved part and leave the rest in the list.
5. Where it does not comply: if the documents hold the answer, write the test first and fix it. If it needs a new decision, do not fix it. Leave it in the list.
6. Where nothing enforces it: add a check (`principles/encode-in-checks.md`). Do not add a check that does not match the sentence exactly.
7. Inject defects one at a time and run the whole test suite. Record which check caught each. Restore (`principles/see-it-fail.md`).
8. Run `scripts/sdd-check.py trace` and `scripts/sdd-check.py keywords`.
9. Do the **Wrap-up** (`wrap-up.md`).

**Report:** the table of the four groups, what was fixed, the checks added and the sentence each enforces, the defect-injection table, the non-compliance left unfixed and the decision it needs, the scope the conformance check did not cover.
