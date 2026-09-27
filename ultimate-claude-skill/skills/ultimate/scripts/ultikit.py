#!/usr/bin/env python3
"""ultikit: checkers and scaffolding for the ultimate skill.

Standard library only, Python 3.9+. Every command prints what it found and why.

Commands:
  slop FILE      scan prose for AI writing patterns and score it out of 50
  design FILE    scan HTML/CSS for generated-page defaults and missing quality-floor rules
  plan DIR       create task_plan.md, findings.md, progress.md for long tasks

Examples:
  python3 ultikit.py slop draft.md
  python3 ultikit.py design index.html
  python3 ultikit.py plan . --goal "Add CSV export to the reports page"
"""
import argparse
import re
import statistics
import sys
from datetime import date
from pathlib import Path

TEMPLATES = Path(__file__).resolve().parent.parent / "assets" / "templates"


def die(msg: str) -> None:
    sys.exit(f"error: {msg}")


def read(path: str) -> str:
    p = Path(path)
    if not p.is_file():
        die(f"no such file: {path}")
    return p.read_text(encoding="utf-8", errors="replace")


# ------------------------------------------------------------------ slop

AI_WORDS = [
    "delve", "tapestry", "testament", "pivotal", "crucial", "robust", "seamless", "seamlessly",
    "leverage", "leveraging", "landscape", "realm", "multifaceted", "intricate", "furthermore",
    "moreover", "unleash", "unlock", "elevate", "embark", "navigate the", "game-changer",
    "cutting-edge", "ever-evolving", "in today's", "vibrant", "bustling", "showcasing",
    "underscore", "underscores", "foster", "fostering", "holistic", "synergy", "paradigm",
]
OPENERS = [
    r"here'?s the thing", r"the truth is", r"let'?s dive in", r"let'?s be honest",
    r"in this (article|post|essay|guide)", r"it'?s worth noting", r"it is important to note",
    r"great question", r"certainly!", r"absolutely!", r"sure!", r"i hope this helps",
    r"let me know if", r"feel free to", r"happy to help", r"as of my last",
    r"in conclusion", r"at the end of the day", r"when it comes to",
]
PATTERNS = [
    ("not X but Y", r"\b(it'?s|is|was|isn'?t|wasn'?t) not (just |only |merely )?\w+[^.]{0,40}?[,;:]? (it'?s|but)\b"),
    ("not X but Y", r"\bnot (just|only|merely) [^.]{1,40}, but\b"),
    ("serves as / stands as", r"\b(serves|stands|acts) as (a|an|the)\b"),
    ("shallow -ing tail", r", (highlighting|underscoring|showcasing|emphasizing|reflecting|demonstrating|ensuring) "),
    ("staged run-up", r"\b(here'?s (what|why|how)|the (answer|reason|secret) is simple)\b"),
    ("knowledge-limit hedge", r"\b(as of my (last|knowledge)|i (don'?t|do not) have access to real-time)\b"),
]
PASSIVE = re.compile(r"\b(is|are|was|were|be|been|being)\s+(\w+ly\s+)?(\w+ed|built|made|done|given|shown|taken|written|known|seen)\b", re.I)
ADVERB_OK = {"only", "early", "family", "apply", "reply", "supply", "fly", "july", "italy", "rely", "ally",
             "belly", "holy", "daily", "likely", "friendly", "monthly", "weekly", "yearly", "costly", "ugly"}


def sentences(text: str) -> list:
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"`[^`]*`", " ", text)
    text = re.sub(r"^\s*(#+|[-*]|\d+\.|\|).*$", " ", text, flags=re.M)
    parts = re.split(r"(?<=[.!?])\s+", text)
    return [s.strip() for s in parts if len(s.split()) >= 3]


def cmd_slop(a) -> None:
    text = read(a.file)
    lines = text.splitlines()
    hits = []  # (line_no, kind, snippet)

    in_code = False
    for n, line in enumerate(lines, 1):
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        low = line.lower()
        for m in re.finditer("—| -- ", line):
            hits.append((n, "em dash", line[max(0, m.start() - 25):m.end() + 25].strip()))
        for w in AI_WORDS:
            m = re.search(rf"\b{re.escape(w)}\b", low)
            if m:
                hits.append((n, f"AI word '{w}'", line[max(0, m.start() - 20):m.end() + 20].strip()))
        for o in OPENERS:
            m = re.search(o, low)
            if m:
                hits.append((n, "filler / chatbot residue", m.group(0)))
        for kind, pat in PATTERNS:
            m = re.search(pat, low)
            if m:
                hits.append((n, kind, m.group(0)))
        for m in PASSIVE.finditer(line):
            hits.append((n, "passive voice?", m.group(0)))
        for m in re.finditer(r"\b(\w{3,}ly)\b", low):
            if m.group(1) not in ADVERB_OK:
                hits.append((n, f"adverb '{m.group(1)}'", line[max(0, m.start() - 20):m.end() + 20].strip()))
        if len(re.findall(r"\*\*[^*]+\*\*", line)) >= 3:
            hits.append((n, "bold used as decoration", line.strip()[:70]))
        for m in re.finditer(r"\b\w+, \w+,? and \w+\b", line):
            hits.append((n, "triad (check it's not forced)", m.group(0)))

    sents = sentences(text)
    lengths = [len(s.split()) for s in sents]
    words = sum(lengths) or 1
    spread = statistics.pstdev(lengths) if len(lengths) > 1 else 0.0
    runs = sum(1 for i in range(len(lengths) - 2)
               if max(lengths[i:i + 3]) - min(lengths[i:i + 3]) <= 2)

    by_kind = {}
    for _, kind, _ in hits:
        key = kind.split("'")[0].strip()
        by_kind[key] = by_kind.get(key, 0) + 1

    def per100(keys):
        return 100 * sum(by_kind.get(k, 0) for k in keys) / words

    directness = 10 - min(10, round(per100(["filler / chatbot residue", "staged run-up", "not X but Y"]) * 8))
    rhythm = 10 - min(10, round(max(0, 6 - spread)) + runs)
    trust = 10 - min(10, round(per100(["adverb", "knowledge-limit hedge"]) * 3))
    human = 10 - min(10, round(per100(["AI word", "em dash", "serves as / stands as", "shallow -ing tail"]) * 6))
    density = 10 - min(10, round(per100(["passive voice?", "bold used as decoration", "triad (check it"]) * 3))
    scores = {"directness": directness, "rhythm": rhythm, "trust": trust, "sounds human": human, "density": density}
    total = sum(scores.values())

    print(f"slop check: {a.file}")
    print(f"  words {words}, sentences {len(lengths)}, sentence length mean "
          f"{statistics.mean(lengths) if lengths else 0:.1f}, spread (stdev) {spread:.1f}")
    print(f"  runs of 3 same-length sentences: {runs}")
    print()
    if hits:
        print("  line  issue                          text")
        for n, kind, snip in hits[: a.limit]:
            print(f"  {n:>4}  {kind[:30]:<30} {snip}")
        if len(hits) > a.limit:
            print(f"  ... {len(hits) - a.limit} more (use --limit)")
    else:
        print("  no pattern hits")
    print()
    for k, v in scores.items():
        print(f"  {k:<13} {v:>2}/10")
    verdict = "ok" if total >= 35 else "revise (under 35/50)"
    print(f"  total         {total}/50  {verdict}")
    print("\n  Heuristic only. 'passive voice?' and 'triad' are flags to read, not automatic errors.")


# ------------------------------------------------------------------ design

DESIGN_TELLS = [
    ("Inter as the only typeface", r"font-family:\s*['\"]?inter['\"]?\s*[,;]", "Pick a typeface for this brief."),
    ("AI purple/indigo gradient", r"gradient\([^)]*#(8b5cf6|7c3aed|6366f1|a855f7|9333ea|4f46e5)", "Reach past the default gradient."),
    ("generic soft card shadow", r"box-shadow:[^;]*rgba\(0,\s*0,\s*0,\s*0?\.1\)", "Vary depth by hierarchy, or drop it."),
    ("cream + terracotta default", r"#(f4f1ea|d97757)", "Common generated palette. Choose on purpose."),
    ("tracked all-caps eyebrow", r"text-transform:\s*uppercase[^}]*letter-spacing|letter-spacing[^}]*text-transform:\s*uppercase", "Eyebrow labels above every heading read as template chrome."),
    ("arrow glued to link/button text", r">[^<]{1,40}(→|&rarr;)\s*<", "Drop the reflexive arrow."),
    ("tinted near-black for black", r"#(0b0b0b|111111|111)\b", "Use the palette's real ink colour."),
]
FLOOR = [
    ("visible keyboard focus", r":focus-visible"),
    ("reduced-motion respected", r"prefers-reduced-motion"),
    ("responsive rule", r"@media[^{]*(max|min)-width|clamp\(|minmax\("),
    ("viewport meta", r"<meta[^>]+name=['\"]viewport"),
]


def cmd_design(a) -> None:
    text = read(a.file)
    low = text.lower()
    print(f"design check: {a.file}")
    print("\n  Generated-page defaults found:")
    found = 0
    for name, pat, hint in DESIGN_TELLS:
        n = len(re.findall(pat, low, flags=re.S))
        if n:
            found += 1
            print(f"    - {name} (x{n}): {hint}")
    if not found:
        print("    none")
    animated = len(re.findall(r"(animation|transition)\s*:", low))
    if animated > 8:
        print(f"    - {animated} animation/transition rules: motion everywhere reads as generated. Keep one orchestrated moment.")
    print("\n  Quality floor:")
    missing = 0
    is_html = a.file.lower().endswith((".html", ".htm"))
    for name, pat in FLOOR:
        if name == "viewport meta" and not is_html:
            continue
        ok = re.search(pat, low, flags=re.S) is not None
        missing += not ok
        print(f"    [{'x' if ok else ' '}] {name}")
    states = [s for s in ("hover", "focus-visible", "active", "disabled") if f":{s}" in low]
    print(f"    interactive states styled: {', '.join(states) or 'none'} "
          "(components also need loading, error, success)")
    print(f"\n  {found} default(s), {missing} floor item(s) missing.")


# ------------------------------------------------------------------ plan

def cmd_plan(a) -> None:
    out = Path(a.dir)
    out.mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()
    for name in ("task_plan.md", "findings.md", "progress.md"):
        target = out / name
        if target.exists() and not a.force:
            print(f"  kept     {target} (exists; --force to overwrite)")
            continue
        body = (TEMPLATES / name).read_text(encoding="utf-8")
        body = body.replace("{{GOAL}}", a.goal or "(state the goal in one sentence)").replace("{{DATE}}", today)
        target.write_text(body, encoding="utf-8")
        print(f"  created  {target}")
    print("\n  Re-read task_plan.md before each major decision. Update all three after every phase.")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("slop", help="scan prose for AI writing patterns")
    s.add_argument("file")
    s.add_argument("--limit", type=int, default=40, help="max issues to list (default 40)")
    s.set_defaults(func=cmd_slop)
    d = sub.add_parser("design", help="scan HTML/CSS for generated defaults and quality-floor gaps")
    d.add_argument("file")
    d.set_defaults(func=cmd_design)
    p = sub.add_parser("plan", help="create planning files for a long task")
    p.add_argument("dir")
    p.add_argument("--goal", default="")
    p.add_argument("--force", action="store_true", help="overwrite existing files")
    p.set_defaults(func=cmd_plan)
    a = ap.parse_args()
    a.func(a)


if __name__ == "__main__":
    main()
