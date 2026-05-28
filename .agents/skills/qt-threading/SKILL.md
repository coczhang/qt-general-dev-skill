---
name: qt-threading
description: Use this skill when designing, implementing, reviewing, or debugging Qt threading and asynchronous workflows, including QThread, worker QObject with moveToThread, QThreadPool, QRunnable, QtConcurrent, QFutureWatcher, UI freezes, shutdown safety, thread lifetime, queued signals, and database/network/image/video work in background threads.
---

# Qt Threading

Act as a senior Qt concurrency engineer. Optimize for correctness, shutdown safety, and UI responsiveness before clever abstractions.

## Workflow

1. Identify the UI thread, worker threads, shared state, blocking calls, ownership, and shutdown path.
2. Choose the simplest suitable model:
   - Long-lived workflow: worker `QObject` + `moveToThread`.
   - Short independent jobs: `QThreadPool`/`QRunnable`.
   - Simple functional async task: `QtConcurrent` + `QFutureWatcher`.
3. Verify all cross-thread communication uses signals/slots or queued invocations.
4. Verify worker cleanup, cancellation, and app shutdown paths.
5. For reviews, report concrete race, lifetime, UI-thread, deadlock, and leak risks first.

## Bundled Resources

When local files are available, run the threading scout as a lead generator:

```bash
python .agents/skills/qt-threading/scripts/qt_thread_scout.py <paths>
python .agents/skills/qt-threading/scripts/qt_thread_scout.py <paths> --json
```

Treat scanner output as leads, not proof. Confirm each item in surrounding code.

Read these references only when needed:

- `references/qthread-worker-guide.md`: safer worker `QObject` + `moveToThread` pattern.
- `references/thread-lifetime-guide.md`: shutdown, cancellation, and cross-thread lifetime review.

## Core Rules

- Never access QWidget from worker threads.
- Use signals/slots for worker results and UI updates.
- Use `Qt::QueuedConnection` when thread affinity is ambiguous or critical.
- Use `deleteLater` for QObject cleanup in the object's owning thread.
- Stop threads with a clear sequence such as `requestInterruption()`, `quit()`, and `wait()`.
- Do not share `QSqlDatabase` or `QSqlQuery` across threads.
- Avoid `waitForReadyRead`, blocking SQL, file IO, image conversion, or video decode on the UI thread.
- Protect shared data with clear ownership, queued message passing, mutexes, or atomics as appropriate.
- Use `QPointer` or lifecycle guards when callbacks can outlive UI objects.

## Safer QThread Pattern

Prefer this shape for long-running workflows:

```cpp
auto thread = new QThread(parent);
auto worker = new Worker;
worker->moveToThread(thread);

QObject::connect(thread, &QThread::started, worker, &Worker::start);
QObject::connect(worker, &Worker::finished, thread, &QThread::quit);
QObject::connect(worker, &Worker::finished, worker, &QObject::deleteLater);
QObject::connect(thread, &QThread::finished, thread, &QObject::deleteLater);
QObject::connect(worker, &Worker::resultReady, receiver, &Receiver::handleResult);
thread->start();
```

Adapt the pattern to existing ownership rules. Do not introduce detached threads without a shutdown owner.

Prefer Chinese explanations when the user writes in Chinese.
