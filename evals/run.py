"""
skill-evaluator evals

Runs three test prompts through the evaluator and checks scores against expected ranges.
Requires: claude CLI logged in, skill-evaluator installed.

Usage:
    python evals/run.py
"""

import subprocess
import json
import re
import sys
from pathlib import Path

SKILL_PATH = Path(__file__).parent.parent / "skills" / "skill-evaluator" / "SKILL.md"
PROMPTS_DIR = Path(__file__).parent / "prompts"
SNAPSHOTS_DIR = Path(__file__).parent / "snapshots"

CASES = [
    {
        "name": "minimal",
        "prompt_file": "minimal.txt",
        "expected_range": (5, 15),
        "expected_tier": "Bronze",
    },
    {
        "name": "karpathy",
        "prompt_file": "karpathy.txt",
        "expected_range": (68, 80),
        "expected_tier": "Gold",
    },
]


def extract_total(output: str) -> int | None:
    match = re.search(r"\*\*Total\*\*\s*\|\s*\*\*(\d+)\*\*", output)
    if match:
        return int(match.group(1))
    return None


def extract_tier(output: str) -> str | None:
    match = re.search(r"###\s*Tier:\s*(Bronze|Silver|Gold|Elite)", output)
    if match:
        return match.group(1)
    return None


def run_case(case: dict) -> dict:
    if case["prompt_file"] is None:
        content = SKILL_PATH.read_text(encoding="utf-8")
    else:
        content = (PROMPTS_DIR / case["prompt_file"]).read_text(encoding="utf-8")

    prompt = f"Evaluate this skill:\n\n{content}"
    skill_content = SKILL_PATH.read_text(encoding="utf-8")

    result = subprocess.run(
        ["claude", "-p", "--system-prompt", skill_content, prompt],
        capture_output=True,
        text=True,
        timeout=120,
    )

    output = result.stdout
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


def main():
    results = []
    print("\n## skill-evaluator eval run\n")
    print(f"{'Test':<12} {'Score':<8} {'Tier':<10} {'Expected':<18} {'Pass'}")
    print("-" * 60)

    for case in CASES:
        r = run_case(case)
        results.append(r)
        lo, hi = r["expected_range"]
        status = "PASS" if r["passed"] else "FAIL"
        expected = f"{lo}\u2013{hi} {r['expected_tier']}"
        print(f"{r['name']:<12} {str(r['total']):<8} {str(r['tier']):<10} {expected:<18} {status}")

    SNAPSHOTS_DIR.mkdir(exist_ok=True)
    (SNAPSHOTS_DIR / "results.json").write_text(
        json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"\nResults saved to evals/snapshots/results.json")

    failures = [r for r in results if not r["passed"]]
    if failures:
        print(f"\n{len(failures)} test(s) failed.")
        sys.exit(1)
    else:
        print("\nAll tests passed.")


if __name__ == "__main__":
    main()
