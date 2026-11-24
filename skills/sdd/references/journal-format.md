# Journal format

- File: `docs/journal/YYYY-MM-DD.md`. One per date.
- Head: `# Work journal — YYYY-MM-DD`, the current phase (`Phase: **Implementation** (plan 01)`), and a link to the previous journal. In a Korean journal: `# 작업 일지 — YYYY-MM-DD`, `단계: **구현** (plan 01)`.
- Each step is a heading `## Step N` (Korean: `## 스텝 N`). Step numbers continue across dates. When the phase changes, insert `---` and a line for the new phase.
- One step is one request. Write a step that only commits or pushes too.
- Write the journal before the commit. So do not record the hash of that commit; see it in `git log`.
- Do not edit past steps. Write what was wrong in a new step.

## Items of a step

Write **Request** (or **Question**), **Done** and **Verification** for every step. Write the other items only when they have content. A step that only commits or pushes has Request and Done only. Keep the order below.

| Item | Korean name | Content |
|---|---|---|
| **Request** or **Question (AI)** | 요청, 질문 (AI) | The user's words in short. If the AI asked, the options and the recommendation. |
| **Answer (user)** | 답 (사용자) | What the user chose. If it differs from the recommendation, say that too. |
| **Done (in order)** | 한 일 (순서대로) | Numbered. Record the number of tests as before → after. Name the playbook steps you skipped and why. |
| **Verification** | 검증 | A table: "What to verify", the result. A table of experiments: what was injected, the result. A table of real results. |
| **Decision** or **Decision (AI)** | 결정, 결정 (AI) | Tell apart who decided. What you stopped for and got approved goes under **Decision**; everything the AI decided goes under **Decision (AI)**. |
| **Rejected alternatives** | 버린 대안 | The alternative and why it was rejected. One sentence on its good point too. |
| **Documents** | 문서 | The documents changed and what was added. For an approved document, point at the approved decision. |
| **Rules not followed** | 지키지 못한 것 | The rule broken and the reason. |
| **Review notes** | 리뷰 메모 | A table: number, content, kind (verified, read, assumed, question). |
| **Remaining work** | 남은 일 | What the next task has to do. Propose whether to put it into the plan. |
| **Observations** | 관찰 | Observations about the process. What this step taught, mistakes of the AI, corrections by the user. |

## Sentences

- Write short statements. One thing per sentence.
- Use numbers ("23 of 30 tests failed").
- Record a mistake of the AI as "mistake of the AI". Say how it was noticed and what would have prevented it.
