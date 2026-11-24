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

A step that only commits gets three lines: what was committed (hash and branch), the check, the candidate for the next step.

In a reply in Korean, the headings are: Goal 목표, Playbook 플레이북, What changed 바뀐 것, Verification 검증, What was verified 검증한 것, Method 방법, Verdict 판정, Evidence 증거, Principles applied 적용한 원칙, Open 남은 것, Candidate for the next step 다음 후보. The verdicts and labels take the forms in `references/doc-style.md`.

## Rules

- There are three verdicts: **verified**, **failed**, **inconclusive**. Inconclusive is not a pass.
- The evidence for "verified" is real output. "It builds" is not evidence of behaviour.
- Label a sentence that has no evidence: read, assumed.
- Do not cite a principle you did not read.
- Put the items of the playbook's `**Report:**` line inside "What changed", "Verification" or "Open", or add a section for them.
- When more than 5 decisions await confirmation, give the count under Open. Recommend **Confirm decisions** as the candidate only at the end of a slice.
- Exactly one candidate line, and it is the last line of the reply.
- A line the harness requires goes at the very start of the reply, outside this format.
