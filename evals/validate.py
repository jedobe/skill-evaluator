"""
validate.py — Structural validation for skill-evaluator. No API calls.

Catches the regressions that have actually bitten this repo:
  - rubric weight columns that no longer sum to 100
  - malformed snapshot / fixture JSON
  - behavioral fixtures missing required keys or files

Runs in CI without secrets, and locally in under a second:

    python evals/validate.py
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
SKILL_MD = ROOT / "skills" / "skill-evaluator" / "SKILL.md"
FIXTURES_DIR = Path(__file__).parent / "fixtures"
SNAPSHOTS_DIR = Path(__file__).parent / "snapshots"

EXPECTED_DIMENSIONS = 7
REQUIRED_TASK_KEYS = ("id", "prompt", "expected_behaviors", "anti_patterns")


def fail(errors: list[str], msg: str) -> None:
    errors.append(msg)


def check_rubric_weights(errors: list[str]) -> None:
    """The Category weights table must have 7 dimensions and Tool/Guideline
    columns that each sum to 100."""
    text = SKILL_MD.read_text(encoding="utf-8")

    # isolate the "### Category weights" table up to the next heading
    section = re.search(r"### Category weights\s*(.+?)\n#", text, re.DOTALL)
    if not section:
        fail(errors, "SKILL.md: '### Category weights' table not found")
        return

    tool_sum = guide_sum = 0
    dim_count = 0
    declared_tool = declared_guide = None

    for line in section.group(1).splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 3:
            continue
        name = cells[0].replace("*", "").strip()
        if name in ("Dimension", "") or name.startswith("---"):
            continue

        def to_int(cell: str):
            digits = re.sub(r"[^0-9]", "", cell)
            return int(digits) if digits else None

        tool, guide = to_int(cells[1]), to_int(cells[2])
        if name == "Total":
            declared_tool, declared_guide = tool, guide
            continue
        if tool is None or guide is None:
            fail(errors, f"SKILL.md weights: non-numeric row '{name}'")
            continue
        tool_sum += tool
        guide_sum += guide
        dim_count += 1

    if dim_count != EXPECTED_DIMENSIONS:
        fail(errors, f"SKILL.md weights: expected {EXPECTED_DIMENSIONS} dimensions, found {dim_count}")
    if tool_sum != 100:
        fail(errors, f"SKILL.md weights: Tool column sums to {tool_sum}, expected 100")
    if guide_sum != 100:
        fail(errors, f"SKILL.md weights: Guideline column sums to {guide_sum}, expected 100")
    if declared_tool not in (None, 100) or declared_guide not in (None, 100):
        fail(errors, f"SKILL.md weights: Total row says {declared_tool}/{declared_guide}, expected 100/100")


def check_json_files(errors: list[str]) -> None:
    """All committed JSON must parse."""
    snapshot = SNAPSHOTS_DIR / "results.json"
    json_files = list(FIXTURES_DIR.glob("*/tasks.json"))
    if snapshot.exists():
        json_files.append(snapshot)
    for path in json_files:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            fail(errors, f"{path.relative_to(ROOT)}: invalid JSON ({e})")


def check_fixtures(errors: list[str]) -> None:
    """Each fixture dir needs tasks.json + judge.md, and every task needs the
    keys behavioral.py reads."""
    if not FIXTURES_DIR.exists():
        return
    for fixture_dir in sorted(p for p in FIXTURES_DIR.iterdir() if p.is_dir()):
        rel = fixture_dir.relative_to(ROOT)
        tasks_path = fixture_dir / "tasks.json"
        judge_path = fixture_dir / "judge.md"
        if not tasks_path.exists():
            fail(errors, f"{rel}: missing tasks.json")
            continue
        if not judge_path.exists():
            fail(errors, f"{rel}: missing judge.md")
        try:
            fixture = json.loads(tasks_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue  # already reported by check_json_files
        tasks = fixture.get("tasks", [])
        if not tasks:
            fail(errors, f"{rel}/tasks.json: no tasks defined")
        for i, task in enumerate(tasks):
            for key in REQUIRED_TASK_KEYS:
                if key not in task:
                    fail(errors, f"{rel}/tasks.json: task #{i} missing '{key}'")
            if not isinstance(task.get("expected_behaviors"), list) or not task.get("expected_behaviors"):
                fail(errors, f"{rel}/tasks.json: task '{task.get('id', i)}' expected_behaviors must be a non-empty list")


def main() -> None:
    errors: list[str] = []
    check_rubric_weights(errors)
    check_json_files(errors)
    check_fixtures(errors)

    if errors:
        print("FAIL: structural validation found issues:\n")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    print("OK: rubric weights sum to 100, JSON valid, fixtures well-formed.")


if __name__ == "__main__":
    main()
