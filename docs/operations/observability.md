# Observability Guide

## Overview

Geo Market Watch provides structured logging, metrics, and audit trails for monitoring system behavior and debugging issues.

---

## Logging

### Log Levels

| Level | Use Case |
|-------|----------|
| DEBUG | Detailed processing steps |
| INFO | Normal operations |
| WARNING | Recoverable issues |
| ERROR | Failures requiring attention |

### Structured Log Format

```json
{
  "timestamp": "2026-03-15T10:30:00Z",
  "level": "INFO",
  "event_id": "evt_001",
  "stage": "normalization",
  "message": "Event normalized successfully",
  "data": {
    "input_headline": "Red Sea shipping disruption",
    "output_category": "shipping",
    "confidence": 0.95
  }
}
```

### Logged Fields

**Per Event Processing:**
- `event_id` — Unique event identifier
- `ingest_timestamp` — When event was received
- `normalization_result` — Success/failure with details
- `dedupe_decision` — Is duplicate? Reason?
- `dedupe_reason` — Why flagged as duplicate
- `score` — Final score (0-10)
- `score_breakdown` — Component scores
- `trigger_decision` — Monitor or analyze?
- `trigger_reason` — Escalation rationale
- `output_path` — Where output was written
- `review_status` — Analyst review state

---

## Metrics

### Core Metrics

| Metric | Description | Type |
|--------|-------------|------|
| `events_processed` | Total events ingested | Counter |
| `duplicates_filtered` | Events deduplicated | Counter |
| `escalations_raised` | Full analysis triggers | Counter |
| `notifications_emitted` | Output files generated | Counter |
| `failures` | Processing errors | Counter |
| `processing_time_ms` | Event processing duration | Histogram |

### Example Metrics Output

```
=== Geo Market Watch Run Summary ===
Timestamp: 2026-03-15T10:30:00Z
Duration: 1.2s

Events Processed: 10
Duplicates Filtered: 2
Escalations Raised: 4
Notifications Emitted: 8
Failures: 0

Score Distribution:
  Low (0-3): 2
  Medium (4-6): 2
  High (7-8): 4
  Critical (9-10): 2

Top Categories:
  shipping: 4
  energy: 3
  sanctions: 2
  conflict: 1
```

---

## Audit Trail

### Event Lifecycle Tracking

```
event_001
  ├── [10:00:00] INGESTED
  ├── [10:00:01] NORMALIZED (category: shipping)
  ├── [10:00:01] DEDUPE_CHECK (is_duplicate: false)
  ├── [10:00:02] SCORED (score: 8, band: high)
  ├── [10:00:02] ESCALATED (decision: full_analysis)
  ├── [10:00:03] ANALYSIS_GENERATED
  ├── [10:00:03] NOTIFICATION_EMITTED
  └── [10:00:03] COMPLETED
```

### Review Status Tracking

```
event_001
  ├── ANALYSIS_GENERATED
  ├── PENDING_REVIEW
  ├── REVIEWED (analyst: amy, decision: approve)
  ├── TRACKING_STARTED (entry: $100.00)
  ├── TRACKING_CLOSED (exit: $115.00, return: +15%)
  └── POSTMORTEM_SCHEDULED (30d)
```

---

## Sample Run Log

```
2026-03-15T10:00:00Z [INFO] Starting agent loop
2026-03-15T10:00:00Z [INFO] Loaded 10 events from intake

2026-03-15T10:00:01Z [INFO] Processing event_001
2026-03-15T10:00:01Z [DEBUG] Normalizing: "Red Sea shipping disruption..."
2026-03-15T10:00:01Z [INFO] Normalized: category=shipping, region=Middle East
2026-03-15T10:00:01Z [DEBUG] Dedupe check: hash=abc123
2026-03-15T10:00:01Z [INFO] Dedupe: is_duplicate=false
2026-03-15T10:00:02Z [DEBUG] Scoring: severity=high, scope=global, immediacy=immediate
2026-03-15T10:00:02Z [INFO] Scored: 8/10 (band: high)
2026-03-15T10:00:02Z [INFO] Escalation: full_analysis (supply chain disruption)
2026-03-15T10:00:03Z [INFO] Analysis generated: outputs/analysis_event_001.md
2026-03-15T10:00:03Z [INFO] Notification emitted: outputs/notify_event_001.md

2026-03-15T10:00:04Z [INFO] Processing event_002
2026-03-15T10:00:04Z [INFO] Normalized: category=conflict, region=Eastern Europe
2026-03-15T10:00:04Z [INFO] Dedupe: is_duplicate=true (similar to event_045)
2026-03-15T10:00:04Z [INFO] Skipping duplicate

2026-03-15T10:00:05Z [INFO] Run complete
2026-03-15T10:00:05Z [INFO] Summary: 10 processed, 2 duplicates, 8 escalations, 0 failures
```

---

## Enabling Logging

### Basic Logging

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
```

### Structured Logging (JSON)

```python
import json
import logging

class JSONFormatter(logging.Formatter):
    def format(self, record):
        return json.dumps({
            'timestamp': self.formatTime(record),
            'level': record.levelname,
            'message': record.getMessage(),
            'data': getattr(record, 'data', {})
        })

handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logger = logging.getLogger()
logger.addHandler(handler)
```

---

## Monitoring Dashboard

### Key Indicators to Watch

1. **Escalation Rate** — Should be 20-40% of events
2. **Duplicate Rate** — Should be <30% of events
3. **Failure Rate** — Should be <5%
4. **Processing Time** — Should be <2s per event

### Alert Conditions

- Failure rate > 10%
- Processing time > 5s per event
- No events processed in 24h (if scheduled)

---

## Debugging with Logs

### Common Issues

**Issue:** Event not escalating  
**Check:** Score breakdown in logs
```
[DEBUG] Score breakdown: severity=3, scope=2, immediacy=2, total=7
```

**Issue:** Duplicate not detected  
**Check:** Dedupe hash comparison
```
[DEBUG] Dedupe: hash_1=abc123, hash_2=def456, match=False
```

**Issue:** Output not generated  
**Check:** Error in analysis generation
```
[ERROR] Analysis failed: template not found
```

---

## Best Practices

1. **Log at appropriate level** — DEBUG for details, INFO for milestones
2. **Include context** — Always log event_id for traceability
3. **Structured data** — Use JSON for machine parsing
4. **Rotate logs** — Don't let logs grow unbounded
5. **Monitor metrics** — Set up alerts for anomaly detection
