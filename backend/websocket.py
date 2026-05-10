# TRPG Online - WebSocket 处理
from typing import Dict, Set, List
from fastapi import WebSocket, WebSocketDisconnect
from sqlalchemy import select

from backend.database import AsyncSessionLocal
from backend.models.models import RoomParticipant, GameLog


class ConnectionManager:
    """WebSocket 连接管理器"""

    def __init__(self):
        # room_id -> set of websockets
        self.active_connections: Dict[int, Set[WebSocket]] = {}
        # websocket -> room_id mapping
        self.socket_rooms: Dict[WebSocket, int] = {}
        # websocket -> (user_id, username) mapping
        self.socket_users: Dict[WebSocket, tuple] = {}

    async def connect(self, websocket: WebSocket, room_id: int, user_id: int, username: str):
        """WebSocket 连接，返回是否是该用户在此房间的第一个连接"""
        is_first = not self._has_user_in_room(room_id, user_id)

        await websocket.accept()
        if room_id not in self.active_connections:
            self.active_connections[room_id] = set()
        self.active_connections[room_id].add(websocket)
        self.socket_rooms[websocket] = room_id
        self.socket_users[websocket] = (user_id, username)

        return is_first

    def disconnect(self, websocket: WebSocket):
        """WebSocket 断开，返回 (room_id, user_id, username, is_last)"""
        room_id = self.socket_rooms.pop(websocket, None)
        info = self.socket_users.pop(websocket, None)
        user_id = info[0] if info else None
        username = info[1] if info else "匿名"

        if room_id and room_id in self.active_connections:
            self.active_connections[room_id].discard(websocket)
            if not self.active_connections[room_id]:
                del self.active_connections[room_id]

        is_last = room_id is not None and not self._has_user_in_room(room_id, user_id)
        return room_id, user_id, username, is_last

    def _has_user_in_room(self, room_id: int, user_id: int) -> bool:
        """检查某用户是否在该房间已有连接"""
        if room_id not in self.active_connections:
            return False
        for ws in self.active_connections[room_id]:
            info = self.socket_users.get(ws)
            if info and info[0] == user_id:
                return True
        return False

    def get_online_users(self, room_id: int) -> List[dict]:
        """获取房间内在线用户列表"""
        users = []
        seen = set()
        if room_id in self.active_connections:
            for ws in self.active_connections[room_id]:
                info = self.socket_users.get(ws)
                if info and info[0] not in seen:
                    seen.add(info[0])
                    users.append({"user_id": info[0], "username": info[1]})
        return users

    async def broadcast_to_room(self, room_id: int, message: dict):
        """向房间内所有人广播消息"""
        if room_id in self.active_connections:
            for connection in self.active_connections[room_id]:
                try:
                    await connection.send_json(message)
                except Exception:
                    pass

    async def broadcast_online_users(self, room_id: int):
        """广播在线用户列表"""
        users = self.get_online_users(room_id)
        await self.broadcast_to_room(room_id, {
            "type": "online_users",
            "users": users
        })


# 全局连接管理器
manager = ConnectionManager()


async def _write_log(room_id: int, user_id: int, detail: str):
    """写入游戏日志"""
    async with AsyncSessionLocal() as db:
        log = GameLog(
            room_id=room_id,
            user_id=user_id,
            action="custom",
            detail=detail
        )
        db.add(log)
        await db.commit()


async def websocket_endpoint(websocket: WebSocket, room_id: int):
    """WebSocket 端点"""
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

    # 建立连接，判断是否是该用户的第一个连接
    is_first = await manager.connect(websocket, room_id, user_id, username)

    try:
        # 只有第一个连接时才广播加入、写日志
        if is_first:
            await _write_log(room_id, user_id, f"{username} 加入了房间")
            await manager.broadcast_to_room(room_id, {
                "type": "user_joined",
                "user_id": user_id,
                "username": username,
                "message": f"{username} 加入了房间"
            })
        await manager.broadcast_online_users(room_id)

        # 持续接收消息
        while True:
            data = await websocket.receive_json()
            await handle_websocket_message(room_id, user_id, username, data)

    except WebSocketDisconnect:
        room_id, user_id, username, is_last = manager.disconnect(websocket)
        # 只有最后一个连接断开时才广播离开、写日志
        if room_id and is_last:
            await _write_log(room_id, user_id, f"{username} 离开了房间")
            await manager.broadcast_to_room(room_id, {
                "type": "user_left",
                "user_id": user_id,
                "username": username,
                "message": f"{username} 离开了房间"
            })
        if room_id:
            await manager.broadcast_online_users(room_id)


async def handle_websocket_message(room_id: int, user_id: int, username: str, data: dict):
    """处理 WebSocket 消息"""
    message_type = data.get("type")

    if message_type == "dice_roll":
        await manager.broadcast_to_room(room_id, {
            "type": "dice_result",
            "dice": data.get("dice"),
            "result": data.get("result"),
            "details": data.get("details"),
            "rolled_by": username,
            "reason": data.get("reason")
        })

    elif message_type == "unit_move":
        await manager.broadcast_to_room(room_id, {
            "type": "unit_moved",
            "unit_id": data.get("unit_id"),
            "unit_name": data.get("unit_name"),
            "x": data.get("x"),
            "y": data.get("y"),
            "moved_by": username
        })

    elif message_type == "hp_change":
        await manager.broadcast_to_room(room_id, {
            "type": "hp_updated",
            "unit_id": data.get("unit_id"),
            "unit_name": data.get("unit_name"),
            "hp": data.get("hp"),
            "max_hp": data.get("max_hp"),
            "changed_by": username
        })

    elif message_type == "new_log":
        await manager.broadcast_to_room(room_id, {
            "type": "log_added",
            "action": data.get("action"),
            "detail": data.get("detail"),
            "username": username
        })

    elif message_type == "resource_visible":
        await manager.broadcast_to_room(room_id, {
            "type": "resource_toggled",
            "resource_id": data.get("resource_id"),
            "resource_title": data.get("resource_title"),
            "is_visible": data.get("is_visible"),
            "changed_by": username
        })

    elif message_type == "unit_created":
        await manager.broadcast_to_room(room_id, {
            "type": "unit_created",
            "unit": data.get("unit"),
            "created_by": username
        })

    elif message_type == "unit_updated":
        await manager.broadcast_to_room(room_id, {
            "type": "unit_updated",
            "unit_id": data.get("unit_id"),
            "updates": data.get("updates"),
            "updated_by": username
        })

    elif message_type == "unit_deleted":
        await manager.broadcast_to_room(room_id, {
            "type": "unit_deleted",
            "unit_id": data.get("unit_id"),
            "unit_name": data.get("unit_name"),
            "deleted_by": username
        })

    elif message_type == "active_map_changed":
        await manager.broadcast_to_room(room_id, {
            "type": "active_map_changed",
            "map_id": data.get("map_id"),
            "map_name": data.get("map_name"),
            "changed_by": username
        })
