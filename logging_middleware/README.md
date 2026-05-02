# Logging Middleware

This package provides reusable decorator-based structured logging for Stage 1.

Every decorated function emits:

- `function_name`
- UTC `timestamp`
- structured `inputs`
- structured `outputs`

The logger writes JSON lines through a custom `sys.stdout.write` implementation. It does not use direct `print` statements, database storage, or built-in logger APIs.
