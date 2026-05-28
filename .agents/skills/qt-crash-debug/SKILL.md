---
name: qt-crash-debug
description: Use this skill when analyzing Qt/C++ crashes, logs, dumps, abnormal exits, watchdog restarts, Event Viewer records, Windows minidumps, Linux core dumps, systemd logs, Crashpad/Breakpad clues, memory corruption, invalid pointers, thread-affinity bugs, QObject lifetime bugs, plugin/dependency load failures, or distinguishing crash, normal exit, forced kill, and hang.
---

# Qt Crash Debug

Act as a senior Qt/C++ crash-analysis engineer. Separate facts from assumptions, classify the failure first, then rank narrow hypotheses.

## Workflow

1. Preserve raw facts: platform, executable, version, Qt version, compiler/runtime, build type, thread, module, exception/signal, exit code, timestamps, and restart source.
2. Classify the event:
   - Normal exit: expected shutdown or known success/handled code.
   - Crash: exception, signal, minidump/core, crash report, or faulting module.
   - Forced kill: watchdog/user/system/service manager killed it.
   - Hang: heartbeat/UI/event-loop timeout while process remained alive.
3. Locate the first faulting frame and first app-owned frame.
4. Check Qt-specific risks: QObject lifetime, thread affinity, QWidget access from worker thread, queued callback after object deletion, plugin load failure, missing DLL/so/dylib, and shutdown races.
5. Propose verification steps before broad refactors.

## Bundled References

Read these references only when needed:

- `references/qt-crash-intake-checklist.md`: smallest useful evidence to request before making root-cause claims.
- `references/qt-crash-hypotheses.md`: common Qt/C++ crash hypotheses and ranking rules.

## Evidence To Request

- Windows: Event Viewer details, WER report, minidump, PDB/symbol status, loaded modules, exception code, and fault offset.
- Linux: `journalctl`, `systemctl status`, `coredumpctl info`, core file, signal, backtrace, library versions, and service restart reason.
- Qt app: logs around startup/shutdown, thread start/stop, plugin loading, network/database/file/render boundaries, and watchdog heartbeats.

## Output Shape

1. Crash summary
2. Evidence
3. Ranked hypotheses
4. Verification steps
5. Minimal safe fixes
6. Logging/dump prevention improvements

Prefer Chinese explanations when the user writes in Chinese.
