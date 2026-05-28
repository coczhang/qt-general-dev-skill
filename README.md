# Qt General Dev Skill

这是一个面向 Codex / AI 编程助手的 Qt/C++ 通用 Skill 体系。它让 Codex 在处理 Qt 桌面项目时，稳定遵循 Qt 工程实践，覆盖需求分析、架构设计、代码生成、代码审查、问题排查、重构建议、性能优化和跨平台部署。

本仓库的可用 Skill 以项目级 `.agents/skills` 为准。也就是说，Codex 真正读取和使用的是 `.agents/skills/<skill-name>` 下的内容。

## `.agents` 结构

```text
.agents/
  skills/
    qt-general-dev/
      SKILL.md
      agents/openai.yaml
      references/
      scripts/
    qt-ui-designer/
    qt-threading/
    qt-cmake-builder/
    qt-network-module/
    qt-database-module/
    qt-qss-style/
    qt-crash-debug/
    qt-video-render/
    qt-performance-review/
    qt-packaging-deploy/
```

`SKILL.md` 是 Codex 触发和使用 Skill 的核心说明。`agents/openai.yaml` 是 UI 展示和默认提示词元数据。`references/` 存放按需读取的专项规则。`scripts/` 存放可执行的诊断扫描脚本。

## Skill 模块

这套 Skill 采用 `1 个主 Skill + 10 个专项 Skill` 的结构。

- `qt-general-dev`：Qt/C++ 通用入口，负责架构设计、通用规范、任务识别和子 Skill 路由。
- `qt-ui-designer`：QWidget/QML UI 设计、布局生成、自定义标题栏、导航栏、弹窗、表格页面等。
- `qt-threading`：QThread、moveToThread、QThreadPool、QtConcurrent、UI 卡顿和线程安全。
- `qt-cmake-builder`：Qt5/Qt6 CMake、target-based CMake、Qt 模块和第三方依赖。
- `qt-network-module`：TCP、UDP、HTTP/HTTPS、WebSocket、JSON、心跳、超时和重连。
- `qt-database-module`：SQLite、MySQL、PostgreSQL、QSqlDatabase、CRUD、分页、事务和线程安全。
- `qt-qss-style`：QSS 样式、主题、控件状态、objectName 选择器和资源文件管理。
- `qt-crash-debug`：Qt/C++ 崩溃、日志、dump、core dump、Event Viewer、watchdog、异常退出和挂死分析。
- `qt-video-render`：QImage、QPixmap、QPainter、QOpenGLWidget、QVideoSink、FFmpeg AVFrame 和视频渲染。
- `qt-performance-review`：UI 卡顿、高 CPU、内存增长、频繁 repaint、慢查询、图片转换和渲染瓶颈。
- `qt-packaging-deploy`：Windows/Linux/macOS、windeployqt、CPack、Inno Setup、deb、systemd、macdeployqt 等打包部署。

如果不确定该用哪个专项 Skill，优先使用 `qt-general-dev`。它会根据任务类型引导使用对应子 Skill。

## 当前项目使用

如果当前项目已经包含 `.agents/skills`，直接在 Codex 中打开该项目即可使用。

示例：

```text
使用 qt-general-dev Skill，帮我审查这个 Qt 项目的架构和线程风险。
```

```text
使用 qt-ui-designer Skill，帮我生成一个带自定义标题栏和左侧导航栏的主界面。
```

```text
使用 qt-threading Skill，帮我审查这段 QThread 代码，重点看 UI 线程访问和释放顺序。
```

```text
使用 qt-cmake-builder Skill，帮我把这个 Qt6 Widgets 项目改成现代 CMake 写法。
```

```text
使用 qt-crash-debug Skill，帮我分析这个 Windows 崩溃日志，判断是崩溃、强杀还是挂死。
```

如果不确定应该使用哪一个子 Skill，可以直接使用 `qt-general-dev`。它是总入口 Skill，会根据任务内容判断应该走 UI、线程、CMake、网络、数据库、QSS、崩溃调试、视频渲染、性能优化还是打包部署方向。

```text
使用 qt-general-dev Skill，帮我判断这个问题应该用哪个 Qt 子 Skill，并给出处理方案。
```

## 指定项目使用

指定项目使用适合把这套 Qt Skill 固定在某一个项目里，便于团队共享同一套 Qt 工程规则。

在本仓库根目录执行以下命令，把 `.agents/skills` 下的所有 Skill 一次性复制到目标项目。`$targetProject` 指目标 Qt 项目的根目录，不是 `.agents` 或 `.agents/skills` 目录。

```powershell
$targetProject = "D:\path\to\your-qt-project"
$sourceSkills = Join-Path (Get-Location) ".agents\skills"
$targetSkills = Join-Path $targetProject ".agents\skills"

New-Item -ItemType Directory -Force -Path $targetSkills | Out-Null
Get-ChildItem -Directory -LiteralPath $sourceSkills | Copy-Item -Destination $targetSkills -Recurse -Force
```

macOS/Linux：

```bash
source_skills="$(pwd)/.agents/skills"
target_project="/path/to/your-qt-project"

mkdir -p "$target_project/.agents/skills"
cp -R "$source_skills"/* "$target_project/.agents/skills/"
```

复制完成后，目标项目结构应类似：

```text
your-qt-project/
  .agents/
    skills/
      qt-general-dev/
      qt-ui-designer/
      qt-threading/
      ...
```

然后在 Codex 中打开目标项目，直接通过 Skill 名称触发。

## 全局使用

全局使用适合让所有 Codex 项目都能默认使用这套 Qt Skill。全局目录是用户级 Codex skills 目录，通常是 `$CODEX_HOME/skills`；如果没有设置 `CODEX_HOME`，则使用 `~/.codex/skills`。

Windows PowerShell：

```powershell
$sourceSkills = Join-Path (Get-Location) ".agents\skills"
$codexHome = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $env:USERPROFILE ".codex" }
$globalSkills = Join-Path $codexHome "skills"

New-Item -ItemType Directory -Force -Path $globalSkills | Out-Null
Get-ChildItem -Directory -LiteralPath $sourceSkills | Copy-Item -Destination $globalSkills -Recurse -Force
```

macOS/Linux：

```bash
source_skills="$(pwd)/.agents/skills"
global_skills="${CODEX_HOME:-$HOME/.codex}/skills"

mkdir -p "$global_skills"
cp -R "$source_skills"/* "$global_skills/"
```

复制完成后，用户级目录结构应类似：

```text
~/.codex/
  skills/
    qt-general-dev/
    qt-ui-designer/
    qt-threading/
    ...
```

如果当前 Codex 会话没有立即识别新增 Skill，新开一个 Codex 会话或重启 Codex 后再试。

全局安装建议用于个人常用 Qt/C++ 工作流。若某个项目需要不同版本的同名 Skill，优先使用项目级 `.agents/skills`。

## 诊断脚本

部分核心 Skill 带有轻量扫描脚本，用于给 Codex 提供项目线索。脚本输出只是线索，不是最终结论，仍需要结合源码确认。

项目级安装后，在目标项目根目录中运行：

```powershell
python .agents\skills\qt-general-dev\scripts\qt_project_scout.py .
```

```powershell
python .agents\skills\qt-threading\scripts\qt_thread_scout.py src include
```

```powershell
python .agents\skills\qt-cmake-builder\scripts\qt_cmake_scout.py .
```

如需机器可读输出，追加 `--json`：

```powershell
python .agents\skills\qt-general-dev\scripts\qt_project_scout.py . --json
```

全局安装后，也可以从用户级 skills 目录调用对应脚本。通常更推荐在项目级 `.agents` 中运行，因为命令更短，也更容易与项目版本保持一致。

## 推荐工作流

1. 以 `.agents/skills` 作为当前可用 Skill 的准入目录。
2. 修改或新增 Skill 后，先确认 `.agents/skills/<skill-name>/SKILL.md` 和 `agents/openai.yaml` 齐全；如该 Skill 需要，再确认 `references/` 和 `scripts/` 齐全。
3. 在当前项目中直接用 `qt-general-dev` 或专项 Skill 处理真实 Qt/C++ 任务。
4. 需要给其他项目使用时，把 `.agents/skills` 复制到目标项目的 `.agents/skills`。
5. 需要所有项目默认可用时，把 `.agents/skills` 复制到用户级 `.codex/skills`。

## 维护建议

- 优先让 `SKILL.md` 保持短而清晰，把细节放到 `references/`。
- 新增规则时，先判断它是通用规则还是某个专项规则。
- 新增脚本时，优先只依赖 Python 标准库，除非确实需要额外依赖。
- 修改后至少检查 `.agents/skills` 下的 `SKILL.md` frontmatter、`agents/openai.yaml` 和诊断脚本可用性。
