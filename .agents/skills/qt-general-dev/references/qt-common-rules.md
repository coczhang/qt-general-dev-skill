# Qt Common Engineering Rules

Use this reference for cross-cutting Qt/C++ rules during design, review, and refactoring.

## Ownership

- Give QObject instances a parent when ownership is hierarchical and same-thread.
- Use `deleteLater()` for QObject destruction across queued/event-loop boundaries.
- Use RAII and smart pointers for non-QObject resources.
- Avoid storing raw pointers to objects whose owner is unclear; prefer parent ownership, `QPointer`, references with narrower lifetime, or explicit ownership comments.

## Threading

- Do not access QWidget outside the GUI thread.
- Do not block the GUI thread with SQL, network, file, image conversion, video decode, compression, or process waits.
- Use signals/slots or `QMetaObject::invokeMethod` for cross-thread interactions.
- Treat `Qt::AutoConnection` carefully when object affinity can change; use `Qt::QueuedConnection` when needed.

## UI

- Prefer layouts and size policies over fixed geometry.
- Use model/view for large tables or frequently updated data.
- Keep IO, database, network, and business logic out of widget classes.
- Load shared QSS from resources; avoid large inline style strings.

## Build And Platform

- Use target-based CMake.
- Avoid absolute local paths in CMake and code.
- Isolate platform-specific code with small interfaces and platform branches.
- Include resources, translations, plugins, and config in install/package rules.

## Diagnostics

- Log at module boundaries: thread start/stop, network request/response, database open/query errors, file paths, plugin loading, frame/render state, and shutdown.
- Include enough context to correlate asynchronous work: request ID, connection name, thread ID, file path, object name, or frame number.
