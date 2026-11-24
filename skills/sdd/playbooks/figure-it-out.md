### Figure it out

**You own a request that has no playbook. Design the playbook steps before you run them.**

In work without playbook steps, verification is the first thing to go missing. So decide the verification first.

1. Write the goal and the end condition as sentences that can pass or fail. If you cannot, ask the user.
2. Pick the closest playbook. Write down what differs.
3. Design the playbook steps. The one that pins the state before the change comes before the change. Verify on the same surface where that state was observed. The last one is the **Wrap-up**.
4. Show the designed playbook steps once. If nothing in them is irreversible, proceed without waiting.
5. Run them. There are three verdicts: verified, failed, inconclusive. Inconclusive is not a pass. If it passes too easily, doubt the measurement before the system.
6. If the output reproduces real behaviour (a widget, a simulation, an example), compare one of its verdict functions with the result of a real run.
7. Do the **Wrap-up** (`wrap-up.md`). Under Observations in the journal, write "no playbook fitted" and the kind of request.

**Report:** the designed playbook steps, the closest playbook and what differed, the table of verdicts, anything that was reduced or only imitated.
