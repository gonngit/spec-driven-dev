### Review

**You own the review notes. Do not decide. Do not fix.**

The author is not the judge. What you do not know shows when you try to tell a reader the reason. "I did not verify the reason" is a sentence that cannot go into a review note. Verify it.

1. Set the target: a commit hash or the working tree. If there are uncommitted changes, ask which to explain. Read `git show --stat` (for the working tree: `git status` and `git diff --stat`): are there files that do not belong to the task?
2. If the target differs from the current working tree, extract that commit into a scratch folder outside the repository and build it (`git archive`). Do not touch the project's working tree.
3. Run boundary experiments: inputs the tests did not think of, what the rules miss, things done at the same time, the time taken. Record numbers.
4. Hand an independent review to the `sdd-reviewer` agent. The brief holds the target as a diff without the journal (`git show <hash> -- . ':!docs/journal'`), the document paths, the rules file path, the checker path (`scripts/sdd-check.py` of this skill), the test command and the user's goal. Do not give it your conclusions. Wait for its report before step 5; do not end the turn while it runs.
5. Write the review notes under "Review notes" in the journal, in the format of `references/review-memo.md`, with IDs `S<step>-<n>`. Merge the reviewer's findings into that table and keep their labels. Label every note with the labels of `principles/label-the-claim.md`.
6. Read `review/explain-diff/SKILL.md` and follow it to produce the explanation document, named as `kickoff.md` step 4 says. Its section 7 repeats the journal's note table. With a one-off script kept outside the repository, compare the quoted code with the diff of the target. Compare widget results with the results of a real run. Do not commit the explanation document.
7. Do the **Wrap-up** (`wrap-up.md`). If anything changed after the target, record it under Observations.

**Report:** the table of review notes, the table of experiments, the result of the comparison (the number of lines, the number that differ), what the independent review found that you missed, one question asking how to handle the notes.
