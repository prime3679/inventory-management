---
name: application-ship-check
description: Run a ship-ready review before marking any change as done. Checks scope/risk, UI consistency, API contracts, security, and generates concrete test ideas. Use this skill after completing a feature, bug fix, or refactor to verify it is ready to merge.
---

# Application Ship Check

Run this review against every change before it is considered done. Work through each section in order. For each check, read the relevant files, state what you found, and flag any issues. Do not skip a section — if it does not apply, say so and move on.

## 1. Scope and Risk Assessment

Identify what changed and how far the blast radius extends.

- List every file that was added, modified, or deleted.
- For each changed file, name the other files that import it or depend on it.
- Classify the overall risk:
  - **Low** — cosmetic, copy, or config-only changes with no runtime impact.
  - **Medium** — logic changes scoped to a single feature area.
  - **High** — changes that touch shared state, data models, API contracts, auth, or payment flows.
- If risk is Medium or High, list the specific downstream paths that could break and should be verified.

## 2. UI Consistency

Check that the user-facing interface stays coherent after the change.

- **Layout and styling**: Open every view or page that could be affected. Confirm spacing, typography, color, and component appearance match the rest of the application. Flag any raw/unstyled elements.
- **Responsive behavior**: If the app supports multiple breakpoints, verify the change does not break at common widths (mobile, tablet, desktop).
- **Translations / i18n**: If the app has a localization system, confirm every new or changed user-visible string has translations in all supported locales. Look for:
  - Hardcoded strings that bypass the translation function.
  - Missing keys in any locale file.
  - Strings that will overflow or truncate in longer locales.
- **Empty and loading states**: Confirm that new UI paths handle zero-data, loading, and error conditions visibly and consistently with existing patterns.
- **Accessibility basics**: Check that interactive elements are keyboard-reachable and that images or icons have text alternatives where needed.

## 3. API Contracts and Error Handling

Verify the interface between frontend and backend is sound.

- **Contract alignment**: For every API call that was added or changed, confirm the request shape (method, path, query params, body) matches what the server expects, and the response shape matches what the client parses.
- **Validation models**: If the backend uses a schema or model layer, confirm models were updated to reflect any data structure changes.
- **Error paths**: Trace what happens when the API returns 400, 404, 422, and 500 for each affected endpoint. Confirm the frontend surfaces a meaningful message rather than silently failing or showing a raw error object.
- **Edge cases**: Consider empty arrays, null fields, very large payloads, and special characters in user input. Flag any that are unhandled.

## 4. Security-Sensitive Areas

Look for issues in authentication, authorization, and data exposure.

- **Auth and session**: If the change touches login, logout, token handling, or session management, verify that credentials are not logged, stored in plaintext, or exposed in URLs.
- **PII and sensitive data**: Check that personally identifiable information (names, emails, phone numbers, addresses, payment details) is not:
  - Leaked into client-side logs or console output.
  - Included in API responses where it is not needed.
  - Stored without appropriate protection.
- **Input handling**: Confirm user-supplied values are not injected into HTML (XSS), database queries (SQL injection), or shell commands. Look for `v-html`, `innerHTML`, raw string interpolation in queries, or unsanitized URL parameters.
- **Secrets and config**: Verify no API keys, tokens, passwords, or internal URLs were added to tracked files. Check `.env.example` was updated if new environment variables were introduced.
- **CORS and headers**: If the change affects CORS configuration or HTTP headers, confirm the new settings are appropriate for the deployment target.

## 5. Test Ideas

Produce a concrete, actionable list of tests for the change. Do not list generic advice — each item should be specific enough that someone could write the test from the description alone.

Format each test idea as:

```
- [unit|integration|e2e] <what to test>: <setup>, <action>, <expected result>
```

Cover at minimum:
- The happy path for each new or changed behavior.
- At least one failure or edge case per changed endpoint or component.
- Any regression paths identified in the risk assessment (Section 1).

## Output Format

Present results as a single report with these headings:

```
## Ship Check Report

### 1. Scope and Risk
<findings>

### 2. UI Consistency
<findings>

### 3. API Contracts
<findings>

### 4. Security Review
<findings>

### 5. Suggested Tests
<test list>

### Verdict
[ ] SHIP — all checks pass
[ ] FIX FIRST — issues listed above must be resolved
```

Mark exactly one verdict. If any section has an unresolved issue, the verdict is FIX FIRST.
