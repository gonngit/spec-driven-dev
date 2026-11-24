---
name: sdd
description: Document-first, test-first development. Write the documents first (brainstorming → spec → domain → ADR → plan), write tests before code, write a journal entry for every step, and do one step at a time. Runs only when invoked by name.
disable-model-invocation: true
---

# sdd

The playbooks, principles, references and script sit next to this file (this skill's base directory). Read a file to the end before you apply it. This file is only the index.

The project rules file depends on the harness: `CLAUDE.md` in Claude Code, `.omp/AGENTS.md` in omp. Wherever this skill says `CLAUDE.md`, it means that file in the current harness.

A **step** is one request and its journal entry. The numbered items of a playbook are **playbook steps**. A **slice** is the smallest flow that a user can run from start to end once; its documents, its number and its branch are described in `references/doc-templates.md`.

## Always

- First message of a task → restate in your own words the goal, the problem being solved, and the smallest thing this step will produce. Do not wait for confirmation. If the evidence does not match the request, show the evidence and stop.
- Before a change → write the end condition as a sentence that can pass or fail. "Better" is not a condition.
- One request → one step. Stop when the step ends. `principles/user-drives-the-pace.md`.
- End of a step → **Wrap-up** (`playbooks/wrap-up.md`). Write the journal for every step, including a step that only commits or pushes.
- Before saying "done" → `principles/see-it-fail.md` and `principles/real-surface.md`.
- You meet something the documents do not decide → `principles/mark-the-source.md`. If the decision requires changing a document, stop and get approval. Otherwise decide it and record it in the journal under "Decision (AI)".
- A MUST in the project rules (`CLAUDE.md`, ADRs) is inconvenient → `principles/rules-as-written.md`. Do not narrow the rule.
- Writing or changing a document → `references/doc-style.md`. Documents are written in the language the user writes in, Korean or English.
- Committing → read `git status` first. Stage files by path. Do not use `git add -A`.
- Before asking the user → sort the questions. Run what can be learned by running it. Do not ask what an approved decision already answers. Ask what only the user can decide one question at a time, with options and a recommendation.
- You received the same correction twice → write it under Observations in the journal. The `sdd-reflect` skill turns it into a rule or a check.

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
- **Always stop and ask.** Pushing. Creating or switching a branch. Changing the history of pushed commits. Deleting or committing files you did not create. Changing the meaning of an approved document. A decision that requires changing a document (`principles/mark-the-source.md`). Changing the project rules. Sending information outside.
- **Write approved decisions into the documents.** Add "Revised (date): what" to the status line. Do not add anything unapproved to an approved document.
- **You may disagree.** If you have grounds, give a different recommendation. If the user chooses against your recommendation, do it their way and record that fact and its result in the journal.

## Delegation

- The main conversation owns the playbook and the todo list. Do not hand the execution of a playbook to a subagent.
- Restate the user's goal in every subagent brief. A subagent's report is not evidence. Read the diff and the output yourself.
- Review is done by an agent that did not write the change: `sdd-reviewer`. Do not give it your conclusions. Give it only the target, the document paths and the user's goal.

## Reporting

- Start with a sentence that restates the goal.
- Every claim has its evidence or a label in the same sentence. A verification you could not run is "inconclusive". It is not a pass.
- Do not hand the user a verification that you can run yourself.
- The format is `references/report-template.md`. A playbook's `**Report:**` line sets the items for that kind of report.
- End with one line naming the candidate for the next step. Do not start it.

## Playbooks

Pick the one playbook that fits the request. Open `playbooks/<name>.md`. Copy its playbook steps into the todo list as they are, then add the detailed todos of the task. Leave a playbook step you do not do as `skip: <reason>`. If none fits, use `playbooks/figure-it-out.md`.

A small addition inside an existing slice does not need a kickoff. It is small when it needs no new ADR, at most three acceptance criteria and one plan task. Say whether the request is a small addition or a new slice and why; the user decides. Show the new acceptance criteria and the task and get approval. Then **Design docs** appends them to that slice's spec and plan with "Revised (date): what" on the status line, and **Plan task** implements the task. If the slice is already merged, propose a branch `slice/NN-<name>-<addition>`. Anything else that is new goes to **Kickoff**.

- **Kickoff** (`playbooks/kickoff.md`). Brainstorming for a new project or a new slice. Draw the topics out of what the user says and the input material, discuss them one at a time, and close them. Write no code. ("kickoff", "brainstorming", "draw out the intent")
- **Design docs** (`playbooks/design-docs.md`). Write or rewrite a slice's spec, domain, ADRs and plan. Unlike kickoff, it fixes decisions in documents. ("write the spec", "ADR", "make the plan")
- **Plan task** (`playbooks/plan-task.md`). Implement one task of the plan, test first. ("do task 3", "go on with the next task")
- **Review** (`playbooks/review.md`). Explain the change in a commit or in the working tree and write review notes. Fix nothing. ("explanation document", "review")
- **Fix** (`playbooks/fix.md`). Fix one review note or one defect. Unlike a plan task, it is not a new feature. ("fix note 1", "fix this defect", "close the gap")
- **Conformance** (`playbooks/conformance.md`). Check every MUST in the documents against the code and the tests. Unlike review, the target is the whole set of documents, not a commit. ("verify the code against the documents", "does every AC have a test")
- **Confirm decisions** (`playbooks/decisions.md`). Collect the decisions the AI made that the user has not confirmed, and get approval. ("approve the proposals", "what needs confirmation")
- **Status** (`playbooks/status.md`). Changes nothing but the journal. Answer with the remaining work in four lists. ("what is left", "where are we")
- **Wrap-up** (`playbooks/wrap-up.md`). Do it at the end of every playbook. Journal, report, and a commit when asked. ("commit")
- **Figure it out** (`playbooks/figure-it-out.md`). When no playbook fits. Design the playbook steps, then run them.

## Check script

`scripts/sdd-check.py` turns written rules into checks. The playbooks call it. Run it from the project root: it reads `docs/`, the test folder and git from the current directory. Do not change the script, the IDs or the end conditions to make it pass.

- `trace`: is every ID in the spec and the domain present in the plan and in the test names? Until the last task of a slice, IDs of tasks not built yet have no test; that is expected.
- `keywords`: are the RFC 2119 keywords in the documents used by the rules?
- `journal`: did today's journal change together with this change?
- `self`: do this skill's index and files agree?

## Explanation skills

`review/` holds three skills that produce explanation documents. Do not look for them in the skill list. When a playbook points at one, read its `SKILL.md` and follow it. Paths inside it are relative to that file's folder. An explanation document is for a person to read. Do not commit it.

- `review/explain-full-map/SKILL.md`: a map of the whole repository. Used by kickoff.
- `review/explain-full-flow/SKILL.md`: the flow of one feature. Used by kickoff.
- `review/explain-diff/SKILL.md`: the explanation of one commit. Used by review.
