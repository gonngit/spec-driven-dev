---
name: sdd-reflect
description: Find repeated corrections and repeated kinds of work in the journal and the git history, and write proposed changes to sdd. Does not change the skill before approval. Only the user starts it; sdd proposes it.
disable-model-invocation: true
---

# sdd-reflect

**You own the proposed changes to sdd. The user decides what is applied.** Do not change the skill in the middle of a task. A retrospective is one step, with the phase **Retrospective** (Korean **회고**). End it with sdd's Wrap-up.

The input is the journal. In this workflow the journal is the record of corrections. There is no need to dig through conversation records.

## Procedure

1. Set the range: the journals (`docs/journal/*.md`) and `git log` since the last step with the phase Retrospective / 회고. If there was none, all of them. Also read that step's "seen once" list and its rejected proposals.
2. Collect signals. Record the source (date, step) of each.
   - From "Observations" in the journal: mistakes of the AI, corrections by the user, the user resetting the pace, requests refused under the kept rules, defects in the skill itself.
   - "Rules not followed" items.
   - Places where the user chose against the AI's recommendation.
   - Playbook steps marked `skip:` under "Done". If the same playbook step is skipped often, that playbook step is wrong. `n/a:` is not a skip.
   - Records of **Figure it out** saying that no playbook fitted.
   - Assumptions that a later step showed to be wrong.
   - Fixing commits in `git log`: ones that fix the commit just before them.
3. Apply the **rule of two**. Keep only the signals that appeared in two or more different steps, counting the previous "seen once" list. Send the ones that appeared once to a new "seen once" list. Drop a signal whose proposal was rejected before, unless it has a new source.
4. For each remaining signal, find what already exists: sdd's "Always", a principle, a playbook step, the check script. If it exists and was not followed, raise the level of enforcement. Do not write more prose.
5. Write the proposed changes. Pick the highest rung of the ladder of enforcement.
   1. The structure makes the mistake impossible (a template, the location of a file).
   2. A script, or a test that checks the structure, checks it. The failure message says how to fix it.
   3. A test catches it.
   4. Write it as a playbook step or a principle. Nothing fails when it is skipped. That is why it is last.
6. Show the proposed changes in three groups: **accept** (recommended), **reject** (with the reason), **postpone** (seen once). Wait.
7. Apply only what was approved. Run `scripts/sdd-check.py self` (it is in the sdd folder); it checks only the index and the shape of the files. A change to a check is verified by seeing it fail on the recorded mistake, and by the checker's tests in the skill repository. Commit the skill change first, in the skill's own repository; it carries no project journal. If the skill folder is not under git, ask, and record the diff in the journal.
8. Write in the project journal: the table of signals, what was approved, the rejected proposals with their reasons, the "seen once" list, and the skill commit.

## Format of a proposed change

| # | Signal (2 or more sources) | What exists now | Proposed change | Level of enforcement | Files changed |
|---|---|---|---|---|---|

## What not to do

- Do not promote a preference that appeared once to a rule. It becomes a rule fitted to that session.
- Do not think first of adding principles. See first whether something can be deleted or merged.
- Do not put into sdd what fits only one project (the name of a technology, the name of a package). Put it into that project's `CLAUDE.md` (`.omp/AGENTS.md` in omp) or an ADR.
- Do not loosen a condition in `sdd-check.py` to make a check pass.

**Report:** the range read, the table of signals, the table of proposed changes (accept, reject, postpone), the files applied, the output of `self` and of the check's failing run.
