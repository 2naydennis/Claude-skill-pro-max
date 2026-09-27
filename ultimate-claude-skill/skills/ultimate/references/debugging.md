# Systematic debugging

Find the root cause before proposing a fix. Distilled from superpowers (systematic-debugging, root-cause-tracing, defense-in-depth, condition-based-waiting).

## Contents

- The iron law
- Phase 1: investigate
- Phase 2: compare
- Phase 3: hypothesize and test
- Phase 4: fix
- The three-strike rule
- Supporting techniques
- When there really is no root cause
- Common mistakes

## The iron law

**No fix without root-cause investigation first.** Symptom patches are failures that haven't surfaced yet.

Use this for every bug, test failure, build failure, performance problem, or surprise. Use it *especially* under time pressure, when a quick fix looks obvious, and after a fix already failed. Systematic is faster than guess-and-check.

Log the work in `assets/templates/debug-log.md` for anything non-trivial.

## Phase 1: investigate

1. **Read the error completely.** Whole stack trace. Note file, line, error code. Warnings too. They often contain the answer.
2. **Reproduce reliably.** Exact steps, every time? If not reproducible, gather more data. Don't guess.
3. **Check what changed.** `git diff`, recent commits, new dependencies, config, environment differences.
4. **Instrument boundaries in multi-layer systems.** CI to build to signing, or API to service to database: log what enters and leaves each layer, check that env and config propagate, run once. The evidence shows which boundary turns good data bad. Then investigate that layer only.
5. **Trace data flow backward.** Where does the bad value originate? What called this with it? Keep going up until you find the source. Fix at the source, not where it crashed.

## Phase 2: compare

1. Find similar code in the same codebase that works.
2. If you're implementing a known pattern, read the reference implementation completely. Don't skim.
3. List every difference between working and broken, however small. Don't assume "that can't matter".
4. Note what the code depends on: other components, settings, environment, assumptions.

## Phase 3: hypothesize and test

1. Write one hypothesis: "X is the root cause because Y". Specific, not vague.
2. Test it with the smallest possible change. One variable at a time.
3. Confirmed? Go to Phase 4. Wrong? Form a new hypothesis. Don't stack another fix on top.
4. If you don't understand something, say "I don't understand X". Research or ask. Don't pretend.

## Phase 4: fix

1. Write a failing test that reproduces the bug (see `references/coding.md`).
2. Make one change that addresses the root cause. No "while I'm here" improvements.
3. Verify: the test passes, the full suite passes, the original symptom is gone. See `references/verification-and-review.md`.
4. Regression check: revert the fix, the test must fail; restore it, the test passes.

## The three-strike rule

After three failed fixes, stop. Count them honestly.

Signs of an architectural problem, not a bad hypothesis:

- Each fix reveals new shared state or coupling somewhere else.
- Fixes need "massive refactoring" to land.
- Each fix creates a new symptom elsewhere.

Stop and discuss with the user whether the pattern itself is sound before attempt four.

## Supporting techniques

**Defense in depth.** After fixing the root cause, add validation at the layers the bad value passed through (entry point, business logic, persistence) so the same class of bug fails loudly and early next time.

**Condition-based waiting.** Flaky tests with `sleep(2)` are timing guesses. Replace fixed sleeps with polling for the actual condition (element visible, file exists, queue empty) with a timeout. Faster when things are quick, reliable when they're slow.

**Bisect.** If it worked at some past commit, `git bisect` finds the breaking change in log2(n) steps.

**Signals from the user that you're off track:** "is that actually happening?" (you assumed), "will it show us...?" (you should have gathered evidence), "stop guessing", "we're stuck?". Each one means back to Phase 1.

## When there really is no root cause

If investigation shows the cause is truly environmental, timing-dependent, or external: document what you investigated, add proper handling (retry, timeout, clear error message), and add logging so the next occurrence leaves evidence. Most "no root cause" conclusions turn out to be incomplete investigations, so be sure first.

## Common mistakes

- "Quick fix now, investigate later."
- "Let me just try changing X and see."
- Changing several things, then running tests. You can't tell what worked.
- Skipping the failing test and "manually verifying".
- Adapting a reference pattern after skimming it.
- Listing fixes before tracing the data flow.
- Attempt four after three failures, without questioning the design.
