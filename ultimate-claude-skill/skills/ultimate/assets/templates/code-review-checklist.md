# Code review checklist

Rank findings by severity. For each: `file:line`, the failure scenario (input X gives wrong result Y), and the fix.

## 1. Correctness

- [ ] Does it do what the request or spec asked, and nothing extra?
- [ ] Edge cases: empty, one item, max size, null / missing, unicode, negative, zero
- [ ] Error paths handled where errors can actually happen
- [ ] Concurrency: shared state, ordering, retries, idempotency
- [ ] Off-by-one, wrong comparison operator, wrong units

## 2. Security

- [ ] No secrets in code or logs
- [ ] Input validated at the boundary
- [ ] Parameterized queries; output escaped
- [ ] Authorization checked, not just authentication
- [ ] Errors don't leak internals

## 3. Data safety

- [ ] Migrations reversible or backed up
- [ ] No silent data loss or truncation

## 4. Tests

- [ ] New behavior has a test that failed first
- [ ] Tests assert real behavior, not mock calls
- [ ] Full suite run and green

## 5. Scope and simplicity

- [ ] Every changed line traces to the request
- [ ] No speculative options or single-use abstractions
- [ ] Matches existing style and patterns

## 6. Performance

- [ ] No N+1 queries or repeated work in loops
- [ ] Large inputs don't blow memory

Skip taste nitpicks unless the author asked for them.
