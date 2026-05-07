# TRPG Online - 角色卡和掷骰子 API
import random
import re
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from backend.database import get_db
from backend.models.models import User, Room, RoomParticipant, CharacterCard, GameLog, RoomStatus
from backend.schemas.schemas import (
    CharacterCardCreate, CharacterCardUpdate, CharacterCardResponse,
    DiceRollRequest, DiceRollResponse, AttackRequest, AttackResponse,
    LogActionEnum, GameLogCreate, GameLogResponse
)
from backend.auth import get_current_user

router = APIRouter(prefix="/api", tags=["角色卡与掷骰"])


def parse_dice(dice: str) -> tuple:
    """解析骰子格式，如 '2d6+3' -> (2, 6, 3)"""
    match = re.match(r'(\d*)d(\d+)([+-]\d+)?', dice.lower())
    if not match:
        raise HTTPException(status_code=400, detail="无效的骰子格式")

    count = int(match.group(1)) if match.group(1) else 1
    sides = int(match.group(2))
    modifier = int(match.group(3)) if match.group(3) else 0
    return count, sides, modifier


def roll_dice(count: int, sides: int, modifier: int = 0) -> tuple:
    """掷骰子"""
    rolls = [random.randint(1, sides) for _ in range(count)]
    total = sum(rolls) + modifier
    return rolls, total


@router.post("/rooms/{room_id}/characters", response_model=CharacterCardResponse)
async def create_character(
    room_id: int,
    char_data: CharacterCardCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """创建角色卡"""
    # 检查房间是否存在
    result = await db.execute(select(Room).where(Room.id == room_id))
    room = result.scalar_one_or_none()
    if not room:
        raise HTTPException(status_code=404, detail="房间不存在")

    # 检查是否是房间参与者
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
        raise HTTPException(status_code=403, detail="您不在房间中")

    # 检查房间是否已开始
    if room.status != RoomStatus.WAITING:
        raise HTTPException(status_code=400, detail="游戏已开始，无法创建角色")

    new_char = CharacterCard(
        room_id=room_id,
        user_id=current_user.id,
        name=char_data.name,
        hp=char_data.hp,
        max_hp=char_data.max_hp,
        attack_bonus=char_data.attack_bonus,
        damage_dice=char_data.damage_dice,
        notes=char_data.notes
    )
    db.add(new_char)
    await db.commit()
    await db.refresh(new_char)
    return new_char


@router.get("/rooms/{room_id}/characters", response_model=List[CharacterCardResponse])
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
    return characters


@router.put("/characters/{char_id}", response_model=CharacterCardResponse)
async def update_character(
    char_id: int,
    char_data: CharacterCardUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """更新角色卡"""
    result = await db.execute(select(CharacterCard).where(CharacterCard.id == char_id))
    char = result.scalar_one_or_none()
    if not char:
        raise HTTPException(status_code=404, detail="角色卡不存在")

    # 只有角色所有者可以修改
    if char.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权限")

    for field, value in char_data.model_dump(exclude_unset=True).items():
        setattr(char, field, value)

    await db.commit()
    await db.refresh(char)
    return char


@router.post("/rooms/{room_id}/dice", response_model=DiceRollResponse)
async def roll_dice_api(
    room_id: int,
    dice_request: DiceRollRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """掷骰子"""
    # 解析骰子
    count, sides, modifier = parse_dice(dice_request.dice)
    rolls, total = roll_dice(count, sides, modifier)

    # 构建结果字符串
    if modifier > 0:
        details = f"{count}d{sides}: {rolls} + {modifier} = {total}"
    elif modifier < 0:
        details = f"{count}d{sides}: {rolls} - {abs(modifier)} = {total}"
    else:
        details = f"{count}d{sides}: {rolls} = {total}"

    # 创建日志
    log = GameLog(
        room_id=room_id,
        user_id=current_user.id,
        action=LogActionEnum.DICE.value,
        detail=f'{{"dice": "{dice_request.dice}", "result": {total}, "details": "{details}", "reason": "{dice_request.reason or ""}"}}'
    )
    db.add(log)
    await db.commit()

    return DiceRollResponse(
        dice=dice_request.dice,
        result=total,
        details=details,
        reason=dice_request.reason,
        rolled_by=current_user.username,
        timestamp=log.created_at
    )


@router.post("/characters/{char_id}/attack", response_model=AttackResponse)
async def quick_attack(
    char_id: int,
    attack_data: AttackRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """快捷攻击"""
    # 获取角色卡
    result = await db.execute(select(CharacterCard).where(CharacterCard.id == char_id))
    char = result.scalar_one_or_none()
    if not char:
        raise HTTPException(status_code=404, detail="角色卡不存在")

    # 验证权限
    if char.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="只能操作自己的角色")

    # 获取房间信息
    result = await db.execute(select(Room).where(Room.id == char.room_id))
    room = result.scalar_one()

    # 掷攻击骰 (1d20 + attack_bonus)
    attack_rolls, attack_total = roll_dice(1, 20, char.attack_bonus)

    # 掷伤害骰
    count, sides, modifier = parse_dice(char.damage_dice)
    damage_rolls, damage_total = roll_dice(count, sides, modifier)

    # 记录日志
    log_detail = {
        "character_name": char.name,
        "attack_roll": attack_total,
        "attack_rolls": attack_rolls,
        "attack_bonus": char.attack_bonus,
        "damage_dice": char.damage_dice,
        "damage_roll": damage_total,
        "damage_rolls": damage_rolls,
        "target": attack_data.target_name or "未知目标"
    }
    import json
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
        attack_bonus=char.attack_bonus,
        damage_dice=char.damage_dice,
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


@router.get("/rooms/{room_id}/logs", response_model=List[GameLogResponse])
async def get_room_logs(
    room_id: int,
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取房间日志"""
    result = await db.execute(
        select(GameLog)
        .where(GameLog.room_id == room_id)
        .order_by(GameLog.created_at.desc())
        .limit(limit)
    )
    logs = result.scalars().all()

    # 获取用户名
    result = []
    for log in logs:
        user_result = await db.execute(select(User).where(User.id == log.user_id))
        user = user_result.scalar_one()

        # 获取角色名
        char_result = await db.execute(
            select(CharacterCard).where(
                and_(
                    CharacterCard.room_id == room_id,
                    CharacterCard.user_id == log.user_id
                )
            )
        )
        char = char_result.scalar_one_or_none()

        result.append(GameLogResponse(
            id=log.id,
            room_id=log.room_id,
            user_id=log.user_id,
            action=log.action,
            detail=log.detail,
            username=user.username,
            character_name=char.name if char else None,
            created_at=log.created_at
        ))

    return result