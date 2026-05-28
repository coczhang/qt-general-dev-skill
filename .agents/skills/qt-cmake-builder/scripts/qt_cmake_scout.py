#!/usr/bin/env python3
"""Scan CMake files for Qt build review leads."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


SKIP_DIRS = {".git", "build", "cmake-build-debug", "cmake-build-release", "__pycache__"}

CHECKS = [
    ("high", "hardcoded_windows_path", re.compile(r"[A-Za-z]:[/\\](?:Users|Qt|Program Files)"), "Hard-coded local paths make builds non-portable."),
    ("high", "hardcoded_unix_home", re.compile(r"/home/[^/\s]+/|/Users/[^/\s]+/"), "Hard-coded home paths make builds non-portable."),
    ("medium", "global_include_directories", re.compile(r"^\s*include_directories\s*\(", re.I), "Prefer target_include_directories for target scope."),
    ("medium", "global_link_directories", re.compile(r"^\s*link_directories\s*\(", re.I), "Prefer imported targets or target_link_directories if unavoidable."),
    ("medium", "file_glob_sources", re.compile(r"^\s*file\s*\(\s*GLOB", re.I), "GLOB sources can hide build graph changes unless CONFIGURE_DEPENDS is used intentionally."),
    ("medium", "cmake_prefix_path", re.compile(r"\bCMAKE_PREFIX_PATH\b"), "Check whether Qt path configuration is local-only or documented."),
    ("low", "qt_wrap_legacy", re.compile(r"\bqt[45]?_wrap_(cpp|ui)\b", re.I), "AUTOMOC/AUTOUIC usually replaces legacy wrap commands."),
]


def iter_cmake_files(paths: list[Path], max_files: int) -> list[Path]:
    files: list[Path] = []
    for raw in paths:
        path = raw.resolve()
        if path.is_file() and (path.name == "CMakeLists.txt" or path.suffix == ".cmake"):
            files.append(path)
            continue
        if not path.is_dir():
            continue
        for child in path.rglob("*"):
            if len(files) >= max_files:
                return files
            if any(part in SKIP_DIRS for part in child.parts):
                continue
            if child.is_file() and (child.name == "CMakeLists.txt" or child.suffix == ".cmake"):
                files.append(child)
    return files


def read_text(path: Path) -> str:
    try:
        if path.stat().st_size > 1_000_000:
            return ""
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


def scan_file(path: Path) -> tuple[list[dict[str, object]], dict[str, object]]:
    text = read_text(path)
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
    features = {
        "find_package_qt5": bool(re.search(r"find_package\s*\(\s*Qt5\b", text)),
        "find_package_qt6": bool(re.search(r"find_package\s*\(\s*Qt6\b", text)),
        "dual_qt": "find_package(QT NAMES Qt6 Qt5" in text or "Qt${QT_VERSION_MAJOR}" in text,
        "automoc": "CMAKE_AUTOMOC" in text,
        "autouic": "CMAKE_AUTOUIC" in text,
        "autorcc": "CMAKE_AUTORCC" in text,
        "target_link_libraries": "target_link_libraries" in text,
        "qt_add_executable": "qt_add_executable" in text,
        "add_executable": "add_executable" in text,
    }
    return findings, features


def main() -> int:
    parser = argparse.ArgumentParser(description="Find Qt CMake review leads.")
    parser.add_argument("paths", nargs="*", default=["."], help="Project roots or CMake files.")
    parser.add_argument("--json", action="store_true", help="Emit JSON.")
    parser.add_argument("--max-files", type=int, default=1000, help="Maximum CMake files to scan.")
    args = parser.parse_args()

    files = iter_cmake_files([Path(p) for p in args.paths], args.max_files)
    findings = []
    features_by_file = {}
    aggregate = {
        "automoc": False,
        "autouic": False,
        "autorcc": False,
        "qt5": False,
        "qt6": False,
        "dual_qt": False,
        "target_link_libraries": False,
    }
    for path in files:
        file_findings, features = scan_file(path)
        findings.extend(file_findings)
        features_by_file[str(path)] = features
        aggregate["automoc"] = aggregate["automoc"] or features["automoc"]
        aggregate["autouic"] = aggregate["autouic"] or features["autouic"]
        aggregate["autorcc"] = aggregate["autorcc"] or features["autorcc"]
        aggregate["qt5"] = aggregate["qt5"] or features["find_package_qt5"]
        aggregate["qt6"] = aggregate["qt6"] or features["find_package_qt6"]
        aggregate["dual_qt"] = aggregate["dual_qt"] or features["dual_qt"]
        aggregate["target_link_libraries"] = aggregate["target_link_libraries"] or features["target_link_libraries"]

    summary = {
        "files": [str(path) for path in files],
        "aggregate": aggregate,
        "features_by_file": features_by_file,
        "findings": findings,
    }

    if args.json:
        print(json.dumps(summary, indent=2, ensure_ascii=False))
        return 0

    print(f"Qt CMake scout: {len(files)} files, {len(findings)} leads")
    print(f"Aggregate: {aggregate}")
    for item in findings:
        print(f"[{item['severity']}] {item['file']}:{item['line']} {item['check']}")
        print(f"  {item['text']}")
        print(f"  {item['message']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
