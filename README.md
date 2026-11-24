# sdd

Agent skills for document-first, test-first development, for omp and Claude Code. Documents come first (brainstorming → spec → domain → ADR → plan), tests come before code, every step gets a journal entry, and the user sets the pace one step at a time.

## Where this comes from

This started as a copy of **Toby Lee's tstack** ([tobyilee/trealworld › tstack](https://github.com/tobyilee/trealworld/tree/main/tstack), commit `68fc5e2`): the `t-mode` skill with its playbooks, principles and check script, `t-reflect`, and the `t-reviewer` agent.

## What changed

1. **Renamed and made editable.** `t-mode` → `sdd`, `t-reflect` → `sdd-reflect`, `t-reviewer` → `sdd-reviewer`, `tstack-check.py` → `sdd-check.py`.
2. **Translated into English.** The skill text is English; the project documents it writes follow the project's language (Korean or English).
3. **Workflow additions.**
   - Kickoff is a discussion: the user speaks first, topics are settled one at a time.
   - Any change to an approved document stops for approval.
   - Existing code gets a map and flow documents first, through the bundled explanation skills in `skills/sdd/review/` (from [gonngit/explain-code](https://github.com/gonngit/explain-code)).
   - Work is cut into slices, each with its own number and branch; small additions have their own route.
   - Ten test rules taken from the lessons in Toby Lee's project `CLAUDE.md`.
4. **Decisions made after test runs.**
   - A changed requirement gets a new ID; the old row is marked `REPLACED` or `REMOVED`.
   - One open design branch per project; later work stacks on top of it.
   - Behaviour that existing code already has is pinned with `pin_` tests before it is changed.
   - A fixed list of what the user may waive and what the agent keeps even when asked.
   - `sdd` can start on its own in a project that uses it; `sdd-reflect` only when the user asks.
   - One language rule for documents, journal, commits and replies.
5. **Checker rewritten.** `sdd-check.py` now:
   - checks the change that is actually being committed (staged files, merges, subfolder projects);
   - reads only test names when matching tests to IDs, including ADR rules, partial plans and end-condition counts;
   - handles Korean keyword forms;
   - reports an unreadable file as inconclusive instead of crashing.

   Regression tests are in `tests/`.
6. **Tested.**
   - 48 scenario runs: simulated sessions, real omp and Claude Code sessions, and two real repositories.
   - Three rounds of fixes, with reruns after each of the first two.

## Layout

| Path | What |
|---|---|
| `skills/sdd/` | The skill: `SKILL.md` (index), `playbooks/`, `principles/`, `references/`, `scripts/sdd-check.py`, `review/` |
| `skills/sdd-reflect/` | Turns repeated corrections into rules or checks |
| `agents/sdd-reviewer.md` | Independent reviewer agent |
| `tests/` | Tests for `sdd-check.py`: `python -m pytest tests` |

## Install

| Harness | Skills folder | Agents folder |
|---|---|---|
| omp | `~/.omp/agent/skills/` | `~/.omp/agent/agents/` |
| Claude Code | `~/.claude/skills/` | `~/.claude/agents/` |

Copy `skills/sdd` and `skills/sdd-reflect` into the skills folder, and `agents/sdd-reviewer.md` into the agents folder.
