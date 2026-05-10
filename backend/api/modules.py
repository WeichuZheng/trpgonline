# TRPG Online - 模组 API
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.database import get_db
from backend.models.models import User, Module, CharacterTemplate
from backend.schemas.schemas import (
    ModuleCreate, ModuleUpdate, ModuleResponse, ModuleWithOwner,
    CharacterTemplateCreate, CharacterTemplateUpdate, CharacterTemplateResponse
)
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
            max_characters=m.max_characters or 20,
            default_max_players=m.default_max_players or 8,
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
        description=module_data.description,
        max_characters=module_data.max_characters,
        default_max_players=module_data.default_max_players
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
        max_characters=module.max_characters or 20,
        default_max_players=module.default_max_players or 8,
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
    if module_data.max_characters is not None:
        module.max_characters = module_data.max_characters
    if module_data.default_max_players is not None:
        module.default_max_players = module_data.default_max_players

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


# ============ 角色模板 API ============

@router.get("/{module_id}/character-templates", response_model=List[CharacterTemplateResponse])
async def get_character_templates(
    module_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取模组的角色模板列表"""
    result = await db.execute(select(Module).where(Module.id == module_id))
    module = result.scalar_one_or_none()
    if not module:
        raise HTTPException(status_code=404, detail="模组不存在")

    result = await db.execute(
        select(CharacterTemplate).where(CharacterTemplate.module_id == module_id)
    )
    return result.scalars().all()


@router.post("/{module_id}/character-templates", response_model=CharacterTemplateResponse)
async def create_character_template(
    module_id: int,
    template_data: CharacterTemplateCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """创建角色模板"""
    result = await db.execute(select(Module).where(Module.id == module_id))
    module = result.scalar_one_or_none()
    if not module:
        raise HTTPException(status_code=404, detail="模组不存在")

    if module.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="只有模组所有者可以管理角色模板")

    template = CharacterTemplate(
        module_id=module_id,
        name=template_data.name,
        profession=template_data.profession,
        hp=template_data.hp,
        max_hp=template_data.max_hp,
        san=template_data.san,
        mp=template_data.mp,
        max_mp=template_data.max_mp,
        attributes=template_data.attributes,
        skills=template_data.skills,
        items=template_data.items,
        spells=template_data.spells,
        notes=template_data.notes,
        is_enemy=template_data.is_enemy
    )
    db.add(template)
    await db.commit()
    await db.refresh(template)
    return template


@router.put("/character-templates/{template_id}", response_model=CharacterTemplateResponse)
async def update_character_template(
    template_id: int,
    template_data: CharacterTemplateUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """更新角色模板"""
    result = await db.execute(select(CharacterTemplate).where(CharacterTemplate.id == template_id))
    template = result.scalar_one_or_none()
    if not template:
        raise HTTPException(status_code=404, detail="模板不存在")

    result = await db.execute(select(Module).where(Module.id == template.module_id))
    module = result.scalar_one()
    if module.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权限")

    for field, value in template_data.model_dump(exclude_unset=True).items():
        setattr(template, field, value)

    await db.commit()
    await db.refresh(template)
    return template


@router.delete("/character-templates/{template_id}")
async def delete_character_template(
    template_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """删除角色模板"""
    result = await db.execute(select(CharacterTemplate).where(CharacterTemplate.id == template_id))
    template = result.scalar_one_or_none()
    if not template:
        raise HTTPException(status_code=404, detail="模板不存在")

    result = await db.execute(select(Module).where(Module.id == template.module_id))
    module = result.scalar_one()
    if module.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权限")

    await db.delete(template)
    await db.commit()
    return {"message": "角色模板已删除"}