---
name: sdd-reflect
description: Find repeated corrections and repeated kinds of work in the journal and the git history, and write proposed changes to sdd. Does not change the skill before approval. Runs only when invoked by name.
disable-model-invocation: true
---

# sdd-reflect

**You own the proposed changes to sdd. The user decides what is applied.** Do not change the skill in the middle of a task. A retrospective is one step.

The input is the journal. In this workflow the journal is the record of corrections. There is no need to dig through conversation records.

## Procedure

1. Set the range: the journals (`docs/journal/*.md`) and `git log` since the last retrospective. If there was none, all of them.
2. Collect signals. Record the source (date, step) of each.
   - From "Observations" in the journal: "mistake of the AI", "the user corrected it", "the user reset the pace".
   - "Rules not followed" items.
   - "The user chose against the AI's recommendation".
   - Playbook steps skipped as `skip: <reason>`. If the same playbook step is skipped often, that playbook step is wrong.
   - "No playbook fitted" (records of **Figure it out**).
   - Assumptions that a later step showed to be wrong.
   - Fixing commits in `git log`: ones that fix the commit just before them.
3. Apply the **rule of two**. Keep only the signals that appeared in two or more different steps. Send the ones that appeared once to a "seen once" list.
4. For each remaining signal, find what already exists: sdd's "Always", a principle, a playbook step, the check script. If it exists and was not followed, raise the level of enforcement. Do not write more prose.
5. Write the proposed changes. Pick the highest rung of the ladder of enforcement.
   1. The structure makes the mistake impossible (a template, the location of a file).
   2. A script, or a test that checks the structure, checks it. The failure message says how to fix it.
   3. A test catches it.
   4. Write it as a playbook step or a principle. Nothing fails when it is skipped. That is why it is last.
6. Show the proposed changes in three groups: **accept** (recommended), **reject** (with the reason), **postpone** (seen once). Wait.
7. Apply only what was approved. Run `scripts/sdd-check.py self` (it is in the sdd folder). A change to the skill is a different commit from a change to the project.
8. Write in the journal: the table of signals, what was approved, what was rejected.

## Format of a proposed change

| # | Signal (2 or more sources) | What exists now | Proposed change | Level of enforcement | Files changed |
|---|---|---|---|---|---|

## What not to do

- Do not promote a preference that appeared once to a rule. It becomes a rule fitted to that session.
- Do not think first of adding principles. See first whether something can be deleted or merged.
- Do not put into sdd what fits only one project (the name of a technology, the name of a package). Put it into that project's `CLAUDE.md` (`.omp/AGENTS.md` in omp) or an ADR.
- Do not loosen a condition in `sdd-check.py` to make a check pass.

**Report:** the range read, the table of signals, the table of proposed changes (accept, reject, postpone), the files applied, the output of `self`.
