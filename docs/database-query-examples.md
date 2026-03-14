# Database Query Examples

Common queries for the Geo Alpha Database.

---

## Setup

Connect to the database:

```bash
sqlite3 data/geo_alpha.db
```

Or use the query script:

```bash
python scripts/query_database.py --db data/geo_alpha.db [options]
```

---

## Basic Queries

### List All Events

```sql
SELECT event_id, event_title, score, band, region
FROM events
ORDER BY date_detected DESC;
```

### Count Events by Band

```sql
SELECT band, COUNT(*) as count
FROM events
GROUP BY band;
```

### Find High-Score Events

```sql
SELECT event_title, score, band
FROM events
WHERE score >= 7
ORDER BY score DESC;
```

---

## Filter Queries

### By Region

```sql
SELECT * FROM events
WHERE region = 'Middle East'
ORDER BY date_detected DESC;
```

### By Category

```sql
SELECT * FROM events
WHERE category = 'Maritime disruption';
```

### By Date Range

```sql
SELECT * FROM events
WHERE date_detected >= '2024-01-01'
ORDER BY date_detected;
```

### By Trigger Status

```sql
SELECT event_title, trigger_full_analysis
FROM events
WHERE trigger_full_analysis = 1;
```

---

## Join Queries

### Events with Sources

```sql
SELECT 
    e.event_title,
    e.region,
    s.source_name,
    s.source_url
FROM events e
JOIN sources s ON e.event_id = s.event_id;
```

### Events with Indicators

```sql
SELECT 
    e.event_title,
    e.score,
    i.physical_disruption,
    i.transport_impact,
    i.policy_sanctions,
    i.market_transmission,
    i.escalation_risk
FROM events e
JOIN indicators i ON e.event_id = i.event_id;
```

### Events with Flags

```sql
SELECT 
    e.event_title,
    f.confirmed_supply_disruption,
    f.strategic_transport_disruption,
    f.major_sanctions_escalation,
    f.military_escalation
FROM events e
JOIN flags f ON e.event_id = f.event_id;
```

---

## Aggregation Queries

### Events by Region

```sql
SELECT region, COUNT(*) as event_count
FROM events
GROUP BY region
ORDER BY event_count DESC;
```

### Events by Category

```sql
SELECT category, COUNT(*) as event_count
FROM events
GROUP BY category
ORDER BY event_count DESC;
```

### Average Score by Region

```sql
SELECT region, AVG(score) as avg_score
FROM events
GROUP BY region
ORDER BY avg_score DESC;
```

---

## Advanced Queries

### Events with Full Analysis Trigger

```sql
SELECT 
    e.event_title,
    e.score,
    e.band,
    f.confirmed_supply_disruption,
    f.major_sanctions_escalation
FROM events e
JOIN flags f ON e.event_id = f.event_id
WHERE e.trigger_full_analysis = 1
ORDER BY e.score DESC;
```

### Events with Notifications

```sql
SELECT 
    e.event_title,
    n.notification_type,
    n.file_path
FROM events e
JOIN notifications n ON e.event_id = n.event_id
ORDER BY n.created_at DESC;
```

### Complex Filter

```sql
SELECT 
    e.event_title,
    e.region,
    e.score,
    i.transport_impact,
    f.strategic_transport_disruption
FROM events e
JOIN indicators i ON e.event_id = i.event_id
JOIN flags f ON e.event_id = f.event_id
WHERE e.region = 'Middle East'
  AND i.transport_impact >= 2
  AND f.strategic_transport_disruption = 1
ORDER BY e.score DESC;
```

---

## Using the Query Script

### List All Events

```bash
python scripts/query_database.py --db data/geo_alpha.db --list
```

### Filter by Region

```bash
python scripts/query_database.py --db data/geo_alpha.db --region "Middle East"
```

### Filter by Band

```bash
python scripts/query_database.py --db data/geo_alpha.db --band full_analysis
```

### Show Statistics

```bash
python scripts/query_database.py --db data/geo_alpha.db --stats
```

### High-Signal Events

Query events that are escalation-worthy (score >= 7 or trigger_full_analysis = true):

```bash
python scripts/query_database.py --db data/geo_alpha.db --high-signal
```

This returns:
- High-scoring events (score >= 7)
- Full-analysis trigger events
- Priority review candidates

Use this for reviewing events that require immediate attention or deep analysis.

### Output as JSON

```bash
python scripts/query_database.py --db data/geo_alpha.db --list --json
```

---

## Python Examples

### Connect and Query

```python
from engine.database import connect_db, list_events, search_events

# Connect
conn = connect_db('data/geo_alpha.db')

# List all events
events = list_events(conn, limit=10)
for event in events:
    print(f"{event['event_title']}: {event['score']}")

# Search by region
results = search_events(conn, region='Middle East')
for event in results:
    print(f"{event['event_title']}: {event['region']}")

conn.close()
```

### Get Statistics

```python
from engine.database import connect_db, get_stats

conn = connect_db('data/geo_alpha.db')
stats = get_stats(conn)
print(f"Total events: {stats['total_events']}")
print(f"Regions: {stats['regions']}")
conn.close()
```

---

## Export Data

### Export to JSON

```bash
python scripts/query_database.py --db data/geo_alpha.db --list --json > events.json
```

### Export to CSV (via SQLite)

```bash
sqlite3 data/geo_alpha.db -csv "SELECT * FROM events" > events.csv
```

---

## Backup Database

```bash
cp data/geo_alpha.db data/geo_alpha_backup_$(date +%Y%m%d).db
```

---

## Notes

- All timestamps are ISO 8601 format
- Boolean values are stored as INTEGER (0/1)
- Foreign key constraints are enforced
- Indexes exist on commonly queried columns
