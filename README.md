# Ultimate

A [Claude skill](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview) that combines the most popular Claude skills on GitHub into one.

There are thousands of skills out there, and the popular ones overlap. superpowers teaches test-first coding and root-cause debugging. Karpathy's guidelines stop Claude from overbuilding. stop-slop and humanizer strip AI tells from prose. taste-skill and hallmark stop every landing page from looking the same. Installing all fourteen means fourteen descriptions competing for attention and rules that repeat or contradict each other. Ultimate reads them all, keeps the rules that matter most, and puts them in one skill with one routing table, so Claude loads only the part a task needs.

## What it does

| Feature | What happens |
|---|---|
| **Thinks before coding** | States assumptions, classifies the request as spike, bounded, or architectural, and waits for your approval before building |
| **Keeps changes small** | Minimum code for the request, no speculative options, no tidying code you didn't ask about |
| **Test-first** | Writes a failing test, watches it fail, writes the simplest code that passes, runs the whole suite |
| **Root-cause debugging** | Four phases: investigate, compare, hypothesize, fix. After three failed fixes it stops and questions the design |
| **Evidence before "done"** | Runs the command that proves a claim and shows the output instead of saying "should work" |
| **Honest code review** | Findings ranked by severity with file, line, and failure scenario. No "You're absolutely right!" when receiving review |
| **Security checklist** | Secrets, input validation, SQL injection, XSS, CSRF, authorization, rate limits, leaky errors |
| **Distinctive design** | A one-line design read, a token plan checked against the brief, a list of generated-page defaults to avoid, and a quality floor (mobile, focus, reduced motion, contrast, all 8 states) |
| **Human-sounding writing** | 25 AI writing patterns to remove, a 50-point score, and marketing-copy rules |
| **Research with sources** | Several source types, dated claims, deduped sources, and a clear line between popularity and quality |
| **Output modes** | Opt-in terse mode (caveman) and action-first mode (ADHD-friendly) that last the whole session |
| **Skill writing** | How to write, structure, and test your own skills |

## Install

### Claude.ai or the Claude desktop app

1. Build the upload zip:
   ```bash
   cd skills && zip -r ../ultimate.zip ultimate -x '*/__pycache__/*' '*.DS_Store'
   ```
2. In Claude, open **Settings** and find **Skills** (under Capabilities or Customize, depending on your app version). Code execution needs to be turned on for skills to work.
3. Click **Upload skill** and choose `ultimate.zip`.
4. Make sure the skill is toggled on.

### Claude Code (as a plugin)

```bash
/plugin marketplace add diederichtd/ultimate-claude-skill
```

```bash
/plugin install ultimate@ultimate
```

### Claude Code (manual copy)

```bash
mkdir -p ~/.claude/skills && cp -r skills/ultimate ~/.claude/skills/
```

For one project only, copy it to `.claude/skills/` inside that project instead.

## How to use it

Work the way you normally do. The skill turns on by itself when you ask Claude to build, fix, debug, plan, design, write, review, or research. Some examples:

- "Add a `--dry-run` flag to the deploy script."
- "This test fails with `KeyError: 'user_id'`. Fix it."
- "Review this PR before I merge."
- "Make a landing page for my pottery studio."
- "Edit this paragraph so it doesn't sound like AI wrote it."
- "What's new with Bun in the last month?"
- "caveman mode" or "I have ADHD, keep answers actionable."

Tips:

- For small changes, Claude presents a two-sentence design and waits. Say "yes" or correct it.
- Say "you pick" on design questions and Claude will state what it assumed so you can redirect.
- Say "normal mode" to turn off an output mode.

## How it works

A skill is a folder with a `SKILL.md` file that Claude reads when a task matches the skill's description. Claude loads only the short description at first, then the full instructions when the skill triggers, and each reference file only when a task needs it. A debugging session never loads the design rules.

```
ultimate-claude-skill/
├── CLAUDE.md                    # instructions for Claude Code when working on this repo
├── SOURCES.md                   # the 14 upstream repos, star counts, licenses
├── .claude-plugin/
│   ├── plugin.json              # Claude Code plugin manifest
│   └── marketplace.json         # lets people install with /plugin
├── skills/
│   └── ultimate/                # the skill itself (this is what you zip)
│       ├── SKILL.md             # core loop, iron laws, routing table, red flags
│       ├── references/          # loaded only when needed
│       │   ├── process.md
│       │   ├── coding.md
│       │   ├── debugging.md
│       │   ├── verification-and-review.md
│       │   ├── security.md
│       │   ├── design.md
│       │   ├── writing.md
│       │   ├── research.md
│       │   ├── output-modes.md
│       │   └── skill-authoring.md
│       ├── assets/templates/    # task plan, findings, progress, spec, implementation plan, debug log, review checklist, design brief
│       └── scripts/
│           └── ultikit.py       # prose checker, design checker, planning-file scaffolder
├── docs/                        # the whole skill as one document (Markdown, HTML, PDF)
├── evals/evals.json             # test prompts for checking skill behavior
├── tests/                       # tests for ultikit.py
├── tools/
│   ├── validate_skill.py        # checks SKILL.md, references, and manifests
│   └── build_docs.py            # rebuilds the docs/ document
└── .github/workflows/validate.yml
```

### The kit

`ultikit.py` works with Python 3.9 or newer and needs no extra packages.

```bash
python3 skills/ultimate/scripts/ultikit.py slop tests/fixtures/sloppy.md
```

```
  line  issue                          text
     1  filler / chatbot residue       let's dive in
     1  filler / chatbot residue       great question
     3  AI word 'testament'            is tool serves as a testament to innovation. It's
     3  not X but Y                    it's not just a product, it's
     3  shallow -ing tail              , highlighting
     3  passive voice?                 were reviewed
     ...
  directness     0/10
  rhythm        10/10
  trust          3/10
  sounds human   0/10
  density        0/10
  total         13/50  revise (under 35/50)
```

```bash
python3 skills/ultimate/scripts/ultikit.py design tests/fixtures/generic.html
```

```
  Generated-page defaults found:
    - Inter as the only typeface (x1): Pick a typeface for this brief.
    - AI purple/indigo gradient (x1): Reach past the default gradient.
    - generic soft card shadow (x1): Vary depth by hierarchy, or drop it.
    ...
  Quality floor:
    [ ] visible keyboard focus
    [ ] reduced-motion respected
  6 default(s), 4 floor item(s) missing.
```

| Command | What it does |
|---|---|
| `slop FILE` | Flags AI writing patterns by line and scores the text out of 50 |
| `design FILE` | Flags generated-page defaults in HTML/CSS and checks the accessibility and responsiveness floor |
| `plan DIR --goal "..."` | Creates `task_plan.md`, `findings.md`, and `progress.md` for a long task |

Run `python3 skills/ultimate/scripts/ultikit.py <command> -h` for options.

## Where it comes from

Ranked by GitHub stars on 2026-09-27 (GitHub publishes no download counts for repos). Full table with licenses in [SOURCES.md](SOURCES.md).

| Repo | Stars | Went into |
|---|---|---|
| [obra/superpowers](https://github.com/obra/superpowers) | 292k | process, coding, debugging, verification and review, skill writing |
| [affaan-m/ECC](https://github.com/affaan-m/ECC) | 268k | coding, review, security |
| [multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills) | 215k | process, coding |
| [anthropics/skills](https://github.com/anthropics/skills) | 179k | design, skill writing |
| [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | 131k | design |
| [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman) | 108k | output modes |
| [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) | 90k | design |
| [mvanhorn/last30days-skill](https://github.com/mvanhorn/last30days-skill) | 63k | research |
| [blader/humanizer](https://github.com/blader/humanizer) | 52k | writing |
| [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) | 52k | writing |
| [ayghri/i-have-adhd](https://github.com/ayghri/i-have-adhd) | 51k | output modes |
| [Nutlope/hallmark](https://github.com/Nutlope/hallmark) | 29k | design |
| [OthmanAdi/planning-with-files](https://github.com/OthmanAdi/planning-with-files) | 27k | process |
| [hardikpandya/stop-slop](https://github.com/hardikpandya/stop-slop) | 18k | writing |

Ultimate paraphrases and condenses these. It doesn't copy them wholesale, and it leaves out their scripts, hooks, and large reference libraries. Install an original when you want its full depth.

## Full documentation

Everything in the skill, combined into one document with a contents page: the method, all ten reference guides, the templates, the sources, and the kit's source code.

- [docs/Ultimate.pdf](docs/Ultimate.pdf) to read or print
- [docs/Ultimate.md](docs/Ultimate.md) as a single Markdown file

## Development

Run the tests and the validator before opening a pull request:

```bash
python3 -m unittest discover tests
```

```bash
pip install pyyaml && python3 tools/validate_skill.py
```

GitHub Actions runs both on every push and pull request.

After editing the skill, rebuild the combined document:

```bash
python3 tools/build_docs.py --pdf
```

To check how the skill behaves, try the prompts in `evals/evals.json` with the skill on and off and compare the answers.

## Contributing

Contributions are welcome: rules Claude still breaks, better references, new checks for `ultikit.py`, or fixes. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Limitations

- Claude can still make mistakes. The skill makes it show evidence so you can check.
- The slop and design checks are heuristics. They flag patterns to read, not errors to fix blindly.
- The approval gates slow down tiny tasks on purpose. Tell Claude to skip them if you don't want them for a given task.
- It condenses fourteen skills into one. Some depth from each original is lost.

## License

[MIT](LICENSE). Upstream licenses are listed in [SOURCES.md](SOURCES.md).
