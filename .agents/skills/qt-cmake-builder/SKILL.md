---
name: qt-cmake-builder
description: Use this skill when creating, reviewing, or fixing CMake builds for Qt/C++ projects, including Qt5/Qt6 CMake, Widgets, Network, Sql, WebEngine, OpenGL, resources, AUTOUIC/AUTOMOC/AUTORCC, third-party dependencies such as FFmpeg/OpenCV/spdlog, cross-platform conditions, install rules, and packaging preparation.
---

# Qt CMake Builder

Act as a senior Qt build engineer. Prefer modern target-based CMake and preserve the project's existing generator, toolchain, and Qt version unless the user asks to migrate.

## Workflow

1. Detect Qt major version, CMake version, compiler, generator, build presets, and platform targets.
2. Inspect current target names, source layout, resources, UI files, and dependency conventions.
3. Add the smallest target-based CMake changes needed.
4. Keep platform-specific logic isolated with `WIN32`, `APPLE`, `UNIX`, generator expressions, or toolchain files.
5. Verify with the existing configure/build command or CMake preset when available.

## Bundled Resources

When local CMake files are available, run the CMake scout as a lead generator:

```bash
python .agents/skills/qt-cmake-builder/scripts/qt_cmake_scout.py <project-root>
python .agents/skills/qt-cmake-builder/scripts/qt_cmake_scout.py <project-root> --json
```

Treat scanner output as leads, not proof. Confirm each item against the build files.

Read these references only when needed:

- `references/qt-cmake-patterns.md`: Qt5/Qt6, dual-version, target-based CMake, and resource patterns.
- `references/third-party-dependency-guide.md`: FFmpeg/OpenCV/spdlog/OpenSSL dependency integration.

## Core Rules

- Use CMake 3.19+ unless the project is constrained.
- Use C++17 or later unless the project says otherwise.
- Enable `CMAKE_AUTOMOC`, `CMAKE_AUTORCC`, and `CMAKE_AUTOUIC`.
- Use `find_package(Qt6 COMPONENTS ... REQUIRED)` or `find_package(Qt5 COMPONENTS ... REQUIRED)` based on the project.
- Link Qt modules through imported targets such as `Qt6::Widgets` or `Qt5::Widgets`.
- Avoid hard-coded absolute local paths.
- Prefer target-specific include directories, compile definitions, and link libraries.
- Keep resources, QSS, icons, translations, and config files in predictable resource/install rules.

## Qt6 Skeleton

```cmake
cmake_minimum_required(VERSION 3.19)
project(AppName LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

find_package(Qt6 REQUIRED COMPONENTS Widgets Network Sql)

add_executable(AppName
    src/main.cpp
    resources/app.qrc
)

target_link_libraries(AppName PRIVATE
    Qt6::Widgets
    Qt6::Network
    Qt6::Sql
)
```

Prefer Chinese explanations when the user writes in Chinese.
