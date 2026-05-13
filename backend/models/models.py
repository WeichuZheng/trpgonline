# TRPG Online - 数据库模型
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, Float, Enum as SQLEnum, Index
from sqlalchemy.orm import relationship
from datetime import datetime, timezone, timedelta
import enum

from backend.database import Base

# UTC+8 中国标准时间
CST = timezone(timedelta(hours=8))

def cst_now():
    return datetime.now(CST)


class User(Base):
    """用户表"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    can_create_module = Column(Boolean, default=False)  # 可创建模组的权限
    requested_gm = Column(Boolean, default=False)       # 已申请 GM 权限
    is_admin = Column(Boolean, default=False)           # 管理员权限
    created_at = Column(DateTime, default=cst_now)

    # 关系
    modules = relationship("Module", back_populates="owner", cascade="all, delete-orphan")
    resources = relationship("Resource", back_populates="owner", cascade="all, delete-orphan")
    rooms_created = relationship("Room", back_populates="gm", cascade="all, delete-orphan")


class Module(Base):
    """模组表"""
    __tablename__ = "modules"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    max_characters = Column(Integer, default=20)  # 角色数上限（NPC+怪物）
    default_max_players = Column(Integer, default=8)  # 默认玩家数上限
    theme = Column(String(50), default="dark")  # 配色方案预设名称
    chapters_config = Column(Text, default='[]')     # JSON 章节结构
    current_chapter_index = Column(Integer, default=0)
    current_scene_index = Column(Integer, default=0)
    created_at = Column(DateTime, default=cst_now)
    updated_at = Column(DateTime, default=cst_now, onupdate=cst_now)

    # 关系
    owner = relationship("User", back_populates="modules")
    resources = relationship("Resource", back_populates="module", cascade="all, delete-orphan")
    rooms = relationship("Room", back_populates="module", cascade="all, delete-orphan")
    maps = relationship("Map", back_populates="module", cascade="all, delete-orphan")
    character_templates = relationship("CharacterTemplate", back_populates="module", cascade="all, delete-orphan")
    module_tasks = relationship("ModuleTask", cascade="all, delete-orphan")


class ResourceType(enum.Enum):
    """资源类型"""
    IMAGE = "image"
    TEXT = "text"


class Resource(Base):
    """资源表"""
    __tablename__ = "resources"
    __table_args__ = (
        Index('idx_resources_module_id', 'module_id'),
    )

    id = Column(Integer, primary_key=True, index=True)
    module_id = Column(Integer, ForeignKey("modules.id"), nullable=False, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    type = Column(SQLEnum(ResourceType), nullable=False)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=True)  # TipTap JSON 文档或图片URL
    default_visible = Column(Boolean, default=False)  # 模组编辑时的默认可见性
    created_at = Column(DateTime, default=cst_now)

    # 关系
    module = relationship("Module", back_populates="resources")
    owner = relationship("User", back_populates="resources")
    room_resources = relationship("RoomResource", back_populates="resource", cascade="all, delete-orphan")


class RoomResource(Base):
    """房间资源可见性表"""
    __tablename__ = "room_resources"

    room_id = Column(Integer, ForeignKey("rooms.id"), primary_key=True)
    resource_id = Column(Integer, ForeignKey("resources.id"), primary_key=True)
    is_shown = Column(Boolean, default=False)  # 房间内当前是否显示给玩家
    revealed_blocks = Column(Text, default="[]")  # JSON array of revealed hidden-block indices

    # 关系
    room = relationship("Room", back_populates="room_resources")
    resource = relationship("Resource", back_populates="room_resources")


class RoomStatus(enum.Enum):
    """房间状态"""
    WAITING = "waiting"   # 等待中
    ACTIVE = "active"     # 进行中
    ENDED = "ended"       # 已结束


class Room(Base):
    """房间表"""
    __tablename__ = "rooms"
    __table_args__ = (
        Index('idx_rooms_module_id', 'module_id'),
    )

    id = Column(Integer, primary_key=True, index=True)
    module_id = Column(Integer, ForeignKey("modules.id"), nullable=False)
    gm_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(100), nullable=False)
    status = Column(SQLEnum(RoomStatus), default=RoomStatus.WAITING)
    active_map_id = Column(Integer, ForeignKey("maps.id"), nullable=True)
    max_players = Column(Integer, default=8)  # 玩家数上限
    created_at = Column(DateTime, default=cst_now)

    # 关系
    module = relationship("Module", back_populates="rooms")
    gm = relationship("User", back_populates="rooms_created")
    active_map = relationship("Map", foreign_keys=[active_map_id])
    participants = relationship("RoomParticipant", back_populates="room", cascade="all, delete-orphan")
    characters = relationship("CharacterCard", back_populates="room", cascade="all, delete-orphan")
    logs = relationship("GameLog", back_populates="room", cascade="all, delete-orphan")
    room_resources = relationship("RoomResource", back_populates="room", cascade="all, delete-orphan")
    player_notes = relationship("PlayerNote", cascade="all, delete-orphan")


class RoomParticipant(Base):
    """房间参与者表"""
    __tablename__ = "room_participants"

    room_id = Column(Integer, ForeignKey("rooms.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    role = Column(String(20), default="player")  # gm / player
    character_name = Column(String(100), nullable=True)
    joined_at = Column(DateTime, default=cst_now)

    # 关系
    room = relationship("Room", back_populates="participants")
    user = relationship("User")


class CharacterCard(Base):
    """角色卡表"""
    __tablename__ = "character_cards"
    __table_args__ = (
        Index('idx_character_cards_room_id', 'room_id'),
    )

    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)
    name = Column(String(100), nullable=False)
    avatar = Column(String(500), nullable=True)  # avatar image URL
    profession = Column(String(50), nullable=True)  # 职业
    hp = Column(Integer, default=10)
    max_hp = Column(Integer, default=10)
    san = Column(Integer, default=50)  # SAN 当前值（上限=意志值）
    mp = Column(Integer, default=0)   # 魔力当前值
    max_mp = Column(Integer, default=0)  # 魔力上限
    attributes = Column(Text, default="{}")  # JSON: {"strength":50,"constitution":50,...}
    skills = Column(Text, default="[]")      # JSON: [{"name":"格斗","value":20,"attribute":"strength","is_career":true},...]
    items = Column(Text, default="[]")       # JSON: [{"name":"手枪","type":"weapon","detail":"1d8+2"},...]
    spells = Column(Text, default="[]")      # JSON: [{"name":"火球术","level":"简单级","mp_cost":3},...]
    notes = Column(Text, nullable=True)
    is_npc = Column(Boolean, default=False)
    created_at = Column(DateTime, default=cst_now)

    # 关系
    room = relationship("Room", back_populates="characters")


class Map(Base):
    """地图表"""
    __tablename__ = "maps"

    id = Column(Integer, primary_key=True, index=True)
    module_id = Column(Integer, ForeignKey("modules.id"), nullable=False)
    name = Column(String(100), nullable=False)
    image_url = Column(String(500), nullable=True)
    grid_size = Column(Float, nullable=True)  # 网格大小（地图像素）
    created_at = Column(DateTime, default=cst_now)

    # 关系
    module = relationship("Module", back_populates="maps")
    units = relationship("MapUnit", back_populates="map", cascade="all, delete-orphan")


class MapUnit(Base):
    """地图单位表"""
    __tablename__ = "map_units"
    __table_args__ = (
        Index('idx_map_units_map_id', 'map_id'),
    )

    id = Column(Integer, primary_key=True, index=True)
    map_id = Column(Integer, ForeignKey("maps.id"), nullable=False)
    character_id = Column(Integer, ForeignKey("character_cards.id"), nullable=True)
    name = Column(String(100), nullable=False)
    x = Column(Float, nullable=False)
    y = Column(Float, nullable=False)
    width = Column(Float, default=1.0)  # token 宽度（网格单位）
    height = Column(Float, default=1.0)  # token 高度（网格单位）
    hp = Column(Integer, nullable=True)
    max_hp = Column(Integer, nullable=True)
    is_enemy = Column(Boolean, default=False)
    icon = Column(String(500), nullable=True)  # avatar image URL
    created_at = Column(DateTime, default=cst_now)

    # 关系
    map = relationship("Map", back_populates="units")


class CharacterTemplate(Base):
    """模组角色模板表"""
    __tablename__ = "character_templates"

    id = Column(Integer, primary_key=True, index=True)
    module_id = Column(Integer, ForeignKey("modules.id"), nullable=False)
    name = Column(String(100), nullable=False)
    avatar = Column(String(500), nullable=True)  # avatar image URL
    profession = Column(String(50), nullable=True)
    hp = Column(Integer, default=10)
    max_hp = Column(Integer, default=10)
    san = Column(Integer, default=50)
    mp = Column(Integer, default=0)
    max_mp = Column(Integer, default=0)
    attributes = Column(Text, default="{}")
    skills = Column(Text, default="[]")
    items = Column(Text, default="[]")
    spells = Column(Text, default="[]")
    notes = Column(Text, nullable=True)
    is_enemy = Column(Boolean, default=False)
    created_at = Column(DateTime, default=cst_now)

    # 关系
    module = relationship("Module", back_populates="character_templates")


class PlayerNote(Base):
    """玩家私有笔记表"""
    __tablename__ = "player_notes"
    __table_args__ = (
        Index('idx_player_notes_room_id', 'room_id'),
    )

    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(Text, default="")
    updated_at = Column(DateTime, default=cst_now, onupdate=cst_now)

    # 关系
    room = relationship("Room", back_populates="player_notes")
    user = relationship("User")


class GameLog(Base):
    """游戏日志表"""
    __tablename__ = "game_logs"
    __table_args__ = (
        Index('idx_game_logs_room_id', 'room_id'),
        Index('idx_game_logs_created_at', 'created_at'),
    )

    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    action = Column(String(50), nullable=False)  # attack / damage / heal / move / dice / custom
    detail = Column(Text, nullable=True)  # JSON 格式的详细信息
    created_at = Column(DateTime, default=cst_now)

    # 关系
    room = relationship("Room", back_populates="logs")
    user = relationship("User")


class ModuleTask(Base):
    """模组任务板——任务定义"""
    __tablename__ = "module_tasks"
    __table_args__ = (
        Index('idx_module_tasks_module_id', 'module_id'),
    )

    id = Column(Integer, primary_key=True, index=True)
    module_id = Column(Integer, ForeignKey("modules.id"), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(20), default="hidden")  # hidden / current / completed
    exploration_percent = Column(Integer, default=5)
    sort_order = Column(Integer, default=0)
    created_at = Column(DateTime, default=cst_now)

    module = relationship("Module", back_populates="module_tasks")
    clocks = relationship("TaskClock", back_populates="task", cascade="all, delete-orphan")


class TaskClock(Base):
    """关键事件时钟"""
    __tablename__ = "task_clocks"
    __table_args__ = (
        Index('idx_task_clocks_task_id', 'task_id'),
    )

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("module_tasks.id"), nullable=False)
    total = Column(Integer, default=6)
    increment_expr = Column(String(20), default="1d3")
    current_value = Column(Integer, default=0)
    is_expired = Column(Boolean, default=False)
    created_at = Column(DateTime, default=cst_now)

    task = relationship("ModuleTask", back_populates="clocks")