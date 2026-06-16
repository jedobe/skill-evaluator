# Contributing to skill-evaluator

Thank you for improving the rubric. This guide covers how to add eval cases, challenge scoring criteria, and submit PRs.

---

## Adding a New Eval Case

1. **Create the prompt file**

   Place the raw SKILL.md content (or a representative excerpt) in `evals/prompts/<name>.txt`:

   ```
   evals/prompts/my-skill.txt
   ```

2. **Add the case to `CASES` in `evals/run.py`**

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

- [ ] `python evals/run.py` passes all cases
- [ ] New eval case (if added) has a tight expected range (≤ 12 pts)
- [ ] `CHANGELOG.md` updated with a brief description of the change
- [ ] No changes to `rubric.md` without a corresponding issue discussion
- [ ] `corpus.md` updated if new repos are added to the calibration set

---

## Repo Structure

```
evals/
  prompts/       — input SKILL.md files for eval cases
  snapshots/     — CI-committed result JSON (do not edit manually)
  run.py         — eval harness
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
