---
name: sdd
description: Document-first, test-first development. Write the documents first (brainstorming → spec → domain → ADR → plan), write tests before code, write a journal entry for every step, and do one step at a time. Use it when the user names sdd, or in a project that has `docs/journal/` or whose rules file says it follows sdd.
---

# sdd

The playbooks, principles, references and script sit next to this file (this skill's base directory). Read a file to the end before you apply it. This file is only the index.

The project rules file depends on the harness: `CLAUDE.md` in Claude Code, `.omp/AGENTS.md` in omp. A rules file the harness already loads (for example a root `AGENTS.md`) counts as the project's rules file. Wherever this skill says `CLAUDE.md`, it means that file in the current harness. Existing repository rules (rules files the harness loads, CONTRIBUTING) come before this skill's defaults for commit messages, branch names, documents and commands to run before a commit (such as `make lint`).

If this harness has no rules file but the other harness's does, follow it and propose to copy it or to point to it.

The **project root** is the folder the user names for the project; it holds or will hold the project's `docs/`. It may be a subfolder of the git repository. **Existing code** means that folder already has code.

A **step** is one request and its journal entry. The numbered items of a playbook are **playbook steps**. A **slice** is the smallest flow that a user can run from start to end once; its documents, its number and its branch are described in `references/doc-templates.md`.

Invoking this skill is the user's request for what the playbooks name: reproducing a reported symptom, running whole test suites, injecting defects, and reading `git`.

## Always

- First message of a task → restate in your own words the goal, the problem being solved, and the smallest thing this step will produce; in a kickoff's first reply, one sentence before the first question. Do not wait for confirmation. If the request names no target ("continue where we left off") and the previous step named a candidate, "continue" means that candidate. With no candidate, read with **Status**, show the state, and ask which step to run; the read and the question are one Status step, and the chosen playbook is the next step. If the evidence does not match the request, show the evidence, then ask.
- Before a change → write the end condition as a sentence that can pass or fail. "Better" is not a condition.
- One request → one step. Stop when the step ends. A request that names several plan tasks runs them one after another, one step per task; stop after the last. Details are in `references/journal-format.md`. `principles/user-drives-the-pace.md`.
- End of a step → **Wrap-up** (`playbooks/wrap-up.md`). Write the journal for every step, including a step that only commits or pushes.
- Before saying "done" → `principles/see-it-fail.md` and `principles/real-surface.md`.
- You meet something the documents do not decide → `principles/mark-the-source.md`. Exit codes, messages and file formats are behaviour visible from outside. If the decision requires changing a document, stop and get approval. Otherwise decide it and record it in the journal under "Decision (AI)".
- A MUST in the project rules (`CLAUDE.md`, ADRs) is inconvenient → `principles/rules-as-written.md`. Do not narrow the rule. What the user may waive and what you keep even when asked is listed there.
- Writing or changing a document → `references/doc-style.md`. The language of documents, the journal, commit messages and replies is set there under Language. After changing a document outside **Design docs**, run `trace --no-tests` and `keywords`.
- Committing → read `git status` first. Stage files by path. Do not use `git add -A`. A commit made while a check fails names the failure in the message and the journal.
- Before asking the user → sort the questions. Run what can be learned by running it. Do not ask what an approved decision already answers. Ask what only the user can decide one question at a time, with options and a recommendation. Quote text that needs approval as it will be written, in the document's language. Approval given before the text was shown is not approval; a batch "yes" covers only what was shown.
- The user corrects you → write it under Observations in the journal, every time. The `sdd-reflect` skill turns a repeated correction into a rule or a check; only the user can start it, so propose it.

## Principles

Read `principles/<name>.md` to the end before you apply a principle. Cite only principles you read in this session. In the report, state the decision the principle changed.

- **The user sets the pace** (`principles/user-drives-the-pace.md`). When a step ends, when the next task is in sight. Do only the requested step and stop.
- **Do only the scope of the step** (`principles/scope-of-the-step.md`). When you think "it would be good to do this now too". Build only what the plan task and the tests require.
- **Trust only a check you have seen fail** (`principles/see-it-fail.md`). When a test passes from the start, when you check a "must not exist" rule. Inject a defect and see red.
- **Look at the real surface** (`principles/real-surface.md`). After all tests pass, before saying it is done. Run it the way it is really used.
- **Assert the reason, not the status** (`principles/assert-the-reason.md`). When a test fails, when a test checks an error. See that it fails for the right reason and passes for the right reason.
- **Label the claim** (`principles/label-the-claim.md`). When you write a fact in the journal, a review note or a report. Tell verified, assumed, read and question apart.
- **Mark the source of a decision** (`principles/mark-the-source.md`). When the AI decided, when an approved document changes. Record who proposed and who approved.
- **Follow the rules as written** (`principles/rules-as-written.md`). When you did not follow a MUST or want to skip one. Do not change the rule; bring the record in line with the rule.
- **Trace by ID** (`principles/trace-by-id.md`). When you write or change acceptance criteria, rules or tests. Link spec → domain → plan → tests by ID.
- **Conclusions in documents, process in the journal** (`principles/conclusions-and-process.md`). When deciding what to write where. Put remaining work into the plan.
- **Encode rules in checks** (`principles/encode-in-checks.md`). When you find a rule that people keep by being careful. Make a test or a script enforce it.
- **Fix the cause** (`principles/fix-the-cause.md`). When fixing a defect. Fix the cause, not one of its symptoms.

## Autonomy

- **Inside a step, proceed without asking.** These can be undone: reading, running tests and builds, running it for real (a server on another port), extracting a copy into a scratch folder and building it, injecting a defect temporarily and restoring it.
- **Between steps, stop.** Start the next plan task, the fix for a review note, or a commit only when the user asks.
- **Always stop and ask.** Pushing (a push requested in this step is approved; name a new remote branch in the report). Creating or switching a branch. Rewriting unpushed commits (squash, amend); a rewrite the user asked for in this step is approved. If the harness blocks it, give the user the exact command, which stages every changed file under `docs/journal/`, and record it. Deleting or committing untracked files you did not create. Changing the meaning of an approved document. A decision that requires changing a document (`principles/mark-the-source.md`). Changing the project rules. Sending information outside.
- **Never rewrite pushed history**, even when asked. Offer a reverting commit instead; if the pushed change is journal-only, there is nothing to revert, so say so.
- **Write approved decisions into the documents.** Add "Revised (date): what" to the status line. Do not add anything unapproved to an approved document; quote every change it needs, including the ones the approved change forces, and get approval.
- **Worktrees are allowed**, because branch switching is often blocked. Put them outside the project folder. A worktree needs the skill too: if the skill sits uncommitted inside the project, start the harness from the main checkout, or install the skill for the user.
- **You may disagree.** If you have grounds, give a different recommendation. If the user chooses against your recommendation, do it their way and record that fact and its result in the journal.

## Delegation

- The main conversation owns the playbook. Do not hand the execution of a playbook to a subagent.
- Restate the user's goal in every subagent brief. A subagent's report is not evidence. Read the diff and the output yourself.
- Review is done by an agent that did not write the change: `sdd-reviewer`. Do not give it your conclusions. Give it the target as a diff without the journal (`git show <hash> -- . ':!docs/journal'`), the document paths, the rules file path, the checker path, the test command and the user's goal. Wait for its report before writing the review notes.

## Reporting

- A line the harness requires goes at the very start of the reply. Then a sentence that restates the goal.
- Every claim has its evidence or a label in the same sentence. A verification you could not run is "inconclusive". It is not a pass.
- Do not hand the user a verification that you can run yourself.
- The format is `references/report-template.md`. A playbook's `**Report:**` line sets the items for that kind of report.
- End with exactly one line naming the candidate for the next step, and write it under Next step in the journal. Do not start it. A reply that stops on a question to the user ends with that question instead.

## Playbooks

Pick the one playbook that fits the request and open `playbooks/<name>.md`. In the journal's Done, name each playbook step: done, `skip: <reason>`, or `n/a: <why the condition is false>`. If none fits, use `playbooks/figure-it-out.md`.

A change whose cause is in a document is a **Fix**: documents → test → code, in one step. A small addition inside an existing slice does not need a kickoff. It is small when it needs no new or changed ADR, at most three acceptance criteria and one plan task; a replacement row counts as one new acceptance criterion. A change to an approved criterion of the open slice stays in that slice, with no small-or-new question; the limit still applies. For any other request, say whether it is a small addition or a new slice and why; the user decides. Ask the ADR-level questions first, then show the new acceptance criteria and the task and get approval. Then **Design docs** appends them to that slice's spec and plan, and a rule to its domain document if one is needed, with "Revised (date): what" on the status line. If the count grows past the limit during Design docs, ask again. Stop there; **Plan task** implements the task in the next step. Keep at most one open design branch per project; stacked branches follow `references/doc-templates.md`. Anything else that is new goes to **Kickoff**.

- **Kickoff** (`playbooks/kickoff.md`). Brainstorming for a new project or a new slice. Draw the topics out of what the user says and the input material, discuss them one at a time, and close them. Write no code. ("kickoff", "brainstorming", "draw out the intent")
- **Design docs** (`playbooks/design-docs.md`). Write or rewrite a slice's spec, domain, ADRs and plan, or change an approved criterion the user asks to change. Unlike kickoff, it fixes decisions in documents. ("write the spec", "ADR", "make the plan", "change AC-1.2")
- **Plan task** (`playbooks/plan-task.md`). Implement one task of the plan, test first. ("do task 3", "go on with the next task")
- **Review** (`playbooks/review.md`). Explain the change in a commit or in the working tree and write review notes. Fix nothing. ("explanation document", "review")
- **Fix** (`playbooks/fix.md`). Fix one review note or one defect. Unlike a plan task, it is not a new feature. ("fix note 1", "fix this defect", "close the gap")
- **Conformance** (`playbooks/conformance.md`). Check every MUST in the documents against the code and the tests. Unlike review, the target is the whole set of documents, not a commit. ("verify the code against the documents", "does every AC have a test")
- **Confirm decisions** (`playbooks/decisions.md`). Collect the decisions the AI made that the user has not confirmed, and get approval. ("approve the proposals", "what needs confirmation")
- **Status** (`playbooks/status.md`). Changes nothing but the journal. Answer with the remaining work in four lists, or answer a question that asks for no change. ("what is left", "where are we", "why did we choose X")
- **Wrap-up** (`playbooks/wrap-up.md`). Do it at the end of every playbook. Journal, report, and a commit, push or merge when asked. ("commit", "push", "merge")
- **Figure it out** (`playbooks/figure-it-out.md`). When no playbook fits. Design the playbook steps, then run them.

## Check script

`scripts/sdd-check.py` turns written rules into checks. The playbooks call it. Run it as `<this skill's folder>/scripts/sdd-check.py <command>` from the project root; `--help` lists the options. Exit codes: 0 PASS, 1 FAIL, 2 INCONCLUSIVE; inconclusive is not a pass. Do not change the script, the IDs, the end conditions or document lines to make it pass.

- `trace`: is every active ID in a plan and in a test name, and do the end-condition counts match? Details: `principles/trace-by-id.md`.
- `keywords`: are the RFC 2119 keywords in the spec, domain and ADR documents used by the rules? Details: `references/doc-style.md`.
- `journal`: does the change being recorded carry the journal? Details: `references/journal-format.md`.
- `self`: do this skill's index and files agree?

## Explanation skills

`review/` holds three skills that produce explanation documents. Do not look for them in the skill list. When a playbook points at one, read its `SKILL.md` and follow it as a non-interactive run: skip its question round and its closing offers, take the user's request as the purpose, and state the reader you assumed. The commit or flow is the one the playbook names. Write their labels as sdd's: confirmed → verified, guess → assumed. Paths inside it are relative to that file's folder; the shared template is `review/explain-diff/assets/template.html`. An explanation document is for a person to read. It lives in the main checkout's `explanations/`. sdd sets the file name (`playbooks/kickoff.md` step 4); it overrides the explanation skill's own name. Committed documents refer to it by file name and commit; replies and the journal, by absolute path. Do not commit it.

- `review/explain-full-map/SKILL.md`: a map of the whole repository. Used by kickoff.
- `review/explain-full-flow/SKILL.md`: the flow of one feature. Used by kickoff.
- `review/explain-diff/SKILL.md`: the explanation of one commit. Used by review.
