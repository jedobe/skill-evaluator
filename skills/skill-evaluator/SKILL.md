---
name: skill-evaluator
description: Score a Claude Code skill against a research-backed rubric derived from the top 9 most-starred skill repos on GitHub (obra/superpowers 228k★, affaan-m/ECC 216k★, anthropics/skills 151k★, and more). Use when a user asks to evaluate, score, review, rate, or improve a skill — or when they share a SKILL.md and want to know how good it is.
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
   - A file path to a `SKILL.md` in the user's message → Read the file
   - A GitHub URL → Fetch the raw content
   - Pasted SKILL.md content directly in the chat → Use as-is
   - **No input provided** → Ask: "Please share the SKILL.md file path, a GitHub URL, or paste the skill content directly." Do not proceed until input is received.

2. Read the full skill content. If the file does not exist or the URL is unreachable, tell the user and stop.

3. Score each dimension using the rubric in `references/rubric.md`. Read that file before scoring.

4. Output the scorecard in the format below.

5. For every dimension scoring below 70% of its maximum, give one specific, actionable improvement with a concrete example.

---

## Output Format

Always output in this exact structure:

```
## Skill Evaluation: {skill name}

| Dimension | Score | Max | Notes |
|-----------|-------|-----|-------|
| Trigger Clarity | X | 20 | one-line observation |
| Instruction Specificity | X | 15 | one-line observation |
| Reference Density | X | 15 | one-line observation |
| Verifiability | X | 15 | one-line observation |
| Tradeoff Transparency | X | 10 | one-line observation |
| Portability | X | 15 | one-line observation |
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
