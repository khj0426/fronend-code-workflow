# Verification

Choose checks based on the change's failure modes and the repository's existing capabilities. More checks are not automatically better.

## Baseline checks

Run the most focused available checks first, followed by broader checks when risk warrants them:

- formatting or linting for edited files;
- type checking;
- focused tests;
- a production build when bundling, routing, rendering, or framework behavior can change.

Read the final exit status. Distinguish unrelated pre-existing failures from failures introduced by the change.

## Match behavior to evidence

| Change | Useful evidence |
| --- | --- |
| Pure transformation or state reducer | Unit test with boundary cases |
| Form or interactive component | Component interaction test and keyboard check |
| Navigation or multi-page journey | Browser or E2E flow |
| Shared component or design token | Consumer checks and visual comparison |
| Async mutation | Pending, success, error, retry, and duplicate-action behavior |
| SSR or hydration boundary | Production build and browser console check |
| Responsive layout | Narrow and wide viewport inspection |
| Theme-dependent UI | Light and dark theme inspection |

Do not install a new test framework solely to prove a small change. When automation is absent, perform a focused manual check and report it as manual.

## Browser verification

For visible or interactive changes, inspect the rendered result when a browser is available. Verify only relevant dimensions:

- the primary interaction and recovery path;
- layout at affected viewport sizes;
- focus order and visible focus;
- accessible name, role, state, and error association;
- affected theme and motion preferences;
- console and network failures caused by the change.

A successful build does not prove that the UI is usable. A screenshot does not prove that interaction works. Use evidence that matches the claim.

## Report verification gaps

If credentials, data, a browser, an external service, or an unavailable command blocks a check, state:

1. what was not verified;
2. why it was unavailable;
3. what substitute check was performed;
4. the remaining risk.

## Review the final diff

Check only items relevant to the change:

- missing loading, error, empty, or recovery states;
- regressions in keyboard operation, focus, naming, or state announcements;
- narrow layouts, long content, and theme differences;
- duplicate requests, stale state, cleanup, and race conditions;
- server/client boundaries and browser-only APIs.

Report only checks that actually completed.
