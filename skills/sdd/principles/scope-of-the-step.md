# Do only the scope of the step

Build only what this plan task and the current tests require. Build the rest in the task that requires it.

**Why:** Something built ahead has no test that requires it. It becomes unverified code and an unverified decision. Fixing things outside the scope blurs the unit of review.

**How:**
- Add a dependency in the task that first uses it. Do not write a version from memory. Verify it at the source.
- Do not create fields, types or exceptions that no test requires. Write them under "Remaining work".
- Leave a defect outside the scope as a review note. Do not fix it now.
- Remove what a tool added along the way that was not requested.

**Stop:** When "it would be good to do this now too" comes to mind, write it down instead of building it.

**Evidence:** "Rejected alternatives" and "Remaining work" in the journal name what was postponed and the task that will do it.
