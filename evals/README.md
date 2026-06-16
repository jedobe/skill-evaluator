# Evals

Validates that skill-evaluator produces consistent, calibrated scores across known reference inputs.

## Design

Three test cases with known expected score ranges, derived from manual analysis of the source repos.

| Test | Input | Expected Total | Expected Tier |
|------|-------|---------------|---------------|
| `karpathy` | karpathy-guidelines SKILL.md | 72–82 | Gold |
| `minimal` | A near-empty skill with only a name | 5–15 | Bronze |

skill-evaluator itself is intentionally excluded from evals. Meta-skills (tools that evaluate other tools) don't fit the rubric dimensions, which were designed for task-performing skills. A self-score would be circular and misleading.

## Running

```bash
# Requires claude CLI logged in
python evals/run.py
```

Output: a markdown table with actual scores vs expected ranges. Pass = within range. Fail = outside range.

## Files

- `prompts/karpathy.txt` — karpathy-guidelines SKILL.md content
- `prompts/minimal.txt` — minimal skill content
- `run.py` — runs each prompt through claude-code with the skill active, captures scored output
- `snapshots/results.json` — last committed run results (deterministic CI reference)
