# Trust only a check you have seen fail

A check you have never seen fail proves nothing. Inject a defect and see red.

**Why:** When there is nothing to check, a test is green from the start. A "must not exist" rule and a test written after the implementation are also green from the start. That green is not evidence that the check works.

**How:**
- Write the test first and see it fail. A compile failure says only "the code does not exist". Put in an empty shell and see the assertion fail. If the empty shell already passes, the test is too weak: strengthen it.
- After writing a test, ask under what other defect it would still pass. Do not stop at seeing it fail once.
- For a check that is green from the start, put in a violation temporarily. See that only that check fails. Restore.
- Add a control. See that the check does not flag an allowed case.
- For a requirement that says "only A is allowed", write tests for what is not allowed. Look for the paths and inputs that the framework opens by itself.
- At the end of the task, inject defects one at a time and run the whole test suite. Record in a table which test caught each.
- Copy the file to a scratch folder outside the repository before you inject a defect, and restore from that copy. Injecting into a copied tree is also allowed. Delete the copies at Wrap-up. For Python, set `PYTHONDONTWRITEBYTECODE=1`. Do not restore through git (`git checkout`, `git restore`, `git stash`): uncommitted work is erased along with the defect.
- A defect the checks missed is a review note. Find out why.

**Stop:** Do not use a check you have not seen red as grounds for "verified". Do not change a check to make it pass.

**Evidence:** The journal has a table "defect injected → test that caught it". `git diff` shows none of the injected defects left behind, and `diff` against each copy is empty after the restore.
