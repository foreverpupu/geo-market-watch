# Geo Alpha Database Specification

This document specifies the minimal event database layer for Geo Market Watch v6.

---

## Overview

**Geo Alpha Database** is the first persistent storage layer for Geo Market Watch.

It stores outputs produced by the v5.5 agent loop, enabling:
- Historical event tracking
- Benchmarkable event history
- Simple event search/filtering
- Future dashboard compatibility
- Future alpha pattern mining

---

## Design Principles

### Local-First
- SQLite database (file-based)
- Zero infrastructure
- Zero external dependencies
- Easy to inspect and query

### Minimal Scope
- NOT a production database service
- NOT a web dashboard
- NOT a live hosted API
- NOT a multi-user backend

This is a **minimal local database** for storing and querying event artifacts.

---

## Technology Stack

| Component | Choice | Reason |
|-----------|--------|--------|
| Database | SQLite | Local-first, zero infrastructure |
| Access | sqlite3 (stdlib) | No ORM, no dependencies |
| Format | JSON + SQL | Human-readable and queryable |

**Not used in v6:**
- PostgreSQL, MySQL (too heavy)
- MongoDB (not needed)
- Elasticsearch (overkill)
- Vector DB (future consideration)
- Graph DB (future consideration)

---

## Database Schema

### Tables

#### 1. events
Canonical event records.

| Column | Type | Description |
|--------|------|-------------|
| event_id | TEXT PRIMARY KEY | Unique identifier |
| event_key | TEXT UNIQUE | Deduplication key |
| event_title | TEXT | Event name |
| date_detected | TEXT | Detection timestamp |
| region | TEXT | Geographic region |
| category | TEXT | Event category |
| summary | TEXT | Brief description |
| score | INTEGER | Signal score (0-10) |
| band | TEXT | Signal band |
| trigger_full_analysis | INTEGER | Boolean (0/1) |
| status | TEXT | active/archived |
| created_at | TEXT | Creation timestamp |
| updated_at | TEXT | Update timestamp |

#### 2. sources
Source metadata linked to events.

| Column | Type | Description |
|--------|------|-------------|
| source_id | TEXT PRIMARY KEY | Unique identifier |
| event_id | TEXT | Foreign key to events |
| source_name | TEXT | Publisher name |
| source_url | TEXT | Article URL |
| published_at | TEXT | Publication timestamp |

#### 3. indicators
Numeric signal dimensions.

| Column | Type | Description |
|--------|------|-------------|
| indicator_id | TEXT PRIMARY KEY | Unique identifier |
| event_id | TEXT | Foreign key to events |
| physical_disruption | INTEGER | Score 0-3 |
| transport_impact | INTEGER | Score 0-2 |
| policy_sanctions | INTEGER | Score 0-2 |
| market_transmission | INTEGER | Score 0-2 |
| escalation_risk | INTEGER | Score 0-1 |

#### 4. flags
Trigger flags.

| Column | Type | Description |
|--------|------|-------------|
| flag_id | TEXT PRIMARY KEY | Unique identifier |
| event_id | TEXT | Foreign key to events |
| confirmed_supply_disruption | INTEGER | Boolean (0/1) |
| strategic_transport_disruption | INTEGER | Boolean (0/1) |
| major_sanctions_escalation | INTEGER | Boolean (0/1) |
| military_escalation | INTEGER | Boolean (0/1) |

#### 5. notifications
Rendered notification artifacts.

| Column | Type | Description |
|--------|------|-------------|
| notification_id | TEXT PRIMARY KEY | Unique identifier |
| event_id | TEXT | Foreign key to events |
| notification_type | TEXT | monitor/full_analysis |
| file_path | TEXT | Path to file |
| content | TEXT | Markdown content |
| created_at | TEXT | Creation timestamp |

#### 6. watchlist
Optional affected companies/tickers.

| Column | Type | Description |
|--------|------|-------------|
| watchlist_id | TEXT PRIMARY KEY | Unique identifier |
| event_id | TEXT | Foreign key to events |
| company_name | TEXT | Company name |
| ticker | TEXT | Stock ticker |
| sector | TEXT | Industry sector |

---

## Usage

### Initialize Database

```bash
python scripts/init_database.py --db data/geo_alpha.db
```

### Seed with Sample Data

```bash
python scripts/seed_database.py --db data/geo_alpha.db --seed data/db-seed-events.json
```

### Query Events

```bash
# List all events
python scripts/query_database.py --db data/geo_alpha.db --list

# Filter by region
python scripts/query_database.py --db data/geo_alpha.db --region "Middle East"

# Show statistics
python scripts/query_database.py --db data/geo_alpha.db --stats
```

### Ingest Agent Loop Output

```bash
python scripts/ingest_artifacts.py \
  --db data/geo_alpha.db \
  --output agent_output.json \
  --notifications outputs/
```

---

## File Locations

| File | Purpose |
|------|---------|
| `data/geo_alpha.db` | Main database file |
| `data/db-seed-events.json` | Sample seed data |
| `engine/database_models.py` | Schema definitions |
| `engine/database.py` | CRUD operations |
| `engine/artifact_ingest.py` | Ingest logic |

---

## Future Expansion

Potential v6.5+ additions:
- PostgreSQL migration path
- Database migrations
- Backup/restore
- Replication
- Hosted option

Current v6 scope: SQLite only.

---

## Constraints

- Single-user (no auth)
- Local filesystem only
- No network access required
- No background processes
- Deterministic and reproducible
