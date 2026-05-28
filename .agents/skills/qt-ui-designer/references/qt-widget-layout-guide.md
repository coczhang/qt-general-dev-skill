# Qt Widget Layout Guide

Use this reference when generating or reviewing QWidget layouts.

## Layout Rules

- Prefer `QVBoxLayout`, `QHBoxLayout`, `QGridLayout`, and `QFormLayout`.
- Avoid `setGeometry()` except for rare custom painting or controlled overlays.
- Set margins and spacing deliberately at each major container.
- Use size policies instead of fixed sizes when content should adapt.
- Use fixed dimensions only for stable controls such as icon buttons, narrow sidebars, title bars, and status indicators.
- Use `QSplitter` for user-resizable panes.
- Use `QStackedWidget` for page-based desktop apps.

## Page Shell Pattern

```text
MainWindow
  rootWidget
    mainLayout
      titleBar
      bodyLayout
        navigationPanel
        contentStack
      statusBar
```

## Model/View Guidance

- Use `QTableView` with a model for large or dynamic data.
- Avoid filling large `QTableWidget` tables synchronously in UI actions.
- Use delegates for custom cell rendering rather than embedding many widgets in cells.

## High DPI And Resizing

- Prefer SVG icons or multiple raster sizes.
- Avoid pixel-perfect assumptions in text-heavy controls.
- Verify narrow and wide window sizes.
- Ensure buttons and labels do not depend on clipped text to communicate state.
