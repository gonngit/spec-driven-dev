---
name: explain-full-flow
description: Turn one data flow through a codebase into a learning document — a single self-contained HTML page that follows one piece of data from where it enters, through each stage that changes it, to where it comes to rest. It gives the background first, the idea in one sentence, a diagram and stage table carrying one real example value, the code stage by stage in the order the data travels, a guide to changing it safely, and a 10–20 question recall quiz. Runs only when invoked by name. For a whole-repository overview use explain-full-map; for a commit, branch or PR use explain-diff.
disable-model-invocation: true
---

# Explain Full — Flow

Turn one data flow through a codebase into a document a person can *learn* from — something they could print and read in a café before touching that feature, not a list of the files it uses.

"Flow" here means the path data takes through the running code at one commit: where it enters, what each stage turns it into, where it is stored or sent, and who reads it back. It is not the history of commits — that is explain-diff.

A code search finds the files a feature touches. It does not tell you in what order things happen, or what the data looks like on the way. This skill tells the flow as a journey:

1. **Context before code** — what must I know to follow this flow?
2. **Intuition before detail** — what is the one idea of this flow?
3. **One real value, in the order it travels** — follow a concrete example through every stage, and show the code in that order, not in file order.
4. **Evidence, not impressions** — there is no diff to anchor the explanation, so every stage names its file and line, and what was run, read or guessed is labelled.
5. **Recall before work** — end with a quiz, because reading a clear walkthrough *feels* like understanding even when it isn't.

This is the second of three zoom levels that share one template and one diagram style:

| Skill | Question it answers | When |
|---|---|---|
| explain-full-map | Where is everything, and what data does the system keep? | Once, when entering a repository |
| explain-full-flow (this one) | How does one feature work, from input to stored result? | When the part to work on is chosen |
| explain-diff | What did this change do? | For every change |

A map first is the usual order, but this skill works on its own. If the request is about the whole repository, use explain-full-map. If it is about a commit, branch or PR, use explain-diff.

The running example in this file: in a study app, what happens when a student answers a question card.

## Workflow

### Step 1 — Pin the repository, and trace the flow

Work on the repository in the current directory, or the path or URL the user names (clone a URL into a scratch directory outside every repository).

- **Pin it.** Record `git rev-parse --short HEAD`, the branch, and `git status --short`. The document describes that commit. If there are uncommitted changes, say in the header whether they are included.
- **Identify the flow.** Take it from the request: a feature, a screen, an endpoint, a file, or a row of an explain-full-map flow list. If the request does not point at one flow, survey lightly (README, routes, entry points) and prepare 3–6 candidates for Step 3.
- **Trace it.** Start where the data enters (a UI event, a route, a job trigger, a CLI command) and follow it until it comes to rest (a store, an external call, a response). If other features read that data back later, those are other flows: name them in one closing line, don't trace them.
- **Read the shape at every boundary** — the schema, type or rule that defines what crosses.
- **Read the tests that exercise the flow.** They hold real example values and the expected results.
- **Read beyond the path**: other callers of a shared stage, and the config or flags that switch branches. Read the repository's own documents on the feature too.

The repository's documents are claims, not facts. Check the ones you repeat against the code; a mismatch is a finding for section 5, not something to smooth over. A number you cannot confirm (a test count, a coverage figure) is reported as the document's claim, not as a fact.

Read only, with one exception: the finished document is saved in the repository's `explanations/` folder (Step 6). Otherwise never create, edit or delete anything inside the repository — no notes, no generated files, no installs. If you run something to confirm a claim or to capture example values (a test, a script), run it in a scratch copy (`git archive <commit> | tar -x -C <scratch>`), not in the repository. If the toolchain is missing, do not install it: say in the header what could not be run.

### Step 2 — Analyze before writing

Write these down for yourself first (a scratch note outside the repository is fine). The document is built from them.

- **The one-sentence intuition.** The core idea of the flow in plain words, without identifiers. Study app: *"Each answer updates one memory record, and that record alone decides when the card comes back."* If you cannot write this sentence, you do not understand the flow yet — read more code.
- **Prerequisite concepts.** What must a reader know to follow it? The framework's request model, the store's data model, the algorithm or protocol in the middle, the domain terms.
- **Stage list.** 3–8 stages in the order the data travels. A stage is a step in what happens to the data, not a file or a function: one function can hold several stages, and one stage can span several files. For each: what it takes in (shape), what it does, what it hands on (shape), where it stores or sends anything, and its main file and function. Each stage should depend only on earlier stages. If there are more, group them and say what you grouped.
- **Example value.** One concrete input, taken from a test, a fixture, seed data, or a real run in a scratch copy. Record what it looks like entering and leaving every stage. If you could only read the code, derive the values by reading and label them "read, not run". For values the code creates at run time (ids, hashes, timestamps), write a clear stand-in (`<uuid>`, `$2a$…`), not a made-up literal. Never present an invented value as real.
- **Boundaries.** Where the data crosses: browser → server, server → store, server → external service, process → process. At each one: what checks it (which schema, which rule), and what is trusted without a check.
- **Path coverage.** Every function and file the data passes through between the start and the end belongs to a stage. Things that hang off the path — logging, analytics, error branches, retries, caching — go on a "not followed" list, one line each. Nothing may silently disappear — a reader who later steps through the code should meet nothing you didn't mention.
- **Edge-case pass.** Push boundary inputs through the stages, in your head or with a test in a scratch copy: a missing or empty field, an oversized value, a duplicate, the same request twice or two at once, an unauthenticated caller, old stored data that lacks a newer field. Note which stage catches each one — or that none does. A reader who understands a flow should also know where it can break, and this pass is where most of the real insight comes from. Results feed section 5.
- **Widget candidates.** Is there a relationship a table cannot show well — many combinations of inputs, or a stored value that changes over repeated events? (See Step 5.)
- **Change guide.** For the change the reader has in mind (Step 3), or else for the two or three most likely changes (add a field, change a rule, add a stage): the places to touch, in the order the data travels — shape definition → producer → store → reader → screen → tests — with real paths.
- **Quiz candidates.** As you analyze, note the points where a reader could nod along without really getting it: why the stages come in this order, what breaks if one stage is skipped, what the flow does with an input the document never showed. These become section 6.

### Step 3 — Calibrate to the reader

Two things shape this document: what the reader already knows, and why they are reading.

1. Check what you already know: the user's prompt ("I know React but not Firestore", "I need to add a field to this"), their own notes (memory, a user-level AGENTS.md — not the repository's), their role, the conversation so far. Whatever that settles, do not ask.
2. Otherwise ask **one short round**, as one form, with only the open items: (a) 1–3 questions naming the actual prerequisite concepts from Step 2, with options like *new to me / roughly / know it well*; (b) the purpose — *just understand it* or *about to change it*, and if so what; (c) which flow, only when the request did not settle it — offer the candidates from Step 1 with your recommendation preselected. In omp, use the `ask` tool (AskUserQuestion in Claude Code). Never ask more than one round; the reader came to read, not to fill in forms.
3. If you cannot ask (non-interactive run), assume a capable engineer who is new to this part of the code and wants to understand it, pick the core flow, and say all of that at the top of the document.

Apply the answers. Knowledge sets the depth of section 1: known concepts get one line, new ones a real explanation, deeper material goes inside `<details>`. Purpose sets section 5: for a reader about to change something, go deeper on the stages that change touches and write the change guide for that change; for a reader who only wants to understand, keep section 5 short.

### Step 4 — Write the document

Build the page from the explain-diff template so all three explain skills look and behave the same:

1. Copy `skill://explain-diff/assets/template.html`. explain-diff is a sibling skill: the same file is `explain-diff/assets/template.html` in the folder that holds this skill's folder.
2. Keep its styles and quiz script exactly as they are — don't rewrite them. In the head, fill only `{{LANG}}` (the document's language code, e.g. `ko`) and `{{SHORT_TITLE}}` (the title in a few words), and drop the template's leading comment.
3. Replace its whole `<main>…</main>` block with the `<main>…</main>` block in this skill's `assets/sections.html`, leaving that file's instruction comments out.
4. Replace every `{{PLACEHOLDER}}` in that block.

Show code as `pre.diff` with one `span.ctx` per line, and write the spans back to back with no line breaks between them: each span is already one line.

Write in the language of the user's prompt (Korean prompt → Korean document). Keep code, identifiers, and file paths as they are. In Korean documents, write "review" as **리뷰**, not 검토.

The document has these sections, in this order:

**0. Header** — a kicker line (the flow, repository and commit), a title that says what happens in reader terms ("What happens when a student answers a card"), the source (repository, commit hash, branch, the date the document was written), the extent (where the flow starts and ends, number of stages), and one box holding the reader assumption and purpose from Step 3, what was not followed, whether uncommitted changes are included, how much was run versus only read, and the default label (see Writing guidance).

**1. Background: what you need to know first** — the prerequisite concepts, and one or two sentences on where this flow sits in the whole system. Prefer small concrete examples and simple static diagrams over abstract definitions. End with a sentence that sets up the question the flow answers.

**2. The flow in one sentence** — the one-sentence intuition, then a short paragraph (3–6 sentences) that expands it in plain words, like a good math teacher giving the meaning before the formula. After this section the reader should be able to predict roughly what the stages will be.

**3. Follow the data** — a static diagram: each stage is a box that names its main file, each arrow carries the **example value** in the shape it has at that point, and boundaries are dashed lines. Then the stage table: stage, takes in, does, hands on, stored or sent, main file. The diagram and the table use the same stage names in the same order as section 4. If a widget passes the gate in Step 5, it closes this section under its own small heading; if none does, add nothing.

**4. The flow, stage by stage** — the literate walkthrough. For each stage:
   - A heading that names the stage as an action ("Stage 2 — Grade the answer").
   - **Why this stage**: 1–3 sentences linking it to the intuition and to the previous stage.
   - **For each file in the stage**: one line on the file's role in the system *before* showing its code. Then the relevant excerpt with its path and line. Trim long excerpts to the meaningful lines and note what you trimmed (`… 12 lines omitted …`). A file that only passes the value along (an interface, a plain data class) can have its role line without an excerpt.
   - Short notes after the code that point at the important lines — what to look at, not a line-by-line paraphrase.
   - **The example value, in and out**: what it looked like entering this stage and what it looks like leaving.
   - **Bridge**: one sentence on what this stage makes possible or what it leaves for the next ("The answer is graded, but nothing is saved yet — that's stage 3.").

**5. Changing it safely** — first the change guide as a table: the change, and the places to touch in the order the data travels. Then 3–8 cautions from the boundaries and the edge-case pass: concrete scenarios ("two answers for the same card arrive at once → the second overwrites the first's memory record"), checks that are missing at a boundary, mismatches between documents and code, untested stages. Give each one an input and a consequence, and a label. If you looked for mismatches between documents and code and found none, say so in one line. Then the short **Not followed** list from path coverage.

**6. Check your understanding** — a recall quiz. People confuse the familiarity of well-written sentences with understanding; a reader can finish this document, feel fine, and then break the flow with their first edit. The quiz exposes those gaps while the document is still open, and sends the reader back to the right section. It is a speed governor, not an exam; a sensible rule for the reader is *"I don't change this flow until I pass."* Say that purpose in one line above the questions.

   - **10 to 20 questions**, scaled to the flow: 10 for a short one of three or four stages, about 15 for a typical one, 20 only for a long flow with many boundaries and edge cases. **Medium difficulty**: answerable by someone who understood the document, not by someone who skimmed it, and not requiring anything the document didn't teach.
   - **Test structure and principle, not memory of details.** Good: "Why must grading happen before the memory record is updated?", "The answer arrives without a card id — which stage rejects it, and what does the student see?", "You add a `confidence` field to an answer. Which stages must change?", "If stage 3 saved the record but stage 4 never read it, what would the student notice tomorrow?". Bad: "What is the function in stage 2 called?", "Which file holds the schema?" — those are answered by Ctrl-F, and knowing them proves nothing.
   - Spread the questions over the document: the intuition, at least one stage-to-stage dependency, at least one boundary, at least two edge cases from section 5, and at least one from the change guide. Prefer questions that make the reader *predict* or *apply* (a new input, a skipped stage, a new field) over ones that restate a sentence from the text.
   - Format: multiple choice, 3–4 options, exactly one correct. Wrong options are the plausible misreadings — what someone who half-understood would pick — never jokes or obvious filler. Vary which position holds the right answer.
   - Each question carries a short explanation (why the right answer is right, and what the tempting wrong one gets wrong) and a link to the section or stage to re-read. Use the quiz markup in `assets/sections.html`; the template's script locks a question after one answer, counts first-try answers, offers a retry, and builds the printed answer key. Don't write your own quiz JS.

### Step 5 — Figures, and the widget gate

Draw static inline SVG, in the diagram style all three explain skills share: a box is a component and names its file; an arrow is data and carries the example value; a dashed line is a boundary (browser / server / external service). Draw only the pieces and boundaries the flow really has. Take colors from the template's tokens, never hard-coded hex — in SVG, set them inline (`style="fill:var(--card);stroke:var(--line)"`).

An interactive widget is valuable only when it lets the reader *explore a causal relationship* that the diagram and the stage table cannot show well. A decorative control is ornament, and it costs the reader attention. Before adding a widget, it must pass all three checks:

1. **Causal**: the reader changes an input the flow really receives, and sees what the stages really compute — which stage accepts or rejects it, and the value after each stage.
2. **Hard to see statically**: there are too many input combinations for a table, or a stored value changes over repeated events (a schedule, a counter, a state machine).
3. **Faithful**: the widget runs the *same logic as the code*. Port the real functions of the stages into the page's JS with their real constants and messages, and label which functions it mirrors. Port only pure logic — validation, normalization, calculation, state transitions. A stage that depends on a database, the network, the clock or a framework is never imitated: let the reader set its answer with a control ("this email is already taken"), or leave the stage out and say so.

Study app passes: answer the same card several times, right or wrong, and watch the memory record and the next review date change. The usual flow widget is an **input runner**: a row of sample inputs — the example value plus the edge cases from Step 2 — and, for the chosen one, each stage's verdict and output. A flow whose edge cases fit in a short table gets no widget.

Read `skill://explain-diff/references/widgets.md` (explain-diff is a sibling skill) for widget patterns and implementation rules before writing one. Put the widget's code in its own `<script>` block and leave the quiz script alone.

### Step 6 — Check and deliver

Before handing over, verify:

- The diagram, the stage table and section 4 name the same stages in the same order.
- Every function and file on the path appears in a stage or in the Not followed list.
- Every code excerpt is copied from the file at the pinned commit (`git show <commit>:<path>`), not retyped from memory, and shows its path and line.
- The example value is the same one from the first stage to the last, each stage's output is the next stage's input, and the diagram's caption says where it came from and whether it was run or read.
- Every file path cited as evidence exists at the pinned commit.
- The header states the default label, and every claim that differs from it is labelled.
- The intuition sentence appears before any code.
- The page loads nothing external except the template's two font stylesheets.
- Each widget passes the gate, runs without network access, names the functions it mirrors, and shows its static fallback in print.
- If you can render the page, look at it once: figure labels do not overlap, and no table or figure runs off the page.
- The quiz has 10–20 questions, every question can be answered from the document alone, no answer is a detail to memorize, and each question's `data-answer` matches the option you explain as correct.
- Nothing was written inside the repository except the document under `explanations/`, and `git status --short` is unchanged.

A small script for assembling the page and for these checks is fine; keep it outside the repository.

Save the file inside the repository being explained, as `explanations/YYYY-MM-DD-explain-full-flow-<repo>-<short-slug>.html` under its root (today's date; the slug is a few English words naming the flow, e.g. `member-signup`; create the folder if it is missing), or where the user asked, and give the user the path. Keep that folder out of git without touching tracked files: if `git check-ignore -q explanations/x` fails, append the line `/explanations/` to the file that `git rev-parse --git-path info/exclude` names — never to `.gitignore`. For a repository you cloned from a URL into a scratch directory, save under `explanations/` in the current directory instead.

## Writing guidance

- Lead every section with the point, then the support.
- One term per concept, and use the repository's own term. If the code says `gapClock` and you call it "exposure clock", say once that they are the same thing, then stay consistent.
- Label how you know: **confirmed** (ran it and saw the result), **read** (read the code or the documents, did not run it), **guess** (inferred), **question** (only the maintainers can say). In Korean: 확인 / 읽음 / 추정 / 질문. State the default once in the header ("unless marked, statements were read in the code, not run") and label only what differs — per table row, bullet or paragraph, not per sentence.
- Prefer concrete numbers and values: "the record's stability goes from 2.31 to 5.02" teaches more than "the record is updated".
- In a table cell a long path may start at the source root, as long as the root is stated once near the table.
- Explain the *why* behind each decision you can infer — why this stage is on the server, why the data is stored in this shape — and mark it as inference.
- Keep the whole document readable in one sitting. If the flow is long, go deep on the stages that carry the idea, keep the mechanical ones to a row in the stage table, and say what you shortened.
