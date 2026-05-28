# Thread Lifetime Guide

Use this reference when reviewing shutdown, cancellation, and cross-thread ownership.

## Shutdown Checklist

- Is there a single owner responsible for stopping the thread?
- Can the worker finish if the network/database/device call blocks?
- Are queued signals harmless after the UI object is gone?
- Are worker objects destroyed in their owning thread?
- Are `quit()` and `wait()` bounded or used where blocking is acceptable?
- Are timers stopped in the right thread?

## Safer Patterns

- Connect the receiver's `destroyed` signal to a worker stop request when UI lifetime controls the task.
- Use `QPointer` in lambdas that reference widgets.
- Disconnect or use context-bound connections so Qt auto-disconnects when receivers die.
- Prefer message passing over shared mutable state.

## Red Flags

- `moveToThread(this)`.
- `delete thread` while it may still be running.
- `Qt::DirectConnection` across threads without a clear reason.
- Mutex held while emitting a signal or calling into UI code.
- Blocking wait in destructors called from the UI thread.
- Shared `QSqlDatabase`, `QTcpSocket`, or `QNetworkReply` across threads.
