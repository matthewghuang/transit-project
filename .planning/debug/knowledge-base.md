# GSD Debug Knowledge Base

Resolved debug sessions. Used by `gsd-debugger` to surface known-pattern hypotheses at the start of new investigations.

---

## syntax-error-api-run — SyntaxError and TabError in api.py
- **Date:** 2026-04-09
- **Error patterns:** SyntaxError, invalid syntax, TabError, inconsistent use of tabs and spaces
- **Root cause:** Indentation error in `api.py`. The `except` block was incorrectly nested, and there was a mix of tabs and spaces.
- **Fix:** Corrected indentation and normalized whitespace.
- **Files changed:** api.py
---
