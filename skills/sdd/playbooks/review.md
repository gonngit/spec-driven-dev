### Review

**You own the review notes. Do not decide. Do not fix.**

The author is not the judge. What you do not know shows when you try to tell a reader the reason. "I did not verify the reason" is a sentence that cannot go into a review note. Verify it.

1. Set the target: a commit hash or the working tree. If there are uncommitted changes, ask which to explain. Read `git show --stat`: are there files that do not belong to the task?
2. If the target differs from the current working tree, extract that commit into a scratch folder and build it (`git archive`). Do not touch the project's working tree.
3. Run boundary experiments: inputs the tests did not think of, what the rules miss, things done at the same time, the time taken. Record numbers.
4. Hand an independent review to the `sdd-reviewer` agent. Give it only the target, the document paths and the user's goal. Do not give it your conclusions.
5. Read `review/explain-diff/SKILL.md` and follow it to produce the explanation document. Compare the quoted code with the commit by script. Compare widget results with the results of a real run. Do not commit the explanation document.
6. Write the review notes under "Review notes" in the journal, in the format of `references/review-memo.md`. Label every note (`principles/label-the-claim.md`).
7. Do the **Wrap-up** (`wrap-up.md`). If anything changed after the target, record it separately.

**Report:** the table of review notes, the table of experiments, the result of the comparison (the number of lines, the number that differ), what the independent review found that you missed, one question asking how to handle the notes.
