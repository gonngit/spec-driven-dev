# Look at the real surface

After all tests pass, run it the way it is really used. Verify a fix on the same surface where you saw the symptom.

**Why:** Tests see only the cases someone thought of. Real results hold things nobody thought of: order, format, defaults, behaviour added by a framework or a library.

**How:**
- Run it the way it is really used. If it serves requests: start it and send requests. A script or a command-line tool: run the command as the user types it (for a Node CLI, not `npm test`), on real input. A screen: open it and click through it; a driven browser is allowed. Name the browser, cover the keyboard and overflow, and record case, action and what was seen. If the port is in use, use another port. Do not change the configuration.
- If the part is not reachable from the entry point yet, or the project has no entry point (a library core with no command or screen), call it with real input from a one-line program and label the result "reduced". The full run belongs to the task that wires it.
- Feed it inputs the tests do not have: invisible characters, wrong types, long values, empty input, the same thing done at the same time.
- Check length and character limits with non-ASCII values (emoji, Hangul, Unicode spaces, characters that grow when their case changes). If it stores values, store the value and read it back.
- Do not trust the default behaviour of a library by assumption. When a requirement relies on it, pin it with a test.
- Turn assumptions into numbers. Do not write "rare"; write "9 out of 12". Measure time.
- For the behaviour of an earlier commit, extract that commit into a scratch folder and build it. Do not touch the working tree.
- `scripts/sdd-check.py` needs `python3`, even in a project that is not Python.
- If something else reproduces the real behaviour (a widget, an example in a document), compare it with the real result.

**Stop:** Do not say "done" on a successful build (if there is one) and passing tests alone.

**Evidence:** The journal has a table of real results (case, input, output).
