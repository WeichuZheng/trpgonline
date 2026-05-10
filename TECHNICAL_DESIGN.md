# TRPG Online 技术设计文档

## 1. 技术架构

### 1.1 技术栈选型

| 层级 | 技术方案 | 理由 |
|------|----------|------|
| 后端 | FastAPI + Python | 高性能、易维护、自动API文档 |
| 前端 | Vue 3 + Vite | 组件化、响应式、热更新 |
| 数据库 | SQLite | 本地开发免安装 |
| 实时通信 | WebSocket | 掷骰子、日志、地图同步 |
| 文件存储 | 本地 uploads/ | 开发阶段先用本地存储 |

### 1.2 系统架构图

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              客户端 (浏览器)                              │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                         Vue 3 前端                              │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐      │    │
│  │  │  登录页   │  │  仪表盘   │  │  游戏房间  │  │  地图编辑  │      │    │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘      │    │
│  │       │             │             │             │             │    │
│  │  ┌────┴─────────────┴─────────────┴─────────────┴────┐       │    │
│  │  │              Pinia 状态管理                         │       │    │
│  │  └─────────────────────┬─────────────────────────────┘       │    │
│  │                        │                                      │    │
│  │  ┌─────────────────────┴─────────────────────────────┐       │    │
│  │  │              Vue Router 路由                       │       │    │
│  │  └─────────────────────┬─────────────────────────────┘       │    │
│  └────────────────────────┼────────────────────────────────────┘    │
│                            │                                          │
│                    ┌───────┴───────┐                                  │
│                    │   HTTP / WS   │                                  │
│                    └───────┬───────┘                                  │
└────────────────────────────┼──────────────────────────────────────────┘
                             │
┌────────────────────────────┼──────────────────────────────────────────┐
│                     服务器端                                            │
│                    ┌───────┴───────┐                                  │
│                    │   FastAPI     │                                  │
│                    │   (端口 8000)  │                                  │
│                    └───────┬───────┘                                  │
│                            │                                          │
│    ┌───────────────────────┼───────────────────────┐                │
│    │                       │                       │                │
│    ▼                       ▼                       ▼                │
│ ┌─────────┐         ┌─────────────┐         ┌───────────┐          │
│ │  REST   │         │  WebSocket  │         │   静态    │          │
│ │   API   │         │   实时通信   │         │   文件    │          │
│ └────┬────┘         └──────┬──────┘         └─────┬─────┘          │
│      │                     │                      │                 │
│      └─────────┬───────────┘                      │                 │
│                ▼                                  │                 │
│         ┌─────────────┐                          │                 │
│         │  SQLAlchemy │◄─────────────────────────┘                 │
│         │  (ORM 层)   │                                            │
│         └──────┬──────┘                                            │
│                ▼                                                    │
│         ┌─────────────┐                                            │
│         │   SQLite    │                                            │
│         │  数据库文件  │                                            │
│         └─────────────┘                                            │
└─────────────────────────────────────────────────────────────────────┘
```

### 1.3 前端架构（重构后）

```
frontend/
├── src/
│   ├── components/
│   │   ├── common/      # 基础组件 (Button, Modal, Card)
│   │   ├── layout/      # 布局组件 (Header, Sidebar)
│   │   ├── auth/        # 认证组件
│   │   ├── module/      # 模组组件
│   │   ├── room/        # 房间组件
│   │   └── game/        # 游戏组件
│   ├── views/           # 页面组件
│   ├── stores/          # Pinia 状态管理
│   ├── services/        # API 服务
│   ├── composables/     # 组合式函数
│   ├── router/          # Vue Router
│   ├── assets/          # 静态资源
│   └── App.vue          # 根组件
├── public/              # 公共资源
├── index.html           # 入口 HTML
├── vite.config.js       # Vite 配置
└── package.json         # 依赖配置
```

---

## 2. 页面设计规范

### 2.1 页面清单与路由

| 路由 | 页面 | 功能 |
|------|------|------|
| /login | 登录页 | 用户登录 |
| /register | 注册页 | 用户注册 |
| / | 仪表盘 | 我的模组列表 |
| /modules/create | 创建模组 | 创建新模组 |
| /modules/:id/edit | 模组编辑 | 编辑模组信息 |
| /modules/:id/resources | 资源管理 | 管理模组资源 |
| /modules/:id/maps | 地图管理 | 管理模组地图 |
| /rooms | 房间列表 | 玩家查看可加入房间 |
| /gm/rooms | GM房间管理 | GM管理房间 |
| /rooms/:id/game | 游戏房间 | 游戏主界面 |
| /rooms/:id/character | 角色卡 | 创建/编辑角色卡 |

### 2.2 页面流程图

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              用户流程                                    │
└─────────────────────────────────────────────────────────────────────────┘

                               ┌──────────────┐
                               │   登录页     │
                               │  /login      │
                               └──────┬───────┘
                                      │
                                      ▼
                               ┌──────────────┐
                    ┌──────────│   仪表盘     │──────────┐
                    │          │   /          │          │
                    │          └──────┬───────┘          │
                    │                 │                  │
           ┌────────┴────────┐        │         ┌────────┴────────┐
           │    GM 流程      │        │         │    玩家流程     │
           └────────┬────────┘        │         └────────┬────────┘
                    │                 │                  │
                    ▼                 │                  ▼
           ┌──────────────┐          │          ┌──────────────┐
           │  模组列表     │          │          │  房间列表     │
           │  /gm/modules │          │          │  /rooms       │
           └──────┬───────┘          │          └──────┬───────┘
                  │                  │                  │
                  ▼                  │                  ▼
          ┌──────────────┐          │         ┌──────────────┐
          │  模组编辑     │          │         │  加入房间    │
          │ /modules/:id │          │         │ /rooms/:id   │
          └──────┬───────┘          │         └──────┬───────┘
                 │                  │                │
        ┌────────┴────────┐         │                │
        │                 │         │                │
        ▼                 ▼         │                ▼
┌──────────────┐  ┌──────────────┐  │       ┌──────────────┐
│  资源管理     │  │  房间管理     │  │       │  游戏房间     │
│ /resources   │  │  /gm/rooms   │  │       │ /rooms/:id   │
└──────────────┘  └──────┬───────┘  │       └──────────────┘
                         │          │                │
                         ▼          │                ▼
                  ┌──────────────┐  │       ┌──────────────┐
                  │  游戏房间     │◄─┘       │  角色卡       │
                  │ /rooms/:id   │          │ /character   │
                  └──────────────┘          └──────────────┘
```

### 2.3 响应式断点

| 断点 | 宽度 | 布局 |
|------|------|------|
| mobile | < 768px | 单列布局，底部导航栏 |
| tablet | 768px-1024px | 双列布局，侧边栏可折叠 |
| desktop | > 1024px | 多列布局，固定侧边栏 |

### 2.4 页面详细规范

#### 2.4.1 登录页 (/login)
- 用户名/邮箱输入框
- 密码输入框
- "记住我" 复选框
- 登录按钮
- "还没有账号？注册" 链接
- 错误提示区域

#### 2.4.2 注册页 (/register)
- 用户名输入框
- 邮箱输入框
- 密码输入框
- 确认密码输入框
- "可创建模组" 权限复选框
- 注册按钮
- "已有账号？登录" 链接
- 表单验证提示

#### 2.4.3 仪表盘 (/)
- 欢迎消息 + 用户信息
- 模组卡片网格展示
- "创建模组" 按钮
- 快捷操作：最近访问的模组
- GM/玩家切换提示

#### 2.4.4 模组编辑 (/modules/:id/edit)
- 模组标题输入
- 模组描述富文本编辑
- 保存/取消按钮
- 返回仪表盘链接

#### 2.4.5 资源管理 (/modules/:id/resources)
- 资源列表（图片/文本分类显示）
- 上传图片区域（拖拽上传支持）
- 创建文本按钮
- 每个资源的可见性开关
- 资源预览模态框

#### 2.4.6 房间列表 (/rooms)
- 可加入房间卡片列表
- 房间状态标签（等待中/进行中）
- 玩家人数显示
- 加入按钮（需确认）
- 刷新按钮

#### 2.4.7 游戏房间 (/rooms/:id/game)
- 顶部：房间名称 + 状态 + 玩家列表
- 左侧：资源/文本展示区（可切换显示内容）
- 中间：地图视图（可选）
- 右侧：角色卡列表 + 快捷操作
- 底部：游戏日志滚动区
- 掷骰面板（浮动）

---

## 3. UI 设计规范

### 3.1 色彩系统

| 用途 | 颜色名称 | 色值 | 使用场景 |
|------|----------|------|----------|
| 主色 | 深蓝灰 | #2c3e50 | 导航栏、主要按钮背景 |
| 强调色 | 蓝色 | #3498db | 链接、次要按钮、交互元素 |
| 成功色 | 绿色 | #27ae60 | 成功状态、确认按钮 |
| 警告色 | 橙色 | #f39c12 | 警告状态、注意提示 |
| 危险色 | 红色 | #e74c3c | 错误状态、删除按钮 |
| 背景色 | 浅灰 | #f5f5f5 | 页面主背景 |
| 卡片背景 | 白色 | #ffffff | 卡片、模态框 |
| 边框色 | 灰色 | #ddd | 输入框、分割线 |
| 文字主色 | 深灰 | #333333 | 主要文字 |
| 文字次色 | 中灰 | #666666 | 次要文字、占位符 |
| 玩家颜色 | 紫色 | #9b59b6 | 玩家相关标识 |
| GM颜色 | 金色 | #f1c40f | GM相关标识 |

### 3.2 排版规范

| 元素 | 字体 | 大小 | 粗细 | 行高 |
|------|------|------|------|------|
| 标题1 | System UI, -apple-system, sans-serif | 2rem (32px) | 700 | 1.2 |
| 标题2 | System UI | 1.5rem (24px) | 600 | 1.3 |
| 标题3 | System UI | 1.25rem (20px) | 600 | 1.4 |
| 正文 | System UI | 1rem (16px) | 400 | 1.5 |
| 按钮 | System UI | 0.875rem (14px) | 500 | 1 |
| 小字 | System UI | 0.75rem (12px) | 400 | 1.4 |
| 代码 | 'Courier New', monospace | 0.875rem | 400 | 1.5 |

### 3.3 间距系统

| 名称 | 大小 | 使用场景 |
|------|------|----------|
| xs | 4px | 组件内部小间距 |
| sm | 8px | 组件内元素间距 |
| md | 16px | 组件之间间距 |
| lg | 24px | 区块之间间距 |
| xl | 32px | 页面大区块间距 |
| xxl | 48px | 页面顶部/底部留白 |

### 3.4 组件规范

#### 按钮
```css
.btn {
  border-radius: 4px;
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
}

.btn-primary {
  background: #3498db;
  color: white;
}
.btn-primary:hover {
  background: #2980b9;
}

.btn-danger {
  background: #e74c3c;
  color: white;
}
.btn-danger:hover {
  background: #c0392b;
}

.btn-success {
  background: #27ae60;
  color: white;
}
.btn-success:hover {
  background: #229954;
}
```

#### 卡片
```css
.card {
  background: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 16px;
  transition: box-shadow 0.2s ease;
}
.card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}
```

#### 输入框
```css
.input {
  border-radius: 4px;
  border: 1px solid #ddd;
  padding: 0.5rem 0.75rem;
  font-size: 1rem;
  transition: border-color 0.2s ease;
}
.input:focus {
  outline: none;
  border-color: #3498db;
  box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
}
```

#### 模态框
```css
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
  max-width: 90vw;
  max-height: 90vh;
  overflow: auto;
  animation: modalSlideIn 0.2s ease;
}

@keyframes modalSlideIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

### 3.5 动画规范

| 动画名称 | 持续时间 | 缓动函数 | 使用场景 |
|----------|----------|----------|----------|
| fade | 0.2s | ease | 元素淡入淡出 |
| slide | 0.2s | ease | 元素滑入滑出 |
| scale | 0.15s | ease | 元素缩放 |
| pulse | 1s | ease-in-out | 脉冲动画（用于提示） |

```css
/* 过渡基类 */
.transition {
  transition: all 0.2s ease;
}

/* 悬停效果 */
.hover-lift:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

/* 点击反馈 */
.active-scale:active {
  transform: scale(0.98);
}
```

### 3.6 图标规范

使用 SVG 图标，尺寸规范：
- 小图标: 16x16px (用于按钮内)
- 中图标: 24x24px (用于列表项)
- 大图标: 32x32px (用于空状态)

图标颜色跟随文字颜色，hover 时使用强调色。

---

## 4. 前端架构重构

### 4.1 当前问题

1. 所有代码在一个 index.html 文件
2. 没有组件拆分
3. 没有路由管理（v-if 切换）
4. 没有状态管理方案
5. CSS 缺乏设计系统
6. 代码难以维护和扩展

### 4.2 重构方案

使用 Vue 3 + Vite + Vue Router + Pinia 重构前端架构，实现真正的组件化开发。

### 4.3 技术选型

| 类别 | 技术 | 版本 |
|------|------|------|
| 构建工具 | Vite | 5.x |
| 框架 | Vue | 3.4+ |
| 路由 | Vue Router | 4.x |
| 状态管理 | Pinia | 2.x |
| HTTP 客户端 | Axios | 1.x |
| CSS 预处理器 | SCSS | 可选 |

### 4.4 目录结构详细说明

```
frontend/
├── src/
│   ├── components/
│   │   ├── common/           # 基础组件（可复用）
│   │   │   ├── AppButton.vue
│   │   │   ├── AppCard.vue
│   │   │   ├── AppModal.vue
│   │   │   ├── AppInput.vue
│   │   │   ├── AppSelect.vue
│   │   │   ├── AppToast.vue
│   │   │   └── index.js
│   │   ├── layout/           # 布局组件
│   │   │   ├── AppHeader.vue
│   │   │   ├── AppSidebar.vue
│   │   │   ├── AppFooter.vue
│   │   │   └── index.js
│   │   ├── auth/             # 认证相关组件
│   │   │   ├── LoginForm.vue
│   │   │   ├── RegisterForm.vue
│   │   │   └── index.js
│   │   ├── module/           # 模组相关组件
│   │   │   ├── ModuleCard.vue
│   │   │   ├── ModuleList.vue
│   │   │   ├── ModuleForm.vue
│   │   │   ├── ResourceCard.vue
│   │   │   ├── ResourceUpload.vue
│   │   │   └── index.js
│   │   ├── room/             # 房间相关组件
│   │   │   ├── RoomCard.vue
│   │   │   ├── RoomList.vue
│   │   │   ├── PlayerList.vue
│   │   │   └── index.js
│   │   ├── game/             # 游戏相关组件
│   │   │   ├── DicePanel.vue
│   │   │   ├── GameLog.vue
│   │   │   ├── CharacterPanel.vue
│   │   │   ├── TextDisplay.vue
│   │   │   ├── MapView.vue
│   │   │   └── index.js
│   │   └── index.js          # 组件导出入口
│   │
│   ├── views/                # 页面组件（路由视图）
│   │   ├── LoginView.vue
│   │   ├── RegisterView.vue
│   │   ├── DashboardView.vue
│   │   ├── ModuleCreateView.vue
│   │   ├── ModuleEditView.vue
│   │   ├── ModuleResourcesView.vue
│   │   ├── RoomListView.vue
│   │   ├── GmRoomListView.vue
│   │   ├── GameRoomView.vue
│   │   ├── CharacterEditView.vue
│   │   └── NotFoundView.vue
│   │
│   ├── stores/               # Pinia 状态管理
│   │   ├── auth.js           # 用户认证状态
│   │   ├── modules.js        # 模组状态
│   │   ├── rooms.js          # 房间状态
│   │   ├── game.js           # 游戏状态（当前房间、玩家、资源、日志）
│   │   └── index.js          # store 导出入口
│   │
│   ├── services/             # API 服务层
│   │   ├── api.js            # Axios 实例配置
│   │   ├── authService.js    # 认证 API
│   │   ├── moduleService.js  # 模组 API
│   │   ├── resourceService.js# 资源 API
│   │   ├── roomService.js    # 房间 API
│   │   ├── characterService.js# 角色卡 API
│   │   ├── diceService.js    # 掷骰 API
│   │   ├── mapService.js     # 地图 API
│   │   ├── logService.js     # 日志 API
│   │   └── index.js          # 服务导出入口
│   │
│   ├── composables/          # 组合式函数
│   │   ├── useAuth.js        # 认证相关逻辑
│   │   ├── useWebSocket.js   # WebSocket 连接
│   │   ├── useDice.js        # 掷骰逻辑
│   │   ├── useNotification.js# 通知提示
│   │   └── index.js          # composable 导出入口
│   │
│   ├── router/               # 路由配置
│   │   ├── index.js          # 路由主配置
│   │   ├── routes.js         # 路由定义
│   │   └── guards.js         # 路由守卫
│   │
│   ├── assets/               # 静态资源
│   │   ├── styles/           # 全局样式
│   │   │   ├── variables.scss
│   │   │   ├── base.scss
│   │   │   ├── utilities.scss
│   │   │   └── main.scss
│   │   └── images/           # 图片资源
│   │
│   ├── utils/                # 工具函数
│   │   ├── format.js         # 格式化函数
│   │   ├── validation.js     # 验证函数
│   │   └── constants.js      # 常量定义
│   │
│   ├── App.vue               # 根组件
│   └── main.js               # 应用入口
│
├── public/                   # 公共资源
│   ├── favicon.ico
│   └── robots.txt
│
├── index.html                # 入口 HTML
├── vite.config.js            # Vite 配置
├── package.json              # 依赖配置
├── .env                      # 环境变量
└── .env.example              # 环境变量模板
```

### 4.5 组件划分原则

| 类型 | 命名规范 | 存放位置 | 说明 |
|------|----------|----------|------|
| 基础组件 | AppXxx.vue | components/common/ | 基础 UI 组件，无业务逻辑 |
| 布局组件 | AppXxx.vue | components/layout/ | 页面布局相关 |
| 业务组件 | XxxCard/ XxxPanel | components/模块/ | 包含业务逻辑的可复用组件 |
| 页面组件 | XxxView.vue | views/ | 对应路由的页面组件 |
| 路由组件 | - | router/ | 路由配置相关 |

### 4.6 状态管理 (Pinia) 设计

#### auth.js - 用户认证状态
```javascript
// 状态
- user: User | null
- token: string | null
- isAuthenticated: boolean

// actions
- login(credentials)
- register(userData)
- logout()
- fetchCurrentUser()
- setToken(token)
```

#### modules.js - 模组状态
```javascript
// 状态
- modules: Module[]
- currentModule: Module | null
- isLoading: boolean

// actions
- fetchModules()
- fetchModule(id)
- createModule(data)
- updateModule(id, data)
- deleteModule(id)
```

#### rooms.js - 房间状态
```javascript
// 状态
- rooms: Room[]
- currentRoom: Room | null
- participants: Participant[]

// actions
- fetchRooms()
- fetchGmRooms()
- createRoom(moduleId, data)
- joinRoom(roomId)
- leaveRoom(roomId)
- startGame(roomId)
- endGame(roomId)
```

#### game.js - 游戏状态
```javascript
// 状态
- currentRoom: Room | null
- players: Player[]
- characters: Character[]
- resources: Resource[]
- logs: GameLog[]
- diceResult: DiceResult | null
- mapData: MapData | null
- wsConnected: boolean

// actions
- connectWebSocket(roomId)
- disconnectWebSocket()
- rollDice(diceType)
- sendChatMessage(message)
- updateCharacter(characterId, data)
- showResource(resourceId)
- hideResource(resourceId)
- moveUnit(unitId, x, y)
- updateUnitHp(unitId, hp)
```

### 4.7 重构实施计划

| 阶段 | 内容 | 优先级 |
|------|------|--------|
| Step 1 | 搭建 Vue 3 + Vite 项目基础 | P0 |
| Step 2 | 配置 Vue Router 路由系统 | P0 |
| Step 3 | 创建基础组件库 (Button/Modal/Card) | P0 |
| Step 4 | 实现 Pinia 状态管理 | P0 |
| Step 5 | 迁移登录/注册页面 | P1 |
| Step 6 | 迁移仪表盘页面 | P1 |
| Step 7 | 迁移模组管理页面 | P1 |
| Step 8 | 迁移房间系统页面 | P1 |
| Step 9 | 迁移游戏主界面 | P1 |
| Step 10 | 添加 WebSocket 连接 | P2 |
| Step 11 | 性能优化与测试 | P2 |

---

## 5. 开发进度跟踪

### 5.1 当前状态总览

| 阶段 | 进度 | 状态 |
|------|------|------|
| Phase 1: 基础框架 | 基本完成（小问题待修复） | ⚠️ |
| Phase 2: 核心游戏功能 | 待开发 | ⏳ |
| Phase 3: 地图功能 | 待开发 | ⏳ |
| Phase 4: 优化与后续 | 待开发 | ⏳ |

### 5.2 Phase 1: 基础框架

**已完成**：
- [x] 用户注册/登录
- [x] 模组 CRUD
- [x] 资源上传与可见性
- [x] 房间系统基础
- [x] 房间列表界面（需重构）

**待修复**：
- [ ] 前端模态框回调问题
- [ ] 创建房间后跳转

### 5.3 Phase 2: 核心游戏功能

**任务**：
- [ ] 完善房间系统（加入/离开/状态管理）
- [ ] 角色卡系统（创建/编辑/快捷操作）
- [ ] 掷骰子功能
- [ ] 游戏日志系统
- [ ] 文本展示组件
- [ ] 快捷操作（攻击）

### 5.4 Phase 3: 地图功能

**任务**：
- [ ] 地图显示（显示模组中的地图图片）
- [ ] 地图标记（在地图上添加标记点）
- [ ] 标记移动（GM 可拖动标记移动位置）
- [ ] 标记显示（玩家可查看标记位置和状态）

### 5.5 Phase 4: 优化与后续

**任务**：
- [ ] 笔记本功能（参与者笔记）
- [ ] CDN 部署准备
- [ ] 性能优化

### 5.6 检查点清单

| 检查点 | 内容 | 状态 |
|--------|------|------|
| CP 1.1 | 项目初始化 | ✅ 已完成 |
| CP 1.2 | 用户认证 | ✅ 已完成 |
| CP 1.3 | 模组与资源 | ⚠️ 部分完成 |
| CP 2.1 | 房间系统 | ⏳ 待开始 |
| CP 2.2 | 角色卡与掷骰 | ⏳ 待开始 |
| CP 2.3 | 文本展示与快捷操作 | ⏳ 待开始 |
| CP 3.1 | 地图标记功能 | ⏳ 待开始 |
| CP 3.2 | 地图显示与同步 | ⏳ 待开始 |
| CP 3.3 | 日志系统 | ⏳ 待开始 |

---

## 6. 验收标准

### 6.1 功能验收

| 功能 | 验收条件 | 状态 |
|------|----------|------|
| 用户注册/登录 | 可以注册、登录、获取 token | ✅ |
| 权限控制 | "可创建模组"权限正常工作 | ✅ |
| 模组 CRUD | 创建/编辑/删除自己的模组 | ✅ |
| 图片上传 | 上传图片到指定模组 | ✅ |
| 文本创建 | 创建文本内容 | ✅ |
| 资源可见性 | GM 可以切换资源显示/隐藏 | ✅ |
| 资源权限 | 上传者可以删除自己的资源 | ✅ |
| 房间创建 | GM 创建房间成功 | ⚠️ 有问题 |
| 房间加入 | 玩家可以加入房间 | ✅ |
| 人数限制 | 6-8 人上限 | ✅ |
| 掷骰子 | 掷骰结果正确 | ✅ |
| 游戏日志 | 记录操作 | ✅ |
| 地图编辑 | GM 可以添加/移动/删除单位 | ⏳ |
| 快捷攻击 | 点击攻击按钮自动掷骰并广播 | ⏳ |

### 6.2 前端验收（重构后）

| 检查点 | 标准 |
|--------|------|
| 路由管理 | 使用 Vue Router，无 v-if 切换视图 |
| 组件化 | 基础组件与业务组件分离 |
| 状态管理 | 使用 Pinia 管理共享状态 |
| 代码组织 | 目录结构清晰，模块化拆分 |
| UI 一致性 | 遵循设计规范 |
| 响应式 | 移动端/平板/桌面正常显示 |

### 6.3 性能验收

| 指标 | 标准 |
|------|------|
| API 响应时间 | < 200ms |
| WebSocket 延迟 | < 100ms |
| 同时在线人数 | 6-8 人流畅 |
| 首屏加载时间 | < 3s |
| 内存占用 | < 200MB |

### 6.4 安全验收

| 检查项 | 标准 |
|--------|------|
| 密码存储 | 使用 bcrypt 哈希 |
| Token 过期 | 合理设置过期时间 |
| 输入验证 | 所有输入参数验证 |
| SQL 注入 | 使用参数化查询 |
| XSS 防护 | 用户输入正确转义 |
| 权限隔离 | GM 和玩家权限正确分离 |

---

## 7. API 设计

### 7.1 认证 API

| 方法 | 路径 | 描述 | 认证 |
|------|------|------|------|
| POST | /api/auth/register | 注册用户 | 否 |
| POST | /api/auth/login | 登录 | 否 |
| GET | /api/auth/me | 获取当前用户信息 | 是 |

### 7.2 模组 API

| 方法 | 路径 | 描述 | 认证 |
|------|------|------|------|
| GET | /api/modules | 获取我的模组列表 | 是 |
| POST | /api/modules | 创建新模组 | 是 |
| GET | /api/modules/{id} | 获取模组详情 | 是 |
| PUT | /api/modules/{id} | 更新模组 | 是 |
| DELETE | /api/modules/{id} | 删除模组 | 是 |

### 7.3 资源 API

| 方法 | 路径 | 描述 | 认证 |
|------|------|------|------|
| GET | /api/modules/{id}/resources | 获取模组资源列表 | 是 |
| POST | /api/modules/{id}/resources | 上传资源（图片/文本） | 是 |
| PUT | /api/resources/{id} | 更新资源（可见性等） | 是 |
| DELETE | /api/resources/{id} | 删除资源 | 是 |
| POST | /api/resources/{id}/toggle-visible | 切换可见性（GM） | 是 |

### 7.4 房间 API

| 方法 | 路径 | 描述 | 认证 |
|------|------|------|------|
| GET | /api/rooms | 获取所有房间（玩家） | 是 |
| GET | /api/rooms/gm | 获取 GM 的房间列表 | 是 |
| POST | /api/modules/{id}/rooms | 创建房间 | 是 |
| PUT | /api/rooms/{id} | 修改房间 | 是 |
| DELETE | /api/rooms/{id} | 删除房间 | 是 |
| GET | /api/rooms/{id} | 获取房间详情 | 是 |
| POST | /api/rooms/{id}/join | 加入房间 | 是 |
| POST | /api/rooms/{id}/leave | 离开房间 | 是 |
| POST | /api/rooms/{id}/start | 开始游戏 | 是 |
| POST | /api/rooms/{id}/end | 结束游戏 | 是 |

### 7.5 角色卡 API

| 方法 | 路径 | 描述 | 认证 |
|------|------|------|------|
| GET | /api/rooms/{id}/characters | 获取房间角色卡 | 是 |
| POST | /api/rooms/{id}/characters | 创建角色卡 | 是 |
| PUT | /api/characters/{id} | 更新角色卡 | 是 |
| DELETE | /api/characters/{id} | 删除角色卡 | 是 |
| POST | /api/characters/{id}/attack | 快捷攻击 | 是 |

### 7.6 掷骰子 API

| 方法 | 路径 | 描述 | 认证 |
|------|------|------|------|
| POST | /api/rooms/{id}/dice | 掷骰子 | 是 |

### 7.7 日志 API

| 方法 | 路径 | 描述 | 认证 |
|------|------|------|------|
| GET | /api/rooms/{id}/logs | 获取房间日志 | 是 |
| POST | /api/rooms/{id}/logs | 添加日志 | 是 |

### 7.8 地图 API

| 方法 | 路径 | 描述 | 认证 |
|------|------|------|------|
| GET | /api/modules/{id}/maps | 获取模组的地图列表 | 是 |
| POST | /api/modules/{id}/maps | 创建地图 | 是 |
| PUT | /api/maps/{id} | 更新地图（编辑模式） | 是 |
| DELETE | /api/maps/{id} | 删除地图 | 是 |
| POST | /api/maps/{id}/units | 添加单位 | 是 |
| PUT | /api/map-units/{id} | 更新单位位置/血量 | 是 |
| DELETE | /api/map-units/{id} | 删除单位 | 是 |

### 7.9 WebSocket 事件

| 事件名 | 方向 | 描述 | 数据格式 |
|--------|------|------|----------|
| connect | Client→Server | 加入房间 WebSocket | `{ room_id, token }` |
| disconnect | Client→Server | 离开房间 | - |
| dice_roll | Server→All | 掷骰结果广播 | `{ player, dice_type, result, timestamp }` |
| unit_move | Server→All | 单位移动广播 | `{ unit_id, x, y }` |
| hp_change | Server→All | 血量变化广播 | `{ unit_id, hp, max_hp }` |
| new_log | Server→All | 新日志广播 | `{ log }` |
| resource_visible | Server→All | 资源可见性变化 | `{ resource_id, is_shown }` |
| player_join | Server→All | 玩家加入广播 | `{ player }` |
| player_leave | Server→All | 玩家离开广播 | `{ player_id }` |
| game_start | Server→All | 游戏开始广播 | `{ room_id }` |
| game_end | Server→All | 游戏结束广播 | `{ room_id }` |

### 7.10 API 响应格式

**成功响应**
```json
{
  "success": true,
  "data": { ... },
  "message": "操作成功"
}
```

**错误响应**
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "错误描述"
  }
}
```

---

## 8. 数据库设计

### 8.1 表结构总览

```sql
-- 用户表
users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    can_create_module BOOLEAN DEFAULT FALSE,
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
    type TEXT CHECK(type IN ('image', 'text')),
    title TEXT NOT NULL,
    content TEXT,
    display_type TEXT DEFAULT 'story',
    default_visible BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)

-- 房间资源可见性表
room_resources (
    room_id INTEGER REFERENCES rooms(id),
    resource_id INTEGER REFERENCES resources(id),
    is_shown BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (room_id, resource_id)
)

-- 房间表
rooms (
    id INTEGER PRIMARY KEY,
    module_id INTEGER REFERENCES modules(id),
    gm_id INTEGER REFERENCES users(id),
    name TEXT NOT NULL,
    status TEXT DEFAULT 'waiting',
    max_players INTEGER DEFAULT 8,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)

-- 房间参与者
room_participants (
    room_id INTEGER REFERENCES rooms(id),
    user_id INTEGER REFERENCES users(id),
    role TEXT DEFAULT 'player',
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
    attack_bonus INTEGER DEFAULT 0,
    damage_dice TEXT DEFAULT '1d6',
    notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)

-- 地图表
maps (
    id INTEGER PRIMARY KEY,
    module_id INTEGER REFERENCES modules(id),
    name TEXT NOT NULL,
    image_url TEXT,
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
    action TEXT NOT NULL,
    detail TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
```

### 8.2 索引设计

```sql
-- 用户名唯一索引
CREATE UNIQUE INDEX idx_users_username ON users(username);

-- 模组拥有者索引
CREATE INDEX idx_modules_owner ON modules(owner_id);

-- 资源模组索引
CREATE INDEX idx_resources_module ON resources(module_id);

-- 房间模组索引
CREATE INDEX idx_rooms_module ON rooms(module_id);

-- 房间参与者索引
CREATE INDEX idx_room_participants_room ON room_participants(room_id);
CREATE INDEX idx_room_participants_user ON room_participants(user_id);

-- 角色卡房间索引
CREATE INDEX idx_character_cards_room ON character_cards(room_id);

-- 游戏日志房间索引
CREATE INDEX idx_game_logs_room ON game_logs(room_id);
CREATE INDEX idx_game_logs_created ON game_logs(created_at);
```

### 8.3 关系图

```
┌─────────┐       ┌──────────┐       ┌─────────┐
│  users  │───────│ modules  │───────│ resources│
└─────────┘       └──────────┘       └─────────┘
      │                 │                  │
      │                 │                  │
      │                 ▼                  │
      │            ┌─────────┐             │
      └───────────►│  rooms  │◄────────────┘
                   └─────────┘
                        │
          ┌─────────────┼─────────────┐
          │             │             │
          ▼             ▼             ▼
   ┌────────────┐ ┌──────────┐ ┌──────────┐
   │ room_      │ │ character│ │  maps    │
   │ participants│ │ _cards   │ └────┬─────┘
   └────────────┘ └──────────┘      │
                                    ▼
                             ┌──────────┐
                             │ map_units│
                             └──────────┘

     ┌──────────┐
     │ game_logs│
     └──────────┘
```

---

## 9. 安全设计

### 9.1 认证与授权

- JWT Token 认证
- Token 过期时间：24 小时
- 密码使用 bcrypt 哈希
- 权限检查装饰器

### 9.2 数据安全

- SQL 注入防护：使用 SQLAlchemy 参数化查询
- XSS 防护：用户输出进行转义
- CORS 配置：限制允许的来源

### 9.3 文件安全

- 上传文件类型限制（图片：jpg, png, gif, webp）
- 文件大小限制：10MB
- 文件重命名：使用 UUID

---

## 10. 部署说明

### 10.1 开发环境

```bash
# 启动后端
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 启动前端（重构后）
cd frontend
npm run dev
```

### 10.2 生产环境

- 使用 Gunicorn + Uvicorn 部署后端
- 前端构建：`npm run build`
- 使用 Nginx 作为反向代理
- 静态文件由 Nginx 服务

---

**文档版本**: 1.0
**创建日期**: 2026/05/08
**最后更新**: 2026/05/08

**注意**：此文档是所有开发工作的最高参考，以后的功能开发必须按照此文档的规范执行。

**待办**：前端重构（从当前的单文件架构改为 Vue 3 + Vite + Router + Pinia）
