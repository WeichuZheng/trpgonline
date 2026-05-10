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
    max_characters: Optional[int] = 20
    default_max_players: Optional[int] = 8


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
    max_characters: int = 20
    default_max_players: int = 8


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
    default_visible: Optional[bool] = None


class ResourceResponse(ResourceBase):
    id: int
    module_id: int
    owner_id: int
    content: Optional[str]
    default_visible: bool
    created_at: datetime

    class Config:
        from_attributes = True


class ResourceToggleVisible(BaseModel):
    default_visible: bool


# ============ 房间资源可见性 schemas ============

class RoomResourceToggle(BaseModel):
    is_shown: bool


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
    max_players: Optional[int] = None


class RoomCreate(RoomBase):
    # module_id 从路径参数获取，不在 body 中
    pass


class RoomUpdate(BaseModel):
    name: Optional[str] = None


class RoomResponse(RoomBase):
    id: int
    module_id: int
    gm_id: int
    status: RoomStatusEnum
    active_map_id: Optional[int] = None
    created_at: datetime
    # 额外字段
    module_title: Optional[str] = None
    gm_username: Optional[str] = None
    current_players: Optional[int] = None
    max_players: int = 8

    class Config:
        from_attributes = True


class RoomWithDetails(RoomResponse):
    # 继承 RoomResponse 的所有字段，包括 module_title, gm_username, current_players, max_players
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
    avatar: Optional[str] = None
    profession: Optional[str] = None
    hp: int = 10
    max_hp: int = 10
    san: int = 50
    mp: int = 0
    max_mp: int = 0
    attributes: str = "{}"
    skills: str = "[]"
    items: str = "[]"
    spells: str = "[]"
    notes: Optional[str] = None


class CharacterCardCreate(CharacterCardBase):
    is_npc: bool = False


class CharacterCardUpdate(BaseModel):
    name: Optional[str] = None
    avatar: Optional[str] = None
    profession: Optional[str] = None
    hp: Optional[int] = None
    max_hp: Optional[int] = None
    san: Optional[int] = None
    mp: Optional[int] = None
    max_mp: Optional[int] = None
    attributes: Optional[str] = None
    skills: Optional[str] = None
    items: Optional[str] = None
    spells: Optional[str] = None
    notes: Optional[str] = None
    is_npc: Optional[bool] = None


class CharacterCardResponse(BaseModel):
    id: int
    room_id: int
    name: str
    avatar: Optional[str] = None
    profession: Optional[str] = None
    hp: int
    max_hp: int
    san: int
    mp: int
    max_mp: int
    attributes: str = "{}"
    skills: str = "[]"
    items: str = "[]"
    spells: str = "[]"
    notes: Optional[str] = None
    is_npc: bool = False
    created_at: datetime

    class Config:
        from_attributes = True


# ============ 地图 schemas ============

class MapBase(BaseModel):
    name: str
    image_url: Optional[str] = None
    grid_size: Optional[float] = None


class MapCreate(MapBase):
    module_id: int
    grid_size: Optional[float] = None


class MapUpdate(BaseModel):
    name: Optional[str] = None
    image_url: Optional[str] = None
    grid_size: Optional[float] = None


class MapResponse(MapBase):
    id: int
    module_id: int
    grid_size: Optional[float] = None
    created_at: datetime

    class Config:
        from_attributes = True


class MapWithUnits(MapResponse):
    units: List["MapUnitResponse"] = []


class MapUnitBase(BaseModel):
    name: str
    character_id: Optional[int] = None
    x: float
    y: float
    width: float = 1.0
    height: float = 1.0
    hp: Optional[int] = None
    max_hp: Optional[int] = None
    is_enemy: bool = False
    icon: Optional[str] = None


class MapUnitCreate(MapUnitBase):
    # map_id comes from URL path, not request body
    pass


class MapUnitUpdate(BaseModel):
    name: Optional[str] = None
    character_id: Optional[int] = None
    x: Optional[float] = None
    y: Optional[float] = None
    width: Optional[float] = None
    height: Optional[float] = None
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
    dice: str = "1d20"  # 默认 d20
    reason: Optional[str] = None
    character_name: Optional[str] = None


class DiceRollResponse(BaseModel):
    dice: str
    result: int
    details: str  # 如 "角色名 掷出 2d6+1 = [2, 4]+1 = 7"
    reason: Optional[str]
    rolled_by: str
    character_name: Optional[str] = None
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


class ActiveMapRequest(BaseModel):
    map_id: Optional[int] = None


# ============ 角色模板 schemas ============

class CharacterTemplateBase(BaseModel):
    name: str
    avatar: Optional[str] = None
    profession: Optional[str] = None
    hp: int = 10
    max_hp: int = 10
    san: int = 50
    mp: int = 0
    max_mp: int = 0
    attributes: str = "{}"
    skills: str = "[]"
    items: str = "[]"
    spells: str = "[]"
    notes: Optional[str] = None
    is_enemy: bool = False


class CharacterTemplateCreate(CharacterTemplateBase):
    # module_id comes from URL path, not request body
    pass


class CharacterTemplateUpdate(BaseModel):
    name: Optional[str] = None
    avatar: Optional[str] = None
    profession: Optional[str] = None
    hp: Optional[int] = None
    max_hp: Optional[int] = None
    san: Optional[int] = None
    mp: Optional[int] = None
    max_mp: Optional[int] = None
    attributes: Optional[str] = None
    skills: Optional[str] = None
    items: Optional[str] = None
    spells: Optional[str] = None
    notes: Optional[str] = None
    is_enemy: Optional[bool] = None


class CharacterTemplateResponse(CharacterTemplateBase):
    id: int
    module_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# 更新前向引用
RoomWithDetails.model_rebuild()
MapWithUnits.model_rebuild()