# TRPG Online - 管理员 API
from typing import List
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete as sql_delete

from backend.database import get_db
from backend.models.models import User, GameLog, cst_now
from backend.schemas.schemas import UserResponse, UserAdminUpdate
from backend.auth import get_current_user, require_admin

router = APIRouter(prefix="/api/admin", tags=["管理员"])


@router.get("/users", response_model=List[UserResponse])
async def list_users(
    current_user: User = Depends(get_current_user),
    _admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    """列出所有用户（仅管理员）"""
    result = await db.execute(select(User).order_by(User.created_at.desc()))
    return result.scalars().all()


@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    update_data: UserAdminUpdate,
    current_user: User = Depends(get_current_user),
    _admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    """修改用户权限（仅管理员）"""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    # 防止取消自己的管理员权限
    if user_id == current_user.id and update_data.is_admin is False:
        raise HTTPException(status_code=403, detail="不能取消自己的管理员权限")

    if update_data.can_create_module is not None:
        user.can_create_module = update_data.can_create_module
    if update_data.is_admin is not None:
        user.is_admin = update_data.is_admin

    await db.commit()
    await db.refresh(user)
    return user


@router.delete("/cleanup-logs")
async def cleanup_old_logs(
    days: int = Query(default=30, ge=7, le=365),
    current_user: User = Depends(get_current_user),
    _admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    """手动清理旧游戏日志（仅管理员）"""
    cutoff = cst_now() - timedelta(days=days)
    result = await db.execute(
        sql_delete(GameLog).where(GameLog.created_at < cutoff)
    )
    await db.commit()
    return {"message": f"已清理 {result.rowcount} 条 {days} 天前的日志"}
