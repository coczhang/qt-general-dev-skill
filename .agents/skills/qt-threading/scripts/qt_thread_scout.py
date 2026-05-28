#!/usr/bin/env python3
"""Scan Qt/C++ files for threading review leads."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


SOURCE_EXTENSIONS = {".cpp", ".cc", ".cxx", ".h", ".hh", ".hpp", ".hxx"}
SKIP_DIRS = {".git", "build", "cmake-build-debug", "cmake-build-release", "__pycache__"}

CHECKS = [
    ("critical", "thread_terminate", re.compile(r"\bterminate\s*\("), "QThread::terminate is unsafe except as a last resort."),
    ("high", "direct_connection", re.compile(r"\bQt::DirectConnection\b"), "DirectConnection across threads can run code in the wrong thread."),
    ("high", "blocking_network_wait", re.compile(r"\bwaitFor(?:ReadyRead|Finished|BytesWritten|Connected)\s*\("), "Blocking waits can freeze the UI thread."),
    ("high", "qsql_thread_risk", re.compile(r"\bQSql(Database|Query)\b"), "QSqlDatabase/QSqlQuery must stay within their owning thread."),
    ("medium", "qthread_wait", re.compile(r"\bwait\s*\("), "Check whether wait() can block the UI thread or shutdown indefinitely."),
    ("medium", "move_to_thread", re.compile(r"\bmoveToThread\s*\("), "Verify parent ownership, affinity, and cleanup around moveToThread."),
    ("medium", "delete_later", re.compile(r"\bdeleteLater\s*\("), "Confirm deleteLater runs while the target thread event loop is alive."),
    ("medium", "mutex_signal_risk", re.compile(r"\b(QMutex|std::mutex|QReadWriteLock|std::lock_guard|QMutexLocker)\b"), "Check lock scope and avoid emitting signals while locked."),
    ("medium", "widget_update", re.compile(r"\b(setText|setValue|setPixmap|update|repaint|show|hide)\s*\("), "If this is worker code, QWidget access must be queued to the GUI thread."),
]


def iter_files(paths: list[Path], max_files: int) -> list[Path]:
    files: list[Path] = []
    for raw in paths:
        path = raw.resolve()
        if path.is_file() and path.suffix in SOURCE_EXTENSIONS:
            files.append(path)
            continue
        if not path.is_dir():
            continue
        for child in path.rglob("*"):
            if len(files) >= max_files:
                return files
            if any(part in SKIP_DIRS for part in child.parts):
                continue
            if child.is_file() and child.suffix in SOURCE_EXTENSIONS:
                files.append(child)
    return files


def scan_file(path: Path) -> list[dict[str, object]]:
    try:
        if path.stat().st_size > 1_000_000:
            return []
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return []

    findings = []
    for line_no, line in enumerate(text.splitlines(), start=1):
        for severity, check_id, pattern, message in CHECKS:
            if pattern.search(line):
                findings.append(
                    {
                        "severity": severity,
                        "check": check_id,
                        "file": str(path),
                        "line": line_no,
                        "text": line.strip()[:180],
                        "message": message,
                    }
                )
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Find Qt threading review leads.")
    parser.add_argument("paths", nargs="*", default=["."], help="Files or directories to scan.")
    parser.add_argument("--json", action="store_true", help="Emit JSON.")
    parser.add_argument("--max-files", type=int, default=5000, help="Maximum files to scan.")
    args = parser.parse_args()

    findings = []
    for path in iter_files([Path(p) for p in args.paths], args.max_files):
        findings.extend(scan_file(path))

    if args.json:
        print(json.dumps({"findings": findings}, indent=2, ensure_ascii=False))
        return 0

    print(f"Qt threading scout: {len(findings)} leads")
    for item in findings:
        print(f"[{item['severity']}] {item['file']}:{item['line']} {item['check']}")
        print(f"  {item['text']}")
        print(f"  {item['message']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
