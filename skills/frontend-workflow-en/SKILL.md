---
name: frontend-workflow-en
description: Plan, implement, and verify changes in an existing frontend codebase. Use for UI features, interactions, client-side bugs, shared components, routing, state, accessibility, responsive behavior, or frontend architecture. Do not use for backend-only work, explanations without code changes, or greenfield project scaffolding.
---

# Frontend Workflow

Start from observable user outcomes and prefer the repository's existing patterns and tools.

## Workflow strength

### Small change

Use for copy, styling, or static content that does not change a state transition or public interface. Inspect the relevant code, make the minimum coherent change, and run focused verification. Do not create planning documents.

### Standard feature

Use when the change includes user input, state, navigation, asynchronous behavior, or multiple UI states.

1. Read [references/specification.md](references/specification.md).
2. Propose the user scenario, relevant UI states, acceptance criteria, and excluded scope.
3. Get approval before implementation when the request does not already resolve meaningful choices.
4. Follow existing patterns and implement in small, verifiable vertical slices.
5. Read [references/verification.md](references/verification.md) and verify the relevant code and browser behavior.

### High-risk change

Identify affected consumers, compatibility requirements, and rollback constraints. Get approval for the approach and implementation order. If implementation reveals a public API change, data-contract change, new dependency, or rollback constraint, report the expanded scope.

Automatically recommend strict mode for:

- authentication, authorization, payments, or personal data;
- data-contract changes or staged migrations with multiple consumers;
- work that requires compatibility or an explicit rollback;
- requests that explicitly require traceability from requirements to evidence.

Explain the additional artifacts and cost in one or two sentences. A recommendation is not approval. If declined, continue with the ordinary high-risk workflow.

## Strict mode

Read [references/strict-mode.md](references/strict-mode.md) only when the user explicitly requests `strict` or approves the recommendation. Do not create planning or traceability files before approval.

## Completion

Report the user-visible result, checks performed, unverified behavior, and remaining risk.
