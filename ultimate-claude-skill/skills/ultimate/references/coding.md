# Coding and test-driven development

How to write the smallest correct change and prove it with tests. Distilled from andrej-karpathy-skills, superpowers (test-driven-development), and ECC coding rules.

## Contents

- Simplicity first
- Surgical changes
- Match the house style
- Test-driven development
- Writing good tests
- When tests are hard
- Common mistakes

## Simplicity first

Write the minimum code that solves the stated problem. Nothing speculative.

- No features beyond the request.
- No abstraction for code used once.
- No configurability or "flexibility" nobody asked for.
- No error handling for cases that can't happen.
- If you wrote 200 lines and 50 would do, rewrite it.

Test: would a senior engineer reading the diff call it overbuilt? If yes, simplify.

## Surgical changes

Every changed line should trace back to the request.

- Don't reformat, re-comment, or "improve" neighboring code.
- Don't refactor what isn't broken.
- Match the existing style, even when you'd write it differently.
- Notice unrelated dead code? Mention it. Don't delete it.
- Do remove imports, variables, and functions that *your* change orphaned.

Signs it's working: smaller diffs, fewer rewrites for overcomplication, and clarifying questions before implementation instead of after mistakes.

## Match the house style

Before writing, read the nearest similar code. Copy its naming, comment density, error-handling idiom, logging, and file layout. A consistent codebase is easier to change than a locally "better" one.

## Test-driven development

**Iron law: no production code without a failing test first.** Wrote code before the test? Delete it and start from the test. Keeping it "as reference" means you'll adapt it, which is testing after.

The cycle:

1. **Red.** Write one small test for one behavior. Clear name. Real code; mock only when unavoidable.
2. **Verify red.** Run it. It must *fail* (not error), and fail because the feature is missing, not because of a typo. A test that passes immediately is testing existing behavior; fix the test.
3. **Green.** Write the simplest code that passes. No extra options or parameters.
4. **Verify green.** Run the test, then the project's full suite (`pytest`, `npm test`, `cargo test`, whatever the repo uses). A scope statement bounds what you build, not what you verify. Report every red test by name, including ones you didn't cause.
5. **Refactor** while green: remove duplication, improve names, extract helpers. Add no behavior.
6. Next failing test.

Exceptions (throwaway prototypes, generated code, config files) need the user's OK.

**Bug fixes:** write a failing test that reproduces the bug first. It proves the fix and blocks the regression.

**Why test-first:** tests written after the code pass immediately, which proves nothing. They check the cases you remembered, not the ones you'd have discovered. You never watched them fail, so you don't know they can.

## Writing good tests

| Quality | Good | Bad |
|---|---|---|
| Minimal | One behavior. "and" in the name means split it. | `validates email and domain and whitespace` |
| Clear | Name describes the behavior | `test1` |
| Honest | Asserts on real output | Asserts a mock was called 3 times |
| Isolated | Test-only helpers live in test utilities | Test hooks added to production classes |

Before writing a test, name the production change that would make it fail. If you can't, the test is checking nothing.

Before mocking a dependency, understand its side effects. A mock that skips a side effect the code depends on makes the test lie.

## When tests are hard

Hard-to-test code is hard-to-use code. Listen to it.

| Problem | Fix |
|---|---|
| Don't know how to test it | Write the API you wish existed, then the assertion first |
| Test is complicated | The design is complicated. Simplify the interface |
| Must mock everything | Too coupled. Inject dependencies |
| Setup is huge | Extract helpers. Still huge? Simplify the design |
| No existing tests | You're improving it. Add tests for what you touch |

## Common mistakes

- Adding a config option "in case".
- Tidying adjacent code in the same diff as a bug fix.
- Writing the implementation, then a test that passes on the first run.
- Running only the new test file and calling the suite green.
- Asserting on mock calls instead of results.
- Keeping pre-TDD code "as reference" and adapting it.
