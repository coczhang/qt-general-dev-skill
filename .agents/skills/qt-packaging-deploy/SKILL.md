---
name: qt-packaging-deploy
description: Use this skill when packaging, deploying, installing, or troubleshooting Qt applications, including Windows windeployqt, Inno Setup, CPack, Visual C++ runtime, Qt plugins, platforms/qwindows.dll, Linux shared libraries, rpath, deb packages, AppImage, systemd services, macOS bundles, macdeployqt, codesign, notarization, resources, QSS, icons, translations, and clean-machine verification.
---

# Qt Packaging Deploy

Act as a senior Qt release/deployment engineer. Package the app so it runs on a clean target machine, not only on the developer machine.

## Workflow

1. Identify platform, compiler/runtime, Qt version, dynamic/static build, third-party libraries, plugins, resources, config files, translations, and service/autostart needs.
2. Build Release artifacts first.
3. Collect Qt runtime dependencies with the platform tool when applicable.
4. Add third-party DLL/so/dylib dependencies, plugins, QSS/resources, config, icons, and translations.
5. Verify on a clean machine, VM, container, or clean user profile.

## Platform Rules

- Windows: use `windeployqt`, include VC runtime or MinGW runtime, `platforms/qwindows.dll`, image formats, TLS libraries, third-party DLLs, and installer rules such as Inno Setup or CPack.
- Linux: check rpath, shared libraries, Qt plugins, distro package dependencies, deb/AppImage strategy, desktop files, and optional `systemd` units.
- macOS: use app bundle layout, `macdeployqt`, `Info.plist`, icons, codesign, notarization, and dylib/plugin paths.

## Core Rules

- Avoid hard-coded development paths.
- Include resources, QSS, icons, translations, config templates, and plugin directories.
- Log startup dependency/plugin failures clearly.
- Verify the package on a clean environment before calling it done.

## Output Shape

For packaging tasks, provide artifact layout, collection commands, installer/package config, clean-machine verification steps, and likely missing dependency checks.

Prefer Chinese explanations when the user writes in Chinese.
