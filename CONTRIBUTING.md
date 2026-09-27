# Contributing to Ultimate

Thanks for helping make Claude better at everyday work.

## Good contributions

- A rule Claude still breaks that the red-flag table in `SKILL.md` should cover
- Better reference material in `skills/ultimate/references/`
- A popular skill repo worth folding in, with its star count and license for `SOURCES.md`
- New checks in `scripts/ultikit.py`, each with a test
- New templates in `skills/ultimate/assets/templates/`
- Fixes to wrong or outdated advice

## Guidelines

- **Keep `SKILL.md` short** (under 500 lines). Put detail in `references/` and link to it from the routing table in section 1 of `SKILL.md`.
- **Explain why.** Instructions that give reasons work better than bare rules.
- **Credit and paraphrase.** Name the upstream repo for any rule you add, and write it in your own words.
- **Test every check.** A new `ultikit.py` check needs a test and a fixture that triggers it, plus a clean fixture that doesn't.
- **Match the style:** plain language, short sections, a contents list at the top of each reference file, and a "Common mistakes" section at the end.

## Before opening a pull request

```bash
python3 -m unittest discover tests
```

```bash
pip install pyyaml && python3 tools/validate_skill.py
```

Rebuild the docs with `python3 tools/build_docs.py --pdf` so `docs/` matches the skill.

If you changed how the skill behaves, try a few prompts from `evals/evals.json` and describe the before and after in your pull request.
