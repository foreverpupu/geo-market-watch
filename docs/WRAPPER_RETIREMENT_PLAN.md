# Wrapper Retirement Plan

This document lists all legacy wrapper scripts in the `scripts/` directory that are scheduled for removal.

## Overview

During the v6.5 refactor closure, all functionality was moved to the official `geo_market_watch` package namespace with proper CLI entry points. The old top-level scripts are now deprecated wrappers that emit deprecation warnings and forward to the new CLI commands.

## Retirement Schedule

**Recommended Removal Version**: v7.0

All wrappers listed below should be removed in the v7.0 release.

## Legacy Wrappers

| 旧脚本名称 | 当前转发到的新 CLI 命令 | 建议正式移除版本 |
|-----------|----------------------|----------------|
| `scripts/init_database.py` | `gmw-init-db` | v7.0 |
| `scripts/query_database.py` | `gmw-query` | v7.0 |
| `scripts/run_agent_loop.py` | `gmw-agent` | v7.0 |
| `scripts/run_benchmark.py` | `gmw-benchmark` | v7.0 |
| `scripts/seed_database.py` | `gmw-seed-db` | v7.0 |
| `scripts/start_idea_tracking.py` | N/A (功能已迁移到包内) | v7.0 |
| `scripts/update_idea_price_reference.py` | N/A (功能已迁移到包内) | v7.0 |
| `scripts/close_trade_idea.py` | N/A (功能已迁移到包内) | v7.0 |
| `scripts/list_active_ideas.py` | N/A (功能已迁移到包内) | v7.0 |
| `scripts/list_tracked_ideas.py` | N/A (功能已迁移到包内) | v7.0 |
| `scripts/export_dashboard_data.py` | N/A (功能已迁移到包内) | v7.0 |
| `scripts/ingest_artifacts.py` | N/A (功能已迁移到包内) | v7.0 |
| `scripts/ingest_watchlist.py` | N/A (功能已迁移到包内) | v7.0 |
| `scripts/approve_trade_idea.py` | N/A (功能已迁移到包内) | v7.0 |
| `scripts/invalidate_trade_idea.py` | N/A (功能已迁移到包内) | v7.0 |
| `scripts/review_trade_ideas.py` | N/A (功能已迁移到包内) | v7.0 |
| `scripts/run_v7_orchestrator.py` | N/A (功能已迁移到包内) | v7.0 |

## Migration Guide

### For CLI Users

**Before (deprecated)**:
```bash
python scripts/init_database.py --db data/geo_alpha.db
python scripts/query_database.py --db data/geo_alpha.db --list
python scripts/run_agent_loop.py --input data/intake.json
```

**After (official)**:
```bash
pip install -e .
gmw-init-db --db data/geo_alpha.db
gmw-query --db data/geo_alpha.db --list
gmw-agent --input data/intake.json --memory data/dedupe.json
```

### For Python API Users

**Before (deprecated)**:
```python
import sys
sys.path.insert(0, "engine")
from database import connect_db
```

**After (official)**:
```python
from geo_market_watch.database import connect_db
from geo_market_watch.agent_loop import run_agent_loop
```

## Removal Checklist for v7.0

- [ ] Remove `scripts/init_database.py`
- [ ] Remove `scripts/query_database.py`
- [ ] Remove `scripts/run_agent_loop.py`
- [ ] Remove `scripts/run_benchmark.py`
- [ ] Remove `scripts/seed_database.py`
- [ ] Remove `scripts/start_idea_tracking.py`
- [ ] Remove `scripts/update_idea_price_reference.py`
- [ ] Remove `scripts/close_trade_idea.py`
- [ ] Remove `scripts/list_active_ideas.py`
- [ ] Remove `scripts/list_tracked_ideas.py`
- [ ] Remove `scripts/export_dashboard_data.py`
- [ ] Remove `scripts/ingest_artifacts.py`
- [ ] Remove `scripts/ingest_watchlist.py`
- [ ] Remove `scripts/approve_trade_idea.py`
- [ ] Remove `scripts/invalidate_trade_idea.py`
- [ ] Remove `scripts/review_trade_ideas.py`
- [ ] Remove `scripts/run_v7_orchestrator.py`
- [ ] Update documentation to remove all references to old script paths
- [ ] Update CHANGELOG with removal notice

## Current Status

All wrappers currently:
- Emit `DeprecationWarning` when executed
- Forward to official CLI commands (where applicable)
- Display migration instructions (where no direct CLI equivalent exists)

No new code should depend on these wrappers. All development should use the official package API or CLI commands.
