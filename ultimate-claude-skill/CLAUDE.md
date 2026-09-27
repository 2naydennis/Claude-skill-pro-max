# CLAUDE.md

Instructions for Claude Code when working in this repository.

## What this repo is

Ultimate is a Claude Agent Skill that condenses fourteen of the most-starred Claude skill repos into one, packaged as a Claude Code plugin. The skill lives in `skills/ultimate/`. Everything else supports it: plugin manifests, tests, a validator, evals, sources, and generated documentation.

## Layout

| Path | Purpose |
|---|---|
| `skills/ultimate/SKILL.md` | The skill: frontmatter, core loop, iron laws, routing table, output modes, red flags, templates list |
| `skills/ultimate/references/*.md` | Topic guides, loaded on demand. One per area |
| `skills/ultimate/assets/templates/*.md` | Fill-in templates the skill offers to users |
| `skills/ultimate/scripts/ultikit.py` | Prose checker, design checker, planning scaffolder. Standard library only, Python 3.9+ |
| `.claude-plugin/plugin.json`, `marketplace.json` | Claude Code plugin install |
| `SOURCES.md` | Upstream repos, star counts, licenses |
| `tests/test_ultikit.py`, `tests/fixtures/` | Tests for every ultikit command |
| `tools/validate_skill.py` | Checks frontmatter, file references, reference structure, and manifests |
| `tools/build_docs.py` | Regenerates `docs/` from the skill files |
| `docs/` | Generated. Never edit by hand |
| `evals/evals.json` | Behavior test prompts with expected answers |

## Commands

```bash
python3 -m unittest discover tests          # run ultikit tests
python3 tools/validate_skill.py             # validate skill + manifests (uses PyYAML if installed)
python3 tools/build_docs.py --pdf           # rebuild docs/ (PDF needs Chrome or Chromium)
python3 skills/ultimate/scripts/ultikit.py <command> -h
```

Run the tests and the validator after every change. Rebuild the docs after any change inside `skills/`, to `README.md`, or to `SOURCES.md`.

## Rules for SKILL.md

- Frontmatter keys: `name`, `description`, `license`, `metadata` only.
- `name` must be `ultimate`: lowercase, matches the folder name, and never contains "claude" or "anthropic" (claude.ai rejects those uploads).
- `description` stays under 1024 characters, has no angle brackets, and has no `": "` (colon followed by a space). A colon-space breaks YAML parsing and the skill will fail to load.
- Keep the body under 500 lines. Put detail in `references/` and add it to the routing table in section 1.
- Every `references/`, `assets/`, or `scripts/` path mentioned in backticks must exist. The validator checks this.

## Rules for content

- **Credit the source.** Each reference names the upstream repos it draws from. New material from a new repo goes in `SOURCES.md` with its star count and license.
- **Paraphrase, don't paste.** Condense upstream skills in your own words. Short phrases are fine; whole sections are not.
- Each reference starts with a title, a one-line summary, and a `## Contents` list matching its `##` headings, and ends with `## Common mistakes`. The validator checks all three.
- Explain why a rule exists. Rules with reasons generalize.
- Plain language, short sections, active voice, no em dashes in prose. Run `ultikit.py slop` on new prose.

## Adding an ultikit command

1. Add a `cmd_<name>(a)` function in `ultikit.py` that prints what it found and why, then register a subparser in `main()`.
2. Standard library only. Validate inputs and exit with `die("...")` on bad input.
3. Add tests in `tests/test_ultikit.py`, with fixtures in `tests/fixtures/`.
4. List the command in the module docstring, in section 4 of `SKILL.md`, and in the README table.

## Releasing

1. Bump the version in `skills/ultimate/SKILL.md` (`metadata.version`), `.claude-plugin/plugin.json`, and `.claude-plugin/marketplace.json`.
2. Add an entry to `CHANGELOG.md`.
3. Run tests, the validator, and `tools/build_docs.py --pdf`.
4. Build the upload zip for GitHub Releases (zips are gitignored, never commit them):
   ```bash
   cd skills && zip -r ../ultimate.zip ultimate -x '*/__pycache__/*' '*.DS_Store'
   ```

## Don't

- Don't commit `*.zip`, `__pycache__/`, or `.DS_Store`.
- Don't add third-party dependencies to `ultikit.py`.
- Don't hand-edit files in `docs/`.
- Don't rename the skill folder without updating `name`, the validator, and both manifests.
