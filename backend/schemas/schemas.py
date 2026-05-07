# TRPG Online - Pydantic Schemas
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


# ============ 基础 schemas ============

class UserBase(BaseModel):
    username: str
    can_create_module: bool = False


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    can_create_module: bool
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ============ 模组 schemas ============

class ModuleBase(BaseModel):
    title: str
    description: Optional[str] = None


class ModuleCreate(ModuleBase):
    pass


class ModuleUpdate(ModuleBase):
    pass


class ModuleResponse(ModuleBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ModuleWithOwner(ModuleResponse):
    owner_username: Optional[str] = None


# ============ 资源 schemas ============

class ResourceTypeEnum(str, Enum):
    IMAGE = "image"
    TEXT = "text"


class DisplayTypeEnum(str, Enum):
    STORY = "story"       # 背景故事
    RULE = "rule"         # 规则说明
    CLUE = "clue"         # 线索卡
    CHARACTER = "character"  # 角色描述
    MISSION = "mission"   # 任务目标


class ResourceBase(BaseModel):
    title: str
    type: ResourceTypeEnum
    display_type: DisplayTypeEnum = DisplayTypeEnum.STORY


class ResourceCreate(ResourceBase):
    content: Optional[str] = None
    module_id: int


class ResourceUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    display_type: Optional[DisplayTypeEnum] = None
    is_visible: Optional[bool] = None


class ResourceResponse(ResourceBase):
    id: int
    module_id: int
    owner_id: int
    content: Optional[str]
    is_visible: bool
    created_at: datetime

    class Config:
        from_attributes = True


class ResourceToggleVisible(BaseModel):
    is_visible: bool


# ============ 房间 schemas ============

class RoomStatusEnum(str, Enum):
    WAITING = "waiting"
    ACTIVE = "active"
    ENDED = "ended"


class RoomRoleEnum(str, Enum):
    GM = "gm"
    PLAYER = "player"


class RoomBase(BaseModel):
    name: str


class RoomCreate(RoomBase):
    # module_id 从路径参数获取，不在 body 中
    pass


class RoomResponse(RoomBase):
    id: int
    module_id: int
    gm_id: int
    status: RoomStatusEnum
    created_at: datetime

    class Config:
        from_attributes = True


class RoomWithDetails(RoomResponse):
    module_title: Optional[str] = None
    gm_username: Optional[str] = None
    participants: List["ParticipantResponse"] = []


class ParticipantResponse(BaseModel):
    user_id: int
    username: str
    role: RoomRoleEnum
    character_name: Optional[str]

    class Config:
        from_attributes = True


# ============ 角色卡 schemas ============

class CharacterCardBase(BaseModel):
    name: str
    hp: int = 10
    max_hp: int = 10
    attack_bonus: int = 0
    damage_dice: str = "1d6"
    notes: Optional[str] = None


class CharacterCardCreate(CharacterCardBase):
    room_id: int


class CharacterCardUpdate(BaseModel):
    name: Optional[str] = None
    hp: Optional[int] = None
    max_hp: Optional[int] = None
    attack_bonus: Optional[int] = None
    damage_dice: Optional[str] = None
    notes: Optional[str] = None


class CharacterCardResponse(CharacterCardBase):
    id: int
    room_id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ============ 地图 schemas ============

class MapBase(BaseModel):
    name: str
    image_url: Optional[str] = None


class MapCreate(MapBase):
    module_id: int


class MapUpdate(BaseModel):
    name: Optional[str] = None
    image_url: Optional[str] = None


class MapResponse(MapBase):
    id: int
    module_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class MapWithUnits(MapResponse):
    units: List["MapUnitResponse"] = []


class MapUnitBase(BaseModel):
    name: str
    x: float
    y: float
    hp: Optional[int] = None
    max_hp: Optional[int] = None
    is_enemy: bool = False
    icon: Optional[str] = None


class MapUnitCreate(MapUnitBase):
    map_id: int


class MapUnitUpdate(BaseModel):
    name: Optional[str] = None
    x: Optional[float] = None
    y: Optional[float] = None
    hp: Optional[int] = None
    max_hp: Optional[int] = None
    is_enemy: Optional[bool] = None
    icon: Optional[str] = None


class MapUnitResponse(MapUnitBase):
    id: int
    map_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ============ 日志 schemas ============

class LogActionEnum(str, Enum):
    DICE = "dice"
    ATTACK = "attack"
    DAMAGE = "damage"
    HEAL = "heal"
    MOVE = "move"
    CUSTOM = "custom"


class GameLogBase(BaseModel):
    action: LogActionEnum
    detail: Optional[str] = None


class GameLogCreate(GameLogBase):
    room_id: int


class GameLogResponse(GameLogBase):
    id: int
    room_id: int
    user_id: int
    username: Optional[str] = None
    character_name: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


# ============ 掷骰子 schemas ============

class DiceRollRequest(BaseModel):
    room_id: int
    dice: str = "1d20"  # 默认 d20
    reason: Optional[str] = None


class DiceRollResponse(BaseModel):
    dice: str
    result: int
    details: str  # 如 "3d6: [2, 4, 1] = 7"
    reason: Optional[str]
    rolled_by: str
    timestamp: datetime


# ============ 快捷攻击 schemas ============

class AttackRequest(BaseModel):
    character_id: int
    target_name: Optional[str] = None


class AttackResponse(BaseModel):
    character_name: str
    attack_bonus: int
    damage_dice: str
    attack_roll: int
    damage_roll: int
    total_damage: int
    target_name: Optional[str]
    log: GameLogResponse


# 更新前向引用
RoomWithDetails.model_rebuild()
MapWithUnits.model_rebuild()