# TRPG Online - 跑团网站

多人在线跑团 (TRPG) 网站，支持 6-8 人同时在线游戏。

## 功能特点

- **用户系统** - 注册/登录，支持 GM 权限
- **模组管理** - GM 创建和管理游戏模组
- **资源管理** - 上传图片、创建文本、配置展示样式
- **资源可见性** - GM 控制资源是否展示给玩家
- **房间系统** - 创建游戏房间，玩家加入
- **角色卡** - 玩家创建角色，支持快捷操作
- **掷骰子** - 支持各种骰子，自动计算结果
- **地图编辑器** - GM 创建战斗地图
- **实时通信** - WebSocket 实时同步

## 快速开始

### 1. 安装依赖

```bash
conda create -n trpg python=3.9
conda activate trpg
pip install -r requirements.txt
```

### 2. 启动服务器

```bash
cd trpgonline
python -m uvicorn backend.main:app --reload
```

### 3. 访问网站

- 前端：http://127.0.0.1:8000/
- API 文档：http://127.0.0.1:8000/docs

### 4. 使用流程

1. **注册账号** - 建议勾选"申请成为 GM"
2. **创建模组** - GM 创建游戏剧本
3. **添加资源** - 上传图片或创建文本
4. **创建房间** - 开启一场游戏
5. **玩家加入** - 其他人通过房间号加入

## 技术栈

- 后端：Python + FastAPI
- 数据库：SQLite
- 前端：Vue 3 (CDN)
- 实时通信：WebSocket

## 目录结构

```
trpgonline/
├── backend/          # 后端代码
│   ├── api/         # API 路由
│   ├── models/      # 数据模型
│   └── schemas/     # Pydantic schemas
├── frontend/        # 前端页面
│   ├── css/        # 样式
│   └── js/         # Vue 应用
├── uploads/        # 上传的文件
├── requirements.txt
└── README.md
```

## 部署

开发完成后可部署到云服务器，并配置 CDN 加速静态资源。

## License

MIT