### Status

**You own the answer to "where are we now", or to a question that asks for no change. Change nothing but the journal.** Fix nothing. Do not start the next piece of work.

Do not answer from memory. Ask the repository and the documents. Ask `git` directly, not the screen.

1. Run `git worktree list` and `git branch -a` first. Read the open slice branch or worktree of this project (`slice/*`, or the form `references/doc-templates.md` names for this repository, such as `<project>/slice/*`), and run the checks there. With stacked branches, read the top open branch and list the lower ones. For a question, run only what the answer needs; steps 2–4 are optional.
2. Read the list of slices, the plan's task table, `git log`, `git status`, and the difference from the remote. With no remote, say so and list the commits not merged into the default branch. A plan task is done when a journal step records its "What to verify" as verified; asking for the next task confirms the current one. If this harness has no rules file but the other harness's does, propose to copy it or to point to it (`SKILL.md`).
3. From the journal, collect "Remaining work", "Review notes" and "Decision (AI)". Leave out what a later step closed or replaced.
4. Run `scripts/sdd-check.py trace`. Put its lines under the remaining plan tasks.
5. Sort into four: the remaining plan tasks / uncommitted changes and unpushed commits / decisions waiting for confirmation / review notes that are not closed. For a question ("why did we choose X"), answer it instead from the documents and the journal, with sources. For "continue where we left off", ask which step to run; the chosen playbook is the next step.
6. Do the **Wrap-up** (`wrap-up.md`). In the journal, record "Question (user)" and "Answer (AI)", or "Request" and "Question (AI)".

**Report:** the four lists or the answer, each item with its source (a journal step or a file), and one candidate for the next step.
