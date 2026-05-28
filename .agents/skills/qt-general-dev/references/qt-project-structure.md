# Qt Project Structure

Use this reference when designing or reorganizing a Qt/C++ desktop project.

## Recommended Layout

```text
project-root/
  CMakeLists.txt
  cmake/
  resources/
    app.qrc
    qss/app.qss
    icons/
  src/
    main.cpp
    app/
    ui/
    modules/
      network/
      database/
      devices/
      rendering/
    common/
    platform/
  include/
  tests/
```

Keep the exact layout compatible with the existing repository when modifying an established project.

## Module Boundaries

- `ui/`: QWidget classes, dialogs, models, delegates, and view-level signal wiring.
- `modules/network/`: protocol clients, connection state, request IDs, timeout/retry logic.
- `modules/database/`: schema, repositories, migrations, thread-owned connections.
- `modules/rendering/`: image/video conversion, painters, OpenGL widgets, coordinate mapping.
- `common/`: DTOs, logging helpers, config objects, utility functions with low coupling.
- `platform/`: OS-specific code behind narrow interfaces.

## Dependency Direction

Prefer this direction:

```text
ui -> modules -> common
ui -> app
modules -> common
platform -> common
```

Avoid module-to-widget dependencies. A database or network service should emit data/state signals, not manipulate QWidget objects.

## Naming Guidance

- Use clear service names: `NetworkClient`, `DatabaseService`, `VideoRenderer`, `SettingsStore`.
- Use page/widget names that match their role: `HistoryPage`, `SettingsPage`, `NavigationBar`.
- Use signal names that describe events: `recordsLoaded`, `connectionStateChanged`, `frameReady`.
