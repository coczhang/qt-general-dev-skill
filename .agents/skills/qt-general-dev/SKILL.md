---
name: qt-general-dev
description: Use this skill when designing, generating, reviewing, refactoring, debugging, optimizing, packaging, or adapting Qt/C++ desktop applications, including QWidget UI, QSS styling, CMake, signals and slots, threading, networking, database access, image/video rendering, crash analysis, and cross-platform Qt engineering.
---

# Qt General Development

Act as a senior Qt/C++ desktop application engineer. Use this as the entry point for Qt/C++ work, then route to a more specific Qt skill when the task is clearly focused.

Prefer practical, maintainable, cross-platform solutions that fit the existing project instead of inventing a new architecture.

## Default Assumptions

- Language: C++17 or later.
- Framework: Qt 5.14+ or Qt 6.x.
- UI stack: QWidget by default unless the user asks for QML.
- Build system: CMake by default.
- Styling: QSS by default.
- Platforms: Windows, Linux, and macOS.
- Architecture: modular, low-coupling, signal/slot based.
- Threading: never block the UI thread.

## Fast Workflow

1. Identify the task type: architecture, UI, threading, CMake, network, database, QSS, crash/debug, rendering, performance, packaging, review, or refactor.
2. Inspect the existing project before proposing changes: Qt version, CMake style, module layout, ownership style, threading model, naming conventions, and platform targets.
3. Route to a specialist skill when useful:
   - UI/layout/window/pages: `qt-ui-designer`.
   - Threads/async/UI freeze from workers: `qt-threading`.
   - CMake/build/dependencies: `qt-cmake-builder`.
   - TCP/UDP/HTTP/WebSocket/API calls: `qt-network-module`.
   - SQLite/MySQL/PostgreSQL/QSqlDatabase: `qt-database-module`.
   - QSS/theme/control styling: `qt-qss-style`.
   - Crashes/logs/dumps/watchdogs: `qt-crash-debug`.
   - Images/video/OpenGL/FFmpeg: `qt-video-render`.
   - CPU/memory/UI freeze/repaint issues: `qt-performance-review`.
   - Deployment/installers/packages: `qt-packaging-deploy`.
4. Keep edits scoped. Preserve existing APIs and module boundaries unless they are the cause of the problem.
5. Prefer minimal safe changes for existing code; use fuller scaffolding only when the user asks for new modules or architecture.

## Bundled Resources

When a local project is available, run the project scout as a lead generator:

```bash
python .agents/skills/qt-general-dev/scripts/qt_project_scout.py <project-root>
python .agents/skills/qt-general-dev/scripts/qt_project_scout.py <project-root> --json
```

Treat scanner output as clues, not proof. Confirm findings by reading the relevant files.

Read these references only when needed:

- `references/qt-project-structure.md`: recommended Qt module layout and dependency direction.
- `references/qt-common-rules.md`: cross-cutting ownership, threading, UI, build, platform, and logging rules.
- `references/qt-output-format-guide.md`: structured formats for design, review, and debugging answers.

## General Qt Rules

- Operate QWidget and GUI objects only on the main thread.
- Keep expensive database, network, file, image, and video work off the UI thread.
- Use signals/slots or `QMetaObject::invokeMethod` for cross-thread calls.
- Prefer `QObject` parent-child ownership for Qt objects.
- Prefer RAII and smart pointers for non-QObject C++ objects.
- Prefer `QLayout` over `setGeometry`.
- Keep UI, business logic, network, database, device, and rendering modules separated.
- Put reusable QSS in `.qss` files or Qt resources; avoid large inline `setStyleSheet` strings.
- Use `objectName` for QSS targeting.
- Use modern target-based CMake with `AUTOMOC`, `AUTOUIC`, and `AUTORCC`.
- Avoid hard-coded absolute paths and platform APIs unless isolated behind platform-specific branches.
- Add logging around IO, network, database, thread, plugin loading, rendering, and crash-sensitive boundaries.

## Output Shape

For design tasks, answer in this order:

1. Goal
2. Recommended Qt approach
3. Module/class design
4. Directory structure
5. Key signal/slot flow
6. Core implementation
7. CMake changes
8. Risks and extension points

For code review or debugging, lead with findings and evidence. State confidence, trigger conditions, production impact, and the smallest safe fix.

Prefer Chinese explanations when the user writes in Chinese.
