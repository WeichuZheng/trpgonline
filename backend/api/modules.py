# TRPG Online - 模组 API
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.database import get_db
from backend.models.models import User, Module
from backend.schemas.schemas import ModuleCreate, ModuleUpdate, ModuleResponse, ModuleWithOwner
from backend.auth import get_current_user

router = APIRouter(prefix="/api/modules", tags=["模组管理"])


@router.get("", response_model=List[ModuleWithOwner])
async def get_modules(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取当前用户有权访问的模组列表"""
    # 获取用户拥有的模组
    result = await db.execute(
        select(Module)
        .where(Module.owner_id == current_user.id)
        .order_by(Module.updated_at.desc())
    )
    modules = result.scalars().all()

    # 转换为响应格式（包含 owner_username）
    return [
        ModuleWithOwner(
            id=m.id,
            owner_id=m.owner_id,
            title=m.title,
            description=m.description,
            created_at=m.created_at,
            updated_at=m.updated_at,
            owner_username=current_user.username
        )
        for m in modules
    ]


@router.post("", response_model=ModuleResponse)
async def create_module(
    module_data: ModuleCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """创建新模组（需要 can_create_module 权限）"""
    if not current_user.can_create_module:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="您没有创建模组的权限"
        )

    new_module = Module(
        owner_id=current_user.id,
        title=module_data.title,
        description=module_data.description
    )
    db.add(new_module)
    await db.commit()
    await db.refresh(new_module)
    return new_module


@router.get("/{module_id}", response_model=ModuleWithOwner)
async def get_module(
    module_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取模组详情"""
    result = await db.execute(select(Module).where(Module.id == module_id))
    module = result.scalar_one_or_none()

    if not module:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="模组不存在"
        )

    # 只有模组所有者可以查看详情
    if module.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="您不是该模组的拥有者"
        )

    # 获取 owner 用户名
    owner_result = await db.execute(select(User).where(User.id == module.owner_id))
    owner = owner_result.scalar_one()

    return ModuleWithOwner(
        id=module.id,
        owner_id=module.owner_id,
        title=module.title,
        description=module.description,
        created_at=module.created_at,
        updated_at=module.updated_at,
        owner_username=owner.username
    )


@router.put("/{module_id}", response_model=ModuleResponse)
async def update_module(
    module_id: int,
    module_data: ModuleUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """更新模组"""
    result = await db.execute(select(Module).where(Module.id == module_id))
    module = result.scalar_one_or_none()

    if not module:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="模组不存在"
        )

    if module.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="您不是该模组的拥有者"
        )

    if module_data.title is not None:
        module.title = module_data.title
    if module_data.description is not None:
        module.description = module_data.description

    await db.commit()
    await db.refresh(module)
    return module


@router.delete("/{module_id}")
async def delete_module(
    module_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """删除模组"""
    result = await db.execute(select(Module).where(Module.id == module_id))
    module = result.scalar_one_or_none()

    if not module:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="模组不存在"
        )

    if module.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="您不是该模组的拥有者"
        )

    await db.delete(module)
    await db.commit()
    return {"message": "模组已删除"}