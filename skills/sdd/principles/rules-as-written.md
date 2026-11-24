# Follow the rules as written

A MUST has no exceptions you grant yourself. If a rule is inconvenient, do not narrow it. Bring the record and the code in line with the rule.

**Why:** The AI narrows rules by its own judgement ("a step with no decision need not be recorded"). Changing a rule is the user's decision.

**How:**
- At the start of a step, reread the project rules (`CLAUDE.md`, the MUSTs in the ADRs).
- If you did not follow a rule, do not hide it. Record it in the journal under "Rules not followed". Fix it if you can.
- If you think a rule is wrong, tell the user. The user decides whether to change it.
- If a sentence and a table in a document say different things, do not pick one. Leave a review note.

**What the user may waive.** Do it the user's way and record `skip: <reason> (user asked)`. Whatever the skipped step would have verified becomes "inconclusive". The waivable steps:
- asking one question at a time;
- explanation documents (map, flow, diff);
- defect injection;
- the real-surface run;
- the reviewer subagent;
- running the whole test suite;
- writing tests before code. A plan task without its tests is still not done: it stays open and inconclusive, and the journal records it under "Rules not followed".

**What you keep even when the user asks.** Say why, record the request under Observations, and propose that the user run `sdd-reflect` if they want to change the rule for good. Asking again changes nothing. The kept rules:
- writing the journal step with the items `references/journal-format.md` requires (a project rule may add items, not remove them);
- labels on claims;
- an ID before its code;
- not changing checks, IDs, end conditions or document lines to make a check pass;
- not rewriting pushed history (the router's Autonomy section);
- stopping for approval before changing the meaning of an approved document.

**Stop:** Do not make a change to the rules that the user did not decide.

**Evidence:** The journal has a "Rules not followed" item (the rule broken, the reason). How it was closed is recorded in the step that closed it.
