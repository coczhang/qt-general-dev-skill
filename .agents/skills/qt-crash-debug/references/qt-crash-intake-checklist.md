# Qt Crash Intake Checklist

Use this reference before making root-cause claims.

## Required Facts

- Platform and OS version.
- App name, version, architecture, build type, compiler/runtime, and Qt version.
- Crash time and whether a watchdog/service restarted it.
- Exit code, exception code, signal, or termination reason.
- Faulting module and first faulting frame.
- First app-owned frame in the stack.
- Recent logs around startup/shutdown/thread/network/database/render boundaries.
- Symbol availability: PDB, DWARF, dSYM, map files, or build ID.

## Windows

- Event Viewer Application error.
- WER report.
- Minidump and matching PDBs.
- Fault offset and loaded module version.
- Dependency/plugin load errors.

## Linux

- `journalctl` around the event.
- `systemctl status` if service-managed.
- `coredumpctl info` and stack trace.
- Signal name/number.
- Shared library versions and rpath clues.

## Ask For Missing Data

Ask for the smallest missing artifact that would change the diagnosis. Do not ask for a full dump if Event Viewer or logs can first classify normal exit vs crash vs kill.
