# TRPG Online - 数据库模型
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, Float, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from backend.database import Base


class User(Base):
    """用户表"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    can_create_module = Column(Boolean, default=False)  # 可创建模组的权限
    created_at = Column(DateTime, default=datetime.utcnow)

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
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系
    owner = relationship("User", back_populates="modules")
    resources = relationship("Resource", back_populates="module", cascade="all, delete-orphan")
    rooms = relationship("Room", back_populates="module", cascade="all, delete-orphan")
    maps = relationship("Map", back_populates="module", cascade="all, delete-orphan")


class ResourceType(enum.Enum):
    """资源类型"""
    IMAGE = "image"
    TEXT = "text"


class Resource(Base):
    """资源表"""
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, index=True)
    module_id = Column(Integer, ForeignKey("modules.id"), nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    type = Column(SQLEnum(ResourceType), nullable=False)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=True)  # 文本内容或图片URL
    display_type = Column(String(50), default="story")  # 文本展示类型: story/rule/clue/character/mission
    is_visible = Column(Boolean, default=False)  # 是否可见
    created_at = Column(DateTime, default=datetime.utcnow)

    # 关系
    module = relationship("Module", back_populates="resources")
    owner = relationship("User", back_populates="resources")


class RoomStatus(enum.Enum):
    """房间状态"""
    WAITING = "waiting"   # 等待中
    ACTIVE = "active"     # 进行中
    ENDED = "ended"       # 已结束


class Room(Base):
    """房间表"""
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    module_id = Column(Integer, ForeignKey("modules.id"), nullable=False)
    gm_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(100), nullable=False)
    status = Column(SQLEnum(RoomStatus), default=RoomStatus.WAITING)
    created_at = Column(DateTime, default=datetime.utcnow)

    # 关系
    module = relationship("Module", back_populates="rooms")
    gm = relationship("User", back_populates="rooms_created")
    participants = relationship("RoomParticipant", back_populates="room", cascade="all, delete-orphan")
    characters = relationship("CharacterCard", back_populates="room", cascade="all, delete-orphan")
    logs = relationship("GameLog", back_populates="room", cascade="all, delete-orphan")


class RoomParticipant(Base):
    """房间参与者表"""
    __tablename__ = "room_participants"

    room_id = Column(Integer, ForeignKey("rooms.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    role = Column(String(20), default="player")  # gm / player
    character_name = Column(String(100), nullable=True)
    joined_at = Column(DateTime, default=datetime.utcnow)

    # 关系
    room = relationship("Room", back_populates="participants")
    user = relationship("User")


class CharacterCard(Base):
    """角色卡表"""
    __tablename__ = "character_cards"

    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(100), nullable=False)
    hp = Column(Integer, default=10)
    max_hp = Column(Integer, default=10)
    attack_bonus = Column(Integer, default=0)  # 攻击加值
    damage_dice = Column(String(20), default="1d6")  # 伤害骰子
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # 关系
    room = relationship("Room", back_populates="characters")
    user = relationship("User")


class Map(Base):
    """地图表"""
    __tablename__ = "maps"

    id = Column(Integer, primary_key=True, index=True)
    module_id = Column(Integer, ForeignKey("modules.id"), nullable=False)
    name = Column(String(100), nullable=False)
    image_url = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # 关系
    module = relationship("Module", back_populates="maps")
    units = relationship("MapUnit", back_populates="map", cascade="all, delete-orphan")


class MapUnit(Base):
    """地图单位表"""
    __tablename__ = "map_units"

    id = Column(Integer, primary_key=True, index=True)
    map_id = Column(Integer, ForeignKey("maps.id"), nullable=False)
    name = Column(String(100), nullable=False)
    x = Column(Float, nullable=False)
    y = Column(Float, nullable=False)
    hp = Column(Integer, nullable=True)
    max_hp = Column(Integer, nullable=True)
    is_enemy = Column(Boolean, default=False)
    icon = Column(String(50), nullable=True)  # 图标标识
    created_at = Column(DateTime, default=datetime.utcnow)

    # 关系
    map = relationship("Map", back_populates="units")


class GameLog(Base):
    """游戏日志表"""
    __tablename__ = "game_logs"

    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    action = Column(String(50), nullable=False)  # attack / damage / heal / move / dice / custom
    detail = Column(Text, nullable=True)  # JSON 格式的详细信息
    created_at = Column(DateTime, default=datetime.utcnow)

    # 关系
    room = relationship("Room", back_populates="logs")
    user = relationship("User")