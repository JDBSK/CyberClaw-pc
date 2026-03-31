# CyberClaw 架构图

> 透明可控的 AI 工作台 · Transparent & Controllable AI Workspace

---

## 🎯 速览图

```mermaid
flowchart TD
    A["📥 输入层<br/>用户消息"] --> B["🧠 智能决策层<br/>双水位记忆 + Agent 循环"]
    B --> C["🛠️ 工具执行层<br/>内置工具 + 可插拔 Skills"]
    B --> D["📡 透明监控层<br/>5 类事件实时审计"]
    C --> E["🔒 安全层<br/>跨平台沙盒 + 越权拦截"]
    D -.-> E

    style A fill:#f8f9fa,stroke:#2c3e50,stroke-width:2px,color:#2c3e50
    style B fill:#3498db,stroke:#2980b9,stroke-width:2px,color:#ffffff
    style C fill:#9b59b6,stroke:#8e44ad,stroke-width:2px,color:#ffffff
    style D fill:#e74c3c,stroke:#c0392b,stroke-width:2px,color:#ffffff
    style E fill:#27ae60,stroke:#229954,stroke-width:2px,color:#ffffff
```

---

## 🔥 核心创新模块图

```mermaid
flowchart TD
    subgraph Innovations["⭐ 三大核心创新"]
        direction TB
        
        I1["🔹 创新 1<br/>两段式技能调用<br/>help → 决策 → run<br/>说明书缓存机制"]
        I2["🔹 创新 2<br/>全行为透明监控<br/>5 类事件审计<br/>JSONL + Rich UI"]
        I3["🔹 创新 3<br/>跨平台自适应<br/>系统信息注入<br/>LLM 自主选择命令"]
    end

    subgraph Foundation["🏛️ 基础架构"]
        direction TB
        F1["双水位记忆系统<br/>长期画像 + 近期摘要"]
        F2["跨平台安全沙盒<br/>Unix + Windows 越权拦截"]
    end

    Innovations --> Foundation

    style Innovations fill:#ecf0f1,stroke:#34495e,stroke-width:3px
    style I1 fill:#3498db,stroke:#2980b9,stroke-width:2px,color:#ffffff
    style I2 fill:#27ae60,stroke:#229954,stroke-width:2px,color:#ffffff
    style I3 fill:#e67e22,stroke:#d35400,stroke-width:2px,color:#ffffff
    style Foundation fill:#f8f9fa,stroke:#7f8c8d,stroke-width:2px
```

---

## 🏗️ 系统架构总览（学术风格）

```mermaid
flowchart TD
    subgraph Layer1["━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"]
        direction LR
        U1["👤 用户<br/>Telegram/CLI/WebChat"]
    end

    subgraph Layer2["━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"]
        direction LR
        I1["📥 输入接口层<br/>main.py / cli.py / Gateway"]
    end

    subgraph Layer3["━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"]
        direction LR
        C1["🧠 核心处理层"]
    end

    subgraph Layer3Detail[" "]
        direction TB
        C2["Agent 循环<br/>LangGraph StateGraph"]
        C3["双水位记忆<br/>SQLite + user_profile.md"]
    end

    subgraph Layer4["━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"]
        direction LR
        T1["🛠️ 工具执行层"]
    end

    subgraph Layer4Detail[" "]
        direction TB
        T2["内置工具<br/>文件操作/沙盒执行"]
        T3["可插拔 Skills<br/>SKILL.md 动态加载"]
    end

    subgraph Layer5["━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"]
        direction LR
        S1["🔒 安全与监控层"]
    end

    subgraph Layer5Detail[" "]
        direction TB
        S2["沙盒安全<br/>路径/命令双拦截"]
        S3["透明监控<br/>JSONL 审计日志"]
    end

    U1 --> I1
    I1 --> C1
    C1 --> C2
    C1 --> C3
    C2 --> T1
    C3 --> C2
    T1 --> T2
    T1 --> T3
    T2 --> S1
    T3 --> S1
    S1 --> S2
    S1 --> S3

    style Layer1 fill:#ffffff,stroke:#bdc3c7,stroke-width:1px,stroke-dasharray:5 5
    style Layer2 fill:#e8f4f8,stroke:#3498db,stroke-width:2px
    style Layer3 fill:#f4ecf7,stroke:#9b59b6,stroke-width:2px
    style Layer3Detail fill:#f9ebea,stroke:#e74c3c,stroke-width:1px
    style Layer4 fill:#fef9e7,stroke:#f1c40f,stroke-width:2px
    style Layer4Detail fill:#f9ebea,stroke:#e74c3c,stroke-width:1px
    style Layer5 fill:#e8f8f5,stroke:#27ae60,stroke-width:2px
    style Layer5Detail fill:#f9ebea,stroke:#e74c3c,stroke-width:1px
```

---

## 📐 核心模块详解

### 1️⃣ 两段式技能调用（预防式安全）

```mermaid
flowchart LR
    A["用户请求"] --> B["Agent 决策"]
    B --> C{"首次调用？"}
    C -->|是 | D["mode=help<br/>返回 SKILL.md"]
    C -->|否 | E["mode=run<br/>直接执行"]
    D --> F["说明书缓存到上下文"]
    F --> G{"能解决问题？"}
    G -->|是 | E
    G -->|否 | H["换工具/告知用户"]
    E --> I["执行结果"]

    style A fill:#f8f9fa,stroke:#2c3e50,stroke-width:2px
    style B fill:#3498db,stroke:#2980b9,stroke-width:2px,color:#fff
    style C fill:#f39c12,stroke:#d68910,stroke-width:2px
    style D fill:#9b59b6,stroke:#8e44ad,stroke-width:2px,color:#fff
    style E fill:#27ae60,stroke:#229954,stroke-width:2px,color:#fff
    style F fill:#e74c3c,stroke:#c0392b,stroke-width:2px,color:#fff
    style G fill:#f39c12,stroke:#d68910,stroke-width:2px
    style H fill:#95a5a6,stroke:#7f8c8d,stroke-width:2px,color:#fff
    style I fill:#27ae60,stroke:#229954,stroke-width:2px,color:#fff
```

### 2️⃣ 透明监控系统（信任建立机制）

```mermaid
flowchart TD
    A["Agent 循环"] --> B["事件触发"]
    B --> C1["🧠 llm_input"]
    B --> C2["💡 tool_call"]
    B --> C3["💻 tool_result"]
    B --> C4["🤖 ai_message"]
    B --> C5["⚙️ system_action"]

    C1 --> D["审计日志<br/>local_geek_master.jsonl"]
    C2 --> D
    C3 --> D
    C4 --> D
    C5 --> D

    D --> E["Monitor 模块<br/>tail -f 监听"]
    E --> F["Rich 终端 UI<br/>颜色/面板区分"]

    style A fill:#3498db,stroke:#2980b9,stroke-width:2px,color:#fff
    style B fill:#9b59b6,stroke:#8e44ad,stroke-width:2px,color:#fff
    style C1 fill:#e74c3c,stroke:#c0392b,stroke-width:2px,color:#fff
    style C2 fill:#e67e22,stroke:#d35400,stroke-width:2px,color:#fff
    style C3 fill:#27ae60,stroke:#229954,stroke-width:2px,color:#fff
    style C4 fill:#3498db,stroke:#2980b9,stroke-width:2px,color:#fff
    style C5 fill:#95a5a6,stroke:#7f8c8d,stroke-width:2px,color:#fff
    style D fill:#f39c12,stroke:#d68910,stroke-width:2px,color:#fff
    style E fill:#8e44ad,stroke:#7d3c98,stroke-width:2px,color:#fff
    style F fill:#27ae60,stroke:#229954,stroke-width:2px,color:#fff
```

### 3️⃣ 双水位记忆系统（个性化 + 连续性）

```mermaid
flowchart TD
    subgraph LongTerm["📌 长期记忆 (静态)"]
        L1["user_profile.md<br/>• 用户姓名/职业<br/>• 个人偏好<br/>• 特殊要求"]
        L2["save_user_profile 工具<br/>触发更新"]
    end

    subgraph ShortTerm["📝 短期记忆 (动态)"]
        S1["SQLite 数据库<br/>完整对话历史"]
        S2["自动摘要机制<br/>每 20 轮触发<br/>保留最近 10 轮"]
        S3["上下文摘要<br/>动态融合"]
    end

    subgraph Agent["🧠 Agent"]
        A1["系统提示词构建"]
        A2["注入长期画像"]
        A3["注入近期摘要"]
    end

    L1 --> A2
    L2 -.-> L1
    S1 --> S2
    S2 --> S3
    S3 --> A3
    A2 --> A1
    A3 --> A1

    style LongTerm fill:#e8f8f5,stroke:#27ae60,stroke-width:2px
    style ShortTerm fill:#fef9e7,stroke:#f1c40f,stroke-width:2px
    style Agent fill:#e8f4f8,stroke:#3498db,stroke-width:2px
```

### 4️⃣ 跨平台安全沙盒（自适应策略）

```mermaid
flowchart TD
    A["📨 工具请求<br/>文件路径 / Shell 命令"] --> B{"类型？"}
    
    B -->|文件路径 | C["🛡️ 路径安全检查"]
    C --> C1["os.path.abspath<br/>转绝对路径"]
    C1 --> C2["startswith 检查<br/>必须以 OFFICE_DIR 开头"]
    C2 --> C3{"越权？"}
    C3 -->|是 | C4["❌ PermissionError"]
    C3 -->|否 | E

    B -->|Shell 命令 | D["🛡️ 命令安全检查"]
    D --> D1["正则匹配危险模式<br/>cd .. / cd / / C:\\ / cd D:"]
    D1 --> D2{"越权？"}
    D2 -->|是 | D3["❌ 权限拒绝"]
    D2 -->|否 | E

    E["⚙️ 安全执行<br/>cwd=OFFICE_DIR<br/>timeout=60s"] --> F["🖥️ 注入系统信息<br/>[当前宿主机系统：X]"]
    F --> G["返回结果<br/>LLM 自主选择命令"]

    style A fill:#f8f9fa,stroke:#2c3e50,stroke-width:2px
    style B fill:#f39c12,stroke:#d68910,stroke-width:2px
    style C fill:#e74c3c,stroke:#c0392b,stroke-width:2px,color:#fff
    style D fill:#e74c3c,stroke:#c0392b,stroke-width:2px,color:#fff
    style E fill:#27ae60,stroke:#229954,stroke-width:2px,color:#fff
    style F fill:#3498db,stroke:#2980b9,stroke-width:2px,color:#fff
    style G fill:#9b59b6,stroke:#8e44ad,stroke-width:2px,color:#fff
```

---

## 📊 核心设计优势对比

| 设计特性 | 传统 Agent | CyberClaw | 优势 |
|---------|-----------|-----------|------|
| **工具调用** | 决定 → 立即执行 | help → 决策 → run | 预防错误，非事后补救 |
| **技能学习** | 每次从零开始 | 说明书缓存到上下文 | Token 节省 66%+ |
| **行为透明** | 黑盒 | Monitor 实时显示所有事件 | 建立信任，调试友好 |
| **记忆系统** | 单一上下文 | 长期画像 + 近期摘要 | 个性化 + 任务连续性 |
| **跨平台** | 硬编码适配 | 系统信息注入 + LLM 自适应 | 代码简洁，扩展性强 |
| **安全沙盒** | 单平台拦截 | Unix + Windows 双平台 | 全平台安全一致 |

---

## 🚀 技术栈

```
┌─────────────────────────────────────────────────────┐
│                   应用层                             │
│  main.py (CLI 入口)  │  monitor.py (监控)           │
├─────────────────────────────────────────────────────┤
│                   核心层                             │
│  agent.py (Agent 循环)  │  skill_loader.py (技能)   │
├─────────────────────────────────────────────────────┤
│                   工具层                             │
│  builtins.py (内置)  │  sandbox_tools.py (沙盒)    │
├─────────────────────────────────────────────────────┤
│                   框架层                             │
│  LangChain  │  LangGraph  │  SQLite                │
├─────────────────────────────────────────────────────┤
│                   运行时                             │
│  Python 3.10+  │  Node.js (技能脚本)                │
└─────────────────────────────────────────────────────┘
```

---

## 📁 项目结构

```
CyberClaw/
├── CyberClaw/                    # 核心包
│   ├── core/
│   │   ├── agent.py              # Agent 循环
│   │   ├── config.py             # 配置管理
│   │   ├── context.py            # 上下文修剪
│   │   ├── provider.py           # LLM 提供商
│   │   ├── skill_loader.py       # 动态技能加载
│   │   ├── logger.py             # 审计日志
│   │   └── tools/
│   │       ├── base.py           # 工具装饰器
│   │       ├── builtins.py       # 内置工具
│   │       └── sandbox_tools.py  # 沙盒工具
│   └── __init__.py
├── workspace/
│   ├── office/                   # 沙盒工位
│   │   ├── skills/               # 可插拔技能
│   │   │   ├── weather/
│   │   │   └── tavily-search/
│   │   └── .env                  # 环境变量
│   ├── memory/
│   │   └── user_profile.md       # 用户长期画像
│   └── state.sqlite3             # 对话历史
├── logs/
│   └── local_geek_master.jsonl   # 审计日志
├── main.py                       # CLI 入口
├── monitor.py                    # 监控终端
├── cli.py                        # 命令行工具
└── setup.py                      # 包配置
```

---

## 🎤 使用指南

### 30 秒快速介绍
> "CyberClaw 是一个透明可控的 AI 工作台，核心解决两个问题：**黑盒问题**（用透明监控层实时显示所有行为）和**不可控问题**（用两段式技能调用预防错误）。底层有双水位记忆系统和跨平台安全沙盒。"

### 3-5 分钟深入讲解
> "三大核心创新：
> 1. **两段式技能调用**：help → 决策 → run，说明书缓存到上下文，Token 节省 66%
> 2. **全行为透明监控**：5 类事件实时审计，JSONL 日志 + Rich 终端 UI
> 3. **跨平台自适应**：系统信息注入，LLM 自主选择命令，无需硬编码适配"

### 技术细节 Q&A
> 滚动到对应模块详解图，展开讨论具体实现。

---

> **设计哲学**: 透明 > 自动，可控 > 智能
> 
> CyberClaw 不是追求"全自动"的黑盒，而是让用户和 AI 都能清楚知道**正在发生什么**、**为什么这么做**、**接下来会怎样**。
