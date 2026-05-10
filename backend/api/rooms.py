# TRPG Online - 房间 API
import os
import io
import uuid
import random
import re
import json
from typing import List, Optional
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from backend.database import get_db
from backend.models.models import (
    User, Module, Room, RoomParticipant, RoomStatus,
    RoomResource, Resource, CharacterCard, GameLog,
    Map, MapUnit, CharacterTemplate
)
from backend.websocket import manager as ws_manager
from backend.schemas.schemas import (
    RoomCreate, RoomResponse, RoomWithDetails,
    ParticipantResponse, RoomRoleEnum, RoomResourceToggle,
    RoomUpdate,
    CharacterCardCreate, CharacterCardUpdate, CharacterCardResponse,
    DiceRollRequest, DiceRollResponse, AttackRequest, AttackResponse,
    LogActionEnum, GameLogResponse,
    MapWithUnits, MapUnitCreate, MapUnitUpdate, MapUnitResponse,
    ActiveMapRequest, CharacterTemplateResponse
)
from backend.auth import get_current_user

# 房间列表路由 - 使用 /api/rooms 前缀，仅包含静态路径
# 必须在 rooms_router 之前注册，确保 GET /api/rooms 和 GET /api/rooms/gm
# 不会被 GET /api/rooms/{room_id} 遮蔽
rooms_list_router = APIRouter(prefix="/api/rooms", tags=["房间系统"])

# 房间详情和操作路由 - 使用 /api 前缀，包含参数化路径
rooms_router = APIRouter(prefix="/api", tags=["房间系统"])


# ============ 工具函数 ============

def parse_dice(dice: str) -> tuple:
    match = re.match(r'(\d*)d(\d+)([+-]\d+)?', dice.lower())
    if not match:
        raise HTTPException(status_code=400, detail="无效的骰子格式")
    count = int(match.group(1)) if match.group(1) else 1
    sides = int(match.group(2))
    modifier = int(match.group(3)) if match.group(3) else 0
    return count, sides, modifier


def roll_dice(count: int, sides: int, modifier: int = 0) -> tuple:
    rolls = [random.randint(1, sides) for _ in range(count)]
    total = sum(rolls) + modifier
    return rolls, total


# ============ 房间列表 API（rooms_list_router，静态路径） ============

@rooms_list_router.get("", response_model=List[RoomResponse])
async def get_all_rooms(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取所有房间列表（玩家用）- 返回所有非已结束的房间"""
    result = await db.execute(
        select(Room)
        .where(Room.status != RoomStatus.ENDED)
        .order_by(Room.created_at.desc())
    )
    rooms = result.scalars().all()

    room_list = []
    for room in rooms:
        result = await db.execute(select(Module).where(Module.id == room.module_id))
        module = result.scalar_one_or_none()
        module_title = module.title if module else None

        result = await db.execute(select(User).where(User.id == room.gm_id))
        gm = result.scalar_one_or_none()
        gm_username = gm.username if gm else None

        result = await db.execute(
            select(RoomParticipant).where(RoomParticipant.room_id == room.id)
        )
        participants = result.scalars().all()
        current_players = len(participants)

        room_list.append(
            RoomResponse(
                id=room.id,
                module_id=room.module_id,
                gm_id=room.gm_id,
                name=room.name,
                status=room.status,
                created_at=room.created_at,
                module_title=module_title,
                gm_username=gm_username,
                current_players=current_players,
                max_players=room.max_players or 8
            )
        )

    return room_list


@rooms_list_router.get("/gm", response_model=List[RoomResponse])
async def get_gm_rooms(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取当前用户 GM 的所有房间"""
    result = await db.execute(
        select(Room)
        .where(Room.gm_id == current_user.id)
        .order_by(Room.created_at.desc())
    )
    rooms = result.scalars().all()

    room_list = []
    for room in rooms:
        result = await db.execute(select(Module).where(Module.id == room.module_id))
        module = result.scalar_one_or_none()
        module_title = module.title if module else None

        result = await db.execute(select(User).where(User.id == room.gm_id))
        gm = result.scalar_one_or_none()
        gm_username = gm.username if gm else None

        result = await db.execute(
            select(RoomParticipant).where(RoomParticipant.room_id == room.id)
        )
        participants = result.scalars().all()
        current_players = len(participants)

        room_list.append(
            RoomResponse(
                id=room.id,
                module_id=room.module_id,
                gm_id=room.gm_id,
                name=room.name,
                status=room.status,
                created_at=room.created_at,
                module_title=module_title,
                gm_username=gm_username,
                current_players=current_players,
                max_players=room.max_players or 8
            )
        )

    return room_list


# ============ 模组房间 API（rooms_router） ============

@rooms_router.get("/modules/{module_id}/rooms", response_model=List[RoomResponse])
async def get_module_rooms(
    module_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取模组下的房间列表"""
    result = await db.execute(select(Module).where(Module.id == module_id))
    module = result.scalar_one_or_none()
    if not module:
        raise HTTPException(status_code=404, detail="模组不存在")

    result = await db.execute(
        select(Room)
        .where(Room.module_id == module_id)
        .order_by(Room.created_at.desc())
    )
    rooms = result.scalars().all()

    room_list = []
    for room in rooms:
        result = await db.execute(select(User).where(User.id == room.gm_id))
        gm = result.scalar_one_or_none()
        gm_username = gm.username if gm else None

        result = await db.execute(
            select(RoomParticipant).where(RoomParticipant.room_id == room.id)
        )
        participants = result.scalars().all()
        current_players = len(participants)

        room_list.append(
            RoomResponse(
                id=room.id,
                module_id=room.module_id,
                gm_id=room.gm_id,
                name=room.name,
                status=room.status,
                created_at=room.created_at,
                module_title=module.title,
                gm_username=gm_username,
                current_players=current_players,
                max_players=room.max_players or 8
            )
        )

    return room_list


@rooms_router.post("/modules/{module_id}/rooms", response_model=RoomResponse)
async def create_room(
    module_id: int,
    room_data: RoomCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """创建房间（GM/模组所有者）"""
    result = await db.execute(select(Module).where(Module.id == module_id))
    module = result.scalar_one_or_none()
    if not module:
        raise HTTPException(status_code=404, detail="模组不存在")

    if module.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有模组所有者可以创建房间"
        )

    new_room = Room(
        module_id=module_id,
        gm_id=current_user.id,
        name=room_data.name,
        status=RoomStatus.WAITING,
        max_players=room_data.max_players or module.default_max_players or 8
    )
    db.add(new_room)
    await db.commit()
    await db.refresh(new_room)

    participant = RoomParticipant(
        room_id=new_room.id,
        user_id=current_user.id,
        role=RoomRoleEnum.GM.value
    )
    db.add(participant)
    await db.commit()

    return RoomResponse(
        id=new_room.id,
        module_id=new_room.module_id,
        gm_id=new_room.gm_id,
        name=new_room.name,
        status=new_room.status,
        created_at=new_room.created_at,
        module_title=module.title,
        gm_username=current_user.username,
        current_players=1,
        max_players=new_room.max_players or 8
    )


# ============ 房间详情和操作 API（rooms_router） ============

@rooms_router.get("/rooms/{room_id}/online-users")
async def get_online_users(
    room_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取房间在线用户列表"""
    result = await db.execute(select(Room).where(Room.id == room_id))
    room = result.scalar_one_or_none()
    if not room:
        raise HTTPException(status_code=404, detail="房间不存在")

    return ws_manager.get_online_users(room_id)


@rooms_router.get("/rooms/{room_id}", response_model=RoomWithDetails)
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

    result = await db.execute(select(Module).where(Module.id == room.module_id))
    module = result.scalar_one()

    result = await db.execute(select(User).where(User.id == room.gm_id))
    gm = result.scalar_one()

    result = await db.execute(
        select(RoomParticipant).where(RoomParticipant.room_id == room_id)
    )
    participants = result.scalars().all()

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
        current_players=len(participants),
        max_players=room.max_players or 8,
        participants=participant_list
    )


@rooms_router.put("/rooms/{room_id}", response_model=RoomResponse)
async def update_room(
    room_id: int,
    room_data: RoomUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """修改房间名称（仅 GM 可修改自己的房间）"""
    result = await db.execute(select(Room).where(Room.id == room_id))
    room = result.scalar_one_or_none()

    if not room:
        raise HTTPException(status_code=404, detail="房间不存在")

    if room.gm_id != current_user.id:
        raise HTTPException(status_code=403, detail="只有房主可以修改房间")

    if room_data.name is not None:
        room.name = room_data.name

    await db.commit()
    await db.refresh(room)

    result = await db.execute(select(Module).where(Module.id == room.module_id))
    module = result.scalar_one_or_none()
    module_title = module.title if module else None

    result = await db.execute(select(User).where(User.id == room.gm_id))
    gm = result.scalar_one_or_none()
    gm_username = gm.username if gm else None

    result = await db.execute(
        select(RoomParticipant).where(RoomParticipant.room_id == room.id)
    )
    participants = result.scalars().all()
    current_players = len(participants)

    return RoomResponse(
        id=room.id,
        module_id=room.module_id,
        gm_id=room.gm_id,
        name=room.name,
        status=room.status,
        created_at=room.created_at,
        module_title=module_title,
        gm_username=gm_username,
        current_players=current_players,
        max_players=room.max_players or 8
    )


@rooms_router.delete("/rooms/{room_id}")
async def delete_room(
    room_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """删除房间（仅 GM 可删除自己的房间）"""
    result = await db.execute(select(Room).where(Room.id == room_id))
    room = result.scalar_one_or_none()

    if not room:
        raise HTTPException(status_code=404, detail="房间不存在")

    if room.gm_id != current_user.id:
        raise HTTPException(status_code=403, detail="只有房主可以删除房间")

    await db.delete(room)
    await db.commit()

    return {"message": "房间已删除"}


@rooms_router.post("/rooms/{room_id}/join")
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

    result = await db.execute(
        select(RoomParticipant).where(RoomParticipant.room_id == room_id)
    )
    current_participants = result.scalars().all()
    if len(current_participants) >= (room.max_players or 8):
        raise HTTPException(status_code=400, detail=f"房间已满（最多{room.max_players or 8}人）")

    participant = RoomParticipant(
        room_id=room_id,
        user_id=current_user.id,
        role=RoomRoleEnum.PLAYER.value,
        character_name=character_name
    )
    db.add(participant)
    await db.commit()

    return {"message": "加入成功"}


@rooms_router.post("/rooms/{room_id}/leave")
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

    return {"message": "已离开房间", "username": current_user.username}


@rooms_router.post("/rooms/{room_id}/start")
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


@rooms_router.post("/rooms/{room_id}/end")
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


# ============ 房间资源可见性 API ============

@rooms_router.get("/rooms/{room_id}/resources")
async def get_room_resources(
    room_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取房间内的资源（包含可见性状态）"""
    result = await db.execute(select(Room).where(Room.id == room_id))
    room = result.scalar_one_or_none()
    if not room:
        raise HTTPException(status_code=404, detail="房间不存在")

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
        raise HTTPException(status_code=403, detail="您不是房间参与者")

    result = await db.execute(
        select(Resource).where(Resource.module_id == room.module_id)
    )
    resources = result.scalars().all()

    result = await db.execute(
        select(RoomResource).where(RoomResource.room_id == room_id)
    )
    room_resources = result.scalars().all()
    room_resources_map = {rr.resource_id: rr.is_shown for rr in room_resources}

    resource_list = []
    for r in resources:
        is_shown = room_resources_map.get(r.id, r.default_visible)
        resource_list.append({
            "id": r.id,
            "title": r.title,
            "type": r.type.value,
            "display_type": r.display_type,
            "content": r.content,
            "is_shown": is_shown,
            "is_gm": participant.role == RoomRoleEnum.GM.value
        })

    return resource_list


@rooms_router.post("/rooms/{room_id}/resources/{resource_id}/toggle")
async def toggle_room_resource_visibility(
    room_id: int,
    resource_id: int,
    toggle_data: RoomResourceToggle,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """切换房间内资源的可见性（仅 GM）"""
    result = await db.execute(select(Room).where(Room.id == room_id))
    room = result.scalar_one_or_none()
    if not room:
        raise HTTPException(status_code=404, detail="房间不存在")

    if room.gm_id != current_user.id:
        raise HTTPException(status_code=403, detail="只有房主可以控制资源可见性")

    result = await db.execute(select(Resource).where(Resource.id == resource_id))
    resource = result.scalar_one_or_none()
    if not resource:
        raise HTTPException(status_code=404, detail="资源不存在")

    if resource.module_id != room.module_id:
        raise HTTPException(status_code=400, detail="资源不属于该模组")

    result = await db.execute(
        select(RoomResource).where(
            and_(
                RoomResource.room_id == room_id,
                RoomResource.resource_id == resource_id
            )
        )
    )
    room_resource = result.scalar_one_or_none()

    if room_resource:
        room_resource.is_shown = toggle_data.is_shown
    else:
        room_resource = RoomResource(
            room_id=room_id,
            resource_id=resource_id,
            is_shown=toggle_data.is_shown
        )
        db.add(room_resource)

    await db.commit()

    return {"message": "资源可见性已更新", "is_shown": toggle_data.is_shown}


# ============ 角色卡 API ============

@rooms_router.post("/rooms/{room_id}/characters", response_model=CharacterCardResponse)
async def create_character(
    room_id: int,
    char_data: CharacterCardCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """创建角色卡（仅 GM 可操作，GM 创建玩家角色或 NPC）"""
    result = await db.execute(select(Room).where(Room.id == room_id))
    room = result.scalar_one_or_none()
    if not room:
        raise HTTPException(status_code=404, detail="房间不存在")

    if room.gm_id != current_user.id:
        raise HTTPException(status_code=403, detail="只有房主可以添加角色")

    # Check character count limit
    result = await db.execute(select(Module).where(Module.id == room.module_id))
    module = result.scalar_one_or_none()
    if module:
        result = await db.execute(
            select(CharacterCard).where(CharacterCard.room_id == room_id)
        )
        current_chars = len(result.scalars().all())
        if current_chars >= module.max_characters:
            raise HTTPException(status_code=400, detail=f"角色数已达上限（{module.max_characters}）")

    new_char = CharacterCard(
        room_id=room_id,
        name=char_data.name,
        avatar=char_data.avatar,
        profession=char_data.profession,
        hp=char_data.hp,
        max_hp=char_data.max_hp,
        san=char_data.san,
        mp=char_data.mp,
        max_mp=char_data.max_mp,
        attributes=char_data.attributes,
        skills=char_data.skills,
        items=char_data.items,
        spells=char_data.spells,
        notes=char_data.notes,
        is_npc=char_data.is_npc
    )

    db.add(new_char)
    await db.commit()
    await db.refresh(new_char)

    # Write character creation log
    char_type = "NPC" if char_data.is_npc else "角色"
    log = GameLog(
        room_id=room_id,
        user_id=current_user.id,
        action="custom",
        detail=f"{current_user.username} 添加了{char_type}: {char_data.name}"
    )
    db.add(log)
    await db.commit()

    return CharacterCardResponse(
        id=new_char.id,
        room_id=new_char.room_id,
        name=new_char.name,
        avatar=new_char.avatar,
        profession=new_char.profession,
        hp=new_char.hp,
        max_hp=new_char.max_hp,
        san=new_char.san,
        mp=new_char.mp,
        max_mp=new_char.max_mp,
        attributes=new_char.attributes,
        skills=new_char.skills,
        items=new_char.items,
        spells=new_char.spells,
        notes=new_char.notes,
        is_npc=new_char.is_npc,
        created_at=new_char.created_at
    )


@rooms_router.get("/rooms/{room_id}/character-templates", response_model=List[CharacterTemplateResponse])
async def get_room_character_templates(
    room_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取房间模组的角色模板列表（GM 快速添加用）"""
    result = await db.execute(select(Room).where(Room.id == room_id))
    room = result.scalar_one_or_none()
    if not room:
        raise HTTPException(status_code=404, detail="房间不存在")

    result = await db.execute(
        select(CharacterTemplate).where(CharacterTemplate.module_id == room.module_id)
    )
    return result.scalars().all()


@rooms_router.get("/rooms/{room_id}/characters", response_model=List[CharacterCardResponse])
async def get_room_characters(
    room_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取房间内的角色卡"""
    result = await db.execute(
        select(CharacterCard).where(CharacterCard.room_id == room_id)
    )
    characters = result.scalars().all()
    return [
        CharacterCardResponse(
            id=c.id, room_id=c.room_id,
            name=c.name, avatar=c.avatar, profession=c.profession,
            hp=c.hp, max_hp=c.max_hp, san=c.san, mp=c.mp, max_mp=c.max_mp,
            attributes=c.attributes, skills=c.skills, items=c.items, spells=c.spells,
            notes=c.notes, is_npc=c.is_npc, created_at=c.created_at
        ) for c in characters
    ]


@rooms_router.put("/characters/{char_id}", response_model=CharacterCardResponse)
async def update_character(
    char_id: int,
    char_data: CharacterCardUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """更新角色卡（仅 GM）"""
    result = await db.execute(select(CharacterCard).where(CharacterCard.id == char_id))
    char = result.scalar_one_or_none()
    if not char:
        raise HTTPException(status_code=404, detail="角色卡不存在")

    # GM-only
    result = await db.execute(select(Room).where(Room.id == char.room_id))
    room = result.scalar_one_or_none()
    if not room or room.gm_id != current_user.id:
        raise HTTPException(status_code=403, detail="只有 GM 可以修改角色")

    for field, value in char_data.model_dump(exclude_unset=True).items():
        setattr(char, field, value)

    await db.commit()
    await db.refresh(char)
    return CharacterCardResponse(
        id=char.id,
        room_id=char.room_id,
        name=char.name,
        avatar=char.avatar,
        profession=char.profession,
        hp=char.hp,
        max_hp=char.max_hp,
        san=char.san,
        mp=char.mp,
        max_mp=char.max_mp,
        attributes=char.attributes,
        skills=char.skills,
        items=char.items,
        spells=char.spells,
        notes=char.notes,
        is_npc=char.is_npc,
        created_at=char.created_at
    )


@rooms_router.delete("/characters/{char_id}")
async def delete_character(
    char_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """删除角色卡（仅 GM）"""
    result = await db.execute(select(CharacterCard).where(CharacterCard.id == char_id))
    char = result.scalar_one_or_none()
    if not char:
        raise HTTPException(status_code=404, detail="角色卡不存在")

    result = await db.execute(select(Room).where(Room.id == char.room_id))
    room = result.scalar_one_or_none()
    if not room or room.gm_id != current_user.id:
        raise HTTPException(status_code=403, detail="只有 GM 可以删除角色")

    await db.delete(char)
    await db.commit()
    return {"message": "角色卡已删除"}


@rooms_router.post("/characters/{char_id}/attack", response_model=AttackResponse)
async def quick_attack(
    char_id: int,
    attack_data: AttackRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """快捷攻击（仅 GM）"""
    result = await db.execute(select(CharacterCard).where(CharacterCard.id == char_id))
    char = result.scalar_one_or_none()
    if not char:
        raise HTTPException(status_code=404, detail="角色卡不存在")

    result = await db.execute(select(Room).where(Room.id == char.room_id))
    room = result.scalar_one_or_none()
    if not room or room.gm_id != current_user.id:
        raise HTTPException(status_code=403, detail="只有 GM 可以执行攻击")

    # Derive attack bonus from attributes
    try:
        attrs = json.loads(char.attributes) if char.attributes else {}
    except (json.JSONDecodeError, TypeError):
        attrs = {}
    attack_bonus = (attrs.get("strength", 50) - 50) // 10

    # Derive damage dice from first weapon in items, default 1d3
    try:
        items_list = json.loads(char.items) if char.items else []
    except (json.JSONDecodeError, TypeError):
        items_list = []
    damage_dice = "1d3"
    for item in items_list:
        if item.get("type") == "weapon" and item.get("detail"):
            damage_dice = item["detail"]
            break

    attack_rolls, attack_total = roll_dice(1, 20, attack_bonus)

    count, sides, modifier = parse_dice(damage_dice)
    damage_rolls, damage_total = roll_dice(count, sides, modifier)

    log_detail = {
        "character_name": char.name,
        "attack_roll": attack_total,
        "attack_rolls": attack_rolls,
        "attack_bonus": attack_bonus,
        "damage_dice": damage_dice,
        "damage_roll": damage_total,
        "damage_rolls": damage_rolls,
        "target": attack_data.target_name or "未知目标"
    }
    log = GameLog(
        room_id=room.id,
        user_id=current_user.id,
        action=LogActionEnum.ATTACK.value,
        detail=json.dumps(log_detail)
    )
    db.add(log)
    await db.commit()

    return AttackResponse(
        character_name=char.name,
        attack_bonus=attack_bonus,
        damage_dice=damage_dice,
        attack_roll=attack_total,
        damage_roll=damage_total,
        total_damage=damage_total,
        target_name=attack_data.target_name,
        log=GameLogResponse(
            id=log.id,
            room_id=log.room_id,
            user_id=log.user_id,
            action=log.action,
            detail=log.detail,
            username=current_user.username,
            character_name=char.name,
            created_at=log.created_at
        )
    )


# ============ 掷骰子 API ============

@rooms_router.post("/rooms/{room_id}/dice", response_model=DiceRollResponse)
async def roll_dice_api(
    room_id: int,
    dice_request: DiceRollRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """掷骰子"""
    count, sides, modifier = parse_dice(dice_request.dice)
    rolls, total = roll_dice(count, sides, modifier)

    char_name = dice_request.character_name

    # Build details string: "角色名 掷出 2d6+1 = [2,4]+1 = 7"
    if modifier > 0:
        roll_detail = f"{count}d{sides}+{modifier}"
    elif modifier < 0:
        roll_detail = f"{count}d{sides}-{abs(modifier)}"
    else:
        roll_detail = f"{count}d{sides}"

    rolls_str = str(rolls).replace(" ", "")
    if modifier > 0:
        calc_detail = f"{rolls_str}+{modifier}"
    elif modifier < 0:
        calc_detail = f"{rolls_str}-{abs(modifier)}"
    else:
        calc_detail = rolls_str

    if char_name:
        details = f"{char_name} 掷出 {roll_detail} = {calc_detail} = {total}"
    else:
        details = f"{roll_detail} = {calc_detail} = {total}"

    log = GameLog(
        room_id=room_id,
        user_id=current_user.id,
        action=LogActionEnum.DICE.value,
        detail=json.dumps({
            "dice": dice_request.dice,
            "result": total,
            "details": details,
            "reason": dice_request.reason or "",
            "character_name": char_name or "",
            "rolls": rolls,
            "modifier": modifier
        })
    )
    db.add(log)
    await db.commit()

    return DiceRollResponse(
        dice=dice_request.dice,
        result=total,
        details=details,
        reason=dice_request.reason,
        rolled_by=current_user.username,
        character_name=char_name,
        timestamp=log.created_at
    )


# ============ 游戏日志 API ============

@rooms_router.get("/rooms/{room_id}/logs", response_model=List[GameLogResponse])
async def get_room_logs(
    room_id: int,
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取房间日志"""
    # Get the newest N logs, then return in chronological order
    result = await db.execute(
        select(GameLog)
        .where(GameLog.room_id == room_id)
        .order_by(GameLog.created_at.desc())
        .limit(limit)
    )
    logs = list(reversed(result.scalars().all()))

    result_list = []
    for log in logs:
        user_result = await db.execute(select(User).where(User.id == log.user_id))
        user = user_result.scalar_one_or_none()

        result_list.append(GameLogResponse(
            id=log.id,
            room_id=log.room_id,
            user_id=log.user_id,
            action=log.action,
            detail=log.detail,
            username=user.username if user else "未知",
            character_name=None,
            created_at=log.created_at
        ))

    return result_list


class CustomLogRequest(BaseModel):
    content: str
    action: Optional[str] = "custom"


@rooms_router.post("/rooms/{room_id}/logs", response_model=GameLogResponse)
async def add_custom_log(
    room_id: int,
    req: CustomLogRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """添加自定义日志条目"""
    result = await db.execute(select(Room).where(Room.id == room_id))
    room = result.scalar_one_or_none()
    if not room:
        raise HTTPException(status_code=404, detail="房间不存在")

    log = GameLog(
        room_id=room_id,
        user_id=current_user.id,
        action=req.action or "custom",
        detail=req.content
    )
    db.add(log)
    await db.commit()
    await db.refresh(log)

    return GameLogResponse(
        id=log.id,
        room_id=log.room_id,
        user_id=log.user_id,
        action=log.action,
        detail=log.detail,
        username=current_user.username,
        character_name=char.name if char else None,
        created_at=log.created_at
    )


@rooms_router.delete("/rooms/{room_id}/logs")
async def clear_room_logs(
    room_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """清空房间日志（仅 GM）"""
    result = await db.execute(select(Room).where(Room.id == room_id))
    room = result.scalar_one_or_none()
    if not room:
        raise HTTPException(status_code=404, detail="房间不存在")

    if room.gm_id != current_user.id:
        raise HTTPException(status_code=403, detail="只有房主可以清空日志")

    result = await db.execute(
        select(GameLog).where(GameLog.room_id == room_id)
    )
    logs = result.scalars().all()
    for log in logs:
        await db.delete(log)
    await db.commit()

    return {"message": "日志已清空", "deleted_count": len(logs)}


# ============ 房间地图 API ============


@rooms_router.get("/rooms/{room_id}/map", response_model=MapWithUnits)
async def get_room_map(
    room_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取房间激活地图（含 units）"""
    result = await db.execute(select(Room).where(Room.id == room_id))
    room = result.scalar_one_or_none()
    if not room:
        raise HTTPException(status_code=404, detail="房间不存在")

    if not room.active_map_id:
        raise HTTPException(status_code=404, detail="房间未设置激活地图")

    result = await db.execute(select(Map).where(Map.id == room.active_map_id))
    map_data = result.scalar_one_or_none()
    if not map_data:
        raise HTTPException(status_code=404, detail="地图不存在")

    result = await db.execute(select(MapUnit).where(MapUnit.map_id == map_data.id))
    units = result.scalars().all()

    return MapWithUnits(
        id=map_data.id,
        module_id=map_data.module_id,
        name=map_data.name,
        image_url=map_data.image_url,
        grid_size=map_data.grid_size,
        created_at=map_data.created_at,
        units=[MapUnitResponse.model_validate(u) for u in units]
    )


@rooms_router.put("/rooms/{room_id}/active-map")
async def set_active_map(
    room_id: int,
    req: ActiveMapRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """GM 设置/清除激活地图"""
    result = await db.execute(select(Room).where(Room.id == room_id))
    room = result.scalar_one_or_none()
    if not room:
        raise HTTPException(status_code=404, detail="房间不存在")

    if room.gm_id != current_user.id:
        raise HTTPException(status_code=403, detail="只有房主可以设置地图")

    # Verify map belongs to this room's module if setting one
    if req.map_id is not None:
        result = await db.execute(select(Map).where(Map.id == req.map_id))
        map_obj = result.scalar_one_or_none()
        if not map_obj:
            raise HTTPException(status_code=404, detail="地图不存在")
        if map_obj.module_id != room.module_id:
            raise HTTPException(status_code=400, detail="地图不属于该房间模组")

    room.active_map_id = req.map_id
    await db.commit()

    return {"message": "激活地图已更新", "active_map_id": req.map_id}


@rooms_router.post("/rooms/{room_id}/map/units", response_model=MapUnitResponse)
async def create_room_map_unit(
    room_id: int,
    unit_data: MapUnitCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """GM 在激活地图上创建 token"""
    result = await db.execute(select(Room).where(Room.id == room_id))
    room = result.scalar_one_or_none()
    if not room:
        raise HTTPException(status_code=404, detail="房间不存在")

    if room.gm_id != current_user.id:
        raise HTTPException(status_code=403, detail="只有房主可以操作")

    if not room.active_map_id:
        raise HTTPException(status_code=400, detail="房间未设置激活地图")

    new_unit = MapUnit(
        map_id=room.active_map_id,
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


@rooms_router.put("/rooms/{room_id}/map/units/{unit_id}", response_model=MapUnitResponse)
async def update_room_map_unit(
    room_id: int,
    unit_id: int,
    unit_data: MapUnitUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """GM 更新 token"""
    result = await db.execute(select(Room).where(Room.id == room_id))
    room = result.scalar_one_or_none()
    if not room:
        raise HTTPException(status_code=404, detail="房间不存在")

    if room.gm_id != current_user.id:
        raise HTTPException(status_code=403, detail="只有房主可以操作")

    result = await db.execute(select(MapUnit).where(MapUnit.id == unit_id))
    unit = result.scalar_one_or_none()
    if not unit:
        raise HTTPException(status_code=404, detail="单位不存在")

    # Verify unit belongs to this room's active map
    if unit.map_id != room.active_map_id:
        raise HTTPException(status_code=400, detail="单位不属于当前地图")

    for field, value in unit_data.model_dump(exclude_unset=True).items():
        setattr(unit, field, value)

    await db.commit()
    await db.refresh(unit)
    return unit


@rooms_router.delete("/rooms/{room_id}/map/units/{unit_id}")
async def delete_room_map_unit(
    room_id: int,
    unit_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """GM 删除 token"""
    result = await db.execute(select(Room).where(Room.id == room_id))
    room = result.scalar_one_or_none()
    if not room:
        raise HTTPException(status_code=404, detail="房间不存在")

    if room.gm_id != current_user.id:
        raise HTTPException(status_code=403, detail="只有房主可以操作")

    result = await db.execute(select(MapUnit).where(MapUnit.id == unit_id))
    unit = result.scalar_one_or_none()
    if not unit:
        raise HTTPException(status_code=404, detail="单位不存在")

    if unit.map_id != room.active_map_id:
        raise HTTPException(status_code=400, detail="单位不属于当前地图")

    await db.delete(unit)
    await db.commit()
    return {"message": "单位已删除"}


# ============ 头像上传 API ============


@rooms_router.post("/upload/avatar")
async def upload_avatar(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
):
    """上传头像图片，自动中心裁剪为正方形"""
    from PIL import Image as PILImage
    from backend.config import settings

    ext = os.path.splitext(file.filename)[1].lower()
    allowed = {'.png', '.jpg', '.jpeg', '.gif', '.webp'}
    if ext not in allowed:
        raise HTTPException(status_code=400, detail="不支持的图片格式")

    content = await file.read()
    if len(content) > settings.max_file_size:
        raise HTTPException(status_code=400, detail="文件过大")

    try:
        img = PILImage.open(io.BytesIO(content))
        img = img.convert("RGBA")

        # Scale so shorter side matches target size
        target_size = 128
        w, h = img.size
        ratio = target_size / min(w, h)
        img = img.resize((int(w * ratio), int(h * ratio)), PILImage.LANCZOS)

        # Center crop to square
        w, h = img.size
        left = (w - target_size) / 2
        top = (h - target_size) / 2
        img = img.crop((int(left), int(top), int(left + target_size), int(top + target_size)))

        # Save
        avatar_dir = os.path.join(settings.upload_dir, "avatars")
        os.makedirs(avatar_dir, exist_ok=True)
        filename = f"{uuid.uuid4()}.png"
        path = os.path.join(avatar_dir, filename)
        img.save(path, "PNG")

        return {"url": f"/uploads/avatars/{filename}"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"图片处理失败: {str(e)}")
