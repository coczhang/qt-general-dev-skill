# Qt Crash Hypotheses

Use this reference to rank common Qt/C++ crash causes.

## High-Probability Qt Causes

- QWidget accessed from a worker thread.
- QObject deleted while queued signals or callbacks still target it.
- Worker thread destroyed before it finishes.
- Parent-child ownership mixed with manual delete.
- Plugin or DLL missing at startup on a clean machine.
- `QSqlDatabase` connection used from the wrong thread.
- `QPixmap` or GUI resource used outside the GUI thread.
- FFmpeg/OpenCV frame buffer lifetime mismatch.

## C++ Memory Causes

- Use-after-free through raw pointer, lambda capture, callback, or queued event.
- Buffer overrun in image/video/native integration code.
- Double free from mixed ownership.
- Data race on shared state.
- Dangling reference/string view/iterator.

## How To Rank

Rank a hypothesis higher when:

- The first app-owned stack frame touches the subsystem.
- The crash happens after shutdown, page close, reconnect, or thread stop.
- The fault address suggests null or freed memory.
- Logs show plugin/dependency failure before startup abort.
- The crash only appears under load, frequent refresh, video frames, or large data.

Rank lower when no stack frame, log clue, lifecycle event, or reproduction condition supports it.
