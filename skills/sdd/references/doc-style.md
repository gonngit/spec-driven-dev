# Document style

Existing repository rules (the rules file the harness loads, CONTRIBUTING) come first for documents, commit messages and branch names. What follows is added on top.

## Language

This is the only language rule of the skill. Other files point here.

- Documents, the journal and commit messages use the project's document language. Choose it in this order:
  1. the language the rules file names;
  2. else the language of the existing sdd documents under `docs/`;
  3. else the language the user writes in.
- Replies to the user follow the harness rules. If those say nothing, use the user's language.
- A line the harness requires goes at the very start of the reply. The reply still ends with the candidate line.
- The fixed words the checker reads are in this file and in `journal-format.md`. In a Korean document, write every other quoted marker in its fixed Korean form from the table below.

| Marker | Korean form |
|---|---|
| closed | 닫음 |
| unverified guess | 검증하지 않은 추측 |
| not reviewed one by one | 하나씩 검토하지 않음 |
| verified | 확인 |
| failed | 실패 |
| inconclusive | 미확정 |
| no playbook fitted | 맞는 플레이북 없음 |
| wrong | 틀림 |
| skip | 생략 |
| n/a | 해당 없음 |
| existing | 기존 |
| no check: documents only | 확인 안 함: 문서만 |
| Existing behaviour this slice changes | 이 슬라이스가 바꾸는 기존 동작 |
| Confirmed assumptions | 확인된 가정 |
| Accepted limits | 받아들인 한계 |
| Pin test | 고정 테스트 |
| Replaced by ID | 대체하는 ID |
| Report: Goal / Playbook / What changed | 목표 / 플레이북 / 바뀐 것 |
| Report: Verification / Principles applied | 검증 / 적용한 원칙 |
| Report: Open / Candidate for the next step | 남은 것 / 다음 후보 |

## Requirement levels (RFC 2119)

| Keyword | Korean form | Meaning |
|---|---|---|
| **MUST** | **반드시 ~해야 한다** | A requirement without exceptions. |
| **MUST NOT** | **절대 ~해서는 안 된다** (polite: **절대 ~해서는 안 됩니다**) | A prohibition without exceptions. |
| **SHOULD** | **~하는 것을 권장한다** | It need not be followed when there is a reason. Write the condition for the exception with it. |
| **MAY** | **~할 수 있다** | Permission. |

- Write keywords in bold. A sentence without a bold keyword is explanation.
- In an English document, write the RFC 2119 words themselves in bold (**MUST**, **MUST NOT**, **SHOULD**, **MAY**). They are keywords only in upper case. Use **MAY** only for permission; for ability or possibility write "can" or "might".
- In a Korean document, use the Korean forms. Bold the whole verb phrase: "시스템은 결과를 **반드시 써야 한다**". Use "~할 수 있다" only for permission, and write permission only that way, not as "~해도 된다". Write 수 with a space before it ("할 수 있다", not "할수있다"); the check reads only that form. For ability or possibility use other words ("다를 수 있다" → "다른 경우가 있다"). Write "~할 수 없다" as a prohibition or reword it, and do not use "반드시" or "절대" as ordinary words (not even in 절대값): the check flags them.
- Write a prohibition as MUST NOT, not as a negative statement ("it does not contain").
- Put a "Level" column (Korean: "수준") in a requirements table. The cell holds the English word (MUST, MUST NOT, SHOULD, MAY, REPLACED, REMOVED), not bold, in both languages. In an active row (MUST, MUST NOT, SHOULD, MAY) the keyword in the sentence must match the cell; a REPLACED or REMOVED row keeps its old sentence.
- Use keywords only in requirements. Do not use them in term tables, context, consequences, accepted limits or rejected alternatives.
- Do not create a recommendation or a permission that the original sentence did not have.
- Put "How to read this document" (Korean: "이 문서를 읽는 법") at the top of one document, with the keyword table and a line for how times and sizes are measured (machine, data size, command). The other documents point to it with a line `- How to read: …` (Korean: `- 읽는 법: …`). These headings and pointers are fixed words.

## Sentences (principles of ASD-STE100)

- State the subject ("the system"). Use the active voice.
- One requirement per sentence. Split "if A or B" into two sentences.
- One term per concept. Terms follow the table in the domain document.
- Do not use words with a blurred range ("empty", "valid", "indistinguishable"). Define the meaning, or state that it is not decided.
- Give numbers a unit (bytes, code points, grapheme clusters). For text, say whether it is NFC or NFD. Give the source of a number.

## Status line

- It is the first item of a document, on one line that starts with `- Status:` (Korean `- 상태:`). Indented continuation lines belong to it. There is one status line per document; say on it which parts the user decided and which the AI proposed. Each `Revised` note goes on its own indented line under it.
- A brainstorming document has a status line too.

| Case | English | Korean |
|---|---|---|
| Being written | `Draft` | `초안` |
| Shown for approval | `Proposed (by the AI)` | `제안 (AI가 제안)` |
| The user decided | `Approved (decided by the user, YYYY-MM-DD)` | `승인 (사용자가 결정, YYYY-MM-DD)` |
| The AI proposed, the user approved | `Approved (proposed by the AI, approved by the user, YYYY-MM-DD)` | `승인 (AI가 제안, 사용자가 승인, YYYY-MM-DD)` |
| Approved as a batch | `Approved (proposed by the AI, approved by the user as a batch, not reviewed one by one, YYYY-MM-DD)` | `승인 (AI가 제안, 사용자가 한꺼번에 승인, 하나씩 검토하지 않음, YYYY-MM-DD)` |
| The user handed the choice to the AI ("pick sensible defaults"), then approved the finished document | `Approved (decided by the AI on the user's delegation, YYYY-MM-DD)`; before that approval, `Proposed (by the AI)` | `승인 (사용자가 맡겨 AI가 결정, YYYY-MM-DD)`; 그 전에는 `제안 (AI가 제안)` |
| Delegated, then the finished document approved as a batch | `Approved (decided by the AI on the user's delegation, approved as a batch, not reviewed one by one, YYYY-MM-DD)` | `승인 (사용자가 맡겨 AI가 결정, 한꺼번에 승인, 하나씩 검토하지 않음, YYYY-MM-DD)` |
| The AI proposed, the user rejected | `Approved (the user rejected the AI's proposal and decided, YYYY-MM-DD)` | `승인 (AI 제안을 사용자가 거절하고 결정, YYYY-MM-DD)` |
| ADR replaced (the status value) | `Replaced by ADR-NNNN (YYYY-MM-DD)` | `ADR-NNNN으로 대체 (YYYY-MM-DD)` |
| Meaning changed | `Revised (YYYY-MM-DD): AC-1.2 replaced by AC-1.6 (narrowed \| widened \| changed: why)` | `수정 (YYYY-MM-DD): AC-1.2를 AC-1.6으로 대체 (좁힘 \| 넓힘 \| 바꿈: 이유)` |
| Wording only | `Revised (YYYY-MM-DD): wording of AC-1.3; the meaning did not change` | `수정 (YYYY-MM-DD): AC-1.3 문구; 뜻은 그대로` |
| An ID, term or limit added | `Revised (YYYY-MM-DD): added <ID, term or limit>` | `수정 (YYYY-MM-DD): <ID, 용어 또는 한계> 추가` |
| Decided against the AI's recommendation (appended to any form) | `(decided by the user against the AI's recommendation)` | `(AI 권고와 달리 사용자가 결정)` |

- A delegated choice is a Decision (AI) in the journal until the document that holds it is approved.
- Approval replaces `Proposed` and any pending marker; keep the `Revised` notes. A `Revised` note may carry its approval form in parentheses: `(proposed by the AI, approved by the user)` (Korean `(AI가 제안, 사용자가 승인)`).
- After approval, change a meaning only by a replacement row (see IDs), with approval first.

## IDs

- Acceptance criterion: `AC-<goal>.<number>`. Domain rule: `R<number>`. ADR rule: `ADR-NNNN.k`, the k-th numbered item under `## Decision`.
- Do not renumber. Append new items at the end.
- Goal numbers and rule numbers continue across slices. A new spec starts at the next unused goal number; it does not start again at 1. `scripts/sdd-check.py trace` fails when an ID is defined twice.
- An ID's meaning never changes in place. To change it, append a new ID and mark the old row. Do not delete it or strike it through.
  - Replaced: the Level cell becomes `REPLACED`. The sentence starts with `Replaced by AC-1.6 (YYYY-MM-DD).` (Korean `AC-1.6으로 대체 (YYYY-MM-DD).`), followed by the old sentence unchanged.
  - Removed with no successor: the Level cell becomes `REMOVED`. The sentence starts with `Removed (YYYY-MM-DD): <reason>.` (Korean `삭제 (YYYY-MM-DD): <이유>.`).
  - Domain rules work the same way.
- Tests named after a REPLACED or REMOVED ID are renamed to the new ID or deleted in the same step.

## Check

`scripts/sdd-check.py keywords` checks part of these rules: the Level column against the keyword, keywords that are not bold, and a Korean "수 있다" or "수 없다" outside a bold keyword when 수 follows a word ending in ㄹ and a space ("볼 수 있다"). A level is satisfied by either the Korean form or the English word.
