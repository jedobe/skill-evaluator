# Evals

Two-layer evaluation suite for skill-evaluator.

- **Static eval** — verifies that skill-evaluator produces consistent, calibrated scores across known reference inputs (fast, cheap, no extra API calls beyond the evaluator itself).
- **Behavioral eval** — verifies that a skill *actually changes model behavior* by running tasks with and without the skill loaded and measuring the delta with an LLM judge (3 API calls per task).

## Static Eval

| Test | Input | Expected Total | Expected Tier |
|------|-------|----------------|---------------|
| `karpathy` | karpathy-guidelines SKILL.md | 72–82 | Gold |
| `minimal` | A near-empty skill with only a name | 5–15 | Bronze |

skill-evaluator itself is intentionally excluded from static evals. Meta-skills (tools that evaluate other tools) don't fit the rubric dimensions, which were designed for task-performing skills. A self-score would be circular and misleading.

## Behavioral Eval

| Fixture | Skill | Tasks | Purpose |
|---------|-------|-------|---------|
| `fixtures/karpathy/` | karpathy-guidelines | 5 | Positive: should suppress gold-plating, surface assumptions, enforce surgical edits |
| `fixtures/minimal/` | minimal (hello) | 3 | Negative control: near-zero delta expected — validates judge is not trivially biased |

Each fixture has:
- `tasks.json` — benchmark tasks with `expected_behaviors` and `anti_patterns`
- `judge.md` — LLM judge instructions for scoring Pass A (with skill) vs Pass B (baseline)

The judge scores each expected behavior 0–2 per response and returns `delta_normalized` in `[-1, 1]`. A delta > 0.20 is a PASS for that task.

## Running

```bash
# Static only (default, fast)
python evals/run.py

# Behavioral only
python evals/run.py --mode behavioral

# Both
python evals/run.py --mode both

# Single skill + verbose judge output
python evals/behavioral.py --skill karpathy --verbose

# Single task within a skill
python evals/behavioral.py --skill karpathy --task no-gold-plating
```

Output: a markdown table with actual scores vs expected ranges. Pass = within range / above threshold. Fail = outside.

## Files

```
evals/
  run.py                        — unified runner (--mode static|behavioral|both)
  behavioral.py                 — behavioral test runner (Pass A/B + judge)
  prompts/
    karpathy.txt                — karpathy-guidelines SKILL.md (static eval input)
    minimal.txt                 — minimal skill content (static eval input)
  fixtures/
    karpathy/
      tasks.json                — 5 behavioral benchmark tasks
      judge.md                  — judge instructions for karpathy tasks
    minimal/
      tasks.json                — 3 negative-control tasks
      judge.md                  — judge instructions for minimal tasks
  snapshots/
    results.json                — last committed run results (CI reference)
    behavioral_karpathy.json    — last behavioral run (karpathy)
    behavioral_minimal.json     — last behavioral run (minimal)
```
