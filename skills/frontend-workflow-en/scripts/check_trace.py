#!/usr/bin/env python3
"""Validate a frontend-workflow strict-mode trace.json file."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


ACCEPTANCE_ID = re.compile(r"AC-\d{3}")
FEATURE_SLUG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
VALID_STATUSES = {"pending", "verified", "excluded"}


def load_trace(path: Path) -> tuple[dict[str, Any] | None, list[str]]:
    if not path.is_file():
        return None, [f"Trace file does not exist: {path}"]
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        return None, [f"Invalid JSON: {error}"]
    if not isinstance(value, dict):
        return None, ["The top-level trace.json value must be an object."]
    return value, []


def _string_list(item: dict[str, Any], key: str, label: str, errors: list[str]) -> list[str]:
    value = item.get(key, [])
    if not isinstance(value, list) or any(not isinstance(entry, str) or not entry for entry in value):
        errors.append(f"{label}: {key} must be a list of non-empty strings.")
        return []
    return value


def validate_trace(trace: dict[str, Any], root: Path, allow_pending: bool = False) -> list[str]:
    errors: list[str] = []
    feature = trace.get("feature")
    if not isinstance(feature, str) or not FEATURE_SLUG.fullmatch(feature):
        errors.append("feature must be a non-empty kebab-case slug.")

    acceptance = trace.get("acceptance")
    if not isinstance(acceptance, list) or not acceptance:
        return errors + ["acceptance must be a non-empty list of objects."]

    seen: set[str] = set()
    for index, raw_item in enumerate(acceptance, 1):
        if not isinstance(raw_item, dict):
            errors.append(f"Acceptance item {index} must be an object.")
            continue

        identifier = raw_item.get("id")
        label = identifier if isinstance(identifier, str) and identifier else f"Acceptance item {index}"
        if not isinstance(identifier, str) or not ACCEPTANCE_ID.fullmatch(identifier):
            errors.append(f"{label}: id must use the AC-001 format.")
        elif identifier in seen:
            errors.append(f"{label}: duplicate id.")
        if isinstance(identifier, str):
            seen.add(identifier)

        status = raw_item.get("status")
        if status not in VALID_STATUSES:
            errors.append(f"{label}: status must be pending, verified, or excluded.")
            continue

        implementation = _string_list(raw_item, "implementation", label, errors)
        tests = _string_list(raw_item, "tests", label, errors)
        manual = _string_list(raw_item, "manual", label, errors)

        if status == "pending":
            if not allow_pending:
                errors.append(f"{label}: status is still pending.")
            continue
        if status == "excluded":
            reason = raw_item.get("excludedReason")
            if not isinstance(reason, str) or not reason.strip():
                errors.append(f"{label}: excluded status requires excludedReason.")
            continue

        if not implementation:
            errors.append(f"{label}: verified status requires implementation files.")
        if not tests and not manual:
            errors.append(f"{label}: verified status requires tests or manual evidence.")

        for key, paths in (("implementation", implementation), ("tests", tests)):
            for relative_path in paths:
                evidence_path = Path(relative_path)
                if evidence_path.is_absolute() or ".." in evidence_path.parts:
                    errors.append(f"{label}: {key} must use a repository-relative path: {relative_path}")
                elif not (root / evidence_path).is_file():
                    errors.append(f"{label}: {key} file does not exist: {relative_path}")

    return errors


def check_trace(path: Path, root: Path, allow_pending: bool = False) -> list[str]:
    trace, errors = load_trace(path)
    if trace is not None:
        errors.extend(validate_trace(trace, root, allow_pending))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate frontend-workflow trace.json")
    parser.add_argument("trace", type=Path, help="Path to trace.json")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Repository root")
    parser.add_argument("--allow-pending", action="store_true", help="Allow pending items during work")
    args = parser.parse_args()

    errors = check_trace(args.trace, args.root.resolve(), args.allow_pending)
    if errors:
        print("Trace validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("Trace validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
