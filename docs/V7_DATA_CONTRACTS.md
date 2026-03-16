# v7.0 Data Contracts

## Contract Goals

This document defines proposed typed interfaces for Source Confidence and Fog of War. These are **design contracts, not yet implemented models**.

The goal is to specify concrete field-level contracts that can guide future implementation without ambiguity.

---

## Proposed Typed Objects

### SourceAssessment

Assessment of evidence quality and reliability provenance for a raw intake item.

### FogOfWarAssessment

Assessment of situational uncertainty and contestation state.

### EvidenceEnvelope

Container that associates assessments with events for downstream processing.

### ReviewConstraint

Explicit constraints passed to analyst review based on assessments.

---

## Source Confidence Contract

### Minimal Schema (Required)

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `confidence_level` | Enum | Discrete confidence tier | Values: `low`, `medium`, `high` |
| `source_type` | Enum | Category of source | Values: `official`, `verified_media`, `social_media`, `anonymous` |
| `assessed_at` | ISO8601 | When assessment was made | Required, auto-generated |

### Extended Schema (Optional Enrichment)

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `confidence_score` | Float | Continuous confidence [0.0, 1.0] | Optional, derived from level |
| `corroboration_state` | Enum | Verification status | Values: `unconfirmed`, `single_source`, `multi_source`, `verified` |
| `provenance_notes` | String | Human-readable provenance | Optional, max 500 chars |
| `assessed_by` | String | Agent or analyst ID | Optional, default to agent ID |
| `source_count` | Int | Number of corroborating sources | Optional, min 1 |

### Enum Definitions

```python
# Pseudocode - for specification only

class ConfidenceLevel(Enum):
    LOW = "low"      # Anonymous, unverified, or conflicting claims
    MEDIUM = "medium"  # Single verified source or multiple unverified
    HIGH = "high"    # Multiple verified sources or official confirmation

class SourceType(Enum):
    OFFICIAL = "official"           # Government, company official statements
    VERIFIED_MEDIA = "verified_media"  # Reuters, Bloomberg, etc.
    SOCIAL_MEDIA = "social_media"     # Twitter, Reddit, etc.
    ANONYMOUS = "anonymous"          # Unattributed claims

class CorroborationState(Enum):
    UNCONFIRMED = "unconfirmed"      # No external verification
    SINGLE_SOURCE = "single_source"  # One source only
    MULTI_SOURCE = "multi_source"    # Multiple independent sources
    VERIFIED = "verified"            # Official or on-the-ground confirmation
```

### Recommended Minimal Schema

For v7.0 MVP, use only:
- `confidence_level` (required)
- `source_type` (required)
- `assessed_at` (auto-generated)

### Recommended Extended Schema

For v7.1+ enrichment, add:
- `confidence_score` (calculated from level)
- `corroboration_state` (if corroboration tracking implemented)
- `source_count` (if multi-source tracking implemented)

---

## Fog of War Contract

### Minimal Schema (Required)

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `fog_of_war` | Boolean | Whether event is in fog state | Required |
| `fog_reason` | Enum | Why fog state applies | Values: `breaking`, `contested`, `evolving`, `disinformation` |
| `review_required` | Boolean | Whether analyst review is mandatory | Required, derived from fog_reason |

### Extended Schema (Optional Enrichment)

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `contested_claims` | List[String] | Specific claims being contested | Optional, max 5 items |
| `confirmation_gap` | Duration | Time since first report without confirmation | Optional, ISO8601 duration |
| `time_sensitivity` | Enum | Urgency of resolution | Values: `immediate`, `urgent`, `routine` |
| `stabilization_state` | Enum | Whether situation is stabilizing | Values: `worsening`, `stable`, `improving`, `resolved` |
| `fog_assessed_at` | ISO8601 | When fog state was assessed | Auto-generated |
| `fog_assessed_by` | String | Agent or analyst ID | Optional |

### Enum Definitions

```python
# Pseudocode - for specification only

class FogReason(Enum):
    BREAKING = "breaking"           # Within first 24-48 hours
    CONTESTED = "contested"         # Multiple conflicting claims
    EVOLVING = "evolving"           # Rapidly changing situation
    DISINFORMATION = "disinformation"  # Active disinformation campaign

class TimeSensitivity(Enum):
    IMMEDIATE = "immediate"  # Decisions needed within hours
    URGENT = "urgent"        # Decisions needed within 24h
    ROUTINE = "routine"      # Standard processing timeline

class StabilizationState(Enum):
    WORSENING = "worsening"    # Situation becoming less clear
    STABLE = "stable"          # No significant changes
    IMPROVING = "improving"    # Clarity increasing
    RESOLVED = "resolved"      # Fog cleared, situation confirmed
```

### Recommended Minimal Schema

For v7.0 MVP, use only:
- `fog_of_war` (required)
- `fog_reason` (required)
- `review_required` (derived: true if fog_reason in [breaking, contested, disinformation])

### Recommended Extended Schema

For v7.1+ enrichment, add:
- `confirmation_gap` (if temporal tracking implemented)
- `stabilization_state` (if situation tracking implemented)
- `contested_claims` (if claim-level tracking implemented)

---

## Attachment Points

### SourceAssessment Attachment

| Attachment Point | Rationale | Recommendation |
|------------------|-----------|----------------|
| `RawIntakeItem` | Source confidence is fundamentally about the source | **Primary** |
| `NormalizedEvent` | Downstream stages need aggregated confidence | **Secondary** |

**Preferred Primary**: `RawIntakeItem`
**Justification**: Confidence is an assessment of the intake source, not the derived event. Aggregation to event level happens during normalization.

### FogOfWarAssessment Attachment

| Attachment Point | Rationale | Recommendation |
|------------------|-----------|----------------|
| `NormalizedEvent` | Fog is a situational assessment of the event | **Primary** |
| `ScoreResult` | Fog could constrain scoring | **Secondary** |
| `TriggerResult` | Fog could constrain trigger | **Secondary** |

**Preferred Primary**: `NormalizedEvent`
**Justification**: Fog of War is a situational state that applies to the event itself, not just the scoring or trigger decision.

---

## Lifecycle and Mutation Rules

### SourceAssessment Lifecycle

| Stage | Action | Allowed? | Notes |
|-------|--------|----------|-------|
| Intake | Initialize | Yes | Default based on source type |
| Source Assessment | Enrich | Yes | Add corroboration info |
| Normalization | Aggregate | Yes | Combine multiple source assessments |
| Scoring | Read-only | Yes | Use for scoring constraints |
| Review | Annotate | Yes | Analyst adds notes, doesn't override |
| Tracking | Update | No | Source confidence should not change post-normalization |

### FogOfWarAssessment Lifecycle

| Stage | Action | Allowed? | Notes |
|-------|--------|----------|-------|
| Normalization | Initialize | Yes | Default based on time since publication |
| Evidence Assessment | Update | Yes | Add corroboration or contestation info |
| Scoring | Read-only | Yes | Use for trigger constraints |
| Review | Update | Yes | Analyst can clear fog if situation resolved |
| Tracking | Update | Yes | Time-based decay or explicit resolution |

### Override Rules

1. **Later stages may NOT override Source Confidence**: Once assessed, confidence is immutable.
2. **Later stages MAY update Fog of War**: Fog is situational and can improve or worsen.
3. **Analysts may annotate but not override**: Analyst judgment is recorded separately.

### Auditability Expectations

- All assessments must include `assessed_at` timestamp
- All assessments must include `assessed_by` (agent or analyst ID)
- Changes to Fog of War must be logged with before/after values
- Source Confidence changes (if any) require explicit justification

---

## Example Object Shapes

### Example 1: High-Confidence Low-Fog Event

```json
{
  "event_id": "evt-001-red-sea",
  "headline": "Major carriers announce rerouting around Africa due to Red Sea security concerns",
  
  "source_assessment": {
    "confidence_level": "high",
    "source_type": "verified_media",
    "corroboration_state": "multi_source",
    "source_count": 3,
    "assessed_at": "2024-01-12T10:30:00Z",
    "assessed_by": "source-agent-v1"
  },
  
  "fog_of_war_assessment": {
    "fog_of_war": false,
    "fog_reason": null,
    "review_required": false,
    "fog_assessed_at": "2024-01-12T10:30:00Z"
  },
  
  "score_result": {
    "score": 8.5,
    "band": "full_analysis",
    "trigger": true
  }
}
```

### Example 2: Medium-Confidence High-Fog Event

```json
{
  "event_id": "evt-002-attack-claims",
  "headline": "Unconfirmed reports of attack on shipping vessel",
  
  "source_assessment": {
    "confidence_level": "medium",
    "source_type": "social_media",
    "corroboration_state": "single_source",
    "source_count": 1,
    "provenance_notes": "First report from regional journalist, awaiting confirmation",
    "assessed_at": "2024-01-15T14:20:00Z",
    "assessed_by": "source-agent-v1"
  },
  
  "fog_of_war_assessment": {
    "fog_of_war": true,
    "fog_reason": "contested",
    "contested_claims": [
      "Attack occurred at 14:00 UTC",
      "Vessel was carrying LNG",
      "No casualties reported"
    ],
    "confirmation_gap": "PT2H",
    "review_required": true,
    "time_sensitivity": "urgent",
    "stabilization_state": "worsening",
    "fog_assessed_at": "2024-01-15T14:20:00Z"
  },
  
  "score_result": {
    "score": 6.0,
    "band": "monitor",
    "trigger": false,
    "trigger_reason": "High fog of war - deferring to analyst review"
  }
}
```

### Example 3: Low-Confidence High-Importance Event

```json
{
  "event_id": "evt-003-sanctions-rumor",
  "headline": "Rumors of new sanctions on technology exports",
  
  "source_assessment": {
    "confidence_level": "low",
    "source_type": "anonymous",
    "corroboration_state": "unconfirmed",
    "source_count": 1,
    "provenance_notes": "Anonymous post on trading forum, no verification",
    "assessed_at": "2024-01-18T09:00:00Z",
    "assessed_by": "source-agent-v1"
  },
  
  "fog_of_war_assessment": {
    "fog_of_war": true,
    "fog_reason": "disinformation",
    "review_required": true,
    "time_sensitivity": "routine",
    "stabilization_state": "stable",
    "fog_assessed_at": "2024-01-18T09:00:00Z"
  },
  
  "score_result": {
    "score": 7.5,
    "band": "full_analysis",
    "trigger": false,
    "trigger_reason": "High importance but low confidence + high fog - suppress pending review"
  },
  
  "review_constraint": {
    "mandatory_review": true,
    "review_reason": "Low confidence source with high market impact potential",
    "escalation_required": true
  }
}
```

---

## Implementation Guardrails

### What Future Implementation Must NOT Do

1. **Do not collapse confidence into score**: Source Confidence and Score are orthogonal. High confidence does not mean high score.

2. **Do not treat fog_of_war as synonym for false**: Fog of War is uncertainty, not falsity. Events in fog may still be true.

3. **Do not let trigger decisions hide uncertainty metadata**: If fog affects trigger, the fog assessment must be visible in output.

4. **Do not allow prompt-only hidden reasoning**: All assessment logic must produce explicit typed fields, not just prompt text.

5. **Do not allow confidence to change post-normalization**: Source Confidence is immutable after initial assessment.

6. **Do not require fog for all events**: Fog of War is an exceptional state, not the default.

### What Future Implementation SHOULD Do

1. **Default confidence by source type**: Official sources default to high, anonymous to low.

2. **Derive review_required from fog_reason**: Breaking/contested/disinformation → true; evolving → false.

3. **Log all assessment changes**: Fog of War updates must be auditable.

4. **Expose assessments in analyst UI**: Analysts must see confidence and fog when reviewing.

5. **Support time-based fog decay**: Fog should automatically reduce after 24-48 hours unless renewed.

---

## Summary

This document specifies:

1. **Source Confidence Contract**: Minimal (3 fields) and Extended (7 fields) schemas
2. **Fog of War Contract**: Minimal (3 fields) and Extended (7 fields) schemas
3. **Attachment Points**: SourceAssessment → RawIntakeItem; FogOfWarAssessment → NormalizedEvent
4. **Lifecycle Rules**: Confidence immutable, Fog mutable, both auditable
5. **Worked Examples**: 3 concrete object shapes showing different confidence/fog combinations
6. **Implementation Guardrails**: 6 prohibitions and 5 recommendations for future implementers

These contracts are ready for implementation in a future v7.0 work order.
