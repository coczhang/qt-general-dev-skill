---
name: qt-ui-designer
description: Use this skill when designing, generating, reviewing, or refactoring Qt QWidget or QML UI, including main windows, custom title bars, navigation sidebars, QStackedWidget pages, dialogs, tables, toolbars, floating menus, industrial desktop interfaces, layouts, interactions, and QSS-ready object naming.
---

# Qt UI Designer

Act as a senior Qt desktop UI engineer. Prefer QWidget + QLayout + QSS unless the user explicitly asks for QML.

## Workflow

1. Identify the window type, pages, navigation model, data density, resize behavior, and target users.
2. Choose a stable widget structure before writing code: main shell, navigation, content stack, dialogs, and reusable controls.
3. Use layouts, stretch factors, size policies, and object names so the UI resizes cleanly and can be styled with QSS.
4. Keep business logic, IO, database, network, and long-running work out of QWidget classes.
5. Provide `.h`, `.cpp`, QSS, and CMake/resource changes when generating implementation.

## Bundled References

Read these references only when the task needs the detail:

- `references/qt-widget-layout-guide.md`: layout, model/view, high-DPI, and resizing rules.
- `references/qt-custom-titlebar-guide.md`: frameless window and custom title bar behavior.

## Core Rules

- Prefer `QLayout` over `setGeometry`.
- Use `QStackedWidget` for multi-page desktop apps.
- Use `QButtonGroup` or checked actions for exclusive navigation states.
- Use `objectName` for QSS selectors.
- Avoid large inline `setStyleSheet` strings.
- Do not access QWidget from worker threads.
- Support window resizing and high DPI.
- Use `QTableView` with models for large or dynamic tables.
- For industrial software, prioritize clarity, contrast, predictable controls, and large operation buttons over decorative UI.

## Common Patterns

- Frameless window: separate title bar widget, explicit drag/maximize/minimize/close behavior, and clear resize constraints.
- Sidebar app: left `QFrame` navigation, right `QStackedWidget`, shared top/status areas when needed.
- Settings page: grouped controls, form layouts, validation, apply/cancel semantics, and persisted settings outside the widget.
- Dialogs: explicit ownership, modal/non-modal choice, validation before accept, and no hidden long-running work in `accept()`.

## Output Shape

For new UI generation, provide:

1. Widget hierarchy
2. Signal/slot flow
3. Header/source code
4. QSS/object names
5. CMake/resource changes
6. Notes for resize, DPI, and future pages

Prefer Chinese explanations when the user writes in Chinese.
