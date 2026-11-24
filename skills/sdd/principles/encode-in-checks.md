# Encode rules in checks

When you find a rule that people keep by being careful, make a test or a script enforce it. Prose is the weakest enforcement.

**Why:** Breaking a rule written as a plain statement goes unnoticed. If the reason "it complies today" is care, it breaks in the next task. A failing check narrows the options of the next task.

**How:**
- Use the ladder of enforcement from the top: (1) the structure makes the mistake impossible → (2) types, tests that check the structure, scripts → (3) tests → (4) a sentence in a document.
- Write document requirements as MUST. A MUST turns a violation into a defect.
- Put the source of the rule in the check's name and failure message ("ADR-0002 rule 3: …").
- If a check does not match the sentence exactly, do not add it.
- When the same correction comes twice, promote it to a check. Do not promote something that came once.

**Stop:** If you cited this principle and the diff has no new check, you did not apply it.

**Evidence:** The diff contains a test or a script. There is a record of seeing that check fail.
