"""
Geo Market Watch v6 — Database Models

Defines the SQLite schema for the minimal Geo Alpha Database.
"""

from typing import Dict, Any, List

# SQL statements for table creation
CREATE_TABLES_SQL = """
-- Events table: canonical event records
CREATE TABLE IF NOT EXISTS events (
    event_id TEXT PRIMARY KEY,
    event_key TEXT UNIQUE NOT NULL,
    event_title TEXT NOT NULL,
    date_detected TEXT NOT NULL,
    region TEXT NOT NULL,
    category TEXT NOT NULL,
    summary TEXT,
    score INTEGER,
    band TEXT,
    trigger_full_analysis INTEGER DEFAULT 0,
    status TEXT DEFAULT 'active',
    raw_data TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

-- Sources table: source metadata linked to events
CREATE TABLE IF NOT EXISTS sources (
    source_id TEXT PRIMARY KEY,
    event_id TEXT NOT NULL,
    source_name TEXT NOT NULL,
    source_url TEXT,
    published_at TEXT,
    FOREIGN KEY (event_id) REFERENCES events(event_id)
);

-- Indicators table: numeric signal dimensions
CREATE TABLE IF NOT EXISTS indicators (
    indicator_id TEXT PRIMARY KEY,
    event_id TEXT NOT NULL,
    physical_disruption INTEGER DEFAULT 0,
    transport_impact INTEGER DEFAULT 0,
    policy_sanctions INTEGER DEFAULT 0,
    market_transmission INTEGER DEFAULT 0,
    escalation_risk INTEGER DEFAULT 0,
    FOREIGN KEY (event_id) REFERENCES events(event_id)
);

-- Flags table: trigger flags
CREATE TABLE IF NOT EXISTS flags (
    flag_id TEXT PRIMARY KEY,
    event_id TEXT NOT NULL,
    confirmed_supply_disruption INTEGER DEFAULT 0,
    strategic_transport_disruption INTEGER DEFAULT 0,
    major_sanctions_escalation INTEGER DEFAULT 0,
    military_escalation INTEGER DEFAULT 0,
    FOREIGN KEY (event_id) REFERENCES events(event_id)
);

-- Notifications table: rendered notification artifacts
CREATE TABLE IF NOT EXISTS notifications (
    notification_id TEXT PRIMARY KEY,
    event_id TEXT NOT NULL,
    notification_type TEXT NOT NULL,
    file_path TEXT,
    content TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY (event_id) REFERENCES events(event_id)
);

-- Watchlist table: optional affected companies/tickers
CREATE TABLE IF NOT EXISTS watchlist (
    watchlist_id TEXT PRIMARY KEY,
    event_id TEXT NOT NULL,
    company_name TEXT,
    ticker TEXT,
    sector TEXT,
    FOREIGN KEY (event_id) REFERENCES events(event_id)
);

-- Create indexes for common queries
CREATE INDEX IF NOT EXISTS idx_events_date ON events(date_detected);
CREATE INDEX IF NOT EXISTS idx_events_region ON events(region);
CREATE INDEX IF NOT EXISTS idx_events_category ON events(category);
CREATE INDEX IF NOT EXISTS idx_events_band ON events(band);
CREATE INDEX IF NOT EXISTS idx_events_status ON events(status);
CREATE INDEX IF NOT EXISTS idx_sources_event ON sources(event_id);
CREATE INDEX IF NOT EXISTS idx_indicators_event ON indicators(event_id);
CREATE INDEX IF NOT EXISTS idx_flags_event ON flags(event_id);
CREATE INDEX IF NOT EXISTS idx_notifications_event ON notifications(event_id);
"""

# Table schemas for reference
TABLE_SCHEMAS = {
    "events": {
        "event_id": "TEXT PRIMARY KEY",
        "event_key": "TEXT UNIQUE NOT NULL",
        "event_title": "TEXT NOT NULL",
        "date_detected": "TEXT NOT NULL",
        "region": "TEXT NOT NULL",
        "category": "TEXT NOT NULL",
        "summary": "TEXT",
        "score": "INTEGER",
        "band": "TEXT",
        "trigger_full_analysis": "INTEGER DEFAULT 0",
        "status": "TEXT DEFAULT 'active'",
        "raw_data": "TEXT",
        "created_at": "TEXT NOT NULL",
        "updated_at": "TEXT NOT NULL"
    },
    "sources": {
        "source_id": "TEXT PRIMARY KEY",
        "event_id": "TEXT NOT NULL",
        "source_name": "TEXT NOT NULL",
        "source_url": "TEXT",
        "published_at": "TEXT"
    },
    "indicators": {
        "indicator_id": "TEXT PRIMARY KEY",
        "event_id": "TEXT NOT NULL",
        "physical_disruption": "INTEGER DEFAULT 0",
        "transport_impact": "INTEGER DEFAULT 0",
        "policy_sanctions": "INTEGER DEFAULT 0",
        "market_transmission": "INTEGER DEFAULT 0",
        "escalation_risk": "INTEGER DEFAULT 0"
    },
    "flags": {
        "flag_id": "TEXT PRIMARY KEY",
        "event_id": "TEXT NOT NULL",
        "confirmed_supply_disruption": "INTEGER DEFAULT 0",
        "strategic_transport_disruption": "INTEGER DEFAULT 0",
        "major_sanctions_escalation": "INTEGER DEFAULT 0",
        "military_escalation": "INTEGER DEFAULT 0"
    },
    "notifications": {
        "notification_id": "TEXT PRIMARY KEY",
        "event_id": "TEXT NOT NULL",
        "notification_type": "TEXT NOT NULL",
        "file_path": "TEXT",
        "content": "TEXT NOT NULL",
        "created_at": "TEXT NOT NULL"
    },
    "watchlist": {
        "watchlist_id": "TEXT PRIMARY KEY",
        "event_id": "TEXT NOT NULL",
        "company_name": "TEXT",
        "ticker": "TEXT",
        "sector": "TEXT"
    }
}


def get_table_schema(table_name: str) -> Dict[str, str]:
    """Get schema for a specific table."""
    return TABLE_SCHEMAS.get(table_name, {})


def list_tables() -> List[str]:
    """List all table names."""
    return list(TABLE_SCHEMAS.keys())


if __name__ == "__main__":
    print("Geo Market Watch v6 — Database Models")
    print("=" * 50)
    print()
    print("Tables:")
    for table in list_tables():
        print(f"  • {table}")
    print()
    print("Run init_database.py to create the database.")
