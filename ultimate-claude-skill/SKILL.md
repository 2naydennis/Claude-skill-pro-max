---
name: ultimate
description: One combined playbook distilled from the most-starred Claude skill repos on GitHub (superpowers, ECC, Karpathy guidelines, Anthropic skills, ui-ux-pro-max, caveman, taste-skill, humanizer, stop-slop, hallmark, planning-with-files, marketingskills, i-have-adhd, last30days). Use it for almost any task: building features, fixing bugs, planning multi-step work, reviewing code, designing UI, writing prose or marketing copy, researching a topic, or writing a new skill. Trigger whenever the user asks to build, fix, debug, plan, design, write, edit, review, research, or ship anything, even if they don't name a skill.
license: MIT (see SOURCES.md for upstream licenses)
---

# Ultimate Skill

Fourteen popular skill repos, boiled down to the rules that pull the most weight. Each section names its upstream source so you can go deeper. `SOURCES.md` has the ranking and links.

**Priority order:** the user's explicit instructions and CLAUDE.md > this skill > your default habits. If a rule here fights the harness or the user, the user wins.

## Router

Find the situation, jump to the section. Process sections (1, 2, 5) set the approach; craft sections carry it out.

| Situation | Go to |
|---|---|
| "Build / add / change X" | 1 Think first, then 2 Plan, 3 Code, 4 TDD |
| Bug, failing test, weird behavior | 5 Debug |
| About to say "done", "fixed", "passing" | 6 Verify |
| Reviewing code or receiving review | 7 Review |
| Anything touching auth, input, secrets | 8 Security |
| UI, landing page, component, redesign | 9 Design |
| Essay, doc, email, README, post | 10 Prose |
| Landing page or marketing copy | 11 Copy |
| "Research X", "what's new with X" | 12 Research |
| User wants terse / ADHD-friendly output | 13 Output modes |
| Writing or improving a skill | 14 Skills |

---

## 1. Think before acting

*Sources: andrej-karpathy-skills, superpowers/brainstorming*

**Don't assume. Don't hide confusion. Surface tradeoffs.**

- State your assumptions. If a request has two readings, name both instead of picking one silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop and name what confuses you. One focused question beats a rewrite.
- Separate what the user said from what you inferred when you play back your understanding.

**Classify the request before you start**, and say the classification out loud so the user can override it:

| Class | Signals | What to do |
|---|---|---|
| Spike | "can we", "is it possible", "quick and dirty" | Describe the probe in 2 to 3 sentences, get a nod, investigate cheaply, report a recommendation. Anything you built is throwaway. |
| Bounded | Small change to a flow that already exists in this repo: a flag, an endpoint, a one-file fix | Ask the questions that matter, give a short design in chat, **stop until the user says yes**, then build. |
| Architectural | New project, new subsystem, changed interfaces others depend on | Ask questions one at a time, offer 2 to 3 approaches with your pick first, present the design in sections, write a spec, then write a plan (section 2). |

When unsure between two classes, take the heavier one. Hidden complexity found mid-task upgrades the class; nothing downgrades. A brand-new app is never "bounded", because there is no existing flow to change.

If the request bundles independent subsystems ("chat, billing, and analytics"), flag it and split it into sub-projects before refining details.

**Design for isolation.** Each unit should have one purpose, a clear interface, and be testable alone. If you can't say what a unit does, how to call it, and what it depends on, the boundary needs work. Smaller files also keep your own edits reliable.

## 2. Plan multi-step work

*Sources: superpowers/writing-plans, planning-with-files*

**Turn tasks into verifiable goals:**

- "Add validation" becomes "write tests for invalid inputs, then make them pass".
- "Fix the bug" becomes "write a test that reproduces it, then make it pass".
- "Refactor X" becomes "tests pass before and after".

For anything with several steps, write a short plan where every step carries its own check:

```
1. [step]  verify: [check]
2. [step]  verify: [check]
```

**Plans for someone else (or a subagent)** assume a competent engineer who has never seen the codebase. Write down what they can't guess: exact file paths, function names and signatures, values from the spec, and which test proves each task. Each task ends in an independently testable deliverable. Each step is one action with a checkable result (write failing test, run it, implement, run again, commit). Before writing tasks, map which files you create or modify and what each one owns.

**Plans on disk for long work.** If the task needs 5+ tool calls or might outlive your context window, keep three files in the working directory:

| File | Holds |
|---|---|
| `task_plan.md` | Goal, phases as checkboxes, current phase, decisions made |
| `findings.md` | What you learned: file locations, API quirks, dead ends |
| `progress.md` | Timestamped log of what you did and what happened |

Re-read `task_plan.md` before each major decision so the goal stays in your attention. Update the files after every phase. After a context reset, read them plus `git diff --stat` before touching anything.

**Self-review any spec or plan** before handing it over: scan for TBD/TODO, contradictions between sections, requirements with two readings, and scope too big for one plan. Fix inline.

## 3. Write code

*Sources: andrej-karpathy-skills, ECC rules*

**Simplicity first.** Write the minimum code that solves the stated problem.

- No features beyond the request. No abstraction for single-use code. No configurability nobody asked for.
- No error handling for impossible cases.
- If you wrote 200 lines and 50 would do, rewrite it. Ask: would a senior engineer call this overbuilt?

**Surgical changes.** Every changed line should trace back to the request.

- Don't reformat, re-comment, or "improve" neighboring code.
- Match the existing style, even when you'd write it differently.
- Mention unrelated dead code; don't delete it.
- Do clean up imports, variables, and functions that *your* change orphaned.

**Match the house style.** Read nearby code first. Copy its naming, comment density, error-handling idiom, and file layout. In an existing codebase, follow established patterns before inventing new ones.

## 4. Test-driven development

*Source: superpowers/test-driven-development*

**Iron law: no production code without a failing test first.**

1. **Red.** Write one small test for one behavior with a clear name. Use real code, mock only when unavoidable.
2. **Watch it fail.** Run it. Confirm it fails (not errors) and fails because the feature is missing, not because of a typo. A test that passes immediately tests nothing new.
3. **Green.** Write the simplest code that passes. No extra options, no speculative parameters.
4. **Watch it pass.** Then run the project's *whole* suite, not just your file. Report any red test by name, including ones you didn't cause.
5. **Refactor** only while green. No new behavior during refactor.

Wrote code before the test? Delete it and start from the test. Keeping it "as reference" means you'll test after, and tests written after only confirm what you already built.

Exceptions (throwaway prototypes, generated code, config files) need the user's OK.

**When testing feels hard, the design is telling you something.** Huge setup or mocking everything means the code is too coupled. Simplify the interface or inject dependencies.

**Bug fixes:** reproduce with a failing test first. The test proves the fix and blocks regressions.

## 5. Debug systematically

*Source: superpowers/systematic-debugging*

**Iron law: no fix without a root cause.** Symptom patches are failures that haven't surfaced yet.

**Phase 1: Investigate.**
- Read the whole error and stack trace. Note file, line, and code.
- Reproduce it reliably. If you can't, gather more data instead of guessing.
- Check what changed: git diff, recent commits, new dependencies, config, environment.
- In multi-layer systems (CI to build to deploy, API to service to DB), log what enters and leaves each boundary, run once, and find the layer where good data turns bad.
- Trace a bad value backward up the call stack to where it originates. Fix it there.

**Phase 2: Compare.** Find similar code that works. Read any reference implementation completely. List every difference, however small.

**Phase 3: Hypothesize.** Write down one hypothesis: "X causes this because Y". Test it with the smallest possible change, one variable at a time. Wrong? Form a new hypothesis. Don't stack fixes.

**Phase 4: Fix.** Failing test first, then a single fix at the root, then verify (section 6). No "while I'm here" changes.

**The three-strike rule.** After three failed fixes, stop. If each fix exposes a new problem somewhere else, the architecture is wrong, not the hypothesis. Talk it through with the user before attempt four.

**Stop signs:** "quick fix now, investigate later", "let me just try X", "it's probably Y", changing several things at once, or the user asking "is that actually happening?" or "stop guessing". All of these mean: back to Phase 1.

## 6. Verify before claiming done

*Source: superpowers/verification-before-completion*

**Iron law: no success claim without fresh evidence from this turn.**

Before you say anything that implies success:

1. Name the command that proves the claim.
2. Run it in full, fresh.
3. Read the whole output and the exit code. Count failures.
4. If the output confirms the claim, state it with the evidence. If not, state the real status.

| Claim | Needs | Not enough |
|---|---|---|
| Tests pass | Test run showing 0 failures | An earlier run, "should pass" |
| Build works | Build exits 0 | Linter passing |
| Bug fixed | Original symptom now gone | Code changed |
| Regression test works | Fails with fix reverted, passes with it restored | Passes once |
| Subagent finished | You checked the diff | The agent said so |
| Requirements met | Line-by-line check against the spec | Tests green |

Words like "should", "probably", "seems to", or an early "Done!" mean you skipped this step.

## 7. Code review

*Sources: superpowers/requesting-code-review, receiving-code-review, ECC code-review*

**Giving review.** Rank findings by severity: correctness and security first, then data loss, then performance, then style. For each finding give file:line, the concrete failure scenario (input X causes wrong output Y), and a fix. Skip taste nitpicks unless asked.

**Receiving review.**
1. Read all the feedback before reacting.
2. Restate each item in your own words, or ask about it.
3. Check each against the actual codebase.
4. If any item is unclear, ask about it *before implementing anything*. Items often depend on each other.
5. Implement in order: blocking (breakage, security), then simple, then complex. Test each one.

No performative agreement ("You're absolutely right!", "Great catch!"). State the technical fix or push back with reasons. Push back when the suggestion breaks existing behavior, ignores context, violates YAGNI (grep for real usage first), or doesn't fit this stack.

## 8. Security checklist

*Source: ECC rules/common/security.md*

Before any commit that touches input, auth, or data:

- [ ] No hardcoded secrets. Use env vars or a secret manager; fail fast at startup if one is missing.
- [ ] All user input validated at the boundary.
- [ ] Parameterized queries only (no string-built SQL).
- [ ] Output escaped or sanitized against XSS.
- [ ] CSRF protection on state-changing requests.
- [ ] Authorization checked on every protected route, not only authentication.
- [ ] Rate limits on public endpoints.
- [ ] Error messages don't leak stack traces, paths, or secrets.

Found a real vulnerability? Stop feature work, fix critical issues first, rotate anything exposed, and search the codebase for the same pattern.

## 9. Frontend and visual design

*Sources: anthropics/frontend-design, taste-skill, hallmark, ui-ux-pro-max*

**Read the room first.** Before code, write one line: *"Reading this as: [page kind] for [audience], with a [vibe] feel, leaning toward [system or aesthetic]."* Ground it in the subject matter: a kids' toy and an analyst dashboard should look nothing alike. If the read could go two very different ways, ask one question. Otherwise declare the read and proceed.

**Respect what exists.** In an existing project, scan for tokens, fonts, framework, and any `design.md` before choosing anything, and reuse them. Name the files you'll change before editing; never delete components or routes without explicit approval. If the brief maps to a real design system (Material, Fluent, Carbon, Primer, GOV.UK, USWDS, Polaris), install the official package instead of hand-copying its CSS. One system per project.

**Plan, then check the plan against the brief.** Draft a compact token plan: 4 to 6 named hex colors, one or two typefaces with roles, a layout concept (ASCII wireframe is fine), and a line on what makes this page unique. Then ask: would I produce this same plan for any similar prompt? If yes, revise that part and say why.

**Avoid the generated-page defaults** unless the brief asks for them:

- Cream background with serif display and terracotta accent; near-black with one acid-green accent.
- Purple-to-blue gradients, centered hero on dark mesh, three equal feature cards.
- Identical rounded cards with the same soft grey shadow on everything.
- ALL-CAPS tracked eyebrow labels over every heading; "A · B · C" meta strings; arrows appended to every button.
- One word in a headline set in italic or a different color.
- Fade-and-slide-up on every section, hover animation on every card.
- 01 / 02 / 03 numbering on content that isn't a sequence.
- Inter plus slate-900 as the whole personality.

**Spend boldness in one place.** One memorable element; everything else quiet. Before shipping, remove one accessory.

**Quality floor, without announcing it:**
- Responsive to phone width, no horizontal scroll.
- Visible keyboard focus; `prefers-reduced-motion` respected; WCAG AA contrast (4.5:1 body text).
- Interactive components ship all states: default, hover, focus-visible, active, disabled, loading, error, success.
- Line length under ~80 characters. Set a real type scale.
- Take a screenshot and critique it if the environment allows.

**Interface copy.** Name things by what users do, not how the system works ("notifications", not "webhook config"). Buttons say what happens ("Save changes", not "Submit"), and the name holds through the flow (a "Publish" button produces a "Published" toast). Errors explain what went wrong and how to fix it, without apologizing. Empty states invite an action. Sentence case, plain verbs.

## 10. Writing prose

*Sources: stop-slop, humanizer*

**Core rules:**
1. Cut throat-clearing openers, emphasis crutches, and adverbs.
2. Active voice. Every sentence needs an actor. No inanimate things doing human verbs ("the data tells us", "the decision emerges").
3. Be specific. Replace "the implications are significant" with the implication.
4. Vary rhythm. Mix short and long sentences. Two items often beat three.
5. Trust the reader. State facts; skip softening and hand-holding.
6. Cut anything that sounds like a pull-quote.

**AI tells to remove:**

| Pattern | Example | Fix |
|---|---|---|
| Not X but Y | "It's not a tool, it's a movement" | State Y |
| Staged run-up | "Here's the thing:", "The truth is:" | Start with the point |
| Dramatic fragment closer | "And that changes everything." | End on content |
| Forced triads | "fast, simple, and powerful" | Keep the one that's true |
| Dash as universal glue | "The result — surprisingly — worked" | Commas, periods, parentheses |
| Inflated significance | "a testament to", "pivotal", "landscape" | Say what happened |
| Shallow -ing tail | "..., highlighting the need for change" | Cut or make it a real sentence |
| Overused AI words | delve, tapestry, crucial, robust, seamless, leverage | Plain word |
| Avoiding "is" | "serves as", "stands as", "boasts" | "is", "has" |
| Bold everywhere | Decorative bold in every paragraph | Bold only what a skimmer must see |
| Chatbot residue | "I hope this helps!", "Great question!" | Delete |
| Knowledge-limit hedges | "As of my last update..." | Check, or state the uncertainty once |

**Score before sending** (1 to 10 each): directness, rhythm, trust in the reader, sounds human, density. Under 35 of 50, revise.

Leave alone: quoted material, legal or technical text where exact wording matters, and a writer's deliberate voice when you're only asked to proofread.

## 11. Marketing copy

*Source: marketingskills/copywriting*

Before writing, pin down: the page type and its **one** primary action; the audience, their problem, their objections, and the words they use for it; what the offer is and how it differs; proof (numbers, testimonials); where traffic comes from and what visitors already know.

- Clarity beats cleverness.
- Benefits over features: say what the feature means for the customer.
- Specific over vague: "cut weekly reporting from 4 hours to 15 minutes", not "save time".
- Mirror customer language from reviews, tickets, and interviews.
- One idea per section, building down the page.
- Simple words ("use", not "utilize"). No buzzwords ("streamline", "innovative"). No exclamation points.
- Never invent statistics or testimonials. Mark placeholders clearly.

## 12. Research

*Sources: last30days, general practice*

- Pin the time window. For "what's new", favor the last 30 days and date every claim.
- Pull from several independent source types (official docs or repos, news, forums like Reddit and HN, social) so one echo chamber can't dominate.
- Cluster findings by theme, rank by evidence strength (how many sources, how credible, how recent), and cite each claim.
- Separate what sources say from your own synthesis. Flag contested or single-source claims.
- Stars, upvotes, and views measure popularity, not correctness. Say which one you're reporting.

## 13. Output modes

*Sources: caveman, i-have-adhd*

These are opt-in. Turn one on when the user asks ("be brief", "caveman mode", "ADHD mode") and keep it for the rest of the session until they say "normal mode".

**Terse mode (caveman).**
- Drop articles, filler ("just", "really", "basically"), pleasantries, and hedging. Fragments are fine.
- Keep code, commands, API names, error strings, and numbers exactly as they are.
- Never drop "not", "never", "no", "only", or "except". Losing one flips the meaning.
- Don't invent abbreviations (cfg, impl, fn) or use arrows. They save no tokens and cost clarity.
- Pattern: `[thing] [action] [reason]. [next step].`
- Switch back to full sentences for security warnings, irreversible actions, and ordered steps that could be misread.
- Code, commits, PRs, docs, and messages to other people stay in normal English.

**Action-first mode (ADHD).**
1. The first line is something the reader can do now: a command, a path, a snippet.
2. Number multi-step work. One bounded action per step. Fewest steps that work.
3. Restate position every turn: "Step 3 of 5 done: schema updated. Next: backfill."
4. Give concrete time estimates ("about 15 minutes if tests exist").
5. Show wins concretely: "Login works with magic links. Try `npm run dev`, open `/login`."
6. Park tangents: finish the current thing, then offer the side issue as a separate question.
7. Show at most five items per group; rank the most relevant first.
8. End with one next action that takes under two minutes.

Break the shape when the user asks for a full explanation, before destructive actions, and after three "still broken" turns (stop coding, name the assumption that might be wrong, ask one diagnostic question).

**Pre-send check (any mode):** delete the first sentence if it only announces what you're about to do, the last sentence if it asks "anything else?" or recaps, and any "by the way" sidebar. If the reader saw only your first and last lines, would they know what happened and what to do next?

## 14. Writing a new skill

*Sources: anthropics/skill-creator, superpowers/writing-skills*

```
skill-name/
├── SKILL.md        # frontmatter (name, description) + instructions
├── references/     # docs loaded only when needed
├── scripts/        # deterministic helpers that run without loading into context
└── assets/         # templates, fonts, icons used in output
```

- **The description triggers the skill.** Put every "when to use" signal in it, including phrases users actually type. Models tend to under-trigger skills, so make the description a little pushy.
- **Progressive disclosure.** Metadata always loads (~100 words); the body loads on trigger (aim under 500 lines); references load on demand. Link each reference from the body with a note on when to read it. Give reference files over 300 lines a table of contents.
- **Explain why.** A rule with its reason generalizes to cases you didn't foresee. Stacks of ALL-CAPS MUSTs don't.
- **Imperative voice**, concrete input and output examples, and exact templates where the output format matters.
- **Test it.** Run the same prompts with and without the skill and compare. Watch for the rationalizations the model uses to skip a rule, then add those to a red-flag table.
- **No surprises.** A skill should do what its description says and nothing hidden.

---

## Red flags, all in one place

If you catch yourself thinking any of these, stop and go to the named section.

| Thought | Reality | Section |
|---|---|---|
| "Too simple to need a design" | Small changes still get a short design and a yes | 1 |
| "I'll call it bounded and skip the spec" | Reaching for the lighter label is the doubt. Go heavier. | 1 |
| "I'll add a config option in case" | Nobody asked. Cut it. | 3 |
| "While I'm here I'll tidy this" | Unrequested diff. Mention it instead. | 3 |
| "I'll write the test after" | Tests written after prove nothing | 4 |
| "Let me just try changing X" | Guessing. Find the root cause. | 5 |
| "One more fix" (after two failed) | Third failure means question the architecture | 5 |
| "Should work now" | Run it | 6 |
| "The agent said it succeeded" | Check the diff | 6 |
| "You're absolutely right!" | Verify first, then state the fix | 7 |
| "Purple gradient hero, three cards" | Generated default. Revisit the design read. | 9 |
| "It's a testament to..." | Inflated. Say what happened. | 10 |
| "Hope this helps!" | Delete | 10, 13 |
