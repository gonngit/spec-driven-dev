### Design docs

**You own the links between the documents.** One document answers one question. The spec says what, the domain says the words and the rules, an ADR says how and why, the plan says the order and the verification.

Gaps appear where two documents meet. Each document being clean is not enough. Do not implement.

1. Reread the kickoff decisions and the input material. If you are rewriting existing documents, first record the list and the count of IDs. That is the baseline.
2. Ask first about the decisions that need an ADR (the structure, how the stages are split, the technology, the way to verify, and the like). Give options and a recommendation. If this answer is wrong, all four kinds of document are rewritten.
3. Read `references/doc-templates.md` and `references/doc-style.md`. Write in the order spec → domain → ADR → plan. When the work continues on existing code, document only the new work. Record the existing behaviour that the new work relies on under "Confirmed assumptions" in the spec.
4. Give IDs to acceptance criteria and rules (`principles/trace-by-id.md`). The plan's "What to verify" points at IDs. Put no code and no ERD in the plan.
5. Mark what the user decided as "Approved" and what the AI decided as "Proposed" (`principles/mark-the-source.md`).
6. Feed boundary inputs to the documents: "when this request comes, what do the documents answer?" Look for numbers in different units, two documents that say different things, and requirements that cannot be tested.
7. Run `scripts/sdd-check.py trace --no-tests` and `scripts/sdd-check.py keywords`. For rewritten documents, compare the ID count with the baseline of playbook step 1.
8. Do the **Wrap-up** (`wrap-up.md`).

**Report:** the list of documents, the number of IDs, what the user decided, what the AI proposed (the large-impact ones separately), the check output, the gaps the boundary inputs found, where the meaning narrowed in rewriting.
