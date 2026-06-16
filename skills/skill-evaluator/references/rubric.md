# Skill Evaluation Rubric v1.0

Derived from analysis of the 9 most-starred Claude Code skill repositories (June 2026).

**Source repos:** obra/superpowers (228k★), affaan-m/ECC (216k★), multica-ai/andrej-karpathy-skills (176k★), anthropics/skills (151k★), nextlevelbuilder/ui-ux-pro-max-skill (92k★), thedotmack/claude-mem (82k★), JuliusBrussee/caveman (73k★), OthmanAdi/planning-with-files (23k★), NeoLabHQ/context-engineering-kit

---

## Dimension 1 — Trigger Clarity (20 pts)

**What it measures:** Does the `description` field tell the model *when* to invoke this skill, not just *what* it does?

| Score | Criteria |
|-------|----------|
| 18–20 | Enumerates 4+ specific trigger conditions or user phrases. Leaves no ambiguity about when NOT to use it. |
| 13–17 | Describes 2–3 trigger conditions. May be slightly vague on edge cases. |
| 7–12 | Description explains what the skill does but not when. Could confuse the model into over- or under-triggering. |
| 0–6 | One-line generic summary. No trigger conditions. Model must guess. |

**Examples:**
- Elite: `"Use when the user asks to evaluate, score, review, rate, or improve a skill — or when they share a SKILL.md and want feedback"` ✓
- Poor: `"A skill for reviewing skills"` ✗

---

## Dimension 2 — Instruction Specificity (15 pts)

**What it measures:** Does the body give the model a concrete decision tree or procedure to follow, not just a description of what output to produce?

| Score | Criteria |
|-------|----------|
| 13–15 | Step-by-step procedure with explicit branching (if X then Y). Model cannot misinterpret. Includes what to do when inputs are missing or ambiguous. |
| 9–12 | Clear steps but missing edge case handling or branching. |
| 5–8 | Describes desired output but not the process to get there. Model must fill in the gaps. |
| 0–4 | Vague prose. "Help the user do X." |

**What to look for:** Numbered steps, conditional logic, explicit fallback behavior.

---

## Dimension 3 — Reference Density (15 pts)

**What it measures:** Is there bundled reference material (data, examples, templates, scripts) that the model can use directly — not just instructions?

| Score | Criteria |
|-------|----------|
| 13–15 | Rich reference data: enumerable lists, code templates, lookup tables, or scripts. Quantified claims ("67 styles", "161 palettes"). |
| 9–12 | Some examples or a reference file, but thin. |
| 5–8 | A few inline examples only. No separate reference files. |
| 0–4 | Pure instructions with no supporting data. Model must rely on training knowledge. |

**What to look for:** `references/` folder, `scripts/` folder, embedded data tables, code snippets with real values.

---

## Dimension 4 — Verifiability (15 pts)

**What it measures:** Can success be verified? Does the skill define what "done" looks like, or better yet, include evals/benchmarks?

| Score | Criteria |
|-------|----------|
| 13–15 | Includes evals, benchmarks, or CI-committed snapshots. Output format is fully specified with examples. |
| 9–12 | Specifies the exact output format or success criteria. No evals but clear definition of done. |
| 5–8 | Rough description of expected output. Leaves ambiguity. |
| 0–4 | No output spec. "Good results" is the only criterion. |

**What to look for:** Defined output templates, `evals/` folder, test prompts, success/failure examples.

---

## Dimension 5 — Tradeoff Transparency (10 pts)

**What it measures:** Does the skill honestly state its limitations, biases, or when NOT to use it?

| Score | Criteria |
|-------|----------|
| 9–10 | Explicit tradeoff statement. States what the skill sacrifices and for what. Names scenarios where it should not be used. |
| 6–8 | Mentions limitations briefly. |
| 3–5 | Implies limitations but doesn't state them. |
| 0–2 | Claims universal applicability. No caveats. |

**Example of elite pattern (karpathy-guidelines):**
> `Tradeoff: These guidelines bias toward caution over speed. For trivial tasks, use judgment.`

---

## Dimension 6 — Portability (15 pts)

**What it measures:** Can anyone install and use this without project-specific context? Does it work across multiple agent harnesses?

| Score | Criteria |
|-------|----------|
| 13–15 | Zero-dependency OR all dependencies auto-install. Works on Claude Code + at least 2 other harnesses. No hardcoded paths or user-specific assumptions. |
| 9–12 | Works on Claude Code. Minor assumptions about environment. |
| 5–8 | Requires manual setup. May reference project-specific paths or tools. |
| 0–4 | Only works in one specific setup. Hardcoded paths, project names, or internal tooling. |

---

## Dimension 7 — Maintenance Maturity (10 pts)

**What it measures:** Does the repository show signs of being maintained and trustworthy over time?

| Score | Criteria |
|-------|----------|
| 9–10 | License, version, CHANGELOG, CONTRIBUTING, and author contact all present. |
| 6–8 | License + version present. Missing 1–2 of the others. |
| 3–5 | Only a README. No version, no license. |
| 0–2 | No metadata at all. |

---

## Calibration Reference

These scores are based on manual analysis of the source repos:

| Skill | Estimated Score | Key Strengths | Key Weaknesses |
|-------|----------------|---------------|----------------|
| karpathy-guidelines | ~78/100 | Tradeoff transparency, instruction specificity | No evals, thin reference data |
| anthropics/skills pdf | ~82/100 | Reference density (full code examples), verifiability | Limited multi-harness |
| anthropics/skills skill-creator | ~88/100 | Eval loop, output format, full procedure | Complex, high token cost |
| JuliusBrussee/caveman | ~85/100 | Real LLM benchmarks, control arm testing | Very narrow use case |
| nextlevelbuilder/ui-ux-pro-max | ~80/100 | Quantified data, multi-platform install | Less instruction specificity |
| OthmanAdi/planning-with-files | ~76/100 | i18n, multi-harness, maintenance maturity | Reference density thin |
