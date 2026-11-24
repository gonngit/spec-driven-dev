# Report format

Answer in this format at the end of a step. Leave out sections that do not apply. Keep it short. Do not leave out content.

```markdown
**Goal.** <the goal restated>
**Playbook.** <name>. Playbook steps skipped: <playbook step, reason>, or none.

**What changed.** <First the change the user sees. Then code and documents.>

**Verification.**

| What was verified | Method | Verdict | Evidence |
|---|---|---|---|
| <end condition or ID> | `<command or path>` | verified | <part of the output, or a file> |
| <second> | `<command>` | inconclusive | <why it could not be run> |

**Principles applied.** <name> → <the decision that principle changed>.

**Open.**
- Decisions awaiting confirmation: <n>. <the one with the largest impact>
- Review notes: <n>. <where the table is>
- Rules not followed: <rule, reason>
- Remaining work: <what to put into the plan>

**Candidate for the next step.** <One line. Do not start it.>
```

## Rules

- There are three verdicts: **verified**, **failed**, **inconclusive**. Inconclusive is not a pass.
- The evidence for "verified" is real output. "It builds" is not evidence of behaviour.
- Label a sentence that has no evidence: read, assumed.
- Do not cite a principle you did not read.
- Put the items of the playbook's `**Report:**` line inside "What changed" and "Verification".
- When more than 5 decisions await confirmation, recommend **Confirm decisions** as the candidate for the next step.
