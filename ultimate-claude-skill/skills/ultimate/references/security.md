# Security

A checklist for any change that touches input, auth, secrets, or stored data. Distilled from ECC rules (security) and common secure-coding practice.

## Contents

- Pre-commit checklist
- Secrets
- Input and output
- Auth
- Dependencies and supply chain
- If you find a vulnerability
- Common mistakes

## Pre-commit checklist

- [ ] No hardcoded secrets (API keys, passwords, tokens, private keys).
- [ ] All user input validated at the boundary: type, length, format, range.
- [ ] Database access uses parameterized queries or a safe query builder.
- [ ] HTML output escaped; untrusted HTML sanitized with a maintained library.
- [ ] CSRF protection on state-changing requests from browsers.
- [ ] Authorization checked on every protected route and object, not just login.
- [ ] Rate limits on public and auth endpoints.
- [ ] Error messages and logs don't leak stack traces, paths, tokens, or personal data.

## Secrets

- Read secrets from environment variables or a secret manager. Never commit them.
- Fail fast at startup when a required secret is missing, with a clear message naming the variable (never its value).
- Keep `.env` in `.gitignore`. Ship a `.env.example` with placeholder values.
- A secret that reached git history is exposed, even after deletion. Rotate it.

## Input and output

- Validate on the server even when the client validates.
- Allowlist over denylist: accept the known-good shapes.
- File uploads: check type by content, cap size, store outside the web root, generate the stored filename yourself.
- Paths from user input: resolve and confirm they stay inside the intended directory.
- Shell commands: pass argument arrays, never string-built commands with user input.
- Deserialization: never unpickle or eval untrusted data.

## Auth

- Hash passwords with a slow, salted algorithm (bcrypt, scrypt, argon2). Never reversible encryption.
- Check object ownership on every read and write (the classic `GET /invoices/123` belonging to someone else).
- Short-lived tokens; rotate refresh tokens; invalidate on logout and password change.
- Same error for "no such user" and "wrong password".

## Dependencies and supply chain

- Pin versions. Review what a new dependency pulls in before adding it.
- Run the ecosystem's audit tool (`npm audit`, `pip-audit`, `cargo audit`) in CI.
- Don't copy-paste install scripts from untrusted sources into CI.

## If you find a vulnerability

1. Stop feature work.
2. Fix critical issues first.
3. Rotate anything that may have been exposed.
4. Search the codebase for the same pattern elsewhere.
5. Tell the user plainly what was exposed and for how long, if known.

## Common mistakes

- Checking that a user is logged in, but not that the record belongs to them.
- Logging full request bodies that contain passwords or tokens.
- Deleting a leaked key from the repo without rotating it.
- Trusting client-side validation.
- Building SQL with f-strings "just for this internal tool".
