# Qt CMake Patterns

Use this reference when creating or repairing a Qt CMake build.

## Qt Version Selection

Prefer matching the existing project:

```cmake
find_package(Qt6 COMPONENTS Widgets Network Sql REQUIRED)
# or
find_package(Qt5 COMPONENTS Widgets Network Sql REQUIRED)
```

For dual-version projects:

```cmake
find_package(QT NAMES Qt6 Qt5 REQUIRED COMPONENTS Widgets)
find_package(Qt${QT_VERSION_MAJOR} REQUIRED COMPONENTS Widgets)
target_link_libraries(app PRIVATE Qt${QT_VERSION_MAJOR}::Widgets)
```

## Target-Based Defaults

```cmake
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTOUIC ON)
set(CMAKE_AUTORCC ON)
```

Use target-specific settings:

```cmake
target_include_directories(app PRIVATE src)
target_compile_definitions(app PRIVATE APP_VERSION="${PROJECT_VERSION}")
target_link_libraries(app PRIVATE Qt6::Widgets)
```

## Resources

```cmake
target_sources(app PRIVATE resources/app.qrc)
```

Keep QSS, icons, translations, and config templates discoverable by CMake and packaging rules.
