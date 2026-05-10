# TRPG Online - 资源 API
import os
import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.config import settings
from backend.database import get_db
from backend.models.models import User, Module, Resource, ResourceType
from backend.schemas.schemas import (
    ResourceCreate, ResourceUpdate, ResourceResponse,
    ResourceToggleVisible, ResourceTypeEnum, DisplayTypeEnum
)
from backend.auth import get_current_user

router = APIRouter(prefix="/api", tags=["资源管理"])

# 确保上传目录存在
os.makedirs(settings.upload_dir, exist_ok=True)


@router.get("/modules/{module_id}/resources", response_model=List[ResourceResponse])
async def get_module_resources(
    module_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取模组的所有资源（仅返回所有者上传的）"""
    # 检查模组是否存在
    result = await db.execute(select(Module).where(Module.id == module_id))
    module = result.scalar_one_or_none()
    if not module:
        raise HTTPException(status_code=404, detail="模组不存在")

    # 检查权限（必须是模组所有者或房间参与者）
    # 这里简化为只允许模组所有者操作
    if module.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="您不是该模组的拥有者"
        )

    # 获取该模组的所有资源（包含所有用户上传的）
    result = await db.execute(
        select(Resource)
        .where(Resource.module_id == module_id)
        .order_by(Resource.created_at.desc())
    )
    resources = result.scalars().all()
    return resources


@router.post("/modules/{module_id}/resources", response_model=ResourceResponse)
async def create_resource(
    module_id: int,
    title: str = Form(...),
    type: ResourceTypeEnum = Form(...),
    display_type: DisplayTypeEnum = Form(DisplayTypeEnum.STORY),
    content: str = Form(None),
    file: UploadFile = File(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """创建资源（图片上传或文本创建）"""
    # 检查模组是否存在
    result = await db.execute(select(Module).where(Module.id == module_id))
    module = result.scalar_one_or_none()
    if not module:
        raise HTTPException(status_code=404, detail="模组不存在")

    # 检查权限
    if module.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="您不是该模组的拥有者"
        )

    # 处理文件上传或文本内容
    file_url = None
    text_content = content

    if type == ResourceTypeEnum.IMAGE:
        if not file:
            raise HTTPException(status_code=400, detail="图片文件不能为空")

        # 验证文件类型
        allowed_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.webp'}
        ext = os.path.splitext(file.filename)[1].lower()
        if ext not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"不支持的文件类型，仅支持: {', '.join(allowed_extensions)}"
            )

        # 生成唯一文件名
        filename = f"{uuid.uuid4()}{ext}"
        file_path = os.path.join(settings.upload_dir, filename)

        # 保存文件
        content = await file.read()
        if len(content) > settings.max_file_size:
            raise HTTPException(status_code=400, detail="文件大小超过限制")
        with open(file_path, 'wb') as f:
            f.write(content)

        file_url = f"/uploads/{filename}"
        text_content = None  # 图片不需要文本内容

    elif type == ResourceTypeEnum.TEXT:
        if not content:
            raise HTTPException(status_code=400, detail="文本内容不能为空")

    # 创建资源
    new_resource = Resource(
        module_id=module_id,
        owner_id=current_user.id,
        type=ResourceType(type.value),
        title=title,
        content=file_url if type == ResourceTypeEnum.IMAGE else text_content,
        display_type=display_type.value,
        default_visible=False
    )
    db.add(new_resource)
    await db.commit()
    await db.refresh(new_resource)
    return new_resource


@router.put("/resources/{resource_id}", response_model=ResourceResponse)
async def update_resource(
    resource_id: int,
    resource_data: ResourceUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """更新资源"""
    result = await db.execute(select(Resource).where(Resource.id == resource_id))
    resource = result.scalar_one_or_none()

    if not resource:
        raise HTTPException(status_code=404, detail="资源不存在")

    # 只有上传者可以修改
    if resource.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="您不是该资源的上传者"
        )

    if resource_data.title is not None:
        resource.title = resource_data.title
    if resource_data.content is not None:
        resource.content = resource_data.content
    if resource_data.display_type is not None:
        resource.display_type = resource_data.display_type.value
    if resource_data.default_visible is not None:
        resource.default_visible = resource_data.default_visible

    await db.commit()
    await db.refresh(resource)
    return resource


@router.post("/resources/{resource_id}/toggle-visible", response_model=ResourceResponse)
async def toggle_resource_visibility(
    resource_id: int,
    toggle_data: ResourceToggleVisible,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """切换资源可见性（GM/模组所有者）"""
    result = await db.execute(select(Resource).where(Resource.id == resource_id))
    resource = result.scalar_one_or_none()

    if not resource:
        raise HTTPException(status_code=404, detail="资源不存在")

    # 获取模组信息检查权限
    result = await db.execute(select(Module).where(Module.id == resource.module_id))
    module = result.scalar_one()

    # 只有模组所有者可以切换可见性
    if module.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有模组所有者可以控制资源可见性"
        )

    resource.default_visible = toggle_data.default_visible
    await db.commit()
    await db.refresh(resource)
    return resource


@router.delete("/resources/{resource_id}")
async def delete_resource(
    resource_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """删除资源"""
    result = await db.execute(select(Resource).where(Resource.id == resource_id))
    resource = result.scalar_one_or_none()

    if not resource:
        raise HTTPException(status_code=404, detail="资源不存在")

    # 只有上传者可以删除
    if resource.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="您不是该资源的上传者"
        )

    # 如果是图片，删除文件
    if resource.type == ResourceType.IMAGE and resource.content:
        filename = resource.content.replace("/uploads/", "")
        file_path = os.path.join(settings.upload_dir, filename)
        if os.path.exists(file_path):
            os.remove(file_path)

    await db.delete(resource)
    await db.commit()
    return {"message": "资源已删除"}