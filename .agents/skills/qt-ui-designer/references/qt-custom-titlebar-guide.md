# Qt Custom Title Bar Guide

Use this reference when building or reviewing a frameless Qt window with a custom title bar.

## Required Behaviors

- Close, minimize, maximize/restore buttons.
- Drag to move the window.
- Double-click title bar to maximize/restore when appropriate.
- Preserve resize behavior when the window is frameless.
- Keep platform quirks isolated in a helper class when native hit testing is required.

## Structure

```text
FramelessWindow
  TitleBar
    icon
    title
    spacer
    minimizeButton
    maximizeButton
    closeButton
  content
```

## Safety Rules

- Do not put business logic in the title bar.
- Keep button object names stable for QSS.
- Avoid swallowing child widget mouse events needed by controls inside the title bar.
- Respect minimum size and restore geometry.

## Styling States

Provide QSS states for window buttons:

- normal
- hover
- pressed
- disabled
- close-button hover/pressed warning color
