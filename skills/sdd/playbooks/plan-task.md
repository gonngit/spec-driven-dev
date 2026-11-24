### Plan task

**You own one task of the plan. Its "What to verify" is the end condition.** Do not start a task the request did not name. A request that names several tasks runs this playbook once per task, each with its own Wrap-up; stop after the last.

Work scientifically. Green is evidence only after you have seen red. Tests see only the inputs someone thought of. If you find a defect outside the task, leave it as a review note. Fixing it is a **Fix**.

1. Reread that plan task and the spec, domain and ADRs it relates to. Each "What to verify" item gets a verdict. Run the project's test suite from the project root and record the baseline (the number the runner reports). On existing code, before changing a part, pin its current behaviour with a test named `pin_<what>` (`test_pin_<what>` in Python) and see it pass.
2. Write the test of the task's whole result first: an acceptance test with the ID in its name. Test names follow `principles/trace-by-id.md` (`pin_`, `task<N>_`). Run it. Look at the reason for the failure of each test (`principles/assert-the-reason.md`).
3. Go inward. For each part (layer, stage, function) write a test, see it fail, and implement. When you meet something the documents do not decide, follow `principles/mark-the-source.md`. If the decision requires changing a document, stop and get approval.
4. Run the build if there is one, and the whole test suite. Record the number of tests as before → after. A pin of behaviour this task changes (listed in the spec's "Existing behaviour this slice changes") goes red: record that red in Verification and delete the pin in this step. Pins of behaviour that must stay remain as regression tests.
5. Inject defects one at a time as `principles/see-it-fail.md` says, at least for the tests that passed from the start and for "must not exist" rules. See each failure and restore.
6. Run it the way it is really used. Also feed it inputs the tests do not have (`principles/real-surface.md`).
7. Write the approved decisions into the documents. Propose adding the remaining work to a later task of the plan. At the end of a slice, carry open notes and decisions to the next slice's brainstorming or the pull request description.
8. Run `scripts/sdd-check.py trace --plan NN --upto K` (K is this task's number; add `--tests <folder>` when tests are elsewhere); on the last task of the slice, run plain `trace`. If a document changed, run `keywords`. Every failure counts.
9. Do the **Wrap-up** (`wrap-up.md`).

**Report:** the "What to verify" table (item, method, verdict, evidence), the defect-injection table, the real results, the decisions the AI made and the rejected alternatives, rules not followed, review notes, remaining work.
