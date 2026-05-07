# TRPG Online 实现计划书

## 1. 项目概述

- **项目名称**: TRPG Online (跑团网站)
- **项目类型**: Web 多人在线应用
- **核心功能**: GM 创建模组和管理资源，玩家加入房间参与游戏
- **目标用户**: 跑团爱好者 (6-8人同时在线)

---

## 2. 技术栈

| 层级 | 技术方案 | 理由 |
|------|----------|------|
| 后端 | FastAPI + Python | 高性能、易维护、自动API文档 |
| 前端 | HTML + Vue 3 (CDN) | 简单、无需构建、直接用浏览器打开 |
| 数据库 | SQLite | 本地开发免安装、零配置 |
| 实时通信 | WebSocket | 掷骰子、日志、地图同步需要实时 |
| 文件存储 | 本地 uploads/ 目录 | 开发阶段先用本地存储 |

---

## 3. 功能模块与优先级

### Phase 1: 基础框架 (MVP)

| 优先级 | 功能 | 描述 |
|--------|------|------|
| P0 | 用户注册/登录 | 基础用户系统，支持"可创建模组"权限 |
| P0 | 模组 CRUD | 创建、编辑、删除自己的模组 |
| P0 | 资源上传 | 图片上传、文本创建 |
| P0 | 资源可见性 | GM 控制资源显示/隐藏 |

### Phase 2: 核心游戏功能

| 优先级 | 功能 | 描述 |
|--------|------|------|
| P1 | 文本展示系统 | 多种可配置的展示组件 |
| P1 | 房间系统 | GM 创建房间、玩家加入 |
| P1 | 角色卡 | 玩家角色数据管理 |
| P1 | 快捷操作 | 攻击等快捷按钮 + 自动掷骰 |

### Phase 3: 地图与战斗

| 优先级 | 功能 | 描述 |
|--------|------|------|
| P2 | 地图编辑器 | GM 创建战斗地图 |
| P2 | 战斗视图 | GM 拖动单位、扣血；玩家查看 |
| P2 | 日志系统 | 记录所有操作 |

### Phase 4: 后续功能

| 优先级 | 功能 | 描述 |
|--------|------|------|
| P3 | 笔记本功能 | 参与者笔记 |
| P3 | CDN 部署 | 静态资源 CDN 分发 |

---

## 4. 数据库设计

### 4.1 表结构

```sql
-- 用户表
users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    can_create_module BOOLEAN DEFAULT FALSE,  -- 可创建模组的权限
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)

-- 模组表
modules (
    id INTEGER PRIMARY KEY,
    owner_id INTEGER REFERENCES users(id),
    title TEXT NOT NULL,
    description TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
)

-- 资源表
resources (
    id INTEGER PRIMARY KEY,
    module_id INTEGER REFERENCES modules(id),
    owner_id INTEGER REFERENCES users(id),
    type TEXT CHECK(type IN ('image', 'text')),  -- image / text
    title TEXT NOT NULL,
    content TEXT,           -- 文本内容或图片URL
    is_visible BOOLEAN DEFAULT FALSE,  -- GM 控制可见性
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)

-- 房间表
rooms (
    id INTEGER PRIMARY KEY,
    module_id INTEGER REFERENCES modules(id),
    gm_id INTEGER REFERENCES users(id),  -- 房主/GM
    name TEXT NOT NULL,
    status TEXT DEFAULT 'waiting',  -- waiting / active / ended
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)

-- 房间参与者
room_participants (
    room_id INTEGER REFERENCES rooms(id),
    user_id INTEGER REFERENCES users(id),
    role TEXT DEFAULT 'player',  -- gm / player
    character_name TEXT,
    PRIMARY KEY (room_id, user_id)
)

-- 角色卡
character_cards (
    id INTEGER PRIMARY KEY,
    room_id INTEGER REFERENCES rooms(id),
    user_id INTEGER REFERENCES users(id),
    name TEXT NOT NULL,
    hp INTEGER DEFAULT 10,
    max_hp INTEGER DEFAULT 10,
    attack_bonus INTEGER DEFAULT 0,  -- 攻击加值
    damage_dice TEXT DEFAULT '1d6',  -- 伤害骰子
    notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)

-- 地图表
maps (
    id INTEGER PRIMARY KEY,
    module_id INTEGER REFERENCES modules(id),
    name TEXT NOT NULL,
    image_url TEXT,  -- 地图图片URL
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)

-- 地图单位（战斗单位）
map_units (
    id INTEGER PRIMARY KEY,
    map_id INTEGER REFERENCES maps(id),
    name TEXT NOT NULL,
    x REAL NOT NULL,
    y REAL NOT NULL,
    hp INTEGER,
    max_hp INTEGER,
    is_enemy BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)

-- 操作日志
game_logs (
    id INTEGER PRIMARY KEY,
    room_id INTEGER REFERENCES rooms(id),
    user_id INTEGER REFERENCES users(id),
    action TEXT NOT NULL,  -- attack / damage / heal / move / custom
    detail TEXT,  -- JSON 格式的详细信息
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
```

---

## 5. API 设计

### 5.1 认证 API

| 方法 | 路径 | 描述 |
|------|------|------|
| POST | /api/auth/register | 注册用户 |
| POST | /api/auth/login | 登录 |
| GET | /api/auth/me | 获取当前用户信息 |

### 5.2 模组 API

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | /api/modules | 获取我的模组列表 |
| POST | /api/modules | 创建新模组 |
| GET | /api/modules/{id} | 获取模组详情 |
| PUT | /api/modules/{id} | 更新模组 |
| DELETE | /api/modules/{id} | 删除模组 |

### 5.3 资源 API

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | /api/modules/{id}/resources | 获取模组资源列表 |
| POST | /api/modules/{id}/resources | 上传资源（图片/文本） |
| PUT | /api/resources/{id} | 更新资源（可见性等） |
| DELETE | /api/resources/{id} | 删除资源 |
| POST | /api/resources/{id}/toggle-visible | 切换可见性（GM） |

### 5.4 房间 API

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | /api/modules/{id}/rooms | 获取模组下的房间 |
| POST | /api/modules/{id}/rooms | 创建房间（GM） |
| POST | /api/rooms/{id}/join | 加入房间 |
| POST | /api/rooms/{id}/leave | 离开房间 |
| GET | /api/rooms/{id} | 获取房间详情（含玩家列表） |

### 5.5 角色卡 API

| 方法 | 路径 | 描述 |
|------|------|------|
| POST | /api/rooms/{id}/character | 创建角色卡 |
| PUT | /api/characters/{id} | 更新角色卡 |
| POST | /api/characters/{id}/attack | 快捷攻击（自动掷骰） |

### 5.6 地图 API

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | /api/modules/{id}/maps | 获取模组的地图列表 |
| POST | /api/modules/{id}/maps | 创建地图 |
| PUT | /api/maps/{id} | 更新地图（编辑模式） |
| POST | /api/maps/{id}/units | 添加单位 |
| PUT | /api/map-units/{id} | 更新单位位置/血量 |
| DELETE | /api/map-units/{id} | 删除单位 |

### 5.7 日志 API

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | /api/rooms/{id}/logs | 获取房间日志 |
| POST | /api/rooms/{id}/logs | 添加日志（GM 操作） |

### 5.8 WebSocket

| 事件 | 方向 | 描述 |
|------|------|------|
| connect | Client→Server | 加入房间websocket |
| dice_roll | Server→All | 掷骰结果广播 |
| unit_move | Server→All | 单位移动广播 |
| hp_change | Server→All | 血量变化广播 |
| new_log | Server→All | 新日志广播 |
| resource_visible | Server→All | 资源可见性变化 |

---

## 6. 前端页面结构

```
pages/
├── index.html           # 首页/登录
├── register.html        # 注册
├── dashboard.html       # 用户仪表盘（我的模组）
├── module-edit.html     # 模组编辑
├── module-view.html     # 模组浏览（资源管理）
├── room.html            # 房间内游戏界面
├── map-editor.html      # 地图编辑器
└── game-battle.html     # 战斗视图
```

### 6.1 核心页面功能

| 页面 | 功能 |
|------|------|
| dashboard | 展示我的模组列表、创建模组按钮 |
| module-edit | 编辑模组信息 |
| module-view | 资源管理：上传图片/文本、控制可见性 |
| room | 游戏主界面：文本展示区、地图、角色卡、日志 |
| map-editor | 拖拽式地图编辑器 |
| game-battle | 战斗视图：GM 拖动单位、玩家查看 |

### 6.2 文本展示组件（可配置）

| 类型 | 描述 | 样式 |
|------|------|------|
| story | 背景故事 | 大标题 + 段落文字 |
| rule | 规则说明 | 带边框的说明框 |
| clue | 线索卡 | 卡片样式、可折叠 |
| character | 角色描述 | 带头像的图片+文字 |
| mission | 任务目标 | 高亮的任务列表 |

---

## 7. 实现步骤

### Step 1: 后端基础框架
- [ ] 初始化 FastAPI 项目
- [ ] 配置 SQLite 数据库
- [ ] 实现用户认证 (JWT)
- [ ] 基础 CRUD API

### Step 2: 资源系统
- [ ] 文件上传接口
- [ ] 文本创建/编辑
- [ ] 资源可见性控制
- [ ] 资源列表 API

### Step 3: 房间与游戏
- [ ] 房间创建/加入
- [ ] WebSocket 连接
- [ ] 角色卡系统
- [ ] 掷骰子功能

### Step 4: 地图系统
- [ ] 地图编辑器前端
- [ ] 地图单位管理
- [ ] 实时位置同步
- [ ] 血量管理

### Step 5: 日志与快捷操作
- [ ] 日志系统后端
- [ ] 快捷攻击按钮
- [ ] 自动掷骰 + 广播

---

## 8. 验收标准

### 8.1 功能验收

| 功能 | 验收条件 |
|------|----------|
| 用户注册/登录 | 可以注册、登录、获取用户信息 |
| 模组管理 | 可以创建、编辑、删除自己的模组 |
| 资源上传 | 可以上传图片、创建文本 |
| 资源可见性 | GM 可以切换资源的可见状态 |
| 房间系统 | GM 创建房间、玩家加入 |
| 掷骰子 | 掷骰结果广播给所有人 |
| 地图编辑 | GM 可以添加/移动/删除单位 |
| 快捷攻击 | 点击攻击按钮，自动掷骰并写入日志 |

### 8.2 性能验收

- API 响应时间 < 200ms
- WebSocket 延迟 < 100ms
- 支持 6-8 人同时在线

---

## 9. 文件结构

```
trpgonline/
├── backend/
│   ├── main.py              # FastAPI 入口
│   ├── config.py            # 配置
│   ├── models.py            # SQLAlchemy 模型
│   ├── schemas.py           # Pydantic schemas
│   ├── database.py          # 数据库连接
│   ├── auth.py              # 认证逻辑
│   ├── api/
│   │   ├── auth.py          # 认证 API
│   │   ├── modules.py       # 模组 API
│   │   ├── resources.py     # 资源 API
│   │   ├── rooms.py         # 房间 API
│   │   ├── maps.py          # 地图 API
│   │   └── logs.py          # 日志 API
│   └── websocket.py         # WebSocket 处理
├── frontend/
│   ├── index.html           # 入口 HTML
│   ├── css/
│   │   └── style.css        # 样式
│   ├── js/
│   │   ├── app.js           # Vue 主应用
│   │   ├── api.js           # API 调用
│   │   ├── ws.js            # WebSocket
│   │   └── components/      # 组件
│   └── pages/               # 页面
├── uploads/                 # 上传的文件
├── database.db              # SQLite 数据库
├── requirements.txt         # Python 依赖
└── CLAUDE.md                # 项目文档
```

---

## 10. 下一步

确认计划书后，我将开始：

1. **Step 1**: 初始化后端项目，安装依赖
2. **Step 2**: 创建数据库模型
3. **Step 3**: 实现用户认证 API

**请确认：**
1. 以上计划是否可以？
2. 有什么需要调整的地方？

确认后我就开始写代码！
