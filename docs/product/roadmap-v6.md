# Geo Market Watch v6.x Roadmap

**Continuous evolution from research framework to production-ready platform.**

---

## Roadmap Overview

| Version | Theme | Focus | Status |
|---------|-------|-------|--------|
| v6.1 | Onboarding | New user experience | ✅ Complete |
| v6.2 | Positioning | Product clarity | ✅ Complete |
| v6.3 | Docs Architecture | Information structure | ✅ Complete |
| v6.4 | Evaluation Framework | Quality assurance | ✅ Complete |
| v6.5 | Engine Refactor | Code organization | ✅ Complete |
| v6.6 | Observability Loop | Runtime monitoring | ✅ Complete |

---

## v6.1 — Onboarding
**Theme:** New user experience  
**Goal:** First-time users can understand and run the system in 10 minutes

### Deliverables
- ✅ README重构为产品着陆页
- ✅ 最小输入→输出闭环示例
- ✅ Quick Start指南
- ✅ 3分钟理解，10分钟跑通

### Key Changes
- What It Does / Who This Is For / What This Is Not
- Minimal End-to-End Example
- Documentation Map
- Example: Input → Output

**PR:** `Improve onboarding: restructure README and add minimal end-to-end example`

---

## v6.2 — Positioning
**Theme:** Product clarity  
**Goal:** Clear understanding of what this is, isn't, and how to use commercially

### Deliverables
- ✅ Product positioning document
- ✅ Commercial use guidelines
- ✅ Clear boundaries and limitations
- ✅ Target user profiles

### Key Changes
- Research framework → Developer toolkit positioning
- MIT License commercial use explanation
- 4-layer architecture documentation
- System value chain visualization

**PR:** `Clarify project positioning and usage boundaries`

---

## v6.3 — Docs Architecture
**Theme:** Information structure  
**Goal:** Documentation organized by concern, not chronologically

### Deliverables
- ✅ 5-layer documentation structure
- ✅ docs/README.md navigation hub
- ✅ Clear migration paths for existing docs
- ✅ Consistent cross-linking

### New Structure
```
docs/
├── product/          # Positioning, roadmap, adoption
├── architecture/     # System design, specs
├── evaluation/       # Benchmarks, validation
├── operations/       # Workflows, guides
└── research/         # Methodology, sources
```

**PR:** `Reorganize documentation structure for clarity`

---

## v6.4 — Evaluation Framework
**Theme:** Quality assurance  
**Goal:** Deterministic, versioned evaluation of analysis quality

### Deliverables
- ✅ 5-case benchmark suite
- ✅ Pipeline regression tests
- ✅ Benchmark design documentation
- ✅ Version evaluation report template

### Coverage
- Shipping disruption
- Sanctions/export controls
- Commodity supply shock
- Military escalation/fog of war
- Election/policy shock

**PR:** `Add evaluation framework and benchmark skeleton`

---

## v6.5 — Engine Refactor
**Theme:** Code organization  
**Goal:** Clear separation between business logic and CLI entry points

### Deliverables
- ✅ Engine vs Scripts boundary defined
- ✅ 16 engine modules (business logic)
- ✅ 17 CLI scripts (entry points)
- ✅ Code structure documentation

### Architecture
- **Engine:** Reusable, testable business logic
- **Scripts:** Thin CLI wrappers
- **Tests:** Unit + integration + pipeline

**PR:** `Refactor project structure: separate engine logic and entry scripts`

---

## v6.6 — Observability Loop
**Theme:** Runtime monitoring  
**Goal:** Complete feedback loop from analysis to learning

### Deliverables
- ✅ Structured logging and metrics
- ✅ Audit trail for event lifecycle
- ✅ Postmortem workflow (48h/7d/30d)
- ✅ 4 adoption paths (solo to enterprise)

### Capabilities
- Events processed, duplicates filtered, escalations raised
- Per-event tracking: ingest → normalize → score → escalate → output
- Postmortem: hypothesis → watchlist → outcome → lessons learned
- Adoption: Solo → Team → Engineering → Enterprise

**PR:** `Add observability, postmortem workflow and adoption paths`

---

## Evolution Summary

### From → To

| Aspect | Before v6.x | After v6.6 |
|--------|-------------|------------|
| **Documentation** | Flat, chronological | Layered by concern |
| **Onboarding** | Design doc homepage | Product landing page |
| **Positioning** | Unclear boundaries | Explicit is/is-not |
| **Quality** | Schema validation only | Benchmark + regression tests |
| **Code** | Mixed logic | Engine/Scripts separation |
| **Operations** | Run and forget | Monitor → Learn → Improve |

### System Maturity

```
v6.0  Database Foundation
  ↓
v6.1  Onboarding Experience
  ↓
v6.2  Product Positioning
  ↓
v6.3  Documentation Architecture
  ↓
v6.4  Evaluation Framework
  ↓
v6.5  Code Organization
  ↓
v6.6  Observability & Learning Loop
```

**Result:** From research prototype to continuous improvement platform

---

## Next Steps (v7.0+)

### Multi-Agent Intelligence Layer
- Risk mapping
- Pattern mining
- Strategy templates
- Automated postmortem

### Production Features
- Real-time data feeds
- Multi-user backend
- Hosted API option
- Enterprise support

---

## Contributing to Roadmap

### Suggest New Features
1. Open an issue with `roadmap` label
2. Describe use case and expected behavior
3. Reference relevant v6.x version theme

### Report Gaps
1. Which adoption path doesn't fit your needs?
2. What observability is missing?
3. Which benchmark case should be added?

---

**Current Status:** v6.6 Complete ✅  
**Next Milestone:** v7.0 Multi-Agent Intelligence
