# Review note format

Review notes are a list of findings. They are not decisions. The user decides what gets fixed.

| # | Finding | Kind |
|---|---|---|
| 1 | <One fact. Give numbers and conditions> | verified (by running it) |
| 2 | <…> | read |
| 3 | <…> | assumed |
| 4 | <…> | question |

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

- **Fix now** → the **Fix** playbook. One note is one step.
- **Put into the plan** → add it to "What to verify" of a later task.
- **Leave** → keep it in the table as it is. **Status** finds it again.

A postponed note sometimes comes back in a larger shape at the next layer. When a note is closed, record it as "closed" in the journal of the step that closed it.
