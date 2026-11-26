#!/usr/bin/env python3

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

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

    def write_trace(self, content: str) -> Path:
        path = self.root / "trace.yaml"
        path.write_text(content, encoding="utf-8")
        return path

    def test_verified_acceptance_passes(self) -> None:
        path = self.write_trace(
            """feature: signup
acceptance:
  - id: AC-001
    status: verified
    implementation:
      - src/SignupForm.tsx
    tests:
      - tests/SignupForm.test.tsx
    manual:
    excluded_reason:
"""
        )

        self.assertEqual(check_trace(path, self.root), [])

    def test_pending_fails_by_default_and_can_be_allowed(self) -> None:
        path = self.write_trace(
            """feature: signup
acceptance:
  - id: AC-001
    status: pending
    implementation:
    tests:
    manual:
    excluded_reason:
"""
        )

        self.assertIn("AC-001: 아직 pending 상태입니다.", check_trace(path, self.root))
        self.assertEqual(check_trace(path, self.root, allow_pending=True), [])

    def test_duplicate_id_fails(self) -> None:
        path = self.write_trace(
            """feature: signup
acceptance:
  - id: AC-001
    status: excluded
    implementation:
    tests:
    manual:
    excluded_reason: 범위에서 제외
  - id: AC-001
    status: excluded
    implementation:
    tests:
    manual:
    excluded_reason: 범위에서 제외
"""
        )

        self.assertIn("AC-001: ID가 중복됐습니다.", check_trace(path, self.root))

    def test_verified_requires_evidence(self) -> None:
        path = self.write_trace(
            """feature: signup
acceptance:
  - id: AC-001
    status: verified
    implementation:
    tests:
    manual:
    excluded_reason:
"""
        )

        errors = check_trace(path, self.root)
        self.assertIn("AC-001: verified 상태에는 implementation 파일이 필요합니다.", errors)
        self.assertIn("AC-001: verified 상태에는 tests 또는 manual 근거가 필요합니다.", errors)

    def test_missing_evidence_file_fails(self) -> None:
        path = self.write_trace(
            """feature: signup
acceptance:
  - id: AC-001
    status: verified
    implementation:
      - src/Missing.tsx
    tests:
      - tests/Missing.test.tsx
    manual:
    excluded_reason:
"""
        )

        errors = check_trace(path, self.root)
        self.assertIn("AC-001: implementation 파일이 없습니다: src/Missing.tsx", errors)
        self.assertIn("AC-001: tests 파일이 없습니다: tests/Missing.test.tsx", errors)

    def test_excluded_requires_reason(self) -> None:
        path = self.write_trace(
            """feature: signup
acceptance:
  - id: AC-001
    status: excluded
    implementation:
    tests:
    manual:
    excluded_reason:
"""
        )

        self.assertIn(
            "AC-001: excluded 상태에는 excluded_reason이 필요합니다.",
            check_trace(path, self.root),
        )

    def test_evidence_path_must_stay_inside_project(self) -> None:
        path = self.write_trace(
            """feature: signup
acceptance:
  - id: AC-001
    status: verified
    implementation:
      - ../Outside.tsx
    tests:
    manual:
      - 브라우저에서 확인
    excluded_reason:
"""
        )

        self.assertIn(
            "AC-001: implementation 경로는 프로젝트 내부 상대 경로여야 합니다: ../Outside.tsx",
            check_trace(path, self.root),
        )


if __name__ == "__main__":
    unittest.main()
