# TRPG Online - 主应用入口
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from backend.config import settings
from backend.database import init_db
from backend.api import auth, modules, resources, rooms, characters, maps
from backend.websocket import websocket_endpoint


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时初始化数据库
    await init_db()
    yield
    # 关闭时清理资源（如果需要）


# 创建 FastAPI 应用
app = FastAPI(
    title="跑团在线 (TRPG Online) - API 文档",
    description="多人在线跑团网站后端 API\n\n功能包括：\n- 用户注册登录 (JWT认证)\n- 模组管理 (创建、编辑、删除)\n- 资源管理 (图片上传、文本创建)\n- 资源可见性控制 (GM控制)\n- 房间系统 (创建房间、加入游戏)\n- 角色卡系统 (属性、快捷操作)\n- 掷骰子系统 (自动计算)\n- 地图编辑器 (战斗场景)\n- 实时通信 (WebSocket)",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 开发环境允许所有来源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth.router)
app.include_router(modules.router)
app.include_router(resources.router)
app.include_router(rooms.router)
app.include_router(characters.router)
app.include_router(maps.router)

# WebSocket 端点
app.websocket("/ws/room/{room_id}")(websocket_endpoint)

# 挂载静态文件目录
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
app.mount("/static", StaticFiles(directory="frontend"), name="static")


@app.get("/")
async def root():
    """根路径 - 返回前端页面"""
    from fastapi.responses import FileResponse
    return FileResponse("frontend/index.html")


@app.get("/index.html")
async def index():
    """前端入口页面"""
    from fastapi.responses import FileResponse
    return FileResponse("frontend/index.html")


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=True
    )