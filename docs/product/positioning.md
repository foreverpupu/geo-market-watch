# Geo Market Watch — Product Positioning

## What This Repository Is

**A research framework evolving toward a developer toolkit.**

Geo Market Watch is a local-first, LLM-native framework for translating geopolitical events into structured market intelligence. It provides:

- **Structured Workflow** — From raw signals to trade ideas to performance tracking
- **Schema-Driven Outputs** — Deterministic, auditable event cards and analysis artifacts
- **Analyst-Review Process** — Human-in-the-loop approval and lifecycle management
- **Paper Performance Tracking** — Research-grade evaluation of idea quality

**Current Form:** Research framework with runnable local pipeline  
**Evolving Toward:** Developer toolkit for building custom geopolitical intelligence systems

---

## What This Repository Is Not

| This Is NOT | Why |
|-------------|-----|
| **Hosted SaaS Product** | No cloud service, no managed infrastructure |
| **Turnkey Investment System** | Requires integration with your data sources and workflows |
| **Live Trading Platform** | Paper tracking only, no broker integration |
| **Multi-User Backend** | Single-user local SQLite, no user management |
| **Production Scheduler** | No built-in cron, bring your own orchestration |
| **Real-Time Data Feed** | Manual or file-based input, no streaming ingestion |

**Important:** This is a framework you run locally, not a service you subscribe to.

---

## Primary Users / ICPs

### Ideal Users

1. **Macro Researchers**
   - Need systematic geopolitical event tracking
   - Want structured outputs for research papers
   - Value audit trail and reproducibility

2. **Quant Analysts**
   - Building event-driven signal systems
   - Need deterministic, backtestable frameworks
   - Want to integrate with existing data pipelines

3. **Asset Management Research Teams**
   - Formal idea generation and review process
   - Performance tracking for research quality
   - Compliance-friendly audit trails

4. **Developers / Technical Analysts**
   - Comfortable with CLI tools and Python
   - Want to customize and extend the framework
   - Building internal intelligence tools

### Non-Ideal Users

- Traders seeking one-click trade execution
- Teams needing managed cloud infrastructure
- Users requiring real-time streaming data
- Organizations needing multi-user collaboration features

---

## Supported Use Cases

### ✅ Personal Research
Individual analyst tracking geopolitical market impacts for personal research or trading decisions.

### ✅ Academic Research
Researchers studying geopolitical event transmission to markets, using structured outputs for papers.

### ✅ Internal Team Tool
Asset management teams using as internal idea generation and review workflow.

### ✅ Developer Prototyping
Developers building custom intelligence systems, using this as starting framework.

### ✅ Integration Foundation
Integrating the event schema and scoring logic into larger internal systems.

---

## Unsupported Use Cases

### ❌ Managed Service Offering
Running this as a hosted SaaS product for external clients without significant modification.

### ❌ Direct Client Delivery
Delivering raw framework outputs to paying clients as investment advice.

### ❌ Production Trading System
Using as primary decision engine for live trading without additional risk controls.

### ❌ White-Label Product
Reselling as turnkey geopolitical intelligence platform.

---

## Current Maturity Level

**v6.4 — Performance-Aware Research Platform**

| Capability | Status | Maturity |
|------------|--------|----------|
| Event Detection | ✅ | Production-ready |
| Signal Scoring | ✅ | Production-ready |
| Database Storage | ✅ | Production-ready |
| Trade Idea Generation | ✅ | Beta |
| Analyst Review Workflow | ✅ | Beta |
| Performance Tracking | ✅ | Beta |
| Multi-Agent System | 🔄 | Alpha (v7) |
| Risk Mapping | 🔄 | Planned (v7) |

**Stability:** Core engine (v5) is stable. Research layer (v6) is functional but evolving. Multi-agent layer (v7) is experimental.

---

## Adoption Path

### Phase 1: Evaluation (1-2 weeks)
- Run minimal example
- Explore database schema
- Review output formats
- Assess fit with your workflow

### Phase 2: Integration (2-4 weeks)
- Connect your data sources
- Customize event schemas
- Adapt scoring logic
- Build internal tooling

### Phase 3: Production Use (ongoing)
- Deploy in your infrastructure
- Integrate with research workflow
- Extend with custom agents
- Contribute improvements back

---

## Commercial Use Note

This project is released under MIT License, which permits commercial use. However:

- **No Warranty** — Provided as-is without guarantees
- **No Support** — Community support only, no SLA
- **Self-Hosted** — You run it, you maintain it
- **Attribution Required** — Must include license and copyright notice

For commercial integration questions, see [Commercial Use Guidelines](commercial-use.md).

---

## Summary

**Geo Market Watch is:**
- A research framework for structured geopolitical intelligence
- A local toolkit you customize and run yourself
- An evolving open-source project

**Geo Market Watch is not:**
- A managed service or SaaS product
- A turnkey investment system
- A replacement for your existing research infrastructure

**Best for:** Technical analysts and research teams who want a structured, auditable workflow for geopolitical market intelligence.
