# Document style

The project's own language and rules for documents come first (`CLAUDE.md`). What follows is added on top.

## Language

- Write the project documents, the journal and commit messages in the language the user writes in: Korean or English.
- If the project already has documents, keep their language.

## Requirement levels (RFC 2119)

| Keyword | Korean form | Meaning |
|---|---|---|
| **MUST** | **반드시 ~해야 한다** | A requirement without exceptions. |
| **MUST NOT** | **절대 ~해서는 안 된다** | A prohibition without exceptions. |
| **SHOULD** | **~하는 것을 권장한다** | It need not be followed when there is a reason. Write the condition for the exception with it. |
| **MAY** | **~할 수 있다** | Permission. |

- Write keywords in bold. A sentence without a bold keyword is explanation.
- In an English document, write the RFC 2119 words themselves in bold (**MUST**, **MUST NOT**, **SHOULD**, **MAY**). They are keywords only in upper case. Use **MAY** only for permission; for ability or possibility write "can" or "might".
- In a Korean document, use the Korean forms. Use "~할 수 있다" only for permission; for ability or possibility use other words ("다를 수 있다" → "다른 경우가 있다").
- Write a prohibition as MUST NOT, not as a negative statement ("it does not contain").
- Put a "Level" column (Korean: "수준") in a requirements table. The value in the column and the keyword in the sentence must be the same.
- Use keywords only in requirements. Do not use them in term tables, context, consequences or rejected alternatives.
- Do not create a recommendation or a permission that the original sentence did not have.
- Put "How to read this document" (Korean: "이 문서를 읽는 법") at the top of a document. Keep the keyword table in one document only; the other documents point to that document.

## Sentences (principles of ASD-STE100)

- State the subject ("the system"). Use the active voice.
- One requirement per sentence. Split "if A or B" into two sentences.
- One term per concept. Terms follow the table in the domain document.
- Do not use words with a blurred range ("empty", "valid", "indistinguishable"). Define the meaning, or state that it is not decided.
- Give numbers a unit (characters, bytes, code points). Give the source of a number.

## Status line

- It is the first item of a document: `- Status: Draft` → `Proposed (by the AI)` → `Approved (decided by the user, YYYY-MM-DD)`.
- When you change a document after approval, add to the line: `Revised (YYYY-MM-DD): what and why`. Do not delete what was there.
- Where a rewrite narrowed the meaning, write "narrowed". Write "the meaning did not change" only when nothing was narrowed.
- In a Korean document: `- 상태: 초안` → `제안 (AI가 제안)` → `승인 (사용자가 결정, YYYY-MM-DD)`, and `수정 (YYYY-MM-DD): 무엇을 왜`.

## IDs

- Acceptance criterion: `AC-<goal>.<number>`. Domain rule: `R<number>`.
- Do not renumber. Append new items at the end.

## Check

`scripts/sdd-check.py keywords` checks part of these rules: the Level column against the keyword, keywords that are not bold, and a Korean "수 있다" that is not a permission. A level is satisfied by either the Korean form or the English word.
