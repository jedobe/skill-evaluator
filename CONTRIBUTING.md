# Contributing to skill-evaluator

Thank you for improving the rubric. This guide covers how to add eval cases, challenge scoring criteria, and submit PRs.

---

The eval suite has two layers. A **static** case checks that the evaluator
assigns a score in an expected range to a known skill. A **behavioral** case
checks that a skill actually changes model behavior, by running tasks with and
without the skill loaded and judging the delta. See `evals/README.md` for the
full design.

## Adding a Static Eval Case

1. **Create the prompt file**

   Place the raw SKILL.md content (or a representative excerpt) in `evals/prompts/<name>.txt`:

   ```
   evals/prompts/my-skill.txt
   ```

2. **Add the case to `STATIC_CASES` in `evals/run.py`**

   ```python
   {
       "name": "my-skill",
       "prompt_file": "my-skill.txt",
       "expected_range": (lo, hi),   # tight band: hi - lo ≤ 12
       "expected_tier": "Gold",       # Bronze / Silver / Gold / Elite
   },
   ```

   **How to pick the expected range:**
   - Run `python evals/run.py` a few times to observe variance.
   - Set `lo = observed_min - 2`, `hi = observed_max + 2`.
   - Keep the band ≤ 12 pts wide to stay meaningful.

3. **Verify locally**

   ```bash
   python evals/run.py
   ```

   All existing cases must still pass before opening a PR.

---

## Adding a Behavioral Eval

A behavioral fixture proves a skill changes what the model *does*, not just how
its document reads.

1. **Create the fixture directory** `evals/fixtures/<skill-name>/` with two files:

   - `tasks.json` — a list of tasks, each with `id`, `prompt`, `expected_behaviors`, and `anti_patterns`.
   - `judge.md` — the judge system prompt. It must return JSON with `delta`, `delta_normalized`, and per-response `raw_score` / `max_possible`. Copy an existing `judge.md` (e.g. `fixtures/karpathy/judge.md`) and adjust the rubric.

2. **Register the pass contract** in `BEHAVIORAL_CASES` in `evals/run.py`:

   ```python
   {"name": "my-skill", "min_score": 55, "min_tasks_pct": 0.6},
   ```

   `min_score` is the aggregate behavioral score (0–100, where no behavioral
   change = 50); `min_tasks_pct` is the fraction of tasks whose
   `delta_normalized` must exceed the pass threshold (0.20).

3. **Verify locally** (needs the `claude` CLI logged in; 3 API calls per task):

   ```bash
   python evals/run.py --mode behavioral --verbose
   ```

---

## Challenging a Rubric Score Band

If you believe a score band is miscalibrated (e.g., "13–15 is too easy to reach"):

1. Open an issue with the title format:
   ```
   [Rubric] Dimension N — <dimension name>: <proposed change>
   ```

2. Include:
   - The specific band you are challenging (e.g., "13–15 band in Reference Density")
   - At least two real SKILL.md examples that demonstrate the miscalibration
   - Your proposed revised criteria

3. Reference `skills/skill-evaluator/references/corpus.md` to show how the change affects the calibration reference skills.

---

## PR Checklist

Before opening a pull request, confirm:

- [ ] `python evals/validate.py` passes (offline structural check — no API key needed; this is what CI runs)
- [ ] `python evals/run.py` passes all cases (needs the `claude` CLI logged in)
- [ ] New eval case (if added) has a tight expected range (≤ 12 pts)
- [ ] `CHANGELOG.md` updated with a brief description of the change
- [ ] No changes to `rubric.md` without a corresponding issue discussion
- [ ] `corpus.md` updated if new repos are added to the calibration set

---

## Repo Structure

```
evals/
  prompts/       — input SKILL.md files for static eval cases
  fixtures/      — behavioral eval fixtures, one dir per skill (tasks.json + judge.md)
  snapshots/     — CI-committed result JSON (do not edit manually)
  run.py         — eval harness (static + behavioral; --mode static|behavioral|both)
  behavioral.py  — behavioral eval engine (Pass A/B + LLM judge)
  validate.py    — offline structural checks (rubric sums, JSON, fixtures); run in CI
.github/
  workflows/
    ci.yml       — runs validate.py on push/PR (no secrets)
skills/
  skill-evaluator/
    SKILL.md     — the evaluator skill itself
    references/
      rubric.md  — pointer to the inlined rubric
      corpus.md  — calibration corpus (9 repos)
CHANGELOG.md
CONTRIBUTING.md  — this file
LICENSE
README.md
```
