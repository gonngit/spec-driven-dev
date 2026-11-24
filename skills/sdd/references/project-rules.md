# Project rules (what goes into a new project's `CLAUDE.md`)

Show this to the user at kickoff and put in only what is approved. Do not add rules the user did not ask for. Write the block in the language of the project's documents.

```markdown
## Process

- Work in small steps. Do one step at a time and move on only after confirming with the user.
- Flow of development: input material → drawing out the intent (brainstorming) → spec → domain → ADR → plan → implementation.
- Implement by plan task. Write the tests first.

## Work journal

- At the end of every step, the step **MUST** be recorded in `docs/journal/YYYY-MM-DD.md`.
- Items written for every step: request or question, what was done, verification. A step that only commits or pushes writes the first two. Write the other items (answer, decision, rejected alternatives, observations) only when they have content.
- Project documents hold only conclusions. The process goes into the journal.

## Documents

- Document language: <Korean or English, the language the user writes in>. Code identifiers, paths and technical terms **MAY** stay in their original form.
- Requirement levels are written with RFC 2119 keywords.
```

## What to ask the user

| Question | Why it is asked first |
|---|---|
| What is the purpose of the project? | The answer sets the kind of output and how finished it has to be. |
| How far is it implemented? | It sets the number of slices. |
