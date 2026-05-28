# Third-Party Dependency Guide

Use this reference when integrating FFmpeg, OpenCV, spdlog, OpenSSL, or other non-Qt dependencies.

## Preferred Order

1. Use an existing package manager/toolchain already present in the repository.
2. Use `find_package` when the dependency provides a reliable config package.
3. Use imported targets for manually located libraries.
4. Keep local absolute paths out of committed CMake files.

## Imported Target Pattern

```cmake
add_library(ThirdParty::Foo UNKNOWN IMPORTED)
set_target_properties(ThirdParty::Foo PROPERTIES
    IMPORTED_LOCATION "${FOO_LIBRARY}"
    INTERFACE_INCLUDE_DIRECTORIES "${FOO_INCLUDE_DIR}"
)
target_link_libraries(app PRIVATE ThirdParty::Foo)
```

## Platform Notes

- Windows: include runtime DLLs beside the executable or in installer rules.
- Linux: check rpath, system packages, and ABI compatibility.
- macOS: check bundle library paths, codesign, and notarization implications.

## Review Red Flags

- Hard-coded developer paths such as `C:/Users/...` or `/home/name/...`.
- Global `include_directories()` and `link_directories()` used for one target.
- Debug and Release libraries mixed accidentally.
- Missing deployment/install handling for runtime libraries.
