### Kickoff

**You own the map of the intent. The user decides.** Write no code. Do not mix facts and guesses.

Send a request to write design documents to **Design docs**. Here, go only as far as closing the topics.

1. Listen to the user first. It does not need an order. If the user has not said anything yet, ask them to say what comes to mind. Read the input material if there is any (references, example files, existing code). Record where the material is by URL and commit number, not by a path on this computer.
2. When the work continues on existing code, make a map first. Read `review/explain-full-map/SKILL.md` and follow it. From the map, pick the flows the new work touches. There may be several. Say which flows and why, then read `review/explain-full-flow/SKILL.md` and follow it for each flow. Do not regenerate an explanation document that was made at the same commit. These documents are input material.
3. If the project has no rules, show `references/project-rules.md` and ask whether to put it into `CLAUDE.md` (`.omp/AGENTS.md` in omp). Create `docs/journal/` if it is missing.
4. Write `docs/brainstorming/NN-<name>.md` and show it. It has three sections: what is settled, the list of topics to settle, and the AI's guesses. Mark each guess "unverified guess". Add the topics the user did not mention (purpose, scope, who uses it) to the list.
5. Discuss the topics one at a time. The purpose of the project comes first. Give options and a recommendation for each topic. Ask about one topic at a time.
6. When a topic is settled, write it in the decisions section and move to the next topic. Keep rejected options with a strikethrough. Do not delete them.
7. Reread the document from the top. Do the earlier decisions agree with the later ones? Does a decision sentence hide a new topic? Does a guess have a counterexample?
8. Do the **Wrap-up** (`wrap-up.md`).

**Report:** the topics settled and their decisions, the topics left, the rejected options and why, the guesses that have a counterexample, what you took for granted.
