#!/usr/bin/env python3
"""Quick Qt project scout.

This script is a lead generator for Codex. It summarizes likely Qt version,
modules, source layout, and common risk patterns. Confirm every finding by
reading the surrounding project files.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path


TEXT_EXTENSIONS = {
    ".c",
    ".cc",
    ".cpp",
    ".cxx",
    ".h",
    ".hh",
    ".hpp",
    ".hxx",
    ".cmake",
    ".txt",
    ".pro",
    ".pri",
    ".qrc",
    ".ui",
    ".qml",
    ".qss",
}

SKIP_DIRS = {
    ".git",
    ".svn",
    ".hg",
    "build",
    "cmake-build-debug",
    "cmake-build-release",
    "node_modules",
    ".venv",
    "venv",
    "__pycache__",
}

PATTERNS = {
    "manual_geometry": re.compile(r"\bsetGeometry\s*\("),
    "inline_stylesheet": re.compile(r"\bsetStyleSheet\s*\("),
    "blocking_wait": re.compile(r"\bwaitFor(?:ReadyRead|Finished|BytesWritten|Connected)\s*\("),
    "thread_usage": re.compile(r"\b(QThread|moveToThread|QThreadPool|QtConcurrent|QRunnable)\b"),
    "database_usage": re.compile(r"\b(QSqlDatabase|QSqlQuery|Qt(?:5|6)?::Sql)\b"),
    "network_usage": re.compile(r"\b(QNetworkAccessManager|QTcpSocket|QUdpSocket|QWebSocket)\b"),
    "render_usage": re.compile(r"\b(QImage|QPixmap|QPainter|QOpenGLWidget|QVideoSink|AVFrame)\b"),
}

QT_MODULE_RE = re.compile(r"\b(?:Qt[56]?::|COMPONENTS\s+)([A-Za-z0-9_ ;\n\r\t]+)")


def iter_files(paths: list[Path], max_files: int) -> list[Path]:
    files: list[Path] = []
    for raw_path in paths:
        path = raw_path.resolve()
        if path.is_file():
            files.append(path)
            continue
        if not path.is_dir():
            continue
        for child in path.rglob("*"):
            if len(files) >= max_files:
                return files
            if any(part in SKIP_DIRS for part in child.parts):
                continue
            if child.is_file() and (child.name == "CMakeLists.txt" or child.suffix in TEXT_EXTENSIONS):
                files.append(child)
    return files


def read_text(path: Path, max_bytes: int = 1_000_000) -> str:
    try:
        if path.stat().st_size > max_bytes:
            return ""
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


def detect_qt_versions(text_by_file: dict[str, str]) -> list[str]:
    joined = "\n".join(text_by_file.values())
    versions = []
    if re.search(r"\b(Qt6|Qt6::|find_package\s*\(\s*Qt6)\b", joined):
        versions.append("Qt6")
    if re.search(r"\b(Qt5|Qt5::|find_package\s*\(\s*Qt5)\b", joined):
        versions.append("Qt5")
    if "find_package(QT NAMES Qt6 Qt5" in joined or "Qt${QT_VERSION_MAJOR}" in joined:
        versions.append("Qt5/Qt6 dual")
    if not versions and re.search(r"\bQT\s*[+]?=", joined):
        versions.append("qmake project")
    return versions


def detect_modules(text_by_file: dict[str, str]) -> list[str]:
    known = {
        "Widgets",
        "Core",
        "Gui",
        "Network",
        "Sql",
        "OpenGL",
        "OpenGLWidgets",
        "Multimedia",
        "WebEngineWidgets",
        "WebSockets",
        "Quick",
        "Qml",
        "Concurrent",
    }
    modules = set()
    for text in text_by_file.values():
        for module in known:
            if f"Qt6::{module}" in text or f"Qt5::{module}" in text:
                modules.add(module)
        for match in re.finditer(r"find_package\s*\(\s*Qt[56]?.*?COMPONENTS\s+([^)]+)\)", text, re.S):
            for token in re.split(r"[\s;]+", match.group(1)):
                token = token.strip()
                if token in known:
                    modules.add(token)
    return sorted(modules)


def collect_pattern_hits(text_by_file: dict[str, str]) -> dict[str, list[dict[str, object]]]:
    hits: dict[str, list[dict[str, object]]] = defaultdict(list)
    for filename, text in text_by_file.items():
        for line_no, line in enumerate(text.splitlines(), start=1):
            for name, pattern in PATTERNS.items():
                if pattern.search(line):
                    hits[name].append({"file": filename, "line": line_no, "text": line.strip()[:180]})
    return dict(hits)


def summarize(paths: list[Path], max_files: int) -> dict[str, object]:
    files = iter_files(paths, max_files=max_files)
    text_by_file = {str(path): read_text(path) for path in files}
    text_by_file = {name: text for name, text in text_by_file.items() if text}
    extensions = Counter(path.suffix or path.name for path in files)
    has_cmake = any(path.name == "CMakeLists.txt" or path.suffix == ".cmake" for path in files)
    has_qmake = any(path.suffix in {".pro", ".pri"} for path in files)
    return {
        "roots": [str(path.resolve()) for path in paths],
        "file_count": len(files),
        "extensions": dict(sorted(extensions.items())),
        "build_systems": {
            "cmake": has_cmake,
            "qmake": has_qmake,
        },
        "qt_versions": detect_qt_versions(text_by_file),
        "qt_modules": detect_modules(text_by_file),
        "pattern_hits": collect_pattern_hits(text_by_file),
    }


def print_text(summary: dict[str, object]) -> None:
    print("Qt project scout")
    print(f"Roots: {', '.join(summary['roots'])}")
    print(f"Files scanned: {summary['file_count']}")
    print(f"Build systems: {summary['build_systems']}")
    print(f"Qt versions: {summary['qt_versions'] or ['unknown']}")
    print(f"Qt modules: {summary['qt_modules'] or ['unknown']}")
    print("Extensions:")
    for ext, count in summary["extensions"].items():
        print(f"  {ext}: {count}")
    print("Pattern hits:")
    hits = summary["pattern_hits"]
    if not hits:
        print("  none")
        return
    for name, items in sorted(hits.items()):
        print(f"  {name}: {len(items)}")
        for item in items[:8]:
            print(f"    {item['file']}:{item['line']} {item['text']}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize a Qt/C++ project and common risk patterns.")
    parser.add_argument("paths", nargs="*", default=["."], help="Project roots or files to scan.")
    parser.add_argument("--json", action="store_true", help="Emit JSON.")
    parser.add_argument("--max-files", type=int, default=5000, help="Maximum files to scan.")
    args = parser.parse_args()

    summary = summarize([Path(p) for p in args.paths], max_files=args.max_files)
    if args.json:
        print(json.dumps(summary, indent=2, ensure_ascii=False))
    else:
        print_text(summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
