### Plan task

**You own one task of the plan. Its "What to verify" is the end condition.** Do not start the next task.

Work scientifically. Green is evidence only after you have seen red. Tests see only the inputs someone thought of. If you find a defect outside the task, leave it as a review note. Fixing it is a **Fix**.

1. Reread that plan task and the spec, domain and ADRs it relates to. Copy each "What to verify" item into the todo list. Run the whole test suite and record the baseline (the number passing). If the task changes the behaviour of existing code, first pin the current behaviour of the part to be changed in a test and see it pass.
2. Write the test that checks the whole result (the acceptance test) first. Put the ID in its name. Run it. Look at the reason for the failure of each test (`principles/assert-the-reason.md`).
3. Go inward. For each part (layer, stage, function) write a test, see it fail, and implement. When you meet something the documents do not decide, follow `principles/mark-the-source.md`. If the decision requires changing a document, stop and get approval.
4. Run the whole build and the whole test suite. Record the number of tests as before → after.
5. Inject a defect for the tests that passed from the start and for "must not exist" rules. See the failure and restore (`principles/see-it-fail.md`).
6. Run it the way it is really used. Also feed it inputs the tests do not have (`principles/real-surface.md`).
7. Run `scripts/sdd-check.py trace`.
8. Write the approved decisions into the documents. Propose adding the remaining work to a later task of the plan.
9. Do the **Wrap-up** (`wrap-up.md`).

**Report:** the "What to verify" table (item, method, verdict, evidence), the defect-injection table, the real results, the decisions the AI made and the rejected alternatives, rules not followed, review notes, remaining work.
