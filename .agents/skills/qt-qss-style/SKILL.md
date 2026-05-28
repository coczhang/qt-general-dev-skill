---
name: qt-qss-style
description: Use this skill when generating, reviewing, or refactoring Qt QSS styles and themes, including buttons, inputs, tables, navigation bars, title bars, dialogs, dark themes, industrial themes, objectName selectors, state styling, Qt resources, and moving large inline setStyleSheet blocks into maintainable .qss files.
---

# Qt QSS Style

Act as a senior Qt UI styling engineer. Build maintainable QSS systems that match the app's widget hierarchy and object names.

## Workflow

1. Inspect widget names, class hierarchy, visual density, theme requirements, and high-DPI icon needs.
2. Put global styles in a shared `.qss` file such as `resources/qss/app.qss`.
3. Use `objectName` selectors for page-specific or role-specific styling.
4. Provide complete interaction states: normal, hover, pressed, checked, disabled, focus, and selection where relevant.
5. Keep spacing, radius, colors, font sizes, and borders consistent across controls.

## Core Rules

- Avoid large inline `setStyleSheet` blocks in C++.
- Prefer Qt resources for QSS, icons, fonts, and theme assets.
- Use SVG icons for high DPI when possible.
- Keep selectors specific enough to avoid accidental global changes.
- Do not rely on brittle widget tree depth selectors unless necessary.
- Test key widgets: `QPushButton`, `QLineEdit`, `QComboBox`, `QTableView`, `QHeaderView`, `QScrollBar`, `QTabWidget`, dialogs, and navigation buttons.

## Output Shape

For style generation, provide object names, QSS file content, resource file changes, loading code, and notes for states that need UI behavior support.

Prefer Chinese explanations when the user writes in Chinese.
