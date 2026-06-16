---
name: skill-evaluator
description: Score a Claude Code skill against a research-backed rubric derived from the top 9 most-starred skill repos on GitHub (obra/superpowers 228k★, affaan-m/ECC 216k★, anthropics/skills 151k★, and more). Use when a user asks to evaluate, score, review, rate, or improve a skill — or when they share a SKILL.md and want to know how good it is. Do NOT use for CLAUDE.md, .cursorrules, or system prompt files — these are not packaged skills; note the file type in the output and score what you can.
license: MIT
platforms:
  - claude-code
  - codex
  - cursor
  - opencode
  - gemini-cli
  - kiro
---

# Skill Evaluator

Score any Claude Code skill against a rubric reverse-engineered from the most-starred skill repositories on GitHub.

**Tradeoff:** This rubric rewards general-purpose, widely distributable skills. Domain-specific or internal-tooling skills will score lower on portability — that's by design, not a flaw.

---

## How to Run

1. Determine the input. Check for:
   - A skill name the user mentions (e.g. "evaluate my karpathy-guidelines skill") → locate the file at `~/.claude/skills/{name}/SKILL.md` and Read it
   - A file path in the user's message → Read the file
   - A GitHub URL → Fetch the raw content
   - Pasted SKILL.md content directly in the chat → Use as-is
   - **No input provided** → Ask: "Please share the skill name, a file path, a GitHub URL, or paste the skill content directly." Do not proceed until input is received.

2. Read the full skill content. If the file does not exist or the URL is unreachable, tell the user and stop.

3. **Classify the skill category** before scoring:

   - **Tool skill** — produces structured output, processes files, calls APIs, or automates a specific task (examples: PDF processor, code reviewer, UI generator, data query tool)
   - **Guideline skill** — modifies how the model behaves or thinks; no structured output; composed of rules, principles, or style guidance (examples: karpathy-guidelines, commit style guides, tone policies)
   - If unclear, default to Tool skill.

   State the category at the top of the output: `Category: Tool skill` or `Category: Guideline skill`.

4. Score each dimension using the rubric below. **Apply the correct weight column for the category.**

5. Output the scorecard in the format below.

6. For every dimension scoring below 70% of its maximum, give one specific, actionable improvement with a concrete example.

---

## Output Format

Always output in this exact structure:

> Fill in `<Max>` from the Category weights table for the category detected in step 3.

```
## Skill Evaluation: {skill name}

Category: {Tool skill / Guideline skill}

| Dimension | Score | Max | Notes |
|-----------|-------|-----|-------|
| Trigger Clarity | X | 20 | one-line observation |
| Instruction Specificity | X | <Max> | one-line observation |
| Reference Density | X | <Max> | one-line observation |
| Verifiability | X | <Max> | one-line observation |
| Tradeoff Transparency | X | <Max> | one-line observation |
| Portability | X | <Max> | one-line observation |
| Maintenance Maturity | X | 10 | one-line observation |
| **Total** | **X** | **100** | |

### Tier: {Bronze / Silver / Gold / Elite}
{One sentence summary of the skill's overall quality.}

### Top 3 Improvements
1. **{Dimension}**: {Specific change with example if possible}
2. **{Dimension}**: {Specific change with example if possible}
3. **{Dimension}**: {Specific change with example if possible}
```

**Tier thresholds:**
- Elite: 85–100
- Gold: 70–84
- Silver: 50–69
- Bronze: 0–49

---

## Scoring Rules

- Score based on what is present in the skill, not what it could theoretically do.
- Do not infer intent — if something is not written, it does not exist.
- Be strict. A karpathy-guidelines-quality skill (176k★) scores ~78/100. Calibrate accordingly.
- If the skill is a CLAUDE.md or command file (not a SKILL.md), note this and still score what you can.

---

## Rubric

Derived from analysis of the 9 most-starred Claude Code skill repositories (June 2026).

**Source repos:** obra/superpowers (228k★), affaan-m/ECC (216k★), multica-ai/andrej-karpathy-skills (176k★), anthropics/skills (151k★), nextlevelbuilder/ui-ux-pro-max-skill (92k★), thedotmack/claude-mem (82k★), JuliusBrussee/caveman (73k★), OthmanAdi/planning-with-files (23k★), NeoLabHQ/context-engineering-kit

### Category weights

| Dimension | Tool skill | Guideline skill | Why different |
|-----------|-----------|-----------------|---------------|
| Trigger Clarity | 20 | 20 | Same for both |
| Instruction Specificity | 15 | **20** | Rules/principles ARE the product — specificity is the entire value |
| Reference Density | 15 | **8** | Guideline skills are intentionally concise; data tables would bloat them |
| Verifiability | 15 | **8** | No structured output to verify; success is behavioral change, not a file |
| Tradeoff Transparency | 10 | **16** | Honest scope limits matter more when the whole skill is "always do X" |
| Portability | 15 | **18** | Guidelines should work anywhere; slightly higher bar |
| Maintenance Maturity | 10 | 10 | Same for both |
| **Total** | **100** | **100** | |

### Dimension 1 — Trigger Clarity (20 pts)

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

### Dimension 2 — Instruction Specificity (Tool: 15 pts · Guideline: 20 pts)

**What it measures:** Does the body give the model a concrete decision tree or procedure to follow, not just a description of what output to produce?

| Tool Score | Guideline Score | Criteria |
|-----------|-----------------|----------|
| 13–15 | 17–20 | Step-by-step procedure with explicit branching (if X then Y). Model cannot misinterpret. Includes what to do when inputs are missing or ambiguous. |
| 9–12 | 12–16 | Clear steps but missing edge case handling or branching. |
| 5–8 | 7–11 | Describes desired output but not the process to get there. Model must fill in the gaps. |
| 0–4 | 0–6 | Vague prose. "Help the user do X." |

**What to look for:** Numbered steps, conditional logic, explicit fallback behavior.

### Dimension 3 — Reference Density (Tool: 15 pts · Guideline: 8 pts)

**What it measures:** Is there bundled reference material (data, examples, templates, scripts) that the model can use directly — not just instructions?

| Tool Score | Guideline Score | Criteria |
|-----------|-----------------|----------|
| 13–15 | 7–8 | Rich reference data: enumerable lists, code templates, lookup tables, or scripts. Quantified claims ("67 styles", "161 palettes"). |
| 9–12 | 5–6 | Some examples or a reference file, but thin. |
| 5–8 | 3–4 | A few inline examples only. No separate reference files. |
| 0–4 | 0–2 | Pure instructions with no supporting data. Model must rely on training knowledge. |

**What to look for:** `references/` folder, `scripts/` folder, embedded data tables, code snippets with real values.

### Dimension 4 — Verifiability (Tool: 15 pts · Guideline: 8 pts)

**What it measures:** Can success be verified? Does the skill define what "done" looks like, or better yet, include evals/benchmarks?

| Tool Score | Guideline Score | Criteria |
|-----------|-----------------|----------|
| 13–15 | 7–8 | Includes evals, benchmarks, or CI-committed snapshots. Output format is fully specified with examples. |
| 9–12 | 5–6 | Specifies the exact output format or success criteria. No evals but clear definition of done. |
| 5–8 | 3–4 | Rough description of expected output. Leaves ambiguity. |
| 0–4 | 0–2 | No output spec. "Good results" is the only criterion. |

**What to look for:** Defined output templates, `evals/` folder, test prompts, success/failure examples.

### Dimension 5 — Tradeoff Transparency (Tool: 10 pts · Guideline: 16 pts)

**What it measures:** Does the skill honestly state its limitations, biases, or when NOT to use it?

| Tool Score | Guideline Score | Criteria |
|-----------|-----------------|----------|
| 9–10 | 14–16 | Explicit tradeoff statement. States what the skill sacrifices and for what. Names scenarios where it should not be used. |
| 6–8 | 10–13 | Mentions limitations briefly. |
| 3–5 | 5–8 | Implies limitations but doesn't state them. |
| 0–2 | 0–4 | Claims universal applicability. No caveats. |

**Example of elite pattern (karpathy-guidelines):**
> `Tradeoff: These guidelines bias toward caution over speed. For trivial tasks, use judgment.`

### Dimension 6 — Portability (Tool: 15 pts · Guideline: 18 pts)

**What it measures:** Can anyone install and use this without project-specific context? Does it work across multiple agent harnesses?

| Tool Score | Guideline Score | Criteria |
|-----------|-----------------|----------|
| 13–15 | 16–18 | Zero-dependency OR all dependencies auto-install. Works on Claude Code + at least 2 other harnesses. No hardcoded paths or user-specific assumptions. |
| 9–12 | 11–14 | Works on Claude Code. Minor assumptions about environment. |
| 5–8 | 6–10 | Requires manual setup. May reference project-specific paths or tools. |
| 0–4 | 0–5 | Only works in one specific setup. Hardcoded paths, project names, or internal tooling. |

### Dimension 7 — Maintenance Maturity (10 pts)

**What it measures:** Does the repository show signs of being maintained and trustworthy over time?

| Score | Criteria |
|-------|----------|
| 9–10 | License, version, CHANGELOG, CONTRIBUTING, and author contact all present. |
| 6–8 | License + version present. Missing 1–2 of the others. |
| 3–5 | Only a README. No version, no license. |
| 0–2 | No metadata at all. |

### Calibration Reference

> Scores use Tool skill weights unless the Category column shows "Guideline".

| Skill | Category | Score | Key Strengths | Key Weaknesses |
|-------|----------|-------|---------------|----------------|
| karpathy-guidelines | Guideline | ~68/100 | Tradeoff transparency, instruction specificity | No evals, thin reference data |
| anthropics/skills pdf | Tool | ~82/100 | Reference density (full code examples), verifiability | Limited multi-harness |
| anthropics/skills skill-creator | Tool | ~88/100 | Eval loop, output format, full procedure | Complex, high token cost |
| JuliusBrussee/caveman | Tool | ~85/100 | Real LLM benchmarks, control arm testing | Very narrow use case |
| nextlevelbuilder/ui-ux-pro-max | Tool | ~80/100 | Quantified data, multi-platform install | Less instruction specificity |
| OthmanAdi/planning-with-files | Tool | ~76/100 | i18n, multi-harness, maintenance maturity | Reference density thin |
