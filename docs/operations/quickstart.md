# Quick Start Guide

**Get up and running in 10 minutes.**

---

## Prerequisites

- Python 3.10 or higher
- OpenAI API key (or compatible local LLM)
- Git

---

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/geo-market-watch.git
cd geo-market-watch

# Install dependencies
pip install -r requirements.txt

# Set your OpenAI API key
export OPENAI_API_KEY="your-key-here"
```

---

## 5-Minute Demo

### 1. Initialize the Database

```bash
python scripts/init_database.py --db data/geo_alpha.db
```

This creates a local SQLite database for storing events and analysis.

### 2. Run the Minimal Example

```bash
python scripts/run_agent_loop.py \
  --input examples/minimal_event.json \
  --output outputs/
```

This processes a sample geopolitical event through the full pipeline.

### 3. View the Output

```bash
cat outputs/notification.md
```

You should see a structured analysis including:
- Event scoring (0-10)
- Sector exposure mapping
- Trade ideas with invalidation conditions
- Monitoring plan

---

## What Just Happened?

The agent loop performed these steps:

1. **Intake** — Loaded the raw event from JSON
2. **Normalization** — Converted to structured event card
3. **Scoring** — Determined signal strength (8/10)
4. **Trigger** — Escalated to full analysis
5. **Analysis** — Generated market intelligence
6. **Output** — Created notification with trade ideas

---

## Next Steps

### Try Your Own Event

Create a file `my_event.json`:

```json
{
  "items": [
    {
      "id": "my-event-001",
      "headline": "Your headline here",
      "summary": "Brief description",
      "source": "News Source",
      "region": "Region Name",
      "category": "category",
      "timestamp": "2026-03-15T10:00:00Z"
    }
  ]
}
```

Run it:

```bash
python scripts/run_agent_loop.py \
  --input my_event.json \
  --output outputs/
```

### Explore the Database

```bash
# List all events
python scripts/query_database.py --db data/geo_alpha.db --list

# Show statistics
python scripts/query_database.py --db data/geo_alpha.db --stats

# Filter by region
python scripts/query_database.py --db data/geo_alpha.db --region "Middle East"
```

### Track a Trade Idea

```bash
# Start tracking (requires approved idea in database)
python scripts/start_idea_tracking.py \
  --db data/geo_alpha.db \
  --idea-id YOUR_ID \
  --entry-price 100.0 \
  --entry-time 2026-03-15T09:30:00Z

# View tracked ideas
python scripts/list_tracked_ideas.py --db data/geo_alpha.db
```

---

## Common Issues

**"No module named 'openai'"**
```bash
pip install openai
```

**"Database not found"**
```bash
python scripts/init_database.py --db data/geo_alpha.db
```

**"API key not set"**
```bash
export OPENAI_API_KEY="your-key"
# Or add to .env file
```

---

## Learn More

- [System Architecture](institutional-system-architecture.md) — Understand the four layers
- [Signal Scoring](signal-scoring.md) — How events become scores
- [Performance Tracking](performance-methodology.md) — Paper-trade evaluation
- [Full Documentation Map](../README.md#documentation-map)

---

**Ready to build your own geopolitical intelligence pipeline?** Start with the [minimal example](../examples/minimal_event.json) and extend from there.
