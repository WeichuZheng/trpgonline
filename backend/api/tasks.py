# TRPG Online - 任务板 API
import random
import re
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from backend.database import get_db
from backend.models.models import User, Module, ModuleTask, TaskClock, Room
from backend.schemas.schemas import (
    ModuleTaskCreate, ModuleTaskUpdate, ModuleTaskResponse,
    TaskClockCreate, TaskClockUpdate, TaskClockResponse
)
from backend.auth import get_current_user

router = APIRouter(prefix="/api", tags=["任务板"])


# ============ 任务 CRUD ============

@router.get("/modules/{module_id}/tasks", response_model=List[ModuleTaskResponse])
async def get_module_tasks(
    module_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取模组任务列表（含时钟）"""
    result = await db.execute(
        select(ModuleTask)
        .where(ModuleTask.module_id == module_id)
        .order_by(ModuleTask.sort_order)
        .options(selectinload(ModuleTask.clocks))
    )
    return result.unique().scalars().all()


@router.post("/modules/{module_id}/tasks", response_model=ModuleTaskResponse)
async def create_task(
    module_id: int,
    task_data: ModuleTaskCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """创建任务"""
    result = await db.execute(select(Module).where(Module.id == module_id))
    module = result.scalar_one_or_none()
    if not module:
        raise HTTPException(status_code=404, detail="模组不存在")
    if module.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="只有模组所有者可以创建任务")

    task = ModuleTask(
        module_id=module_id,
        title=task_data.title,
        description=task_data.description,
        status=task_data.status,
        exploration_percent=task_data.exploration_percent,
        sort_order=task_data.sort_order
    )
    db.add(task)
    await db.commit()
    # Reload with clocks to satisfy response schema
    result = await db.execute(
        select(ModuleTask).where(ModuleTask.id == task.id).options(selectinload(ModuleTask.clocks))
    )
    return result.unique().scalar_one()


@router.put("/tasks/{task_id}", response_model=ModuleTaskResponse)
async def update_task(
    task_id: int,
    task_data: ModuleTaskUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """更新任务（GM）"""
    result = await db.execute(
        select(ModuleTask).where(ModuleTask.id == task_id).options(selectinload(ModuleTask.clocks))
    )
    task = result.unique().scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")

    result = await db.execute(select(Module).where(Module.id == task.module_id))
    module = result.scalar_one()
    if module.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="只有模组所有者可以修改任务")

    for field, value in task_data.model_dump(exclude_unset=True).items():
        setattr(task, field, value)

    await db.commit()
    result = await db.execute(
        select(ModuleTask).where(ModuleTask.id == task.id).options(selectinload(ModuleTask.clocks))
    )
    return result.unique().scalar_one()


@router.delete("/tasks/{task_id}")
async def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """删除任务"""
    result = await db.execute(select(ModuleTask).where(ModuleTask.id == task_id))
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")

    result = await db.execute(select(Module).where(Module.id == task.module_id))
    module = result.scalar_one()
    if module.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="只有模组所有者可以删除任务")

    await db.delete(task)
    await db.commit()
    return {"message": "任务已删除"}


# ============ 时钟 CRUD ============

@router.post("/tasks/{task_id}/clocks", response_model=TaskClockResponse)
async def create_clock(
    task_id: int,
    clock_data: TaskClockCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """为任务添加时钟"""
    result = await db.execute(select(ModuleTask).where(ModuleTask.id == task_id))
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")

    result = await db.execute(select(Module).where(Module.id == task.module_id))
    module = result.scalar_one()
    if module.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="只有模组所有者可以操作")

    clock = TaskClock(
        task_id=task_id,
        total=clock_data.total,
        increment_expr=clock_data.increment_expr
    )
    db.add(clock)
    await db.commit()
    await db.refresh(clock)
    return clock


@router.put("/clocks/{clock_id}", response_model=TaskClockResponse)
async def update_clock(
    clock_id: int,
    clock_data: TaskClockUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """更新时钟"""
    result = await db.execute(select(TaskClock).where(TaskClock.id == clock_id))
    clock = result.scalar_one_or_none()
    if not clock:
        raise HTTPException(status_code=404, detail="时钟不存在")

    result = await db.execute(select(ModuleTask).where(ModuleTask.id == clock.task_id))
    task = result.scalar_one()
    result = await db.execute(select(Module).where(Module.id == task.module_id))
    module = result.scalar_one()
    if module.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="只有模组所有者可以操作")

    for field, value in clock_data.model_dump(exclude_unset=True).items():
        setattr(clock, field, value)

    await db.commit()
    await db.refresh(clock)
    return clock


@router.delete("/clocks/{clock_id}")
async def delete_clock(
    clock_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """删除时钟"""
    result = await db.execute(select(TaskClock).where(TaskClock.id == clock_id))
    clock = result.scalar_one_or_none()
    if not clock:
        raise HTTPException(status_code=404, detail="时钟不存在")

    result = await db.execute(select(ModuleTask).where(ModuleTask.id == clock.task_id))
    task = result.scalar_one()
    result = await db.execute(select(Module).where(Module.id == task.module_id))
    module = result.scalar_one()
    if module.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="只有模组所有者可以操作")

    await db.delete(clock)
    await db.commit()
    return {"message": "时钟已删除"}


# ============ 聚光灯推进 ============

def parse_dice_expr(expr: str) -> tuple:
    """解析骰子表达式如 1d3 → (count, sides)"""
    match = re.match(r'(\d*)d(\d+)', expr.lower())
    if not match:
        return 1, 1
    count = int(match.group(1)) if match.group(1) else 1
    sides = int(match.group(2))
    return count, sides


@router.post("/rooms/{room_id}/advance-clocks")
async def advance_clocks(
    room_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """GM 聚光灯：所有当前任务的关键事件时钟推进"""
    result = await db.execute(select(Room).where(Room.id == room_id))
    room = result.scalar_one_or_none()
    if not room:
        raise HTTPException(status_code=404, detail="房间不存在")
    if room.gm_id != current_user.id:
        raise HTTPException(status_code=403, detail="只有 GM 可以推进时钟")

    result = await db.execute(
        select(ModuleTask)
        .where(ModuleTask.module_id == room.module_id, ModuleTask.status == "current")
        .options(selectinload(ModuleTask.clocks))
    )
    tasks = result.unique().scalars().all()

    results = []
    for task in tasks:
        for clock in task.clocks:
            if clock.is_expired:
                continue
            count, sides = parse_dice_expr(clock.increment_expr)
            increment = sum(random.randint(1, sides) for _ in range(count))
            clock.current_value += increment
            if clock.current_value >= clock.total:
                clock.is_expired = True
            results.append({
                "clock_id": clock.id,
                "task_title": task.title,
                "increment": increment,
                "current": clock.current_value,
                "total": clock.total,
                "expired": clock.is_expired
            })
    await db.commit()

    # Broadcast via WebSocket
    from backend.websocket import manager as ws_manager
    for r in results:
        await ws_manager.broadcast_to_room(room_id, {
            "type": "clock_advanced",
            "clock_id": r["clock_id"],
            "task_title": r["task_title"],
            "increment": r["increment"],
            "current": r["current"],
            "total": r["total"],
            "expired": r["expired"]
        })

    return {"results": results}
