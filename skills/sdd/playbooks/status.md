### Status

**You own the answer to "where are we now". Change nothing but the journal.** Fix nothing. Do not start the next piece of work.

Do not answer from memory. Ask the repository and the documents. Ask `git` directly, not the screen.

1. Read the list of slices, the plan's task table, `git log`, `git status`, and the difference from the remote. A plan task is done when a journal step records its "What to verify" as verified.
2. From the journal, collect "Remaining work", "Review notes" and "Decision (AI)". Leave out what a later step closed.
3. Run `scripts/sdd-check.py trace`.
4. Sort into four: the remaining plan tasks / uncommitted changes and unpushed commits / decisions waiting for confirmation / review notes that are not closed.
5. Do the **Wrap-up** (`wrap-up.md`). In the journal, record the question and the answer.

**Report:** the four lists, each item with its source (a journal step or a file), and one candidate for the next step.
