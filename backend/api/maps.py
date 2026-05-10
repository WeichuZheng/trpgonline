# TRPG Online - 地图 API
import os
import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.config import settings
from backend.database import get_db
from backend.models.models import User, Module, Map, MapUnit
from backend.schemas.schemas import (
    MapCreate, MapUpdate, MapResponse, MapWithUnits,
    MapUnitCreate, MapUnitUpdate, MapUnitResponse
)
from backend.auth import get_current_user

router = APIRouter(prefix="/api", tags=["地图编辑器"])


@router.get("/modules/{module_id}/maps", response_model=List[MapResponse])
async def get_module_maps(
    module_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取模组的地图列表"""
    result = await db.execute(select(Map).where(Map.module_id == module_id))
    maps = result.scalars().all()
    return maps


@router.post("/modules/{module_id}/maps", response_model=MapResponse)
async def create_map(
    module_id: int,
    name: str = Form(...),
    grid_size: str = Form(None),
    file: UploadFile = File(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """创建地图"""
    # 检查模组
    result = await db.execute(select(Module).where(Module.id == module_id))
    module = result.scalar_one_or_none()
    if not module:
        raise HTTPException(status_code=404, detail="模组不存在")

    if module.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="只有模组所有者可以管理地图")

    # 处理图片上传
    image_url = None
    if file:
        ext = os.path.splitext(file.filename)[1].lower()
        allowed = {'.png', '.jpg', '.jpeg', '.gif', '.webp'}
        if ext not in allowed:
            raise HTTPException(status_code=400, detail="不支持的图片格式")

        filename = f"{uuid.uuid4()}{ext}"
        file_path = os.path.join(settings.upload_dir, filename)
        content = await file.read()
        with open(file_path, 'wb') as f:
            f.write(content)
        image_url = f"/uploads/{filename}"

    parsed_grid_size = float(grid_size) if grid_size else None

    new_map = Map(
        module_id=module_id,
        name=name,
        image_url=image_url,
        grid_size=parsed_grid_size
    )
    db.add(new_map)
    await db.commit()
    await db.refresh(new_map)
    return new_map


@router.get("/maps/{map_id}", response_model=MapWithUnits)
async def get_map(map_id: int, db: AsyncSession = Depends(get_db)):
    """获取地图详情（含单位）"""
    result = await db.execute(select(Map).where(Map.id == map_id))
    map_data = result.scalar_one_or_none()
    if not map_data:
        raise HTTPException(status_code=404, detail="地图不存在")

    result = await db.execute(select(MapUnit).where(MapUnit.map_id == map_id))
    units = result.scalars().all()

    return MapWithUnits(
        id=map_data.id,
        module_id=map_data.module_id,
        name=map_data.name,
        image_url=map_data.image_url,
        created_at=map_data.created_at,
        units=[MapUnitResponse.model_validate(u) for u in units]
    )


@router.put("/maps/{map_id}", response_model=MapResponse)
async def update_map(
    map_id: int,
    map_data: MapUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """更新地图"""
    result = await db.execute(select(Map).where(Map.id == map_id))
    map_data_obj = result.scalar_one_or_none()
    if not map_data_obj:
        raise HTTPException(status_code=404, detail="地图不存在")

    # 检查权限
    result = await db.execute(select(Module).where(Module.id == map_data_obj.module_id))
    module = result.scalar_one()
    if module.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权限")

    if map_data.name is not None:
        map_data_obj.name = map_data.name
    if map_data.image_url is not None:
        map_data_obj.image_url = map_data.image_url
    if map_data.grid_size is not None:
        map_data_obj.grid_size = map_data.grid_size

    await db.commit()
    await db.refresh(map_data_obj)
    return map_data_obj


@router.delete("/maps/{map_id}")
async def delete_map(
    map_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """删除地图"""
    result = await db.execute(select(Map).where(Map.id == map_id))
    map_obj = result.scalar_one_or_none()
    if not map_obj:
        raise HTTPException(status_code=404, detail="地图不存在")

    result = await db.execute(select(Module).where(Module.id == map_obj.module_id))
    module = result.scalar_one()
    if module.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权限")

    await db.delete(map_obj)
    await db.commit()
    return {"message": "地图已删除"}


@router.post("/maps/{map_id}/units", response_model=MapUnitResponse)
async def create_map_unit(
    map_id: int,
    unit_data: MapUnitCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """添加地图单位"""
    result = await db.execute(select(Map).where(Map.id == map_id))
    map_obj = result.scalar_one_or_none()
    if not map_obj:
        raise HTTPException(status_code=404, detail="地图不存在")

    result = await db.execute(select(Module).where(Module.id == map_obj.module_id))
    module = result.scalar_one()
    if module.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权限")

    new_unit = MapUnit(
        map_id=map_id,
        character_id=unit_data.character_id,
        name=unit_data.name,
        x=unit_data.x,
        y=unit_data.y,
        width=unit_data.width,
        height=unit_data.height,
        hp=unit_data.hp,
        max_hp=unit_data.max_hp,
        is_enemy=unit_data.is_enemy,
        icon=unit_data.icon
    )
    db.add(new_unit)
    await db.commit()
    await db.refresh(new_unit)
    return new_unit


@router.put("/map-units/{unit_id}", response_model=MapUnitResponse)
async def update_map_unit(
    unit_id: int,
    unit_data: MapUnitUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """更新地图单位（位置/血量）"""
    result = await db.execute(select(MapUnit).where(MapUnit.id == unit_id))
    unit = result.scalar_one_or_none()
    if not unit:
        raise HTTPException(status_code=404, detail="单位不存在")

    # 检查权限 - 需要是模组所有者
    result = await db.execute(select(Map).where(Map.id == unit.map_id))
    map_obj = result.scalar_one()
    result = await db.execute(select(Module).where(Module.id == map_obj.module_id))
    module = result.scalar_one()
    if module.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权限")

    if unit_data.name is not None:
        unit.name = unit_data.name
    if unit_data.character_id is not None:
        unit.character_id = unit_data.character_id
    if unit_data.x is not None:
        unit.x = unit_data.x
    if unit_data.y is not None:
        unit.y = unit_data.y
    if unit_data.width is not None:
        unit.width = unit_data.width
    if unit_data.height is not None:
        unit.height = unit_data.height
    if unit_data.hp is not None:
        unit.hp = unit_data.hp
    if unit_data.max_hp is not None:
        unit.max_hp = unit_data.max_hp
    if unit_data.is_enemy is not None:
        unit.is_enemy = unit_data.is_enemy
    if unit_data.icon is not None:
        unit.icon = unit_data.icon

    await db.commit()
    await db.refresh(unit)
    return unit


@router.delete("/map-units/{unit_id}")
async def delete_map_unit(
    unit_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """删除地图单位"""
    result = await db.execute(select(MapUnit).where(MapUnit.id == unit_id))
    unit = result.scalar_one_or_none()
    if not unit:
        raise HTTPException(status_code=404, detail="单位不存在")

    result = await db.execute(select(Map).where(Map.id == unit.map_id))
    map_obj = result.scalar_one()
    result = await db.execute(select(Module).where(Module.id == map_obj.module_id))
    module = result.scalar_one()
    if module.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权限")

    await db.delete(unit)
    await db.commit()
    return {"message": "单位已删除"}