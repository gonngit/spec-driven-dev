# Document templates

Keep documents brief. Most of a document is tables. One document answers one question. Style follows `doc-style.md`. The templates below are in English; in a Korean document write the headings and sentences in Korean and use the fixed Korean forms listed in `doc-style.md`.

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
- The list of slices lives in the project kickoff's brainstorming document (`docs/brainstorming/00-<name>.md`) as a table: number, name, the flow in one line.
- One slice, one branch: `slice/NN-<name>`. A small addition made after the slice was merged gets its own branch `slice/NN-<name>-<addition>`.
- A domain document carries the number of the slice that first needed it. A later slice adds to that document for a concept it already covers and creates a new document for a new concept.

## spec

```markdown
# Spec NN. <name of the slice>

- Status: Draft
- Slice: <flow>
- Terms: follow the [domain model](../domain/NN-<name>.md).

This document says only **what** is built. How it is built and the technology are in the ADRs.

## How to read this document
<The keyword table. The meaning of words used many times, such as "the system", "result", "rejects".>

## Goal 1. <who does what>

| ID | Level | Acceptance criterion |
|---|---|---|
| AC-1.1 | MUST | When <condition>, the system **MUST** <result>. |

## Confirmed assumptions
## Accepted limits
## Out of scope
## Differences from the original
<Only when there is an original that is being ported or rebuilt.>
## Sources
<For each acceptance criterion, where in the input material it came from.>
```

## domain

```markdown
# Domain NN. <name>

- Status: Draft
- Scope: covers only what [Spec NN](../spec/…) needs.

## Terms

| Term | Name in code | Meaning |
|---|---|---|

| Word not used | Word used instead |
|---|---|

## Model
<The core concepts and how they relate. What is not part of the domain model.>

## Rules

| ID | Level | Rule | Where it is enforced |
|---|---|---|---|
| R1 | MUST | … | <name of the model or the feature> |
```

The "Where it is enforced" column sets the scope of the plan's tasks.

## ADR

```markdown
# ADR-NNNN. <name of the decision>

- Status: Proposed (by the AI)   ← if the user decided: Approved (decided by the user, date)

## Context
## Decision
<Write requirements with keywords. Number the rules. The tests that check the rules use the numbers.>
## Consequences
<Good points, bad points. The condition under which the decision holds.>
## Rejected alternatives
<For each alternative, one good point and the reason it was rejected.>
```

## plan

```markdown
# Plan NN. <name of the slice>

- Status: Draft. Implementation starts when the user says so.
- Input: Spec NN, Domain NN, ADRs

## Approach
- Every task is test first: failing test → implementation → pass → tidy up.
- When a task ends, run the whole test suite and write the journal.
- Move to the next task only after the user has confirmed the current one.

## Task order

| # | Task | What to verify |
|---|---|---|
| 1 | Create the project skeleton. | The build succeeds. An empty program runs. |
| 2 | If the ADRs have structure rules, write the tests that check them. | The ADR rules exist as tests. Breaking a rule on purpose makes a test fail. |
| 3 | <starting with the inner parts> | R1, R2. <a sentence that can pass or fail> |
| N | Verify the whole flow. | The flow runs through in one test. Every AC and R has a test. |

## Inner order of a feature task
<A test of the whole result → a test and the implementation for each inner part → tidy up.>

## End condition
- All <n> acceptance criteria have a passing test.
- All <n> rules have a passing test.
- The journal has a record for every task.
```

- "What to verify" holds only IDs and sentences that can pass or fail. Put no code and no ERD in it.
- The numbers in the end condition must equal the number of IDs in the spec and the domain.
