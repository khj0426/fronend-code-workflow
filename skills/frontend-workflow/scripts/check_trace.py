#!/usr/bin/env python3
"""frontend-workflow strict 모드의 trace.json을 검사한다."""

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
        return None, [f"추적 파일이 없습니다: {path}"]
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        return None, [f"JSON 형식이 올바르지 않습니다: {error}"]
    if not isinstance(value, dict):
        return None, ["trace.json의 최상위 값은 객체여야 합니다."]
    return value, []


def _string_list(item: dict[str, Any], key: str, label: str, errors: list[str]) -> list[str]:
    value = item.get(key, [])
    if not isinstance(value, list) or any(not isinstance(entry, str) or not entry for entry in value):
        errors.append(f"{label}: {key}는 비어 있지 않은 문자열 목록이어야 합니다.")
        return []
    return value


def validate_trace(trace: dict[str, Any], root: Path, allow_pending: bool = False) -> list[str]:
    errors: list[str] = []
    feature = trace.get("feature")
    if not isinstance(feature, str) or not FEATURE_SLUG.fullmatch(feature):
        errors.append("feature는 비어 있지 않은 영문 kebab-case여야 합니다.")

    acceptance = trace.get("acceptance")
    if not isinstance(acceptance, list) or not acceptance:
        return errors + ["acceptance는 하나 이상의 객체를 포함한 목록이어야 합니다."]

    seen: set[str] = set()
    for index, raw_item in enumerate(acceptance, 1):
        if not isinstance(raw_item, dict):
            errors.append(f"{index}번째 acceptance는 객체여야 합니다.")
            continue

        identifier = raw_item.get("id")
        label = identifier if isinstance(identifier, str) and identifier else f"{index}번째 항목"
        if not isinstance(identifier, str) or not ACCEPTANCE_ID.fullmatch(identifier):
            errors.append(f"{label}: ID는 AC-001 형식이어야 합니다.")
        elif identifier in seen:
            errors.append(f"{label}: ID가 중복됐습니다.")
        seen.add(identifier) if isinstance(identifier, str) else None

        status = raw_item.get("status")
        if status not in VALID_STATUSES:
            errors.append(f"{label}: status는 pending, verified, excluded 중 하나여야 합니다.")
            continue

        implementation = _string_list(raw_item, "implementation", label, errors)
        tests = _string_list(raw_item, "tests", label, errors)
        manual = _string_list(raw_item, "manual", label, errors)

        if status == "pending":
            if not allow_pending:
                errors.append(f"{label}: 아직 pending 상태입니다.")
            continue
        if status == "excluded":
            if not isinstance(raw_item.get("excludedReason"), str) or not raw_item["excludedReason"].strip():
                errors.append(f"{label}: excluded 상태에는 excludedReason이 필요합니다.")
            continue

        if not implementation:
            errors.append(f"{label}: verified 상태에는 implementation 파일이 필요합니다.")
        if not tests and not manual:
            errors.append(f"{label}: verified 상태에는 tests 또는 manual 근거가 필요합니다.")

        for key, paths in (("implementation", implementation), ("tests", tests)):
            for relative_path in paths:
                evidence_path = Path(relative_path)
                if evidence_path.is_absolute() or ".." in evidence_path.parts:
                    errors.append(f"{label}: {key} 경로는 프로젝트 내부 상대 경로여야 합니다: {relative_path}")
                elif not (root / evidence_path).is_file():
                    errors.append(f"{label}: {key} 파일이 없습니다: {relative_path}")

    return errors


def check_trace(path: Path, root: Path, allow_pending: bool = False) -> list[str]:
    trace, errors = load_trace(path)
    if trace is not None:
        errors.extend(validate_trace(trace, root, allow_pending))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="frontend-workflow trace.json 검사")
    parser.add_argument("trace", type=Path, help="검사할 trace.json 경로")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="프로젝트 루트")
    parser.add_argument("--allow-pending", action="store_true", help="작업 중에는 pending 상태를 허용")
    args = parser.parse_args()

    errors = check_trace(args.trace, args.root.resolve(), args.allow_pending)
    if errors:
        print("trace 검사 실패:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("trace 검사를 통과했습니다.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
