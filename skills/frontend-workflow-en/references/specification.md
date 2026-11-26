# Specification

Read this reference before implementing standard and high-risk frontend changes.

## Define the user outcome

Describe the primary scenario in observable terms:

> When `<starting condition>`, the user can `<action>` and observes `<result>`.

Separate outcomes from implementation. “The filter is reflected in the URL” is observable. “Use Zustand” is a technical decision.

## Select relevant UI states

Do not list every possible state ceremonially. Consider these states and keep only those the feature can actually enter:

- initial or idle;
- loading or pending;
- success;
- empty;
- validation failure;
- recoverable error;
- unavailable or unauthorized;
- stale, optimistic, or partially updated data.

For each relevant state, define what the user sees, which actions remain available, and how the state exits.

## Check affected environments

Include an environment only when the result can differ there:

- narrow and wide viewports;
- keyboard and pointer input;
- light and dark themes;
- reduced motion;
- server rendering and hydration;
- slow networks or repeated submissions;
- authenticated and unauthenticated sessions.

## Write acceptance criteria

Acceptance criteria must describe observable or testable outcomes. Prefer a short list of meaningful criteria over a restatement of the request.

Good:

- Submitting a valid form sends one request and prevents duplicate submission while pending.
- A validation error is associated with its input, and focus moves to the first invalid field.
- Returning to the results page restores the filter encoded in the URL.

Avoid:

- The component works correctly.
- Use clean code.
- Add a hook for the form.

## Bound the work

State exclusions that could otherwise cause scope drift, such as analytics, cross-device persistence, animation, new design-system primitives, or support for legacy routes.

Ask one focused question at a time only when the answer materially changes the result. If the repository or request already provides the answer, proceed without asking again.
