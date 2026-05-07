# TRPG Online - 房间 API
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from backend.database import get_db
from backend.models.models import User, Module, Room, RoomParticipant, RoomStatus
from backend.schemas.schemas import (
    RoomCreate, RoomResponse, RoomWithDetails,
    ParticipantResponse, RoomRoleEnum
)
from backend.auth import get_current_user

router = APIRouter(prefix="/api", tags=["房间系统"])


@router.get("/modules/{module_id}/rooms", response_model=List[RoomResponse])
async def get_module_rooms(
    module_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取模组下的房间列表"""
    # 检查模组是否存在
    result = await db.execute(select(Module).where(Module.id == module_id))
    module = result.scalar_one_or_none()
    if not module:
        raise HTTPException(status_code=404, detail="模组不存在")

    # 获取房间列表
    result = await db.execute(
        select(Room)
        .where(Room.module_id == module_id)
        .order_by(Room.created_at.desc())
    )
    rooms = result.scalars().all()
    return rooms


@router.post("/modules/{module_id}/rooms", response_model=RoomResponse)
async def create_room(
    module_id: int,
    room_data: RoomCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """创建房间（GM/模组所有者）"""
    # 检查模组是否存在
    result = await db.execute(select(Module).where(Module.id == module_id))
    module = result.scalar_one_or_none()
    if not module:
        raise HTTPException(status_code=404, detail="模组不存在")

    # 检查是否是模组所有者
    if module.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有模组所有者可以创建房间"
        )

    # 创建房间
    new_room = Room(
        module_id=module_id,
        gm_id=current_user.id,
        name=room_data.name,
        status=RoomStatus.WAITING
    )
    db.add(new_room)
    await db.commit()
    await db.refresh(new_room)

    # 添加 GM 为参与者
    participant = RoomParticipant(
        room_id=new_room.id,
        user_id=current_user.id,
        role=RoomRoleEnum.GM.value
    )
    db.add(participant)
    await db.commit()

    return new_room


@router.get("/rooms/{room_id}", response_model=RoomWithDetails)
async def get_room(
    room_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取房间详情"""
    result = await db.execute(select(Room).where(Room.id == room_id))
    room = result.scalar_one_or_none()

    if not room:
        raise HTTPException(status_code=404, detail="房间不存在")

    # 获取模组信息
    result = await db.execute(select(Module).where(Module.id == room.module_id))
    module = result.scalar_one()

    # 获取 GM 用户名
    result = await db.execute(select(User).where(User.id == room.gm_id))
    gm = result.scalar_one()

    # 获取参与者列表
    result = await db.execute(
        select(RoomParticipant).where(RoomParticipant.room_id == room_id)
    )
    participants = result.scalars().all()

    # 获取参与者详细信息
    participant_list = []
    for p in participants:
        result = await db.execute(select(User).where(User.id == p.user_id))
        user = result.scalar_one()
        participant_list.append(
            ParticipantResponse(
                user_id=user.id,
                username=user.username,
                role=RoomRoleEnum(p.role),
                character_name=p.character_name
            )
        )

    return RoomWithDetails(
        id=room.id,
        module_id=room.module_id,
        gm_id=room.gm_id,
        name=room.name,
        status=room.status,
        created_at=room.created_at,
        module_title=module.title,
        gm_username=gm.username,
        participants=participant_list
    )


@router.post("/rooms/{room_id}/join")
async def join_room(
    room_id: int,
    character_name: str = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """加入房间"""
    result = await db.execute(select(Room).where(Room.id == room_id))
    room = result.scalar_one_or_none()

    if not room:
        raise HTTPException(status_code=404, detail="房间不存在")

    if room.status == RoomStatus.ENDED:
        raise HTTPException(status_code=400, detail="房间已结束")

    # 检查是否已是参与者
    result = await db.execute(
        select(RoomParticipant).where(
            and_(
                RoomParticipant.room_id == room_id,
                RoomParticipant.user_id == current_user.id
            )
        )
    )
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="您已在房间中")

    # 添加参与者
    participant = RoomParticipant(
        room_id=room_id,
        user_id=current_user.id,
        role=RoomRoleEnum.PLAYER.value,
        character_name=character_name
    )
    db.add(participant)
    await db.commit()

    return {"message": "加入成功"}


@router.post("/rooms/{room_id}/leave")
async def leave_room(
    room_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """离开房间"""
    result = await db.execute(
        select(RoomParticipant).where(
            and_(
                RoomParticipant.room_id == room_id,
                RoomParticipant.user_id == current_user.id
            )
        )
    )
    participant = result.scalar_one_or_none()

    if not participant:
        raise HTTPException(status_code=400, detail="您不在房间中")

    if participant.role == RoomRoleEnum.GM.value:
        raise HTTPException(status_code=400, detail="房主不能离开房间")

    await db.delete(participant)
    await db.commit()

    return {"message": "已离开房间"}


@router.post("/rooms/{room_id}/start")
async def start_room(
    room_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """开始游戏（GM）"""
    result = await db.execute(select(Room).where(Room.id == room_id))
    room = result.scalar_one_or_none()

    if not room:
        raise HTTPException(status_code=404, detail="房间不存在")

    if room.gm_id != current_user.id:
        raise HTTPException(status_code=403, detail="只有房主可以开始游戏")

    room.status = RoomStatus.ACTIVE
    await db.commit()

    return {"message": "游戏开始"}


@router.post("/rooms/{room_id}/end")
async def end_room(
    room_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """结束游戏（GM）"""
    result = await db.execute(select(Room).where(Room.id == room_id))
    room = result.scalar_one_or_none()

    if not room:
        raise HTTPException(status_code=404, detail="房间不存在")

    if room.gm_id != current_user.id:
        raise HTTPException(status_code=403, detail="只有房主可以结束游戏")

    room.status = RoomStatus.ENDED
    await db.commit()

    return {"message": "游戏已结束"}