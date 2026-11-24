# Look at the real surface

After all tests pass, run it the way it is really used. Verify a fix on the same surface where you saw the symptom.

**Why:** Tests see only the cases someone thought of. Real results hold things nobody thought of: order, format, defaults, behaviour added by a framework or a library.

**How:**
- Run it the way it is really used. A server: start it and send requests. A script or a command-line tool: run it on real input. A screen: open it and click through it. If the port is in use, use another port. Do not change the configuration.
- Feed it inputs the tests do not have: invisible characters, wrong types, long values, empty input, the same thing done at the same time.
- Turn assumptions into numbers. Do not write "rare"; write "9 out of 12". Measure time.
- For the behaviour of an earlier commit, extract that commit into a scratch folder and build it. Do not touch the working tree.
- If something else reproduces the real behaviour (a widget, an example in a document), compare it with the real result.

**Stop:** Do not say "done" on a successful build and passing tests alone.

**Evidence:** The journal has a table of real results (case, input, output).
