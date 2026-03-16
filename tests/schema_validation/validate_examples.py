#!/usr/bin/env python3
"""
Validate Geo Market Watch example JSON files against local JSON Schemas.

Expected repository layout:

repo/
├── schemas/
│   ├── event-object.json
│   ├── watchlist-item.json
│   └── analysis-output.json
├── examples/
│   └── schema-examples/
│       ├── event-object.sample.json
│       ├── watchlist-item.sample.json
│       └── analysis-output.sample.json
└── tests/
    └── schema_validation/
        └── validate_examples.py

Usage:
    python tests/schema_validation/validate_examples.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

try:
    from jsonschema import Draft202012Validator
    from referencing import Registry, Resource
except ImportError as exc:
    print(
        "Missing dependency. Install with:\n"
        "  pip install jsonschema referencing",
        file=sys.stderr,
    )
    raise SystemExit(2) from exc


def load_json(path: Path) -> dict[str, Any]:
    """Load a JSON file into a Python dictionary."""
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"[ERROR] File not found: {path}", file=sys.stderr)
        raise
    except json.JSONDecodeError as exc:
        print(f"[ERROR] Invalid JSON in {path}: {exc}", file=sys.stderr)
        raise


def build_registry(schema_dir: Path) -> Registry:
    """
    Build a schema registry that supports local cross-file $ref resolution.

    The schemas use IDs like:
        https://geo-market-watch/schemas/event-object.json

    We register each schema by both:
        - its $id
        - its filename (e.g. "event-object.json")
    so local references like "$ref": "event-object.json" also resolve.
    """
    registry = Registry()

    for schema_path in schema_dir.glob("*.json"):
        schema = load_json(schema_path)
        resource = Resource.from_contents(schema)

        schema_id = schema.get("$id")
        if isinstance(schema_id, str) and schema_id:
            registry = registry.with_resource(schema_id, resource)

        registry = registry.with_resource(schema_path.name, resource)

    return registry


def validate_instance(
    instance_path: Path,
    schema_path: Path,
    registry: Registry,
) -> list[str]:
    """Validate one instance file against one schema file and return error messages."""
    schema = load_json(schema_path)
    instance = load_json(instance_path)

    validator = Draft202012Validator(schema, registry=registry)
    errors = sorted(validator.iter_errors(instance), key=lambda e: list(e.path))

    messages: list[str] = []
    for error in errors:
        path_str = "$"
        if error.path:
            path_str += "".join(
                f"[{repr(p)}]" if isinstance(p, int) else f".{p}"
                for p in error.path
            )
        messages.append(f"{path_str}: {error.message}")

    return messages


def main() -> int:
    repo_root = Path(__file__).resolve().parents[2]
    schema_dir = repo_root / "schemas"
    examples_dir = repo_root / "examples" / "schema-examples"

    required_files = [
        schema_dir / "event-object.json",
        schema_dir / "watchlist-item.json",
        schema_dir / "analysis-output.json",
        examples_dir / "event-object.sample.json",
        examples_dir / "watchlist-item.sample.json",
        examples_dir / "analysis-output.sample.json",
    ]

    missing = [p for p in required_files if not p.exists()]
    if missing:
        print("[ERROR] Missing required files:", file=sys.stderr)
        for path in missing:
            print(f"  - {path}", file=sys.stderr)
        return 2

    registry = build_registry(schema_dir)

    validations = [
        (
            examples_dir / "event-object.sample.json",
            schema_dir / "event-object.json",
        ),
        (
            examples_dir / "watchlist-item.sample.json",
            schema_dir / "watchlist-item.json",
        ),
        (
            examples_dir / "analysis-output.sample.json",
            schema_dir / "analysis-output.json",
        ),
    ]

    total = len(validations)
    passed = 0
    failed = 0

    print("Geo Market Watch Schema Validation")
    print("=" * 40)

    for instance_path, schema_path in validations:
        rel_instance = instance_path.relative_to(repo_root)
        rel_schema = schema_path.relative_to(repo_root)

        print(f"\nValidating: {rel_instance}")
        print(f"Against:    {rel_schema}")

        try:
            errors = validate_instance(instance_path, schema_path, registry)
        except Exception as exc:  # broad catch for clearer CI output
            failed += 1
            print(f"[FAIL] Validation execution error: {exc}")
            continue

        if errors:
            failed += 1
            print("[FAIL]")
            for msg in errors:
                print(f"  - {msg}")
        else:
            passed += 1
            print("[PASS]")

    print("\n" + "=" * 40)
    print(f"Passed: {passed}/{total}")
    print(f"Failed: {failed}/{total}")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
