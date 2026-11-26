#!/usr/bin/env python3
"""frontend-workflow strict 모드의 trace.yaml을 검사한다."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path


ACCEPTANCE_ID = re.compile(r"AC-\d{3}")
FEATURE_SLUG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
LIST_FIELDS = {"implementation", "tests", "manual"}
SCALAR_FIELDS = {"status", "excluded_reason"}
VALID_STATUSES = {"pending", "verified", "excluded"}


@dataclass
class Acceptance:
    identifier: str
    status: str = ""
    implementation: list[str] = field(default_factory=list)
    tests: list[str] = field(default_factory=list)
    manual: list[str] = field(default_factory=list)
    excluded_reason: str = ""


@dataclass
class Trace:
    feature: str = ""
    acceptance: list[Acceptance] = field(default_factory=list)


def _value(raw: str) -> str:
    value = raw.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def parse_trace(path: Path) -> tuple[Trace, list[str]]:
    trace = Trace()
    errors: list[str] = []
    current: Acceptance | None = None
    current_list: str | None = None

    for line_number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue

        if match := re.fullmatch(r"feature:\s*(.*)", raw_line):
            trace.feature = _value(match.group(1))
            current_list = None
            continue

        if re.fullmatch(r"acceptance:\s*", raw_line):
            current_list = None
            continue

        if match := re.fullmatch(r"  - id:\s*(.*)", raw_line):
            current = Acceptance(identifier=_value(match.group(1)))
            trace.acceptance.append(current)
            current_list = None
            continue

        if match := re.fullmatch(r"    ([a-z_]+):\s*(.*)", raw_line):
            if current is None:
                errors.append(f"{line_number}행: 수용 기준보다 필드가 먼저 나왔습니다.")
                continue
            key, raw_value = match.groups()
            if key in LIST_FIELDS:
                if raw_value.strip():
                    errors.append(f"{line_number}행: {key}는 다음 행부터 목록으로 작성해야 합니다.")
                current_list = key
            elif key in SCALAR_FIELDS:
                setattr(current, key, _value(raw_value))
                current_list = None
            else:
                errors.append(f"{line_number}행: 알 수 없는 필드 '{key}'입니다.")
                current_list = None
            continue

        if match := re.fullmatch(r"      -\s+(.+)", raw_line):
            if current is None or current_list is None:
                errors.append(f"{line_number}행: 목록이 연결된 필드가 없습니다.")
                continue
            getattr(current, current_list).append(_value(match.group(1)))
            continue

        errors.append(f"{line_number}행: 지원하지 않는 YAML 형식입니다: {raw_line.strip()}")

    return trace, errors


def validate_trace(trace: Trace, root: Path, allow_pending: bool = False) -> list[str]:
    errors: list[str] = []

    if not FEATURE_SLUG.fullmatch(trace.feature):
        errors.append("feature는 비어 있지 않은 영문 kebab-case여야 합니다.")
    if not trace.acceptance:
        errors.append("acceptance 항목이 하나 이상 필요합니다.")

    seen: set[str] = set()
    for item in trace.acceptance:
        label = item.identifier or "<ID 없음>"

        if not ACCEPTANCE_ID.fullmatch(item.identifier):
            errors.append(f"{label}: ID는 AC-001 형식이어야 합니다.")
        elif item.identifier in seen:
            errors.append(f"{label}: ID가 중복됐습니다.")
        seen.add(item.identifier)

        if item.status not in VALID_STATUSES:
            errors.append(f"{label}: status는 pending, verified, excluded 중 하나여야 합니다.")
            continue

        if item.status == "pending":
            if not allow_pending:
                errors.append(f"{label}: 아직 pending 상태입니다.")
            continue

        if item.status == "excluded":
            if not item.excluded_reason:
                errors.append(f"{label}: excluded 상태에는 excluded_reason이 필요합니다.")
            continue

        if not item.implementation:
            errors.append(f"{label}: verified 상태에는 implementation 파일이 필요합니다.")
        if not item.tests and not item.manual:
            errors.append(f"{label}: verified 상태에는 tests 또는 manual 근거가 필요합니다.")

        for field_name in ("implementation", "tests"):
            for relative_path in getattr(item, field_name):
                evidence_path = Path(relative_path)
                if evidence_path.is_absolute() or ".." in evidence_path.parts:
                    errors.append(
                        f"{label}: {field_name} 경로는 프로젝트 내부 상대 경로여야 합니다: "
                        f"{relative_path}"
                    )
                    continue
                candidate = root / relative_path
                if not candidate.is_file():
                    errors.append(f"{label}: {field_name} 파일이 없습니다: {relative_path}")

    return errors


def check_trace(path: Path, root: Path, allow_pending: bool = False) -> list[str]:
    if not path.is_file():
        return [f"추적 파일이 없습니다: {path}"]

    trace, errors = parse_trace(path)
    errors.extend(validate_trace(trace, root, allow_pending=allow_pending))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="frontend-workflow trace.yaml 검사")
    parser.add_argument("trace", type=Path, help="검사할 trace.yaml 경로")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="프로젝트 루트")
    parser.add_argument(
        "--allow-pending",
        action="store_true",
        help="작업 중 구조 검사에서는 pending 상태를 허용",
    )
    args = parser.parse_args()

    errors = check_trace(args.trace, args.root.resolve(), allow_pending=args.allow_pending)
    if errors:
        print("trace 검사 실패:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("trace 검사를 통과했습니다.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
