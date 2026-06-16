"""
skill-evaluator evals

Runs static and/or behavioral tests against one or more skills.

Usage:
    python evals/run.py                         # static only (default)
    python evals/run.py --mode behavioral       # behavioral only
    python evals/run.py --mode both             # static + behavioral
    python evals/run.py --mode both --verbose   # with judge detail output

Static mode: feeds each prompt through the skill-evaluator rubric and checks
the returned score falls within an expected range.

Behavioral mode: for each skill that has an evals/fixtures/<skill>/ directory,
runs tasks with and without the skill loaded, judges the delta, and reports
a behavioral score.
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

SKILL_PATH = Path(__file__).parent.parent / "skills" / "skill-evaluator" / "SKILL.md"
PROMPTS_DIR = Path(__file__).parent / "prompts"
SNAPSHOTS_DIR = Path(__file__).parent / "snapshots"
FIXTURES_DIR = Path(__file__).parent / "fixtures"

STATIC_CASES = [
    {
        "name": "minimal",
        "prompt_file": "minimal.txt",
        "expected_range": (5, 15),
        "expected_tier": "Bronze",
    },
    {
        "name": "karpathy",
        "prompt_file": "karpathy.txt",
        "expected_range": (72, 82),
        "expected_tier": "Gold",
    },
]

# Skills with behavioral fixtures — auto-detected from fixtures/ directory but
# listed here with pass thresholds so CI has an explicit expected contract.
BEHAVIORAL_CASES = [
    {"name": "karpathy", "min_score": 55, "min_tasks_pct": 0.6},
    {"name": "minimal",  "min_score": 0,  "min_tasks_pct": 0.0},
]


# ── Static helpers ─────────────────────────────────────────────────────────────

def extract_total(output: str) -> int | None:
    if not output:
        return None
    match = re.search(r"\*\*Total\*\*\s*\|\s*\*\*(\d+)\*\*", output)
    if match:
        return int(match.group(1))
    return None


def extract_tier(output: str) -> str | None:
    if not output:
        return None
    match = re.search(r"###\s*Tier:\s*(Bronze|Silver|Gold|Elite)", output)
    if match:
        return match.group(1)
    return None


def run_static_case(case: dict) -> dict:
    content = (PROMPTS_DIR / case["prompt_file"]).read_text(encoding="utf-8")
    prompt = f"Evaluate this skill:\n\n{content}"
    skill_content = SKILL_PATH.read_text(encoding="utf-8")

    result = subprocess.run(
        ["claude", "-p", "--system-prompt", skill_content, prompt],
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=120,
    )

    output = result.stdout or ""
    if result.returncode != 0 and result.stderr:
        print(f"  [stderr] {result.stderr[:200]}", file=sys.stderr)

    total = extract_total(output)
    tier = extract_tier(output)
    lo, hi = case["expected_range"]
    passed = total is not None and lo <= total <= hi and tier == case["expected_tier"]

    return {
        "name": case["name"],
        "total": total,
        "tier": tier,
        "expected_range": case["expected_range"],
        "expected_tier": case["expected_tier"],
        "passed": passed,
        "raw_output": output[:500],
    }


def run_static(cases: list[dict]) -> tuple[list[dict], bool]:
    results = []
    print("\n── Static ───────────────────────────────────────────────")
    print(f"{'Test':<12} {'Score':<8} {'Tier':<10} {'Expected':<18} {'Pass'}")
    print("-" * 60)

    for case in cases:
        r = run_static_case(case)
        results.append(r)
        lo, hi = r["expected_range"]
        status = "PASS" if r["passed"] else "FAIL"
        expected = f"{lo}-{hi} {r['expected_tier']}"
        print(f"{r['name']:<12} {str(r['total']):<8} {str(r['tier']):<10} {expected:<18} {status}")

    all_passed = all(r["passed"] for r in results)
    print("-" * 60)
    print(f"Static: {sum(r['passed'] for r in results)}/{len(results)} passed")
    return results, all_passed


# ── Behavioral helpers ─────────────────────────────────────────────────────────

def run_behavioral_suite(behavioral_cases: list[dict], verbose: bool) -> tuple[list[dict], bool]:
    """Import and run behavioral.py for each case that has fixtures."""
    import importlib.util

    behavioral_path = Path(__file__).parent / "behavioral.py"
    spec = importlib.util.spec_from_file_location("behavioral", behavioral_path)
    bmod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(bmod)

    results = []
    all_passed = True

    print("\n── Behavioral ───────────────────────────────────────────")
    print(f"{'Skill':<14} {'BehScore':>9} {'Tasks':>7} {'MinScore':>9} {'Pass'}")
    print("-" * 52)

    for case in behavioral_cases:
        skill = case["name"]
        fixture_dir = FIXTURES_DIR / skill
        if not fixture_dir.exists():
            print(f"{skill:<14} {'N/A':>9} {'N/A':>7} {'N/A':>9} SKIP (no fixtures)")
            continue

        result = bmod.run_behavioral(skill, verbose=verbose)

        if verbose:
            bmod.print_summary(result)

        bscore = result["behavioral_score"]
        t_pass = result["tasks_passed"]
        t_total = result["tasks_total"]
        t_pct = t_pass / t_total if t_total > 0 else 0.0
        case_passed = (
            bscore >= case["min_score"]
            and t_pct >= case["min_tasks_pct"]
        )
        if not case_passed:
            all_passed = False

        status = "PASS" if case_passed else "FAIL"
        threshold = f">= {case['min_score']}"
        print(f"{skill:<14} {bscore:>9} {t_pass}/{t_total:>4} {threshold:>9} {status}")

        bmod.save_snapshot(result)
        results.append({**result, "case_passed": case_passed})

    print("-" * 52)
    passed_count = sum(1 for r in results if r.get("case_passed"))
    print(f"Behavioral: {passed_count}/{len(results)} passed")
    return results, all_passed


# ── Entry point ────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="skill-evaluator eval runner")
    parser.add_argument(
        "--mode",
        choices=["static", "behavioral", "both"],
        default="static",
        help="Which eval suite to run (default: static)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print per-task behavioral details",
    )
    args = parser.parse_args()

    print("\n## skill-evaluator eval run")

    static_ok = True
    behavioral_ok = True
    all_results: dict = {}

    if args.mode in ("static", "both"):
        static_results, static_ok = run_static(STATIC_CASES)
        all_results["static"] = static_results

    if args.mode in ("behavioral", "both"):
        behavioral_results, behavioral_ok = run_behavioral_suite(
            BEHAVIORAL_CASES, verbose=args.verbose
        )
        all_results["behavioral"] = behavioral_results

    # Save combined snapshot
    SNAPSHOTS_DIR.mkdir(exist_ok=True)
    (SNAPSHOTS_DIR / "results.json").write_text(
        json.dumps(all_results, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"\nResults saved to evals/snapshots/results.json")

    if not (static_ok and behavioral_ok):
        failed_modes = []
        if not static_ok:
            failed_modes.append("static")
        if not behavioral_ok:
            failed_modes.append("behavioral")
        print(f"\nFailed: {', '.join(failed_modes)}")
        sys.exit(1)
    else:
        print("\nAll tests passed.")


if __name__ == "__main__":
    main()
