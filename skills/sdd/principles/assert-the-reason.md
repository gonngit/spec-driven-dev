# Assert the reason, not the status

See that a test fails for the right reason and passes for the right reason. The outside of a result (a status code, an exit code, "an error occurred") can be right while the reason is different.

**Why:** A test that looks only at the status lets the same status through for a wrong reason. If a server error shows up as 401, a test that "expects 401" passes. An error caused by a missing file also satisfies a test that says "a wrong format raises an error".

**How:**
- When tests fail, read the failure message of each one. Is it the failure you expected (an assertion, a compile error, or some other error)?
- In a test that checks an error, also look at a value that tells the reasons apart (the kind of error, the message, a field of the body).
- Give a test one reason to fail. When two different faults can make it fail, split it.
- Assert a status with the expected value. "Not 200" lets 500 pass.
- Check a rule that covers two fields once for each field. A test that breaks both at once still passes when one of the two constraints is removed.
- For results that must be equal, check that the content is equal too. For results that must differ, check that the content differs.
- If you injected a defect and the test still passes, verify the reason for that pass on the real surface.

**Stop:** Do not close a step with "it passed; I did not verify why". Verify it or leave a review note.

**Evidence:** The journal records the reason for the failures ("all 18 fail with the same error: the path does not exist").
