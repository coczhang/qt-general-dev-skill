# QThread Worker Guide

Use this reference when implementing long-running workflows with `QThread` and worker `QObject`.

## Preferred Shape

```cpp
auto thread = new QThread(owner);
auto worker = new Worker;

worker->moveToThread(thread);

QObject::connect(thread, &QThread::started, worker, &Worker::start);
QObject::connect(worker, &Worker::resultReady, receiver, &Receiver::handleResult);
QObject::connect(worker, &Worker::errorOccurred, receiver, &Receiver::handleError);
QObject::connect(worker, &Worker::finished, thread, &QThread::quit);
QObject::connect(worker, &Worker::finished, worker, &QObject::deleteLater);
QObject::connect(thread, &QThread::finished, thread, &QObject::deleteLater);

thread->start();
```

## Worker Rules

- Worker slots run in the worker thread only after `moveToThread`.
- Do not give the worker a GUI-thread parent before moving it.
- Do not update QWidget from the worker.
- Emit value objects or immutable data back to the UI.
- Use cancellation flags, `requestInterruption()`, or a queued stop slot for long loops.

## Common Mistakes

- Subclassing `QThread` and placing work in slots that still run in the caller thread.
- Destroying a running thread.
- Calling `wait()` from the GUI thread during a long shutdown.
- Capturing deleted UI objects in lambdas connected to worker signals.
- Creating `QSqlDatabase` in one thread and using it in another.
