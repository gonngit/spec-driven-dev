# Mark the source of a decision

For every decision, record who proposed it and who approved it. Even when the status is the same, the source differs.

**Why:** Implementation forces decisions that the documents did not make. The number grows with every layer. Without a source, an assumption of the AI reads as a decision of the user. Items approved as a batch are less reviewed. If confirmation is collected later, code piles up on the decision in the meantime.

**How:**
- When you meet a decision that requires changing a document (spec, domain, ADR, plan), stop. Give options and a recommendation and get approval. This covers behaviour visible from outside, the shape of stored data, a new input, output or stage, a new library, and anything that widens the scope.
- A decision that needs no document change (a name, how to split functions) is yours to make. Record every one under "Decision (AI)" in the journal, with the rejected alternatives and the reason.
- What the user decided is "Approved (decided by the user, date)". A document the AI wrote is "Proposed" until it is approved.
- Change an approved document only after approval. Use the status line forms and replacement rows in `references/doc-style.md`.
- When you get approval, record how: reviewed one by one, accepted as a batch ("not reviewed one by one"), or handed to the AI ("pick sensible defaults"). A delegated choice is a Decision (AI) until the document that holds it is approved.
- Record the condition under which the decision holds. If the condition breaks, look at the decision again.
- If the user chooses against the AI's recommendation, do it their way and add `(decided by the user against the AI's recommendation)` to the status line form. Record where that result collides with other decisions: in the spec under "Accepted limits", or on the ADR's status line.

**Stop:** Do not settle a decision that requires a document change without approval and carry on. Do not record an unconfirmed AI decision as "Approved". Do not remove "proposed by the AI" after approval.

**Evidence:** The status lines of the documents, "Decision (AI)" in the journal, the number of "decisions awaiting confirmation" in the report.
