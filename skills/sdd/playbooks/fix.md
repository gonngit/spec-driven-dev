### Fix

**You own one defect or one review note.** Fix only what was requested. Leave the other notes in the table.

Every line comes from evidence you saw. A change that "might help" is a hypothesis. Do not add it.

1. Split the target: what an approved decision already answers, and what needs a new decision. Ask only about the new decisions. Give options and a recommendation. If the cause also covers other notes, ask whether to close them together.
2. Reproduce the symptom on the real surface as it is now. Record it in numbers. See whether the same symptom appears elsewhere.
3. If the cause is in a document, this step goes documents → test → code. Get approval before changing an approved meaning (`references/doc-style.md`). New IDs go into the plan: a new fix task before the final whole-flow task, or the task's "What to verify" marked Revised. Update the end-condition counts. Run `scripts/sdd-check.py trace --no-tests` and `keywords`.
4. Write a failing test. If it can be written at several parts (layers, stages), write one at each. See that it fails for the right reason (`principles/assert-the-reason.md`).
5. Fix the cause (`principles/fix-the-cause.md`). Make the smallest change.
6. Run the whole test suite. Repeat the experiment of playbook step 2 on the same surface. Record before and after in a table.
7. Inject the fixed defect again. See that the new test catches it. Restore.
8. Do the **Wrap-up** (`wrap-up.md`). The closed note goes under Closed notes with its evidence. When a commit is asked, the fix and this journal step go into one commit.

**Report:** the symptom (in numbers), the cause, how it was fixed, the before-and-after table, the tests added, the rejected alternatives, what was not fixed. If your first assumption was wrong, say that too.
