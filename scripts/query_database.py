#!/usr/bin/env python3
"""
DEPRECATED: Use gmw-* CLI commands instead.

This script is kept for backward compatibility but will be removed in a future version.
Please use the official CLI entry points:
  - gmw-init-db
  - gmw-query
  - gmw-agent
  - gmw-seed-db
  - gmw-benchmark
"""

import warnings
import sys

warnings.warn(
    "This script is deprecated. Use 'gmw-query' CLI command instead.",
    DeprecationWarning,
    stacklevel=2
)

# Import and run the official CLI
from geo_market_watch.scripts.query import main

if __name__ == "__main__":
    sys.exit(main())
