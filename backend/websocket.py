# TRPG Online - WebSocket 处理
from typing import Dict, Set
from fastapi import WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.database import AsyncSessionLocal
from backend.models.models import Room, RoomParticipant


class ConnectionManager:
    """WebSocket 连接管理器"""

    def __init__(self):
        # room_id -> set of websockets
        self.active_connections: Dict[int, Set[WebSocket]] = {}
        # websocket -> room_id mapping
        self.socket_rooms: Dict[WebSocket, int] = {}
        # websocket -> user_id mapping
        self.socket_users: Dict[WebSocket, int] = {}

    async def connect(self, websocket: WebSocket, room_id: int, user_id: int):
        """WebSocket 连接"""
        await websocket.accept()
        if room_id not in self.active_connections:
            self.active_connections[room_id] = set()
        self.active_connections[room_id].add(websocket)
        self.socket_rooms[websocket] = room_id
        self.socket_users[websocket] = user_id

    def disconnect(self, websocket: WebSocket):
        """WebSocket 断开"""
        room_id = self.socket_rooms.pop(websocket, None)
        user_id = self.socket_users.pop(websocket, None)
        if room_id and room_id in self.active_connections:
            self.active_connections[room_id].discard(websocket)
            if not self.active_connections[room_id]:
                del self.active_connections[room_id]

    async def broadcast_to_room(self, room_id: int, message: dict):
        """向房间内所有人广播消息"""
        if room_id in self.active_connections:
            for connection in self.active_connections[room_id]:
                try:
                    await connection.send_json(message)
                except Exception:
                    pass  # 忽略发送失败

    async def send_personal(self, websocket: WebSocket, message: dict):
        """发送个人消息"""
        try:
            await websocket.send_json(message)
        except Exception:
            pass


# 全局连接管理器
manager = ConnectionManager()


async def websocket_endpoint(websocket: WebSocket, room_id: int):
    """WebSocket 端点"""
    # 获取用户认证（这里简化为从 URL 参数获取，生产环境应该用 token）
    user_id = int(websocket.query_params.get("user_id", "0"))
    username = websocket.query_params.get("username", "匿名")

    # 验证用户是否在房间中
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(RoomParticipant).where(
                RoomParticipant.room_id == room_id,
                RoomParticipant.user_id == user_id
            )
        )
        participant = result.scalar_one_or_none()
        if not participant:
            await websocket.close(code=4003, reason="不在房间中")
            return

        # 获取房间信息
        result = await db.execute(select(Room).where(Room.id == room_id))
        room = result.scalar_one()

    # 建立连接
    await manager.connect(websocket, room_id, user_id)

    try:
        # 通知其他人用户已加入
        await manager.broadcast_to_room(room_id, {
            "type": "user_joined",
            "user_id": user_id,
            "username": username,
            "message": f"{username} 加入了房间"
        })

        # 持续接收消息
        while True:
            data = await websocket.receive_json()
            await handle_websocket_message(room_id, user_id, username, data)

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        # 通知其他人用户已离开
        await manager.broadcast_to_room(room_id, {
            "type": "user_left",
            "user_id": user_id,
            "username": username,
            "message": f"{username} 离开了房间"
        })


async def handle_websocket_message(room_id: int, user_id: int, username: str, data: dict):
    """处理 WebSocket 消息"""
    message_type = data.get("type")

    if message_type == "dice_roll":
        # 广播掷骰结果
        await manager.broadcast_to_room(room_id, {
            "type": "dice_result",
            "dice": data.get("dice"),
            "result": data.get("result"),
            "details": data.get("details"),
            "rolled_by": username,
            "reason": data.get("reason")
        })

    elif message_type == "unit_move":
        # 广播单位移动
        await manager.broadcast_to_room(room_id, {
            "type": "unit_moved",
            "unit_id": data.get("unit_id"),
            "unit_name": data.get("unit_name"),
            "x": data.get("x"),
            "y": data.get("y"),
            "moved_by": username
        })

    elif message_type == "hp_change":
        # 广播血量变化
        await manager.broadcast_to_room(room_id, {
            "type": "hp_updated",
            "unit_id": data.get("unit_id"),
            "unit_name": data.get("unit_name"),
            "hp": data.get("hp"),
            "max_hp": data.get("max_hp"),
            "changed_by": username
        })

    elif message_type == "new_log":
        # 广播新日志
        await manager.broadcast_to_room(room_id, {
            "type": "log_added",
            "action": data.get("action"),
            "detail": data.get("detail"),
            "username": username
        })

    elif message_type == "resource_visible":
        # 广播资源可见性变化
        await manager.broadcast_to_room(room_id, {
            "type": "resource_toggled",
            "resource_id": data.get("resource_id"),
            "resource_title": data.get("resource_title"),
            "is_visible": data.get("is_visible"),
            "changed_by": username
        })