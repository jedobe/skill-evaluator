# skill-evaluator

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![Version](https://img.shields.io/badge/version-1.0.0-green.svg)
![Platform](https://img.shields.io/badge/platform-Claude%20Code%20%7C%20Codex%20%7C%20Cursor-lightgrey.svg)

**Everyone's writing skills. Nobody knows if they're any good.**

This skill scores yours — against a rubric reverse-engineered from the 9 most-starred Claude Code skill repos on GitHub.

---

## How it works

Most skill feedback is vibes. This isn't.

The rubric was built by analyzing what actually separates top-tier skills (obra/superpowers 228k★, affaan-m/ECC 216k★, anthropics/skills 151k★) from the rest. Seven dimensions. 100 points. A tier you can point to.

```
## Skill Evaluation: karpathy-guidelines

| Dimension            | Score | Max |
|----------------------|-------|-----|
| Trigger Clarity      |  16   |  20 |
| Instruction Specificity |  14 | 15 |
| Reference Density    |   8   |  15 |
| Verifiability        |   9   |  15 |
| Tradeoff Transparency|  10   |  10 |
| Portability          |  12   |  15 |
| Maintenance Maturity |   9   |  10 |
| **Total**            | **78**|**100**|

### Tier: Gold
Strong behavioral guidelines, but thin on bundled reference data and evals.

### Top 3 Improvements
1. **Reference Density**: Add a `references/` folder with lookup tables or code examples...
2. **Verifiability**: Define an output spec or add test prompts to an `evals/` folder...
3. **Trigger Clarity**: Add "do NOT use when..." conditions to the description...
```

---

## Install

```
/plugin install skill-evaluator
```

Or clone and point at it manually:

```bash
git clone https://github.com/jedobe/skill-evaluator
```

## Usage

Ask Claude to evaluate any skill — by file path, GitHub URL, or pasted content:

```
evaluate ~/.claude/skills/my-skill/SKILL.md
```

```
evaluate this skill: [paste SKILL.md here]
```

---

## The 7 dimensions

| # | Dimension | Pts | The question it answers |
|---|-----------|-----|-------------------------|
| 1 | **Trigger Clarity** | 20 | Does the description tell the model *when* to invoke — not just *what* it does? |
| 2 | **Instruction Specificity** | 15 | Is there a concrete procedure, or just a description of desired output? |
| 3 | **Reference Density** | 15 | Is supporting data bundled in — or does the model rely on training alone? |
| 4 | **Verifiability** | 15 | Is there a defined output spec, eval suite, or success criteria? |
| 5 | **Tradeoff Transparency** | 10 | Does the skill honestly state its limits and when NOT to use it? |
| 6 | **Portability** | 15 | Zero-dep? Multi-harness? No hardcoded paths? |
| 7 | **Maintenance Maturity** | 10 | License, version, CHANGELOG — does it look maintained? |

**Tiers:** Elite (85+) · Gold (70–84) · Silver (50–69) · Bronze (0–49)

---

## Calibration

Scores are grounded in real repos. A few reference points:

| Skill | Stars | Score | Tier |
|-------|-------|-------|------|
| anthropics/skills — skill-creator | — | ~88 | Elite |
| JuliusBrussee/caveman | 73k★ | ~85 | Elite |
| multica-ai/andrej-karpathy-skills | 176k★ | ~78 | Gold |
| OthmanAdi/planning-with-files | 23k★ | ~76 | Gold |

If your skill scores 85+, it's in genuinely rare company.

> **Note:** skill-evaluator itself is not in this table. Meta-skills (tools that evaluate other tools) don't fit the rubric — the dimensions were designed for task-performing skills. Scoring a rubric tool against its own rubric is circular.

---

## Why this exists

The skill ecosystem is growing fast. There's no shared standard for what "good" looks like — so most feedback is either "looks fine" or a wall of subjective opinions.

This rubric is an attempt to make that judgment concrete, reproducible, and grounded in what the community has already validated with stars.

---

## License

MIT
