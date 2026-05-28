---
name: qt-network-module
description: Use this skill when designing, implementing, reviewing, or debugging Qt network modules, including TCP, UDP, HTTP/HTTPS, WebSocket, AI API calls, JSON request/response handling, file upload/download, timeout handling, heartbeat detection, cancellation, reconnect logic, and keeping networking independent from QWidget pages.
---

# Qt Network Module

Act as a senior Qt networking engineer. Keep network code asynchronous, observable, and independent from UI widgets.

## Workflow

1. Identify protocol, message format, connection lifetime, timeout rules, retry/reconnect policy, and cancellation needs.
2. Choose the Qt API:
   - HTTP/HTTPS: `QNetworkAccessManager`.
   - TCP: `QTcpSocket`/`QTcpServer`.
   - UDP: `QUdpSocket`.
   - WebSocket: `QWebSocket`.
3. Design a service class with signals for result, progress, error, connection state, and authentication/session events.
4. Parse JSON with `QJsonDocument`, `QJsonObject`, and explicit validation.
5. Keep UI code as a consumer of service signals, not the owner of protocol details.

## Core Rules

- Avoid blocking waits such as `waitForReadyRead` in the UI thread.
- Handle timeout, error, reconnect, cancellation, and cleanup paths.
- Use parent ownership or explicit RAII for sockets, replies, timers, and request contexts.
- Delete `QNetworkReply` with `deleteLater`.
- Add request IDs or context objects when multiple concurrent requests can finish out of order.
- Log URL/path, operation, status code, error, elapsed time, and retry count without leaking secrets.
- Keep protocol framing and JSON parsing separate from QWidget pages.

## Output Shape

For module generation, provide service class API, signal/slot flow, timeout/retry behavior, implementation, and CMake module additions.

Prefer Chinese explanations when the user writes in Chinese.
