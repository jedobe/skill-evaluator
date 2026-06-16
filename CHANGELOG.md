# Changelog

## v1.2.0 — 2026.06.16

- fix: rebalance Guideline skill weights so strong behavioral skills clear the Gold threshold decisively (Instruction Specificity 20→24, Tradeoff 16→18; Verifiability 8→5, Maintenance 10→7) — a low-70s boundary score is not a credible "excellent" signal
- fix: align karpathy calibration anchor back to ~78 (matches corpus.md and Scoring Rules)
- fix: README synced with category-weighted scorecard (Category line + Tool/Guideline columns)
- fix: eval karpathy band set to 72–82 Gold; snapshot regenerated from a live run
- fix: ASCII hyphen in eval console output (en-dash crashed on Windows cp949 stdout)
- fix: corpus accuracy — replace NeoLabHQ/context-engineering-kit (1.1k★, the lone outlier breaking the "most-starred" claim) with mattpocock/skills (131k★); correct star counts against live GitHub data (obra 228k→229k, claude-mem 82k→83k)

## v1.1.0 — 2026.06.16

- feat: skill category detection (Tool skill / Guideline skill) with separate rubric weights
- feat: corpus.md reference data for all 9 source repos
- feat: karpathy eval prompt + snapshots dir tracking
- fix: rubric criteria tables updated with Guideline skill score ranges per dimension
- fix: output format template clarified — replaced ambiguous `{X or Y}` with `<Max>` + note
- fix: calibration table updated with Category column and correct weight basis per skill
- docs: CONTRIBUTING.md added

## v1.0.0 — 2026.06.16

- Initial release
- 7-dimension rubric derived from top 9 GitHub skill repos
- Tier system: Bronze / Silver / Gold / Elite
- Calibration reference table included in rubric
