# v7.0 Design Prework

## Purpose and Non-Goals

**Purpose**: This document prepares the conceptual foundation for v7.0's Source Confidence and Fog of War features without destabilizing the current v6.x codebase.

**Non-Goals**:
- No runtime behavior is changed
- No business logic is implemented
- No database migrations are added
- No placeholder agent implementations are created
- No speculative framework code is introduced

This is a design-only document to establish typed contracts and lifecycle semantics before implementation.

---

## Current State Summary

### Current Pipeline (v6.x)

The current pipeline operates on typed models through these stages:

1. **Intake/Scout** → `RawIntakeItem` (dict-like boundary, immediately typed)
2. **Normalization** → `NormalizedEvent` (structured event card)
3. **Deduplication** → Filter against `DedupeMemory`
4. **Scoring** → `ScoreResult` (0-10 impact assessment)
5. **Trigger** → `TriggerResult` (escalation decision)
6. **Output** → `NotificationArtifact` (analyst handoff)

### Where v7.0 Concepts Attach

| Concept | Current Stage | v7.0 Attachment Point |
|---------|---------------|----------------------|
| Source Confidence | Not present | Post-intake, pre-normalization |
| Fog of War | Not present | Parallel to scoring, affects trigger |

---

## Design Principles

1. **Facts ≠ Judgments**: Raw intake items are factual claims. Source Confidence is an assessment of those claims.

2. **Confidence ≠ Importance**: High confidence does not mean high market impact. These are orthogonal dimensions.

3. **Fog of War ≠ Low Confidence**: Fog of War is a situational uncertainty state, not merely low source reliability.

4. **Decision Constraints Must Be Explicit**: Any constraint on trigger, review, or analyst escalation must be explicit and auditable.

5. **Typed Object Exchange**: Future agents must exchange typed objects (`SourceAssessment`, `FogOfWarAssessment`), not raw prompt text.

---

## v7.0 Conceptual Pipeline

```
Intake/Scout
    ↓
Source Assessment ← Source Confidence attached here
    ↓
Normalization → NormalizedEvent
    ↓
Deduplication
    ↓
Evidence Assessment ← Fog of War assessed here
    ↓
Scoring/Trigger ← Both assessments constrain decisions
    ↓
Analysis/Review ← Analyst sees both assessments
    ↓
Invalidation/Tracking ← Assessments may be updated over time
```

### Stage Responsibilities

| Stage | Reads | Writes |
|-------|-------|--------|
| Intake | Raw signals | `RawIntakeItem` |
| Source Assessment | `RawIntakeItem` | `SourceAssessment` |
| Normalization | `RawIntakeItem`, `SourceAssessment` | `NormalizedEvent` |
| Evidence Assessment | `NormalizedEvent`, external corroboration | `FogOfWarAssessment` |
| Scoring/Trigger | `NormalizedEvent`, `SourceAssessment`, `FogOfWarAssessment` | `ScoreResult`, `TriggerResult` |
| Analysis/Review | All assessments | Review decision, potential invalidation |

---

## Source Confidence Semantics

### Definition

Source Confidence is an **assessment of evidence quality and reliability provenance**. It answers: "How much should we trust this claim?"

### Distinctions

| Concept | What It Measures | Example |
|---------|------------------|---------|
| Source Confidence | Evidence quality/reliability | "Reuters with 3 corroborating sources" |
| Market Importance | Potential market impact | "Shipping disruption affects 30% of trade" |
| Severity | Event intensity | "Major route closure" |
| Trigger Score | Escalation threshold | "8/10 → Full analysis" |

### Attachment Points

**Primary**: `RawIntakeItem` (per-source assessment)
**Secondary**: `NormalizedEvent` (aggregated confidence)

Rationale: Source Confidence is fundamentally about the intake source, not the derived event. However, downstream stages need access to aggregated confidence on the normalized event.

### Schema Preference

**Minimal Schema** (required):
- `confidence_level`: Enum [low, medium, high]
- `source_type`: Enum [official, verified_media, social_media, anonymous]
- `assessed_at`: Timestamp

**Extended Schema** (optional enrichment):
- `confidence_score`: Float [0.0, 1.0]
- `corroboration_state`: Enum [unconfirmed, single_source, multi_source, verified]
- `provenance_notes`: String
- `assessed_by`: String (agent or analyst ID)

---

## Fog of War Semantics

### Definition

Fog of War is an **uncertainty/contestation state around fast-moving or weakly confirmed situations**. It answers: "Is this situation still unfolding or contested?"

### Distinctions

| Concept | What It Measures | Example |
|---------|------------------|---------|
| Fog of War | Situational uncertainty | "Claims and counterclaims about attack" |
| Source Confidence | Source reliability | "Reuters says X, but still unconfirmed" |
| Invalidation | Post-hoc rejection | "Event was fabricated" |

### When Fog of War Applies

- Multiple conflicting claims about the same event
- Rapidly evolving situation with incomplete information
- Deliberate information warfare or disinformation campaigns
- Breaking news within first 24-48 hours

### Downstream Constraints

| Fog State | Trigger Behavior | Review Behavior |
|-----------|------------------|-----------------|
| High Fog | Defer automatic trigger; queue for analyst | Mandatory analyst review |
| Medium Fog | Trigger with warning annotation | Enhanced review UI |
| Low Fog | Normal trigger behavior | Standard review |

### Schema Preference

**Minimal Schema** (required):
- `fog_of_war`: Boolean
- `fog_reason`: Enum [breaking, contested, evolving, disinformation]
- `review_required`: Boolean

**Extended Schema** (optional enrichment):
- `contested_claims`: List[String]
- `confirmation_gap`: Duration
- `time_sensitivity`: Enum [immediate, urgent, routine]
- `stabilization_state`: Enum [worsening, stable, improving, resolved]

---

## Decision Impact Matrix

| Source Confidence | Fog of War | Trigger Action | Review Action | Example |
|-------------------|------------|----------------|---------------|---------|
| High | Low | Normal trigger | Standard review | Confirmed Reuters report of route closure |
| High | High | Defer + flag | Mandatory analyst review | Reuters reports attack, but claims contested |
| Low | Low | Suppress or low-priority queue | Optional review | Anonymous social media claim, no corroboration |
| Low | High | Suppress + analyst queue | Mandatory review | Anonymous claim during active disinformation campaign |
| Medium | Medium | Trigger with warning | Enhanced review | Single-source report from verified journalist |

### Key Insights

- **High Confidence + High Fog**: Trust the source, but situation is unclear. Require analyst judgment.
- **Low Confidence + Low Fog**: Source is weak, but situation is stable. Can suppress without urgency.
- **Low Confidence + High Fog**: Dangerous combination. Suppress and require analyst review to avoid amplifying disinformation.

---

## Open Questions for v7.0

### Unresolved Design Decisions

1. **Confidence Aggregation**: How should confidence from multiple sources be aggregated when normalizing into a single event?
   - Options: Minimum, average, weighted by source tier
   - Recommendation: Weighted by source tier, with minimum floor

2. **Fog Decay**: Should Fog of War automatically decay over time, or require explicit confirmation to clear?
   - Options: Time-based decay, explicit resolution, hybrid
   - Recommendation: Hybrid with time-based decay + explicit resolution override

3. **Analyst Override**: Should analysts be able to override automated confidence/fog assessments?
   - Options: Yes (full override), No (read-only), Annotate only
   - Recommendation: Annotate only; analyst judgment recorded separately

4. **Audit Trail**: How long should confidence/fog assessment history be retained?
   - Options: Current only, last N versions, full history
   - Recommendation: Full history for compliance; current for runtime

### Likely Migration Concerns

- **Backward Compatibility**: v6.x events have no confidence/fog data. Default values needed.
- **Database Schema**: New fields required. Migration strategy needed.
- **UI/UX**: Analyst interfaces need new confidence/fog visualization.

### Human Policy Choices Required

- [ ] Define official source tier list (Reuters, Bloomberg, etc.)
- [ ] Define corroboration thresholds (how many sources = "verified")
- [ ] Define fog decay time constants (24h? 48h? 7d?)
- [ ] Define mandatory review triggers (high fog + high importance?)

---

## Summary

This document establishes:

1. **Source Confidence** as a source-level assessment of evidence quality
2. **Fog of War** as a situational uncertainty state
3. **Explicit contracts** for both concepts with minimal and extended schemas
4. **Decision impact matrix** showing how combinations affect trigger and review
5. **Open questions** requiring human policy decisions before implementation

Next step: `V7_DATA_CONTRACTS.md` for concrete field-level specifications.
