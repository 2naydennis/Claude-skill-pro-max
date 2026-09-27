# Writing skills

How to write a Claude skill that triggers when it should and changes behavior when it does. Distilled from anthropics/skills (skill-creator) and superpowers (writing-skills).

## Contents

- Anatomy
- Frontmatter
- Progressive disclosure
- Writing the body
- Testing a skill
- Packaging
- Common mistakes

## Anatomy

```
skill-name/
├── SKILL.md        # required: frontmatter + instructions
├── references/     # docs loaded only when needed
├── scripts/        # deterministic helpers; run without loading into context
└── assets/         # templates, fonts, icons used in output
```

## Frontmatter

- `name`: lowercase letters, digits, and hyphens; 64 characters max; matches the folder name. Names containing "claude" or "anthropic" are rejected by claude.ai uploads.
- `description`: the trigger. Under 1024 characters, no angle brackets. Say what the skill does **and** every context it should fire in, including phrases users actually type. Models tend to under-trigger skills, so be a little pushy: "Use whenever the user mentions X, Y, or Z, even if they don't ask for a skill."
- Avoid a colon followed by a space inside an unquoted description. It breaks YAML parsing and the skill won't load.

## Progressive disclosure

Three loading levels:

1. **Metadata** (name + description): always in context, ~100 words.
2. **SKILL.md body:** loaded when the skill triggers. Aim for under 500 lines.
3. **Bundled files:** loaded or run only when needed. No size limit; scripts don't enter context at all.

Keep SKILL.md as a router: method, a table pointing to references, and the rules that apply every time. Put detail in references. Link each reference from the body with a note on when to read it. Give any reference over 300 lines a table of contents. For multi-framework skills, one reference per variant (`aws.md`, `gcp.md`) so only one loads.

## Writing the body

- **Imperative voice.** "Run the tests", not "tests should be run".
- **Explain why.** A rule with its reason generalizes to cases you didn't foresee. A wall of ALL-CAPS MUSTs doesn't.
- **Concrete examples** of input and output. Show good and bad side by side.
- **Exact templates** where output format matters.
- **Red-flag tables** for discipline skills: the rationalization the model uses to skip a rule, next to why it's wrong.
- **Deterministic work goes in scripts.** Math, parsing, file generation: code does it exactly and saves tokens.
- **No surprises.** The skill does what its description says. Nothing hidden, nothing malicious.

## Testing a skill

1. Write 5 to 10 realistic prompts, including edge cases and near-misses that should *not* trigger it.
2. Run each with and without the skill.
3. Compare outputs against expected behavior. Grade what you can objectively.
4. Watch how the model skips or bends rules. Add those rationalizations to a red-flag table.
5. Test the description separately: does it trigger on the prompts it should and stay quiet on the others?
6. Iterate. Keep the evals in the repo (`evals/evals.json`).

## Packaging

- Claude Code: copy the skill folder into `~/.claude/skills/` (all projects) or `.claude/skills/` (one project), or ship it as a plugin with `.claude-plugin/plugin.json` and `marketplace.json`.
- Claude.ai and desktop: zip the skill folder itself (not its parent) and upload it under Settings, Skills. Code execution must be on.

## Common mistakes

- A description that says what the skill is but not when to use it.
- A 1,500-line SKILL.md that loads everything on every trigger.
- References never linked from SKILL.md, so they never get read.
- Rules without reasons that the model rationalizes around.
- Doing arithmetic in prose instead of a script.
- Zipping the parent folder so SKILL.md isn't at the top level.
