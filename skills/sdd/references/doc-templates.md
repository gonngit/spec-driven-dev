# Document templates

Keep documents brief. Most of a document is tables. One document answers one question. Style and language follow `doc-style.md`. The templates below are in English; in a Korean document write the headings and sentences in Korean and use the fixed Korean forms listed in `doc-style.md`.

| Document | Location | Question it answers |
|---|---|---|
| Brainstorming | `docs/brainstorming/NN-<name>.md` | What is not known yet? |
| spec | `docs/spec/NN-<slice>.md` | What is being built? |
| domain | `docs/domain/NN-<name>.md` | Which words are used, and what must not break? |
| ADR | `docs/adr/NNNN-<decision>.md` | How is it built, and why was that chosen? |
| plan | `docs/plan/NN-<slice>.md` | In what order is it built, and what verifies it? |

## Slices

- A slice is the smallest flow that a user can run from start to end once. One slice has one brainstorming document, one spec and one plan.
- Numbers: the project kickoff is `00`. Slice N uses the number N for its brainstorming document, its spec and its plan.
- The list of slices lives in the project kickoff's brainstorming document (`docs/brainstorming/00-<name>.md`) as a table: number, name, the flow in one line. On existing code with no sdd documents there is no `00`: the list starts in `01-<name>.md`.
- One slice, one branch: `slice/NN-<name>`. `<name>` is short ASCII kebab-case. If the repository names its branches its own way (CONTRIBUTING), propose that form. In a repository shared by several projects, use `<project>/slice/NN-<name>`; `<project>` is short ASCII kebab-case too.
- At most one design branch per project is open at a time: a branch whose document changes are not yet merged into the default branch, whether it holds a slice, an addition or a fix. Design the next slice or addition after that branch is merged.
- If the user wants to start before the merge, create the new branch from the open branch (stacked), never from the default branch. IDs, plan task numbers and journal step numbers then continue.
- Once a branch has a branch stacked on it, the lower branch takes no new steps. Further work, including fixes the lower branch needs, goes on the top branch. With stacked branches, merge only the top branch: it carries the lower ones, in one merge step. If the lower branch is rejected, the stacked branch goes with it: ask the user.
- A small addition or a fix made after the slice was merged gets its own branch `slice/NN-<name>-<addition>`. It ends when it is merged.
- With no remote, merge locally into the default branch.
- Worktrees are allowed. Put them outside the project folder.
- A domain document carries the number of the slice that first needed it. A later slice adds to that document for a concept it already covers and creates a new document for a new concept.
- A slice ends when its last plan task is recorded as verified.

## spec

```markdown
# Spec NN. <name of the slice>

- Status: Draft
- Slice: <flow>
- Terms: follow the [domain model](../domain/NN-<name>.md).

This document says only **what** is built. How it is built and the technology are in the ADRs.

## How to read this document
<Only in the first spec; later specs use a `- How to read: …` line instead. The keyword table. The meaning of words used many times, such as "the system", "result", "rejects". How times and sizes are measured: machine, data size, command.>

## Goal 1. <who does what>

| ID | Level | Acceptance criterion |
|---|---|---|
| AC-1.1 | MUST | When <condition>, the system **MUST** <result>. |
| AC-1.2 | REPLACED | Replaced by AC-1.3 (YYYY-MM-DD). <the old sentence unchanged> |

## Existing behaviour this slice changes
<Only on existing code. Each pin test goes red when the change lands, and is deleted in that step.>

| Behaviour | Where | Pin test | Replaced by ID |
|---|---|---|---|

## Confirmed assumptions
<Existing behaviour that must stay. Its pin tests stay as regression tests.>

| Behaviour | Where | Pin test |
|---|---|---|

## Accepted limits
<Known limits the slice does not fix. They are not requirements: no keywords, no IDs, no tests. Collisions between decisions go here too.>
## Out of scope
## Differences from the original
<Only when there is an original that is being ported or rebuilt.>
## Sources
<A list, not a table: "- AC-1.1: <where in the input material>".>
```

## domain

```markdown
# Domain NN. <name>

- Status: Draft
- Scope: covers only what [Spec NN](../spec/…) needs.
- How to read: follow [Spec NN](../spec/…).

## Terms

| Term | Name in code | Meaning |
|---|---|---|
| <term the code already has> | … | existing. <meaning> |

| Word not used | Word used instead |
|---|---|

## Model
<The core concepts and how they relate. What is not part of the domain model.>

## Rules

| ID | Level | Rule | Where it is enforced |
|---|---|---|---|
| R1 | MUST | … | <name of the model or the feature> |
```

- The "Where it is enforced" column sets the scope of the plan's tasks.
- A definition that settles an undecided word goes into the Terms table.

## ADR

```markdown
# ADR-NNNN. <name of the decision>

- Status: Proposed (by the AI)   ← if the user decided: Approved (decided by the user, date)
- How to read: follow [Spec NN](../spec/…).
- Depends on: <other ADRs or lookups this decision needs, if any>

## Context
## Decision
1. The system **MUST** … (this is ADR-NNNN.1; its tests are named `adrNNNN_1_…`)
2. …
<Stages: a table of stage / receives / passes, when the decision splits the work into stages.>
## Consequences
<Good points, bad points. The condition under which the decision holds.>
## Rejected alternatives
<For each alternative, one good point and the reason it was rejected.>
```

- Each numbered item under `## Decision` that holds a bold keyword is a rule with the ID `ADR-NNNN.k`.
- A collision with another decision goes on the ADR's status line.
- An ADR that is replaced keeps its file; its status value starts with `Replaced by ADR-NNNN (YYYY-MM-DD)` (Korean `ADR-NNNN으로 대체 (YYYY-MM-DD)`). All its rules are then retired, like REPLACED rows. One rule is retired by starting its item with `Replaced by ADR-NNNN.k (YYYY-MM-DD).` or `Removed (YYYY-MM-DD): <reason>.` (Korean `ADR-NNNN.k으로 대체 (YYYY-MM-DD).`, `삭제 (YYYY-MM-DD): <이유>.`), followed by the old sentence.

## plan

```markdown
# Plan NN. <name of the slice>

- Status: Draft. Implementation starts when the user says so.
- Input: Spec NN, Domain NN, ADRs

## Approach
- Every task is test first: failing test → implementation → pass → tidy up.
- When a task ends, run the whole test suite and write the journal.
- Move to the next task only when the user asks for it. A request that names several tasks covers all of them.

## Task order

| # | Task | What to verify |
|---|---|---|
| 1 | Create the project skeleton. (first slice only) | The build succeeds. An empty program runs. |
| 2 | If the ADRs have structure rules, write the tests that check them. (first slice only) | ADR-0001. Breaking a rule on purpose makes a test fail. |
| 3 | <starting with the inner parts> | R1, R2. <a sentence that can pass or fail> |
| N | Verify the whole flow. | The flow runs through in one test. Every ID this plan covers has a test. |

## Inner order of a feature task
<A test of the whole result → a test and the implementation for each inner part → tidy up.>

## End condition
- All <n> acceptance criteria have a passing test.
- All <n> rules have a passing test.
- All <n> ADR rules have a passing test.
- The journal has a record for every task.
```

- "What to verify" holds only IDs and sentences that can pass or fail. Put no code and no ERD in it.
- Rows 1 and 2 are for the first slice only. On existing code, row 1 writes the pin tests of "Existing behaviour this slice changes" and "Confirmed assumptions" instead.
- New tasks go before the final whole-flow task.
- The numbers in the end condition count the active IDs this plan covers, by kind. `trace` reads the phrases "All N acceptance criteria", "All N rules" and "All N ADR rules" (Korean "인수 조건 N개", "규칙 N개", "ADR 규칙 N개"); a plan with no phrase it can read fails. Leave out a line whose count is zero. ADR rules need tests only when the plan that mentions them has the "All N ADR rules" line; without it, `trace` gives a warning.
