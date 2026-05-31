<div align="center">

# 🚀 MockPilot-CLI

**Lightweight Terminal API Mock Server Intelligent Engine**

**轻量级终端API Mock服务器智能引擎**

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Zero Dependencies](https://img.shields.io/badge/Zero-Dependencies-brightgreen.svg)]()
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey.svg)]()

[English](#english) | [简体中文](#简体中文) | [繁體中文](#繁體中文)

</div>

---

<a name="english"></a>
## 🎉 Project Introduction

**MockPilot-CLI** is a lightweight, zero-dependency terminal-based API mock server designed for developers who need fast, flexible, and intelligent API simulation. Unlike traditional mock tools that require complex setups or heavy dependencies, MockPilot runs purely on Python's standard library.

### ✨ Key Differentiators

- **🎯 Zero Core Dependencies** - Pure Python standard library, no pip install headaches
- **🎨 Dynamic Template Engine** - Generate realistic mock data with built-in generators
- **📊 Real-time TUI Dashboard** - Monitor requests and responses in a beautiful terminal UI
- **📖 OpenAPI Compatible** - Import Swagger/OpenAPI specs and auto-generate mock routes
- **⚡ Lightning Fast** - Minimal overhead, maximum performance
- **🔧 Developer Friendly** - Simple JSON configuration, intuitive CLI commands

### 🌟 Why MockPilot?

| Feature | MockPilot | JSON Server | Mockoon | WireMock |
|---------|-----------|-------------|---------|----------|
| Zero Dependencies | ✅ | ❌ | ❌ | ❌ |
| Terminal Dashboard | ✅ | ❌ | ❌ | ❌ |
| OpenAPI Import | ✅ | ❌ | ✅ | ✅ |
| Dynamic Data | ✅ | Limited | ✅ | ✅ |
| Lightweight | ✅ | ✅ | ❌ | ❌ |

---

## ✨ Core Features

### 🎯 Zero Dependencies
```bash
# No installation required!
python3 mockpilot.py start
```

### 🎨 Dynamic Template Engine
Built-in data generators for realistic mock responses:
- `{{$uuid}}` - Generate UUID v4
- `{{$name}}` - Random full names
- `{{$email}}` - Random email addresses
- `{{$phone}}` - Random phone numbers
- `{{$company}}` - Random company names
- `{{$lorem}}` - Lorem ipsum text
- `{{$date}}` / `{{$datetime}}` - Timestamps
- `{{$bool}}` - Boolean values
- `{{$int}}` / `{{$float}}` - Numbers
- `{{$word}}` / `{{$sentence}}` - Text content

### 📊 TUI Dashboard
```
╔══════════════════════════════════════════════════════════════╗
║                    🚀 MockPilot-CLI v1.0.0                   ║
║         Lightweight API Mock Server Intelligent Engine       ║
╚══════════════════════════════════════════════════════════════╝

📊 Statistics
  Total Requests: 42
  Avg Response Time: 12.5ms
  Status Distribution:
    200: 38
    404: 4

📋 Recent Requests (Last 10)
Time         Method   Path                           Status   Duration
----------------------------------------------------------------------
14:32:15     GET      /api/users                     200      8.2ms
14:32:10     POST     /api/users                     201      15.1ms
...
```

### 📖 OpenAPI Support
```bash
# Generate mock routes from OpenAPI spec
mockpilot openapi swagger.json
mockpilot start mockpilot.json
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- No additional dependencies required!

### Installation

#### Option 1: Direct Usage (Recommended)
```bash
# Clone the repository
git clone https://github.com/gitstq/MockPilot-Server.git
cd MockPilot-Server

# Start with default routes
python3 mockpilot.py start
```

#### Option 2: Install via pip
```bash
pip install mockpilot-cli
mockpilot start
```

#### Option 3: Global Installation
```bash
# Make executable
chmod +x mockpilot.py
sudo cp mockpilot.py /usr/local/bin/mockpilot

# Run from anywhere
mockpilot start
```

### First Run
```bash
# Create a sample configuration
mockpilot init

# Start the server
mockpilot start mockpilot.json

# Server running at http://localhost:8080
```

---

## 📖 Detailed Usage Guide

### Configuration File

Create a `mockpilot.json` file:

```json
{
  "cors": {
    "enabled": true
  },
  "defaultResponse": {
    "status": 404,
    "body": {
      "error": "Not Found"
    }
  },
  "routes": [
    {
      "method": "GET",
      "path": "/api/users",
      "response": {
        "status": 200,
        "body": {
          "users": [
            {
              "id": "{{$uuid}}",
              "name": "{{$name}}",
              "email": "{{$email}}"
            }
          ]
        }
      }
    },
    {
      "method": "GET",
      "path": "/api/users/:id",
      "response": {
        "status": 200,
        "body": {
          "id": "{{$uuid}}",
          "name": "{{$name}}",
          "email": "{{$email}}"
        }
      }
    },
    {
      "method": "POST",
      "path": "/api/users",
      "response": {
        "status": 201,
        "body": {
          "id": "{{$uuid}}",
          "message": "User created"
        }
      }
    }
  ]
}
```

### CLI Commands

```bash
# Start server with config
mockpilot start config.json

# Start with default routes
mockpilot start

# Validate configuration
mockpilot validate config.json

# Generate config from OpenAPI
mockpilot openapi swagger.json

# Show version
mockpilot version

# Show help
mockpilot help
```

### Route Matching

- **Static routes**: `/api/users`
- **Path parameters**: `/api/users/:id`
- **Query parameters**: Match specific query strings
- **Method matching**: GET, POST, PUT, DELETE, PATCH

### Response Delay

Simulate network latency:

```json
{
  "method": "GET",
  "path": "/api/slow",
  "delay": 2000,
  "response": {
    "status": 200,
    "body": {"message": "Delayed response"}
  }
}
```

---

## 💡 Design Philosophy

### Why Zero Dependencies?

In modern development, dependency bloat is a real problem. MockPilot's zero-dependency approach means:

- **No version conflicts** - Works with any Python environment
- **No security vulnerabilities** from third-party packages
- **Instant startup** - No lengthy pip installs
- **Portable** - Copy the single file and run anywhere

### Template Engine Design

The template engine uses simple `{{$generator}}` syntax that's:
- **Intuitive** - Easy to understand and write
- **Flexible** - Combine multiple generators
- **Extensible** - Easy to add new generators

---

## 📦 Packaging & Deployment

### Standalone Script
```bash
# Single file deployment
python3 mockpilot.py start
```

### Docker
```dockerfile
FROM python:3.9-alpine
COPY mockpilot.py /app/
COPY mockpilot.json /app/
WORKDIR /app
EXPOSE 8080
CMD ["python3", "mockpilot.py", "start", "mockpilot.json"]
```

### Systemd Service
```ini
[Unit]
Description=MockPilot API Mock Server
After=network.target

[Service]
Type=simple
User=mockpilot
WorkingDirectory=/opt/mockpilot
ExecStart=/usr/bin/python3 /opt/mockpilot/mockpilot.py start /opt/mockpilot/config.json
Restart=always

[Install]
WantedBy=multi-user.target
```

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup

```bash
# Clone repository
git clone https://github.com/gitstq/MockPilot-Server.git
cd MockPilot-Server

# Run tests
python3 -m pytest tests/

# Format code
black mockpilot.py
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<a name="简体中文"></a>
## 🎉 项目介绍

**MockPilot-CLI** 是一个轻量级、零依赖的终端API Mock服务器，专为需要快速、灵活和智能API模拟的开发者设计。与传统需要复杂设置或繁重依赖的Mock工具不同，MockPilot完全基于Python标准库运行。

### ✨ 核心差异化亮点

- **🎯 零核心依赖** - 纯Python标准库，无需pip安装烦恼
- **🎨 动态模板引擎** - 使用内置生成器生成真实的Mock数据
- **📊 实时TUI仪表盘** - 在美观的终端界面中监控请求和响应
- **📖 OpenAPI兼容** - 导入Swagger/OpenAPI规范并自动生成Mock路由
- **⚡ 闪电般快速** - 最小开销，最大性能
- **🔧 开发者友好** - 简单的JSON配置，直观的CLI命令

---

## ✨ 核心特性

### 🎯 零依赖
```bash
# 无需安装！
python3 mockpilot.py start
```

### 🎨 动态模板引擎
内置数据生成器，用于生成真实的Mock响应：
- `{{$uuid}}` - 生成UUID v4
- `{{$name}}` - 随机全名
- `{{$email}}` - 随机邮箱地址
- `{{$phone}}` - 随机电话号码
- `{{$company}}` - 随机公司名称
- `{{$lorem}}` - Lorem ipsum文本
- `{{$date}}` / `{{$datetime}}` - 时间戳
- `{{$bool}}` - 布尔值
- `{{$int}}` / `{{$float}}` - 数字
- `{{$word}}` / `{{$sentence}}` - 文本内容

### 📊 TUI仪表盘
实时监控API请求和响应统计信息。

---

## 🚀 快速开始

### 环境要求
- Python 3.7 或更高版本
- 无需额外依赖！

### 安装

#### 方式1：直接使用（推荐）
```bash
# 克隆仓库
git clone https://github.com/gitstq/MockPilot-Server.git
cd MockPilot-Server

# 使用默认路由启动
python3 mockpilot.py start
```

#### 方式2：通过pip安装
```bash
pip install mockpilot-cli
mockpilot start
```

### 首次运行
```bash
# 创建示例配置
mockpilot init

# 启动服务器
mockpilot start mockpilot.json

# 服务器运行在 http://localhost:8080
```

---

## 📖 详细使用指南

### 配置文件

创建 `mockpilot.json` 文件：

```json
{
  "cors": {
    "enabled": true
  },
  "routes": [
    {
      "method": "GET",
      "path": "/api/users",
      "response": {
        "status": 200,
        "body": {
          "users": [
            {
              "id": "{{$uuid}}",
              "name": "{{$name}}",
              "email": "{{$email}}"
            }
          ]
        }
      }
    }
  ]
}
```

### CLI命令

```bash
# 使用配置启动服务器
mockpilot start config.json

# 验证配置
mockpilot validate config.json

# 从OpenAPI生成配置
mockpilot openapi swagger.json

# 显示版本
mockpilot version

# 显示帮助
mockpilot help
```

---

## 📄 开源协议

本项目采用 MIT 协议 - 详见 [LICENSE](LICENSE) 文件。

---

<a name="繁體中文"></a>
## 🎉 專案介紹

**MockPilot-CLI** 是一個輕量級、零依賴的終端API Mock伺服器，專為需要快速、靈活和智能API模擬的開發者設計。與傳統需要複雜設定或繁重依賴的Mock工具不同，MockPilot完全基於Python標準庫運行。

### ✨ 核心差異化亮點

- **🎯 零核心依賴** - 純Python標準庫，無需pip安裝煩惱
- **🎨 動態模板引擎** - 使用內建生成器生成真實的Mock資料
- **📊 即時TUI儀表板** - 在美觀的終端介面中監控請求和回應
- **📖 OpenAPI相容** - 匯入Swagger/OpenAPI規範並自動生成Mock路由
- **⚡ 閃電般快速** - 最小開銷，最大效能
- **🔧 開發者友善** - 簡單的JSON設定，直觀的CLI命令

---

## ✨ 核心特性

### 🎯 零依賴
```bash
# 無需安裝！
python3 mockpilot.py start
```

### 🎨 動態模板引擎
內建資料生成器，用於生成真實的Mock回應：
- `{{$uuid}}` - 生成UUID v4
- `{{$name}}` - 隨機全名
- `{{$email}}` - 隨機郵箱地址
- `{{$phone}}` - 隨機電話號碼
- `{{$company}}` - 隨機公司名稱
- `{{$lorem}}` - Lorem ipsum文本
- `{{$date}}` / `{{$datetime}}` - 時間戳
- `{{$bool}}` - 布林值
- `{{$int}}` / `{{$float}}` - 數字
- `{{$word}}` / `{{$sentence}}` - 文本內容

### 📊 TUI儀表板
即時監控API請求和回應統計資訊。

---

## 🚀 快速開始

### 環境要求
- Python 3.7 或更高版本
- 無需額外依賴！

### 安裝

#### 方式1：直接使用（推薦）
```bash
# 克隆倉庫
git clone https://github.com/gitstq/MockPilot-Server.git
cd MockPilot-Server

# 使用預設路由啟動
python3 mockpilot.py start
```

#### 方式2：透過pip安裝
```bash
pip install mockpilot-cli
mockpilot start
```

### 首次執行
```bash
# 建立範例設定
mockpilot init

# 啟動伺服器
mockpilot start mockpilot.json

# 伺服器執行於 http://localhost:8080
```

---

## 📖 詳細使用指南

### 設定檔

建立 `mockpilot.json` 檔案：

```json
{
  "cors": {
    "enabled": true
  },
  "routes": [
    {
      "method": "GET",
      "path": "/api/users",
      "response": {
        "status": 200,
        "body": {
          "users": [
            {
              "id": "{{$uuid}}",
              "name": "{{$name}}",
              "email": "{{$email}}"
            }
          ]
        }
      }
    }
  ]
}
```

### CLI命令

```bash
# 使用設定啟動伺服器
mockpilot start config.json

# 驗證設定
mockpilot validate config.json

# 從OpenAPI生成設定
mockpilot openapi swagger.json

# 顯示版本
mockpilot version

# 顯示說明
mockpilot help
```

---

## 📄 開源協議

本專案採用 MIT 協議 - 詳見 [LICENSE](LICENSE) 檔案。

---

<div align="center">

**Made with ❤️ by MockPilot Team**

[⭐ Star us on GitHub](https://github.com/gitstq/MockPilot-Server) | [🐛 Report Issue](https://github.com/gitstq/MockPilot-Server/issues)

</div>
