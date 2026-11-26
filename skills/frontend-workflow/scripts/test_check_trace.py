#!/usr/bin/env python3

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from typing import Any

from check_trace import check_trace


class CheckTraceTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        (self.root / "src").mkdir()
        (self.root / "tests").mkdir()
        (self.root / "src/SignupForm.tsx").write_text("export {}", encoding="utf-8")
        (self.root / "tests/SignupForm.test.tsx").write_text("test.todo('signup')", encoding="utf-8")

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def write_trace(self, *items: dict[str, Any], feature: str = "signup") -> Path:
        path = self.root / "trace.json"
        path.write_text(
            json.dumps({"feature": feature, "acceptance": list(items)}, ensure_ascii=False),
            encoding="utf-8",
        )
        return path

    @staticmethod
    def item(**overrides: Any) -> dict[str, Any]:
        value = {
            "id": "AC-001",
            "status": "verified",
            "implementation": ["src/SignupForm.tsx"],
            "tests": ["tests/SignupForm.test.tsx"],
            "manual": [],
            "excludedReason": None,
        }
        value.update(overrides)
        return value

    def test_verified_acceptance_passes(self) -> None:
        self.assertEqual(check_trace(self.write_trace(self.item()), self.root), [])

    def test_pending_fails_by_default_and_can_be_allowed(self) -> None:
        path = self.write_trace(self.item(status="pending", implementation=[], tests=[]))
        self.assertIn("AC-001: 아직 pending 상태입니다.", check_trace(path, self.root))
        self.assertEqual(check_trace(path, self.root, allow_pending=True), [])

    def test_duplicate_id_fails(self) -> None:
        excluded = self.item(status="excluded", implementation=[], tests=[], excludedReason="범위에서 제외")
        path = self.write_trace(excluded, excluded.copy())
        self.assertIn("AC-001: ID가 중복됐습니다.", check_trace(path, self.root))

    def test_verified_requires_evidence(self) -> None:
        errors = check_trace(
            self.write_trace(self.item(implementation=[], tests=[], manual=[])),
            self.root,
        )
        self.assertIn("AC-001: verified 상태에는 implementation 파일이 필요합니다.", errors)
        self.assertIn("AC-001: verified 상태에는 tests 또는 manual 근거가 필요합니다.", errors)

    def test_missing_evidence_file_fails(self) -> None:
        errors = check_trace(
            self.write_trace(
                self.item(
                    implementation=["src/Missing.tsx"],
                    tests=["tests/Missing.test.tsx"],
                )
            ),
            self.root,
        )
        self.assertIn("AC-001: implementation 파일이 없습니다: src/Missing.tsx", errors)
        self.assertIn("AC-001: tests 파일이 없습니다: tests/Missing.test.tsx", errors)

    def test_excluded_requires_reason(self) -> None:
        path = self.write_trace(self.item(status="excluded", implementation=[], tests=[]))
        self.assertIn(
            "AC-001: excluded 상태에는 excludedReason이 필요합니다.",
            check_trace(path, self.root),
        )

    def test_evidence_path_must_stay_inside_project(self) -> None:
        path = self.write_trace(
            self.item(implementation=["../Outside.tsx"], tests=[], manual=["브라우저에서 확인"])
        )
        self.assertIn(
            "AC-001: implementation 경로는 프로젝트 내부 상대 경로여야 합니다: ../Outside.tsx",
            check_trace(path, self.root),
        )


if __name__ == "__main__":
    unittest.main()
