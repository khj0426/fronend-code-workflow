# Strict Mode

Use strict mode when acceptance criteria must remain traceable through implementation and verification.

## Artifacts

Use the following location unless the repository already has a convention:

```text
docs/frontend-workflow/<feature-slug>/
├── spec.md
├── plan.md
└── trace.json
```

Add `journal.md` only when important observations, decisions, or rejected alternatives arise. Copy initial files from `assets/templates/` and replace every instruction placeholder with actual content.

## Specification and plan

In `spec.md`, write the user scenario, observable acceptance criteria using IDs such as `AC-001`, relevant UI states, and excluded scope.

In `plan.md`, connect each vertical work item to acceptance criteria and verification evidence. Include any new dependency, public interface, data migration, compatibility requirement, or rollback constraint.

Present the specification and plan drafts together and get one approval before implementation. If meaning or scope changes during implementation, update both documents first and tell the user.

## Traceability

Record every acceptance criterion and its evidence in `trace.json`.

- `pending`: implementation or verification is incomplete.
- `verified`: implementation exists with test or manual evidence.
- `excluded`: the criterion was excluded by agreement and has a reason.

Do not mark unverified work as `verified`. Record files as paths relative to the repository root.

## Validation

Run from the repository root:

```text
python3 <skill-path>/scripts/check_trace.py docs/frontend-workflow/<feature-slug>/trace.json --root .
```

The validator checks JSON structure, IDs, status, evidence, and file existence. Use ordinary verification and final diff review to assess test meaning and implementation quality.
