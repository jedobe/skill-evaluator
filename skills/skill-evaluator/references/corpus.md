# Reference Corpus

Structural analysis of the 9 most-starred Claude Code skill repositories (June 2026) used to calibrate the rubric dimensions.

---

## obra/superpowers (228k★)

| Dimension | Pattern observed |
|-----------|-----------------|
| Trigger Clarity | Description lists 6+ distinct action verbs; explicit "when not to use" |
| Instruction Specificity | Multi-branch decision tree; numbered steps with conditional logic |
| Reference Density | Bundled lookup tables, code templates, scripts |
| Verifiability | Defined output schema; snapshot tests |
| Tradeoff Transparency | States cost/latency tradeoffs explicitly |
| Portability | Zero-dep; multi-harness declared |
| Maintenance Maturity | License + CHANGELOG + CONTRIBUTING present |

**Estimated score: ~90/100 · Elite**

---

## affaan-m/ECC (216k★)

| Dimension | Pattern observed |
|-----------|-----------------|
| Trigger Clarity | Clear "use when user asks to…" phrasing; 4+ phrases |
| Instruction Specificity | Step-by-step with fallback on missing input |
| Reference Density | Embedded code examples; references/ folder with data files |
| Verifiability | Output format fully templated; evals present |
| Tradeoff Transparency | Scope limitations stated |
| Portability | Works Claude Code + Cursor + opencode |
| Maintenance Maturity | MIT + version + CHANGELOG |

**Estimated score: ~88/100 · Elite**

---

## multica-ai/andrej-karpathy-skills (176k★)

| Dimension | Pattern observed |
|-----------|-----------------|
| Trigger Clarity | 3 trigger conditions; no explicit NOT conditions |
| Instruction Specificity | 4 numbered sections with concrete sub-rules |
| Reference Density | Inline examples only; no references/ folder |
| Verifiability | No evals; no output spec beyond prose description |
| Tradeoff Transparency | Explicit: "bias toward caution over speed" |
| Portability | MIT; single harness declared; no hardcoded paths |
| Maintenance Maturity | MIT license; no CHANGELOG; no version |

**Estimated score: ~78/100 · Gold** — calibration anchor for this rubric

---

## anthropics/skills (151k★) — skill-creator

| Dimension | Pattern observed |
|-----------|-----------------|
| Trigger Clarity | Trigger phrase list + explicit NOT conditions |
| Instruction Specificity | Eval loop pattern; step-by-step with success criteria per step |
| Reference Density | Template files bundled; example SKILL.md output provided |
| Verifiability | Output spec exact; eval assertions present |
| Tradeoff Transparency | Token cost warning; complexity caveat |
| Portability | Multi-harness; zero external deps |
| Maintenance Maturity | License + CHANGELOG + CONTRIBUTING |

**Estimated score: ~88/100 · Elite**

---

## nextlevelbuilder/ui-ux-pro-max-skill (92k★)

| Dimension | Pattern observed |
|-----------|-----------------|
| Trigger Clarity | 3 trigger conditions; moderately specific |
| Instruction Specificity | Clear output description; procedure less explicit |
| Reference Density | Quantified data ("161 color palettes", "67 design patterns") |
| Verifiability | Output format described; no automated evals |
| Tradeoff Transparency | Limited caveats |
| Portability | Multi-platform install listed |
| Maintenance Maturity | MIT + version |

**Estimated score: ~80/100 · Gold**

---

## thedotmack/claude-mem (82k★)

| Dimension | Pattern observed |
|-----------|-----------------|
| Trigger Clarity | Narrow scope, clear trigger |
| Instruction Specificity | Simple procedure; few edge cases handled |
| Reference Density | No bundled reference data |
| Verifiability | Minimal output spec |
| Tradeoff Transparency | Memory persistence limitations stated |
| Portability | Claude Code only |
| Maintenance Maturity | License present; no CHANGELOG |

**Estimated score: ~65/100 · Silver**

---

## JuliusBrussee/caveman (73k★)

| Dimension | Pattern observed |
|-----------|-----------------|
| Trigger Clarity | Very narrow scope; clear trigger |
| Instruction Specificity | Concrete rule set; no ambiguity |
| Reference Density | Embedded benchmark data; real LLM comparison results |
| Verifiability | Control arm test methodology; pass/fail criteria defined |
| Tradeoff Transparency | Explicitly narrow — "only for X use case" |
| Portability | Limited harness support; narrow scope |
| Maintenance Maturity | License + version |

**Estimated score: ~85/100 · Elite**

---

## OthmanAdi/planning-with-files (23k★)

| Dimension | Pattern observed |
|-----------|-----------------|
| Trigger Clarity | 2 trigger conditions; i18n version available |
| Instruction Specificity | Step-by-step; some branching |
| Reference Density | Template files; thin on data |
| Verifiability | Output format defined |
| Tradeoff Transparency | Briefly mentions scope limits |
| Portability | Multi-harness; i18n (EN/FR/ES) |
| Maintenance Maturity | License + CHANGELOG + CONTRIBUTING |

**Estimated score: ~76/100 · Gold**

---

## NeoLabHQ/context-engineering-kit

| Dimension | Pattern observed |
|-----------|-----------------|
| Trigger Clarity | Moderate; 2–3 conditions |
| Instruction Specificity | Procedure described; moderate branching |
| Reference Density | Reference data bundled |
| Verifiability | Output examples provided |
| Tradeoff Transparency | Mentions context window limits |
| Portability | Multi-harness |
| Maintenance Maturity | License present |

**Estimated score: ~79/100 · Gold**

---

## Dimension-level patterns across corpus

| Dimension | What top scorers do | What low scorers miss |
|-----------|--------------------|-----------------------|
| Trigger Clarity | List 4+ specific phrases; name NOT conditions | Generic one-liner description |
| Instruction Specificity | Numbered steps + conditional branches | "Help user with X" prose |
| Reference Density | Quantified bundled data files | Instructions only, no data |
| Verifiability | Evals + output template | No definition of "done" |
| Tradeoff Transparency | Named limitations + scope boundary | Implied universal applicability |
| Portability | Multi-harness + zero deps | Single platform, hardcoded paths |
| Maintenance Maturity | License + CHANGELOG + CONTRIBUTING | README only |
