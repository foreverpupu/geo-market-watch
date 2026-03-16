#!/usr/bin/env python3
"""
DEPRECATED: This script functionality has been moved to geo_market_watch package.

Please use the official CLI or import from geo_market_watch directly.
"""

import warnings
import sys

warnings.warn(
    "This script is deprecated. Import from geo_market_watch package instead.",
    DeprecationWarning,
    stacklevel=2
)

print("""
This script has been deprecated.

Please use one of the following:
1. Official CLI commands:
   - gmw-init-db
   - gmw-query
   - gmw-agent
   - gmw-seed-db
   - gmw-benchmark

2. Import from the package directly:
   from geo_market_watch.watchlist import ingest_watchlist
   etc.

See geo_market_watch/README.md for details.
""")

sys.exit(1)
