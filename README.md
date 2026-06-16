# skill-evaluator

Score any Claude Code skill against a research-backed rubric.

The rubric was reverse-engineered from the **9 most-starred** Claude Code skill repositories on GitHub — including obra/superpowers (228k★), affaan-m/ECC (216k★), and anthropics/skills (151k★). It captures what actually separates top-tier skills from everything else.

## What you get

A 7-dimension scorecard (100 pts total) + tier rating + top 3 actionable improvements:

| Dimension | Pts | What it checks |
|-----------|-----|----------------|
| Trigger Clarity | 20 | Does the description tell the model *when* to invoke — not just *what* it does? |
| Instruction Specificity | 15 | Is there a concrete decision tree, or just a description of desired output? |
| Reference Density | 15 | Is reference data (examples, tables, scripts) bundled — or does the model rely on training alone? |
| Verifiability | 15 | Is there an output spec, eval suite, or defined success criteria? |
| Tradeoff Transparency | 10 | Does the skill honestly state its limits and when NOT to use it? |
| Portability | 15 | Zero-dep? Multi-harness? No hardcoded paths? |
| Maintenance Maturity | 10 | License, version, CHANGELOG, CONTRIBUTING? |

**Tiers:** Elite (85+) · Gold (70–84) · Silver (50–69) · Bronze (0–49)

## Install

```
/plugin install skill-evaluator
```

## Usage

```
/skill-evaluator path/to/SKILL.md
```

Or paste a SKILL.md directly in the chat and ask: *"evaluate this skill"*.

## Calibration

Scores are calibrated against real repos. karpathy-guidelines (176k★) scores ~78. anthropics/skills skill-creator scores ~88. If your skill hits 85+, it's genuinely Elite.

## License

MIT
