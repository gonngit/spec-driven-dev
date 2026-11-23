---
name: explain-full-map
description: Turn a whole repository into a map a person can learn from — a single self-contained HTML document that says what the repository is for, shows the system in one picture with example data, lists the data it keeps and where that data lives (a data dictionary), gives every top-level folder one line, lists the data flows through the system and walks one of them lightly, and ends with a 10–20 question recall quiz. Runs only when invoked by name. For one feature's data flow in depth use explain-full-flow; for a commit, branch or PR use explain-diff.
disable-model-invocation: true
---

# Explain Full — Map

Turn a whole repository into a map a person can *learn* from — something they could print and read in a café before their first day on the project, not a file tree with comments.

A file tree shows where the files are. It does not show what the system keeps, or how anything moves through it. This skill builds the map in a different order:

1. **Context before folders** — what is this repository for, and for whom?
2. **Intuition before detail** — what is the one idea of the system?
3. **Data before code** — what data does the system keep, where does it live, who writes it and who reads it? The folders are the index, not the story.
4. **Evidence, not impressions** — a repository has no diff to anchor its explanation, so every claim carries a path and a label, every top-level folder gets a line, and what was left out is said.
5. **Recall before work** — end with a quiz, because reading a clear map *feels* like knowing the territory even when it isn't.

This is the first of three zoom levels that share one template and one diagram style:

| Skill | Question it answers | When |
|---|---|---|
| explain-full-map (this one) | Where is everything, and what data does the system keep? | Once, when entering a repository |
| explain-full-flow | How does one feature work, from input to stored result? | When the part to work on is chosen |
| explain-diff | What did this change do? | For every change |

If the request is about one feature ("how does login work?"), use explain-full-flow. If it is about a commit, branch or PR, use explain-diff.

The running example in this file: a study app where a student uploads a PDF, the server turns it into question cards, and the app keeps showing the cards the student is about to forget.

## Workflow

### Step 1 — Pin the repository, and read what it says about itself

Work on the repository in the current directory, or the path or URL the user names (clone a URL into a scratch directory outside every repository).

- **Pin it.** Record `git rev-parse --short HEAD`, the branch, and `git status --short`. The document describes that commit; a map without a commit hash cannot be checked later. If there are uncommitted changes, say in the header whether they are included.
- **Measure it.** `git ls-files | wc -l`, the file count of each top-level entry, the main languages of the product code. Size decides depth (see Writing guidance).
- **Read its own account first.** README, AGENTS.md / CLAUDE.md, the docs index, per-feature READMEs, ADRs. They state purpose, vocabulary and rules that code alone does not.
- **Then the files that define stored data** — schemas, types, migrations, database rules and indexes, storage clients — and the manifests, CI and deploy config.
- **Then the entry points** — routes, handlers, `main`, scheduled jobs, CLI commands — and follow the core path far enough to name its stages.

The repository's documents are claims, not facts. Check the ones you repeat against the code; a mismatch is a finding for section 6, not something to smooth over. A number you cannot confirm (a test count, a coverage figure) is reported as the document's claim, not as a fact.

Read only, with one exception: the finished document is saved in the repository's `explanations/` folder (Step 6). Otherwise never create, edit or delete anything inside the repository — no notes, no generated files, no installs. If a claim needs a run to confirm it (a test, a script), run it in a scratch copy (`git archive <commit> | tar -x -C <scratch>`), not in the repository. If the toolchain is missing, do not install it: say in the header what could not be run.

If the repository holds more than one thing — an application plus a documentation set, tooling, generated artifacts — map the running system first. Everything else still gets its row in the folder map.

### Step 2 — Analyze before writing

Write these down for yourself first (a scratch note outside the repository is fine). The document is built from them.

- **The one-sentence intuition.** What the system does and for whom, in plain words, without identifiers. Study app: *"Turn a student's own PDFs into question cards, then keep showing the ones they are about to forget."* If you cannot write this sentence, you do not understand the repository yet — read more.
- **Prerequisite concepts.** What must a reader know to follow the map? The framework and runtime model, the hosting and storage services, the domain terms the repository uses.
- **System picture.** The runtime pieces — clients, servers, background jobs, data stores, external services — and the data that moves between them. Pick one concrete example value to put on the arrows. This becomes section 2.
- **Data dictionary.** Start from the stored data, not from the code: database rules, indexes, migrations, storage clients, schema files. For each main kind of data the system keeps: the name the repository uses for it, the file that defines its shape, where it lives (which store, and which collection, table, bucket or key pattern), who creates it, who reads it, and how you know. List as many as the system really keeps — a small service may have one or two, a large product fifteen — and do not pad the table. Data that only passes through (a request body, a token) belongs here only when the reader needs it to follow the flows, marked as not stored. Study app: *question card — shape in `src/cards/schema.ts`, lives in the `cards` table, created by the PDF pipeline, read by the review screen.* This becomes section 3.
- **Folder map.** Every top-level tracked entry (compare with `git ls-files | cut -d/ -f1 | sort -u`): one line on its role, one file that shows it, and its file count. Go one level deeper for the folders that hold most of the product code; root files of one kind can share a row (give the glob and the count). Nothing may silently disappear — a reader who later opens the repository should find no top-level entry you didn't mention. This becomes section 4.
- **Flow list.** The main data flows, each named `start → end` in the repository's own terms: where it starts (entry file), which stores it touches, where it ends. Aim for 3–8. Study app: *PDF upload → question cards*; *answer a card → memory record → today's review list*. Each row is a candidate for explain-full-flow.
- **The sample flow.** The flow a newcomer needs first — usually the product's core path. Trace it lightly: 4–7 stages, the file for each, and the example value as it enters and leaves each stage.
- **Rules and cautions.** The conventions the repository states or enforces (AGENTS.md, lint and architecture tests, CI); the boundaries where data crosses (browser → server, server → store, server → external service) and whether it is validated there; places where documents and code disagree; areas without tests; anything that looks legacy. This becomes section 6.
- **Left out.** What you did not read or cover, and why.
- **Quiz candidates.** As you analyze, note the points where a reader could nod along without really getting it: why a kind of data lives where it does, which places a change would have to touch, what a boundary does and does not check. These become section 7.

### Step 3 — Calibrate to the reader

The background section is the personalized part. Its depth depends on what this reader already knows.

1. Check what you already know: the user's prompt ("I know React but not Firestore"), their own notes (memory, a user-level AGENTS.md — not the repository's), their role, the conversation so far. If that settles it, do not ask.
2. Otherwise ask **one short round**, as one form: 1–3 questions naming the actual prerequisite concepts from Step 2 with options like *new to me / roughly / know it well*, plus one question offering the flow list and asking which flow the map should walk through as its sample, with your recommendation preselected. In omp, use the `ask` tool (AskUserQuestion in Claude Code). Never ask more than one round, and do not ask why they are reading: a map is for the whole picture.
3. If you cannot ask (non-interactive run), assume a capable engineer who is new to this repository, pick the sample flow yourself, and say both at the top of the document.

Apply the answer: concepts the reader knows well get one line; concepts that are new get a real explanation with a small example. Put the deeper background inside `<details>` blocks so an expert can skip them and a beginner can open them.

### Step 4 — Write the document

Build the page from the explain-diff template so all three explain skills look and behave the same:

1. Copy `skill://explain-diff/assets/template.html`. explain-diff is a sibling skill: the same file is `explain-diff/assets/template.html` in the folder that holds this skill's folder.
2. Keep its styles and quiz script exactly as they are — don't rewrite them. In the head, fill only `{{LANG}}` (the document's language code, e.g. `ko`) and `{{SHORT_TITLE}}` (the title in a few words), and drop the template's leading comment.
3. Replace its whole `<main>…</main>` block with the `<main>…</main>` block in this skill's `assets/sections.html`, leaving that file's instruction comments out.
4. Replace every `{{PLACEHOLDER}}` in that block.

Show code as `pre.diff` with one `span.ctx` per line, and write the spans back to back with no line breaks between them: each span is already one line.

Write in the language of the user's prompt (Korean prompt → Korean document). Keep code, identifiers, and file paths as they are. In Korean documents, write "review" as **리뷰**, not 검토.

The document has these sections, in this order:

**0. Header** — a kicker line (repository and commit), a title that says what the repository *is* in reader terms (not just its name), the source (repository, commit hash, branch, the date the document was written), the size (tracked files, main languages of the product code), and one box holding the reader assumption from Step 3 and the scope: what this map covers, what it leaves out, whether uncommitted changes are included, how much was run versus only read, and the default label (see Writing guidance).

**1. Background: what this repository is for** — the problem it solves, who uses it, the stack, and the prerequisite concepts. Prefer small concrete examples over abstract definitions. End with a sentence that sets up the picture in section 2.

**2. The system in one picture** — the one-sentence intuition, then a short paragraph (3–6 sentences) that expands it in plain words, then a static system diagram: the runtime pieces, the data stores, the external services, and arrows that carry **example data** — one concrete value followed across the system. After this section the reader should be able to guess where a given piece of data probably lives.

**3. Data dictionary** — one table with a row per kind of data: the data (in the repository's own term, with its label), the file that defines its shape, where it lives, who creates it, who reads it. Below the table, 2–4 sentences on the relationships that matter: what points at what, what is derived from what, what is per-user and what is shared.

**4. Folder map** — one table: path, role in one line, evidence (a file that shows it), number of files. Every top-level tracked entry appears. This is the index of the document — the reader comes back here to find things.

**5. Data flows** — first the flow list as a table: the flow (`start → end`), where it starts, the stores it touches, where it ends. Then the sample flow, lightly: one sentence on why this flow first, a stage table (stage, takes in, does, hands on, stored or sent, file) with the example value running through it, and at most two short code excerpts (about 15 lines each). Close by telling the reader that every row of the flow list can become its own document with explain-full-flow.

**6. Rules and cautions** — 5–12 bullets from Step 2: rules the repository enforces, boundaries and what they check, mismatches between documents and code, untested or legacy areas. Give each one a path and a label. Then a short **Left out** list.

**7. Check your understanding** — a recall quiz. People confuse the familiarity of a tidy map with knowing the territory; a reader can finish this document, feel fine, and then not know where to start on their first task. The quiz exposes those gaps while the document is still open, and sends the reader back to the right section. Say that purpose in one line above the questions.

   - **10 to 20 questions**, scaled to the repository: 10 for a small one with one or two flows, about 15 for a mid-sized one, 20 only for a large product with many kinds of data and many flows. **Medium difficulty**: answerable by someone who understood the document, not by someone who skimmed it, and not requiring anything the document didn't teach.
   - **Test structure and principle, not memory of details.** Good: "A student uploads a PDF. Which store receives the file bytes, and which record points at them?", "You must add a `difficulty` field to question cards. Which places have to change, and in what order?", "Why does today's review list read memory records and not the cards table?", "The server trusts this field from the browser without checking it — which stored data could be wrong as a result?". Bad: "How many files are in `src/`?", "What is the indexes file called?" — those are answered by Ctrl-F, and knowing them proves nothing.
   - Spread the questions over the document: the system picture, the data dictionary, folder roles, the sample flow, and at least two from rules and cautions. Prefer questions that make the reader *predict* or *apply* (a new field, a new request, a missing check) over ones that restate a sentence from the text.
   - Format: multiple choice, 3–4 options, exactly one correct. Wrong options are the plausible misreadings — what someone who half-understood would pick — never jokes or obvious filler. Vary which position holds the right answer.
   - Each question carries a short explanation (why the right answer is right, and what the tempting wrong one gets wrong) and a link to the section to re-read. Use the quiz markup in `assets/sections.html`; the template's script locks a question after one answer, counts first-try answers, offers a retry, and builds the printed answer key. Don't write your own quiz JS.

### Step 5 — Figures: static only

A map gets no interactive widgets. Draw static inline SVG, in the diagram style all three explain skills share: a box is a component and names its folder or file; an arrow is data and carries an example value; a dashed line is a boundary (browser / server / external service). Draw only the pieces and boundaries the system really has. Take colors from the template's tokens, never hard-coded hex — in SVG, set them inline (`style="fill:var(--card);stroke:var(--line)"`).

### Step 6 — Check and deliver

Before handing over, verify:

- Every top-level tracked entry appears in section 4 (compare with `git ls-files | cut -d/ -f1 | sort -u`).
- Every row of the data dictionary names a shape-defining file and a store, and every file path cited as evidence exists at the pinned commit.
- Every flow in the flow list names an entry file.
- Every code excerpt is copied from the file at the pinned commit (`git show <commit>:<path>`), not retyped from memory, and shows its path.
- The header states the default label, every claim that differs from it is labelled, and the Left out list is there.
- The system diagram carries example data, and its caption says where that example came from.
- The intuition sentence appears before any code.
- The page loads nothing external except the template's two font stylesheets.
- If you can render the page, look at it once: figure labels do not overlap, and no table or figure runs off the page.
- The quiz has 10–20 questions, every question can be answered from the document alone, no answer is a detail to memorize, and each question's `data-answer` matches the option you explain as correct.
- Nothing was written inside the repository except the document under `explanations/`, and `git status --short` is unchanged.

A small script for assembling the page and for these checks is fine; keep it outside the repository.

Save the file inside the repository being explained, as `explanations/YYYY-MM-DD-explain-full-map-<repo>.html` under its root (today's date; create the folder if it is missing), or where the user asked, and give the user the path. Keep that folder out of git without touching tracked files: if `git check-ignore -q explanations/x` fails, append the line `/explanations/` to the file that `git rev-parse --git-path info/exclude` names — never to `.gitignore`. For a repository you cloned from a URL into a scratch directory, save under `explanations/` in the current directory instead. Suggest the next step in one line: pick a row of the flow list and run explain-full-flow on it.

## Writing guidance

- Lead every section with the point, then the support.
- One term per concept, and use the repository's own term. If the code says `Deck` and you call it "question set", say once that they are the same thing, then stay consistent.
- Label how you know: **confirmed** (ran it and saw the result), **read** (read the code or the documents, did not run it), **guess** (inferred), **question** (only the maintainers can say). In Korean: 확인 / 읽음 / 추정 / 질문. State the default once in the header ("unless marked, statements were read in the code, not run") and label only what differs — per table row, bullet or paragraph, not per sentence.
- Prefer concrete things: a real example value, a real count ("38 feature folders"), a real path. Counts come from commands, not from memory.
- In a table cell a long path may start at the source root, as long as the root is stated once near the table.
- Explain the *why* you can infer — why this data lives in that store, why the folders are split this way — and mark it as inference.
- Keep the whole document readable in one sitting. A map stays shallow on purpose: table rows are one line each. For a large repository, group below the top level instead of enumerating, and say what you grouped. Depth belongs in explain-full-flow.
