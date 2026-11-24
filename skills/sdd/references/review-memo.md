# Review note format

Review notes are a list of findings. Note IDs are `S<step>-<n>`, unique across the journal (`journal-format.md`). They are not decisions. The user decides what gets fixed.

| ID | Finding | Kind |
|---|---|---|
| S<step>-1 | <One fact. Give numbers and conditions> | verified (by running it) |
| S<step>-2 | <…> | read |
| S<step>-3 | <…> | assumed |
| S<step>-4 | <…> | question |

## Kinds

| Kind | Korean | Meaning |
|---|---|---|
| verified | 확인 | You ran it and saw it. Attach the method: by running it for real, by a test, by injecting a defect. |
| read | 읽음 | You read the code or a document. You did not run it. |
| assumed | 추정 | You did not verify it. Say how to verify it, as far as you know. |
| question | 질문 | You do not know the intent. It is for the user to decide. |

## Where to look

- What is not in the files: defaults, versions that were pulled in, behaviour added by a framework.
- Inputs the tests did not think of: invisible characters, long values, wrong types, simultaneous requests.
- What the rules miss: packages a check does not look at, a MUST without a check.
- Where two documents meet: numbers in different units, a difference between a sentence and a table.
- Blurred words in the documents: code demands a definition.
- Whether the commit contains changes that do not belong to the task.
- Places where the AI changed an approved document.

## Handling

Ask the user how to handle the notes. There are three options.

- **Fix now** → the **Fix** playbook. One note is one step. Turn the reviewer's claim into a test and see it fail before you fix.
- **Put into the plan** → add it to "What to verify" of a later task.
- **Leave** → keep it in the table as it is; record the choice under Decision, not under Closed notes. **Status** finds it again.

A postponed note sometimes comes back in a larger shape at the next layer. When a note is closed, list its ID under **Closed notes** of the step that closed it, with the evidence. A note whose fix is inconclusive stays open.
