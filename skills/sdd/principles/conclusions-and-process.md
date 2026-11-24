# Conclusions in documents, process in the journal

Write only conclusions in the project documents. Write why, in what order, and what was rejected in the journal. Write what the next task has to do in the plan.

**Why:** Mixing process into the documents scatters the order of events over several documents. "Remaining work" that exists only in the journal is outside the process. The next task does not verify it.

**How:**
- When a step ends, write the journal. Write it before the commit.
- Write a conclusion reached in implementation into the document for that subject (domain, ADR).
- Propose adding remaining work to "What to verify" of a later plan task.
- Do not delete discarded ideas and wrong hypotheses. Keep them with a strikethrough or marked "wrong".
- Do not edit past journals. They are the record of that time. Leave the hashes of commits that no longer exist as they are.

**Stop:** Do not close a step without writing the journal.

**Evidence:** `scripts/sdd-check.py journal` passes. The plan's status line records the work that was added.
