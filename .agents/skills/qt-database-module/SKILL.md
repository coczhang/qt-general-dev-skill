---
name: qt-database-module
description: Use this skill when designing, implementing, reviewing, or debugging Qt database modules, including SQLite, MySQL, PostgreSQL, QSqlDatabase, QSqlQuery, CRUD services, connection ownership, database work in background threads, prepared statements, transactions, pagination, history queries, and result delivery back to the UI via signals.
---

# Qt Database Module

Act as a senior Qt database engineer. Prioritize thread-correct connections, prepared statements, clear transactions, and UI responsiveness.

## Workflow

1. Identify database driver, schema ownership, connection lifetime, thread model, transaction needs, and query volume.
2. Encapsulate database access in a service/repository module instead of scattering SQL through widgets.
3. Use one named `QSqlDatabase` connection per thread.
4. Return results to UI through signals, models, DTOs, or callbacks that do not carry live `QSqlQuery` objects across threads.
5. Add pagination, indexes, and lazy loading for large result sets.

## Core Rules

- Do not share `QSqlDatabase` or `QSqlQuery` across threads.
- Create, use, and close each connection in the same thread.
- Use prepared statements and bound values.
- Use transactions for batch writes and multi-step state changes.
- Avoid heavy SQL queries in the UI thread.
- Check and report `lastError()` with enough context.
- Keep schema migration/init logic explicit and idempotent.
- Use pagination for large tables and history records.

## Output Shape

For new database modules, provide schema/init strategy, service API, thread model, query examples, result signals/models, and CMake `Sql` linkage.

Prefer Chinese explanations when the user writes in Chinese.
