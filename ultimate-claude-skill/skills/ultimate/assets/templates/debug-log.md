# Debug log

**Symptom:** exact error text or observed vs expected behavior
**Reproduce:** exact steps or command
**Reproduces every time?** yes / no / sometimes (how often)

## Phase 1: evidence

- Error and stack trace read in full: 
- Recent changes (git log, deps, config, env): 
- Boundary logs (what enters and leaves each layer): 
- Where the bad value first appears: 

## Phase 2: comparison

- Working example found at: 
- Differences between working and broken: 

## Phase 3: hypotheses

| # | Hypothesis ("X causes it because Y") | Smallest test | Result |
|---|---|---|---|
| 1 |  |  |  |
| 2 |  |  |  |
| 3 |  |  |  |

Three failed? Stop. Question the architecture with the user before a fourth.

## Phase 4: fix

- Failing test that reproduces it: 
- Root-cause fix (one change): 
- Verification (command + output): 
- Regression check (revert fix, test fails; restore, test passes): 
