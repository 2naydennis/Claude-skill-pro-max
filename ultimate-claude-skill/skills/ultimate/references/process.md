# Process: think, classify, design, plan

How to go from a request to an approved design and a plan before writing code. Distilled from andrej-karpathy-skills, superpowers (brainstorming, writing-plans), and planning-with-files.

## Contents

- Think before acting
- Classify the request
- Brainstorming an architectural change
- Writing a spec
- Writing an implementation plan
- Planning files for long tasks
- Common mistakes

## Think before acting

Don't assume, don't hide confusion, and surface tradeoffs.

- State your assumptions out loud. If you're unsure, ask.
- If the request has two readings, show both. Don't pick one silently.
- If a simpler approach exists, say so. Push back when it's warranted.
- If something is unclear, stop and name the confusing part.
- When you play your understanding back, separate what the user said from what you inferred.

A good first message on a vague request: one focused question about purpose ("who will use this, and what should they be able to do?"), not a list of ten.

## Classify the request

Say the class out loud before your first question, so the user can override it.

| Class | Signals | Path |
|---|---|---|
| **Spike** | "can we", "is it possible", "quick and dirty is fine" | Describe the question and the probe in 2 to 3 sentences. Get a nod. Investigate as cheaply as correctness allows. Report a recommendation. Anything built is labeled throwaway. |
| **Bounded** | A small change to a flow that already exists in this repo: a flag, an endpoint, a one-file fix | Explore context. Ask only the questions that matter, one at a time. Present a short design in chat (approach, files touched, how you'll test). **Stop and wait for yes.** Then build with TDD. No spec file. |
| **Architectural** | New project, new subsystem, restructured components, changed interfaces others depend on | Full process below: questions, approaches, sectioned design, written spec, user review of the spec, then an implementation plan. |

Rules for classifying:

- When in doubt between two classes, pick the heavier one. Reaching for the lighter label to skip work is itself the warning sign.
- "Bounded" measures the repo, not your familiarity with the kind of app. A new app has no existing flow, so it is architectural.
- Hidden complexity found mid-task upgrades the class. Stop, say so, and step up. Nothing downgrades mid-task.
- Each task gets its own classification and approval. Approving a spike doesn't approve keeping its code.
- An approval covers the stage actually presented. Approving an idea doesn't approve a spec that doesn't exist yet.

## Brainstorming an architectural change

1. **Explore context.** Read the files, docs, and recent commits that matter.
2. **Check scope.** If the request bundles independent subsystems (chat, billing, analytics), flag it now and split it into sub-projects. Each gets its own spec, plan, and build cycle.
3. **Ask clarifying questions one at a time.** Prefer multiple choice. Focus on purpose, constraints, and success criteria.
4. **Propose 2 or 3 approaches** with tradeoffs. Lead with your recommendation and why. Apply YAGNI to every option.
5. **Present the design in sections**, each sized to its complexity (a few sentences up to ~300 words). Ask after each whether it looks right. Cover architecture, components, data flow, error handling, and testing.
6. **Write the spec** (template: `assets/templates/spec.md`), self-review it, and ask the user to review the file.
7. **Write the implementation plan** only after the spec is approved.

**Design for isolation.** Each unit gets one purpose, a clear interface, and independent tests. For each unit you should be able to answer: what does it do, how do you use it, what does it depend on? If someone can't understand a unit without reading its internals, the boundary needs work. Smaller, focused files also make your own edits more reliable.

**In an existing codebase**, follow established patterns. Include targeted improvements only where existing problems block the work (a file too big to change safely, tangled responsibilities). No unrelated refactors.

## Writing a spec

Use `assets/templates/spec.md`. Then self-review with fresh eyes:

1. **Placeholder scan.** Any TBD, TODO, or vague requirement? Fill it in.
2. **Consistency.** Do sections contradict each other? Does the architecture match the features?
3. **Ambiguity.** Could a requirement be read two ways? Pick one and write it down.
4. **Scope.** Is it small enough for one implementation plan?

Fix issues inline, then hand the file to the user for review. Wait for approval.

## Writing an implementation plan

Write it for a competent engineer who has never seen this codebase or the spec. They'll write idiomatic code once they know the exact interface and test. What they can't know is what you decided. Write down:

- Exact file paths to create or modify, with line ranges.
- Function names, signatures, and the types passed between tasks.
- Values copied verbatim from the spec (limits, names, versions).
- The test that proves each task.

Structure (template: `assets/templates/implementation-plan.md`):

- **Header:** goal, architecture, tech stack, link to the spec.
- **Global constraints:** project-wide requirements, one line each.
- **Review focus:** the inputs or conditions the spec implies but no test exercises, most likely first. Give each one a test in the task that owns the code.
- **File map:** every file and its single responsibility. Split by responsibility, not by technical layer. Files that change together live together.
- **Tasks:** each is the smallest unit with its own test cycle that a reviewer could approve or reject on its own. Fold setup and config into the task that needs them.
- **Steps:** each is one action with a checkable result. Write failing test, run it, implement, run suite, commit.

## Planning files for long tasks

For work needing 5+ tool calls, or anything that may outlive the context window, keep three files on disk. `scripts/ultikit.py plan DIR --goal "..."` creates them from the templates.

| File | Holds | Update when |
|---|---|---|
| `task_plan.md` | Goal, success criteria, phases, current phase, decisions | Phase changes, decisions made |
| `findings.md` | Where things live, confirmed facts, dead ends, sources | The moment you learn something |
| `progress.md` | Timestamped log: did, result, next | After every step |

Why it works: the context window is volatile memory, the disk is persistent. Re-reading `task_plan.md` before a big decision pulls the goal back into recent attention after dozens of tool calls have pushed it out.

**Recovering after a reset:** read all three files, then run `git diff --stat` to catch code changes the files don't mention yet. Only then continue.

## Common mistakes

- Starting to code in the same message that presents a design. The approval is the gate.
- Calling a new app "bounded" because it's a familiar kind of app.
- Asking five questions at once. Ask one, wait, ask the next.
- Refining details of a project that should have been split into sub-projects first.
- Plans that say "add validation" instead of naming the file, function, and test.
- Letting `findings.md` go stale and rediscovering the same dead end after a reset.
