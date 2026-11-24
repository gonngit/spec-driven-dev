# Journal format

- File: `docs/journal/YYYY-MM-DD.md`. One per date: the date of the request. Language: `doc-style.md`.
- Head, English: `# Work journal — YYYY-MM-DD`, then `Phase: **Implementation** (plan 01)`, then `Previous: [YYYY-MM-DD](YYYY-MM-DD.md)`.
- Head, Korean: `# 작업 일지 — YYYY-MM-DD`, then `단계: **구현** (plan 01)`, then `이전: [YYYY-MM-DD](YYYY-MM-DD.md)`.
- Each step is a heading `## Step N` (Korean: `## 스텝 N`). Step numbers continue across dates. A stacked branch continues the numbers of the branch it came from; once it exists, new steps go only on the top branch (`doc-templates.md`, Slices). When the phase changes, insert `---` and a line for the new phase.
- Write the journal before the commit. So do not record the hash of that commit; see it in `git log`.
- Do not edit past steps. Write what was wrong in a new step.

## Phases

One phase per playbook. Commit, push and merge steps keep the current phase.

| English | Korean |
|---|---|
| Kickoff | 킥오프 |
| Design docs | 설계 문서 |
| Implementation | 구현 |
| Review | 리뷰 |
| Fix | 결함 수정 |
| Conformance | 적합성 확인 |
| Confirm decisions | 결정 확인 |
| Status | 상태 |
| Figure it out | 알아보기 |
| Retrospective | 회고 |

## Steps

- One step per playbook run. Quote the request in each step.
- A request that names several plan tasks is approval to run them one after another: one step per task, each with its own Wrap-up and Verification table. Stop after the last task.
- A request that bundles a commit and a task gives a commit step and a task step.
- A reply that only answers the AI's question (kickoff discussion) is a short step: Answer (user), Done and, when there is one, Decision. Its Verification is "no check: documents only" (Korean `확인 안 함: 문서만`).
- A request that resumes a step that was cut off is a new step. Its Observations name the step that was cut off and where.

## Items of a step

Write **Request** (or **Question (AI)** / **Question (user)**; in a short step **Answer (user)**), **Done** and **Verification** for every step except commit, push and merge steps (below). Write the other items only when they have content. Keep the order below. Several questions and answers in one step are numbered lists. `journal` checks that each new step holds **Done**, but it looks at the change set as a whole, not at each uncommitted step.

| Item | Korean name | Content |
|---|---|---|
| **Request** | 요청 | The user's words, quoted. |
| **Question (AI)** | 질문 (AI) | The options and the recommendation. A proposed change to an approved document that waits for approval goes here too. |
| **Answer (user)** | 답 (사용자) | What the user chose. If it differs from the recommendation, say that too. |
| **Question (user)** | 질문 (사용자) | A question the user asked. |
| **Answer (AI)** | 답 (AI) | The answer, with labels (`principles/label-the-claim.md`). |
| **Done (in order)** | 한 일 (순서대로) | Numbered. See Done below. |
| **Verification** | 검증 | A table: "What to verify", the result. A table of experiments: what was injected, the result. A table of real results. A pin test that went red on purpose is recorded here. |
| **Decision** | 결정 | What you stopped for and got approved. |
| **Decision (AI)** | 결정 (AI) | Everything the AI decided, numbered within the step. |
| **Rejected alternatives** | 버린 대안 | The alternative and why it was rejected. One sentence on its good point too. |
| **Documents** | 문서 | The documents changed and what was added. For an approved document, point at the approved decision. |
| **Rules not followed** | 지키지 못한 것 | The rule broken and the reason. |
| **Review notes** | 리뷰 메모 | A table: ID, content, kind (verified, read, assumed, question). |
| **Closed notes** | 닫은 메모 | The note IDs this step closed, each with its evidence. |
| **Remaining work** | 남은 일 | What the next task has to do. Propose whether to put it into the plan. |
| **Next step** | 다음 후보 | The candidate line of the report. |
| **Observations** | 관찰 | Observations about the process. What this step taught, mistakes of the AI, corrections by the user. |

## Done

- Name each playbook step by number: done, `skip: <reason>`, or `n/a: <why the condition is false>`. Korean: `생략: <이유>`, `해당 없음: <이유>`. A step the user waived is `skip: <reason> (user asked)`.
- Write only actions that left output.
- Test count: the number the test runner reports, before → after.

## Review notes

- Note IDs are unique across the journal: `S<step>-<n>` (`S10-1`).
- "Note 1" from the user means note 1 of the latest Review step. If that is unclear, ask.
- Closing a note goes under Closed notes of the step that closed it, with its evidence.

## Decision (AI)

- Number the entries within a step.
- A later decision that reverses one writes `(replaces S8 Decision (AI) 2)` (Korean `(S8 결정 (AI) 2 대체)`).
- Confirm decisions skips replaced decisions.

## Commit, push and merge steps

- They have Request and Done. Done states the intent ("pushes …"); the next step's Done records the result, including a failure, and the check (`git log`, `git rev-parse`). Corrections still go under Observations.
- A commit-only step records no test count. Uncommitted steps are committed together unless the user asks otherwise.
- Write the entry before the commit.
- A push-only step's entry goes into the next commit on the branch that will hold it. Each merge is its own step; its entry goes into the merge commit (`git merge --no-ff --no-commit`, then the entry, then the commit).

## Sentences

- Write short statements. One thing per sentence.
- Use numbers ("23 of 30 tests failed").
- Record a mistake of the AI as "mistake of the AI". Say how it was noticed and what would have prevented it.
- Record a correction as "correction by the user: <quote>" (Korean "사용자의 정정: <인용>").
