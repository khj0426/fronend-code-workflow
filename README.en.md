# frontend-code-workflow

Reusable Codex skills for planning, implementing, verifying, and independently reviewing changes in existing frontend codebases.

| Skill | Purpose |
| --- | --- |
| `frontend-workflow-en` | Plan, implement, and verify frontend changes. |
| `frontend-review-en` | Review completed changes for evidence-based defects and regressions without modifying code. |

Korean versions are available as `frontend-workflow` and `frontend-review`. See [README.md](README.md).

## Installation

Ask Codex to install either skill from its GitHub path:

```text
Install the frontend-workflow-en skill from
https://github.com/khj0426/fronend-code-workflow/tree/main/skills/frontend-workflow-en
```

```text
Install the frontend-review-en skill from
https://github.com/khj0426/fronend-code-workflow/tree/main/skills/frontend-review-en
```

## Usage

Plan and implement a standard feature:

```text
$frontend-workflow-en synchronize the results filter with the URL.
```

Use strict traceability for high-risk work:

```text
$frontend-workflow-en strict improve error handling in the payment form.
```

Review a completed change independently:

```text
$frontend-review-en review the frontend changes on the current branch.
```

## Workflow strength

The workflow skill scales its process to the change:

- **Small:** localized copy, styling, or static content with focused verification.
- **Standard:** stateful or interactive work with user scenarios, UI states, acceptance criteria, and browser verification.
- **High risk:** changes with broad consumers, compatibility requirements, or rollback constraints.

It recommends strict mode for authentication, authorization, payments, personal data, multi-consumer data contracts, staged migrations, explicit rollback requirements, or requests for traceability. A recommendation does not activate strict mode without user approval.

## Strict mode

Strict mode creates the following artifacts unless the target repository has an established convention:

```text
docs/frontend-workflow/<feature-slug>/
├── spec.md
├── plan.md
└── trace.json
```

`journal.md` is optional and should be added only for important observations, decisions, or rejected alternatives. The specification and plan are presented together for one approval before implementation.

Validate the trace file from the target repository root:

```text
python3 <skill-path>/scripts/check_trace.py \
  docs/frontend-workflow/<feature-slug>/trace.json \
  --root .
```

The validator checks JSON structure, acceptance-criterion IDs, status, evidence, repository-relative paths, and file existence. It does not prove test meaning or implementation quality.

## Repository structure

```text
skills/
├── frontend-workflow/       # Korean
├── frontend-review/         # Korean
├── frontend-workflow-en/    # English
└── frontend-review-en/      # English
```

Each skill is self-contained and can be installed independently.
