---
name: frontend-review-en
description: Review frontend code changes for evidence-based defects and regressions. Use when the user requests a frontend code review, diff review, UI change review, or regression audit. Do not use for ordinary implementation, code modification, or backend-only review.
---

# Frontend Review

Review the final diff and affected user flows independently. Do not modify code.

## Procedure

1. Read repository instructions, the user's request, the final diff, and relevant tests.
2. If the repository has requirements, issues, a pull request description, design documents, or traceability artifacts, compare them with the actual change. Do not require a particular format or create missing documents.
3. Look for real defects and regressions in:
   - loading, success, empty, error, and recovery states;
   - duplicate requests, stale state, cleanup, and race conditions;
   - keyboard operation, focus, accessible names, and state announcements;
   - narrow viewports, long content, themes, and motion preferences;
   - server/client boundaries, hydration, and browser-only APIs;
   - public props, routes, URLs, storage keys, and data shapes.
4. Report a finding only when it is reproducible or supported by the code.
5. Order findings by severity. If there are no findings, state the reviewed scope and remaining verification gaps.

## Severity

- `P1`: release-blocking security, data loss, or critical-flow failure
- `P2`: functional or accessibility regression that affects real users
- `P3`: lower-risk issue that occurs under limited conditions

Separate low-confidence assumptions from findings and label them as needing verification.

## Finding format

For each finding, include severity and summary, the file and exact line when possible, evidence, and user or system impact. Suggest a fix only when it helps explain the defect, and keep it brief.

## Exclusions

Do not report formatting, personal taste, minor naming preferences, issues already enforced by automated tools, or unsupported refactoring ideas. Do not modify code, commits, or pull requests unless the user separately asks for a fix.
