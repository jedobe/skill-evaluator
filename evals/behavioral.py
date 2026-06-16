"""
behavioral.py — Behavioral evaluation for Claude Code skills.

Tests whether a skill actually changes model behavior, not just document quality.

For each task in a fixture:
  Pass A: call claude WITH the skill as system prompt
  Pass B: call claude WITHOUT any system prompt (baseline)
  Judge:  call claude with judge.md to compare A vs B

Usage:
    python evals/behavioral.py --skill karpathy
    python evals/behavioral.py --skill karpathy --task no-gold-plating
    python evals/behavioral.py --skill karpathy --verbose
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

EVALS_DIR = Path(__file__).parent
FIXTURES_DIR = EVALS_DIR / "fixtures"
SNAPSHOTS_DIR = EVALS_DIR / "snapshots"
SKILLS_DIR = EVALS_DIR.parent / "skills"
PROMPTS_DIR = EVALS_DIR / "prompts"

PASS_THRESHOLD = 0.20  # delta_normalized must exceed this to PASS


def call_claude(system_prompt: str | None, user_prompt: str, timeout: int = 120) -> str:
    """Call the claude CLI. Returns stdout text or empty string on error."""
    cmd = ["claude", "-p"]
    if system_prompt:
        cmd += ["--system-prompt", system_prompt]
    cmd.append(user_prompt)

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=timeout,
    )
    if result.returncode != 0 and result.stderr:
        print(f"    [stderr] {result.stderr[:200]}", file=sys.stderr)
    return result.stdout or ""


def extract_json(text: str) -> dict | None:
    """Extract the first JSON object from text (strips markdown fences if present)."""
    # strip ```json ... ``` fences
    text = re.sub(r"```(?:json)?\s*", "", text)
    text = re.sub(r"```", "", text)
    match = re.search(r"\{[\s\S]*\}", text)
    if not match:
        return None
    try:
        return json.loads(match.group())
    except json.JSONDecodeError:
        return None


def resolve_skill_path(skill_name: str) -> Path | None:
    """Find the SKILL.md for a given skill name.

    Checks:
    1. skills/{skill_name}/SKILL.md  (installed in this repo)
    2. evals/prompts/{skill_name}.txt (eval prompt stubs)
    """
    candidate = SKILLS_DIR / skill_name / "SKILL.md"
    if candidate.exists():
        return candidate
    stub = PROMPTS_DIR / f"{skill_name}.txt"
    if stub.exists():
        return stub
    return None


def run_task(
    task: dict,
    skill_content: str,
    judge_prompt: str,
    verbose: bool = False,
) -> dict:
    task_id = task["id"]
    user_prompt = task["prompt"]
    expected = task.get("expected_behaviors", [])
    anti = task.get("anti_patterns", [])

    print(f"  [{task_id}] Pass A (with skill)...", end=" ", flush=True)
    response_a = call_claude(skill_content, user_prompt)
    print("done")

    print(f"  [{task_id}] Pass B (baseline)...", end=" ", flush=True)
    response_b = call_claude(None, user_prompt)
    print("done")

    judge_input = (
        f"TASK_ID: {task_id}\n\n"
        f"TASK:\n{user_prompt}\n\n"
        f"EXPECTED_BEHAVIORS:\n"
        + "\n".join(f"- {b}" for b in expected)
        + f"\n\nANTI_PATTERNS:\n"
        + "\n".join(f"- {a}" for a in anti)
        + f"\n\nRESPONSE_A (with skill):\n{response_a}\n\n"
        f"RESPONSE_B (baseline):\n{response_b}"
    )

    print(f"  [{task_id}] Judging...", end=" ", flush=True)
    judgment_raw = call_claude(judge_prompt, judge_input)
    print("done")

    judgment = extract_json(judgment_raw)
    if judgment is None:
        print(f"  [{task_id}] WARNING: could not parse judge output", file=sys.stderr)
        if verbose:
            print(f"  raw judge output:\n{judgment_raw[:500]}", file=sys.stderr)
        return {
            "task_id": task_id,
            "error": "judge_parse_failed",
            "passed": False,
            "delta_normalized": None,
            "summary": "judge output could not be parsed",
        }

    delta_norm = judgment.get("delta_normalized", 0.0)
    passed = isinstance(delta_norm, (int, float)) and delta_norm > PASS_THRESHOLD

    if verbose:
        print(f"    delta_normalized={delta_norm:.2f}  summary={judgment.get('summary', '')}")

    return {
        "task_id": task_id,
        "passed": passed,
        "delta_normalized": delta_norm,
        "delta_raw": judgment.get("delta"),
        "summary": judgment.get("summary", ""),
        "score_a": judgment.get("response_a", {}).get("raw_score"),
        "score_b": judgment.get("response_b", {}).get("raw_score"),
        "max_possible": judgment.get("response_a", {}).get("max_possible"),
    }


def compute_behavioral_score(task_results: list[dict]) -> int:
    """Aggregate per-task delta_normalized into a 0-100 behavioral score."""
    valid = [
        r["delta_normalized"]
        for r in task_results
        if r.get("delta_normalized") is not None
    ]
    if not valid:
        return 0
    mean_delta = sum(valid) / len(valid)
    # delta_normalized is in [-1, 1]; map to [0, 100] where 0 delta = 50
    raw = (mean_delta + 1) / 2 * 100
    return max(0, min(100, round(raw)))


def run_behavioral(skill_name: str, task_filter: str | None = None, verbose: bool = False) -> dict:
    fixture_dir = FIXTURES_DIR / skill_name
    if not fixture_dir.exists():
        print(f"ERROR: No fixtures found for skill '{skill_name}' at {fixture_dir}", file=sys.stderr)
        sys.exit(1)

    tasks_path = fixture_dir / "tasks.json"
    judge_path = fixture_dir / "judge.md"
    if not tasks_path.exists():
        print(f"ERROR: Missing {tasks_path}", file=sys.stderr)
        sys.exit(1)
    if not judge_path.exists():
        print(f"ERROR: Missing {judge_path}", file=sys.stderr)
        sys.exit(1)

    fixture = json.loads(tasks_path.read_text(encoding="utf-8"))
    judge_prompt = judge_path.read_text(encoding="utf-8")
    tasks = fixture.get("tasks", [])

    if task_filter:
        tasks = [t for t in tasks if t["id"] == task_filter]
        if not tasks:
            print(f"ERROR: No task with id='{task_filter}' in {tasks_path}", file=sys.stderr)
            sys.exit(1)

    skill_path = resolve_skill_path(skill_name)
    if skill_path is None:
        print(f"ERROR: SKILL.md not found for '{skill_name}'", file=sys.stderr)
        sys.exit(1)

    skill_content = skill_path.read_text(encoding="utf-8")

    print(f"\n  skill : {skill_name}  ({skill_path.name})")
    print(f"  tasks : {len(tasks)}")
    print()

    task_results = []
    for task in tasks:
        result = run_task(task, skill_content, judge_prompt, verbose=verbose)
        task_results.append(result)

    behavioral_score = compute_behavioral_score(task_results)
    passed_count = sum(1 for r in task_results if r.get("passed"))
    all_passed = passed_count == len(task_results)

    return {
        "skill": skill_name,
        "behavioral_score": behavioral_score,
        "tasks_passed": passed_count,
        "tasks_total": len(task_results),
        "all_passed": all_passed,
        "task_results": task_results,
    }


def print_summary(result: dict) -> None:
    skill = result["skill"]
    bscore = result["behavioral_score"]
    passed = result["tasks_passed"]
    total = result["tasks_total"]
    status = "PASS" if result["all_passed"] else "FAIL"

    print(f"\n── Behavioral: {skill} ───────────────────────────────")
    print(f"{'Task':<22} {'Delta':>7}  {'Pass'}")
    print("-" * 44)
    for r in result["task_results"]:
        dn = r.get("delta_normalized")
        delta_str = f"{dn:+.2f}" if dn is not None else "  N/A"
        p = "PASS" if r.get("passed") else "FAIL"
        summary_short = r.get("summary", "")[:45]
        print(f"{r['task_id']:<22} {delta_str:>7}  {p}  {summary_short}")

    print("-" * 44)
    print(f"Behavioral score: {bscore}/100  ({passed}/{total} tasks passed)  {status}")


def save_snapshot(result: dict) -> None:
    SNAPSHOTS_DIR.mkdir(exist_ok=True)
    path = SNAPSHOTS_DIR / f"behavioral_{result['skill']}.json"
    path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nResults saved to {path.relative_to(EVALS_DIR.parent)}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Behavioral eval for Claude Code skills")
    parser.add_argument("--skill", required=True, help="Skill name (must match evals/fixtures/<name>/)")
    parser.add_argument("--task", help="Run only the task with this id")
    parser.add_argument("--verbose", action="store_true", help="Print raw judge output details")
    parser.add_argument("--no-save", action="store_true", help="Skip writing snapshot JSON")
    args = parser.parse_args()

    print("\n## Behavioral Eval Run")
    result = run_behavioral(args.skill, task_filter=args.task, verbose=args.verbose)
    print_summary(result)

    if not args.no_save:
        save_snapshot(result)

    sys.exit(0 if result["all_passed"] else 1)


if __name__ == "__main__":
    main()
