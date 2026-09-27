# Verification and code review

Evidence before claims, and review that is technical rather than performative. Distilled from superpowers (verification-before-completion, requesting-code-review, receiving-code-review) and ECC code-review rules.

## Contents

- Verify before claiming done
- What counts as evidence
- Giving a code review
- Receiving a code review
- Delegated work
- Common mistakes

## Verify before claiming done

**Iron law: no completion claim without fresh verification evidence from this turn.**

Before any status claim or expression of satisfaction:

1. **Identify** the command that proves the claim.
2. **Run** it, fresh and in full.
3. **Read** the whole output and the exit code. Count failures.
4. **Compare.** Does the output confirm the claim? If no, state the real status with the evidence. If yes, state the claim with the evidence.
5. Only then make the claim.

This applies to exact phrases, paraphrases, and anything that implies success: "Done!", "Perfect", "should work now", "looks good", moving to the next task, committing, opening a PR.

## What counts as evidence

| Claim | Evidence needed | Not enough |
|---|---|---|
| Tests pass | Test run output with 0 failures | An earlier run; "should pass" |
| Linter clean | Linter output with 0 errors | Partial check |
| Build succeeds | Build command exits 0 | Linter passing; logs look fine |
| Bug fixed | Original symptom re-tested and gone | Code changed; assumed fixed |
| Regression test works | Fails with fix reverted, passes restored | Passes once |
| Requirements met | Re-read spec, line-by-line checklist | Tests green |
| UI works | Screenshot or DOM check of the actual page | Code compiles |

Words that mean you skipped this step: should, probably, seems to, looks correct.

## Giving a code review

Use `assets/templates/code-review-checklist.md`.

- **Rank by severity:** correctness and security, then data loss, then performance, then maintainability. Style last, and only if asked.
- **Every finding gets three things:** `file:line`, a concrete failure scenario (input X produces wrong result Y, or crash Z), and a suggested fix.
- **Verify before reporting.** Trace the code path. A plausible-sounding finding that's wrong costs the author time.
- **Separate must-fix from optional.** Label them.
- **Check scope.** Does every change trace to the request? Flag speculative additions.

## Receiving a code review

1. **Read** all the feedback before reacting.
2. **Restate** each item in your own words, or ask about it.
3. **Verify** each item against the actual codebase.
4. **Evaluate:** is it technically right for *this* codebase?
5. **Respond** with a technical acknowledgment or reasoned pushback.
6. **Implement** one item at a time, testing each.

**If anything is unclear, ask before implementing anything.** Items often depend on each other; partial understanding produces a wrong implementation. "I understand 1, 2, 3, and 6. I need clarification on 4 and 5 before I start."

**Order:** blocking issues (breakage, security) first, then simple fixes (typos, imports), then complex ones (refactors, logic).

**No performative agreement.** Not "You're absolutely right!", "Great catch!", or "Let me implement that now" before checking. State the fix, or just do it.

**Push back** with technical reasons when a suggestion:

- breaks existing behavior,
- ignores context the reviewer doesn't have,
- adds something unused (grep for real callers first; "this endpoint has no callers, remove it instead?"),
- is wrong for this stack or platform,
- conflicts with a decision the user already made (stop and ask the user).

If you can't verify a suggestion, say so: "I can't confirm this without X. Should I investigate, ask, or proceed?"

## Delegated work

When a subagent or tool reports success, check the diff yourself. Verify the changes exist and do what was claimed. Report the actual state, not the agent's report.

## Common mistakes

- "Tests pass" based on a run from before the last edit.
- "Build passes" because the linter did.
- Implementing four of six review items and asking about the other two afterward.
- Agreeing with a reviewer before reading the code they're talking about.
- Reporting style nitpicks at the same weight as a data-loss bug.
