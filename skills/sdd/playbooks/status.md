### Status

**You own the answer to "where are we now". Read only.** Fix nothing. Do not start the next piece of work.

Do not answer from memory. Ask the repository and the documents. Ask `git` directly, not the screen.

1. Read the plan's task table, `git log`, `git status`, and the difference from the remote.
2. From the journal, collect "Remaining work", "Review notes", "needs confirmation" and "not fixed". Leave out what a later step closed.
3. Run `scripts/sdd-check.py trace`.
4. Sort into four: the remaining plan tasks / uncommitted changes and unpushed commits / decisions waiting for confirmation / things known but not fixed.
5. Do the **Wrap-up** (`wrap-up.md`). In the journal, record the question and the answer.

**Report:** the four lists, each item with its source (a journal step or a file), and one candidate for the next step.
