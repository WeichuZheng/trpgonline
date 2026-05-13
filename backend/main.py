# TRPG Online - 主应用入口
import asyncio
import traceback
from datetime import datetime, timedelta, timezone, timedelta as td
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text, select, delete as sql_delete

from backend.config import settings
from backend.database import init_db, engine, AsyncSessionLocal
from backend.api import auth, modules, resources, rooms, maps, tasks, admin as admin_api
from backend.models.models import User, GameLog, cst_now
from backend.websocket import websocket_endpoint, _heartbeat_loop


async def migrate_schema():
    """为现有数据库添加缺失的列（幂等迁移）"""
    async with engine.begin() as conn:
        result = await conn.execute(text("PRAGMA table_info(users)"))
        columns = [row[1] for row in result]
        if 'is_admin' not in columns:
            await conn.execute(text("ALTER TABLE users ADD COLUMN is_admin BOOLEAN DEFAULT 0"))
        if 'requested_gm' not in columns:
            await conn.execute(text("ALTER TABLE users ADD COLUMN requested_gm BOOLEAN DEFAULT 0"))


async def ensure_initial_admin():
    """如果配置了 INITIAL_ADMIN_USERNAME 且用户已存在，确保其为管理员"""
    if settings.initial_admin_username:
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(User).where(User.username == settings.initial_admin_username)
            )
            user = result.scalar_one_or_none()
            if user and (not user.is_admin or not user.can_create_module):
                user.is_admin = True
                user.can_create_module = True
                await session.commit()


async def gamelog_cleanup_loop():
    """每小时删除超过 30 天的 GameLog 条目"""
    while True:
        await asyncio.sleep(3600)
        try:
            cutoff = cst_now() - timedelta(days=30)
            async with AsyncSessionLocal() as session:
                await session.execute(
                    sql_delete(GameLog).where(GameLog.created_at < cutoff)
                )
                await session.commit()
        except Exception:
            pass


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    await init_db()
    await migrate_schema()
    await ensure_initial_admin()
    heartbeat_task = asyncio.create_task(_heartbeat_loop())
    cleanup_task = asyncio.create_task(gamelog_cleanup_loop())
    yield
    heartbeat_task.cancel()
    cleanup_task.cancel()
    try:
        await heartbeat_task
    except asyncio.CancelledError:
        pass
    try:
        await cleanup_task
    except asyncio.CancelledError:
        pass


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


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """全局异常处理器：输出完整堆栈到终端，返回通用 500"""
    traceback.print_exc()
    return JSONResponse(
        status_code=500,
        content={"detail": "服务器内部错误"}
    )


# 配置 CORS (H3 fix: use configurable origins)
cors_origins = ["http://localhost:5173"] if settings.debug else []
if settings.cors_origins:
    cors_origins = [o.strip() for o in settings.cors_origins.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth.router)
app.include_router(modules.router)
app.include_router(resources.router)
app.include_router(rooms.rooms_list_router)
app.include_router(rooms.rooms_router)
app.include_router(maps.router)
app.include_router(tasks.router)
app.include_router(admin_api.router)

# WebSocket 端点
app.websocket("/ws/room/{room_id}")(websocket_endpoint)

# 挂载静态文件目录
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


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
