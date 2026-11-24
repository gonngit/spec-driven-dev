### Wrap-up

**You own the record of the step.** Do it at the end of every playbook. Start from playbook step 1 even when only a commit was requested.

Bring the record in line with the rules. "A simple step with no decision" is still a step.

1. Read `git status` and `git diff --stat`. Look for files you did not create, files that do not belong to this step, leftover temporary files, and defects that were not restored.
2. Write the journal (`references/journal-format.md`). Write it before the commit.
3. Run `scripts/sdd-check.py journal`.
4. Write the report (`references/report-template.md`).
5. If no commit was requested, go to playbook step 8.
6. Commit. Stage files by path. Ask before including a file you did not create. Do not commit explanation documents (`explanations/`). Write the message in the language of the project's documents.
7. Push only when asked. Do not change the history of pushed commits. To verify, ask `git` directly (`git status -sb`, `git ls-remote`).
8. Stop. Name the candidate for the next step in one line. Do not start it (`principles/user-drives-the-pace.md`).

**Report:** the format of `references/report-template.md`. If you committed, one line per commit on its content, plus the files left out and why.
