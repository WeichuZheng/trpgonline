# TRPG Online - WebSocket 处理
import asyncio
from typing import Dict, Set, List
from fastapi import WebSocket, WebSocketDisconnect
from sqlalchemy import select

from backend.database import AsyncSessionLocal
from backend.models.models import RoomParticipant, GameLog, Room
from backend.auth import decode_token


def decode_ws_token(token: str):
    """Decode JWT token for WebSocket authentication. Returns (user_id, username) or None."""
    try:
        payload = decode_token(token)
        user_id = payload.get("user_id")
        username = payload.get("sub")
        if user_id is None or username is None:
            return None
        return int(user_id), username
    except Exception:
        return None


class ConnectionManager:
    """WebSocket 连接管理器"""

    def __init__(self):
        # room_id -> set of websockets
        self.active_connections: Dict[int, Set[WebSocket]] = {}
        # websocket -> room_id mapping
        self.socket_rooms: Dict[WebSocket, int] = {}
        # websocket -> (user_id, username, role) mapping
        self.socket_users: Dict[WebSocket, tuple] = {}

    async def connect(self, websocket: WebSocket, room_id: int, user_id: int, username: str, role: str):
        """WebSocket 连接，返回是否是该用户在此房间的第一个连接"""
        is_first = not self._has_user_in_room(room_id, user_id)

        await websocket.accept()
        if room_id not in self.active_connections:
            self.active_connections[room_id] = set()
        self.active_connections[room_id].add(websocket)
        self.socket_rooms[websocket] = room_id
        self.socket_users[websocket] = (user_id, username, role)

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

    def is_gm(self, room_id: int, user_id: int) -> bool:
        """检查用户在指定房间是否是 GM"""
        for ws in self.active_connections.get(room_id, set()):
            info = self.socket_users.get(ws)
            if info and info[0] == user_id:
                return info[2] == "gm"
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
                    users.append({"user_id": info[0], "username": info[1], "role": info[2]})
        return users

    async def broadcast_to_room(self, room_id: int, message: dict):
        """向房间内所有人广播消息"""
        if room_id in self.active_connections:
            dead = []
            for connection in self.active_connections[room_id]:
                try:
                    await connection.send_json(message)
                except Exception:
                    dead.append(connection)
            # Clean up dead connections
            for conn in dead:
                self.active_connections[room_id].discard(conn)
                self.socket_rooms.pop(conn, None)
                self.socket_users.pop(conn, None)

    async def broadcast_online_users(self, room_id: int):
        """广播在线用户列表"""
        users = self.get_online_users(room_id)
        await self.broadcast_to_room(room_id, {
            "type": "online_users",
            "users": users
        })


async def _heartbeat_loop():
    """每30秒向所有连接发送ping，保持连接活跃并清理死连接"""
    while True:
        await asyncio.sleep(30)
        dead = []
        for ws in list(manager.socket_rooms.keys()):
            try:
                await ws.send_json({"type": "ping"})
            except Exception:
                dead.append(ws)
        for ws in dead:
            room_id = manager.socket_rooms.get(ws)
            info = manager.socket_users.get(ws)
            if room_id and info:
                _handle_disconnect(ws, room_id, info[0], info[1])


# 全局连接管理器
manager = ConnectionManager()

# GM-only message types
GM_ONLY_MESSAGES = {
    "unit_created", "unit_deleted", "hp_change", "resource_visible",
    "active_map_changed", "character_created", "character_deleted",
    "block_toggled", "unit_updated",
}


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
    """WebSocket 端点 — 通过 JWT token 认证"""
    # C1 fix: Authenticate via JWT token instead of trusting client-supplied user_id
    token = websocket.query_params.get("token")
    if not token:
        await websocket.close(code=4001, reason="缺少认证 token")
        return

    user_info = decode_ws_token(token)
    if not user_info:
        await websocket.close(code=4001, reason="无效的认证 token")
        return

    user_id, username = user_info

    # Verify user is a room participant and get their role
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
        role = participant.role

    # 建立连接，判断是否是该用户的第一个连接
    is_first = await manager.connect(websocket, room_id, user_id, username, role)

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
            await handle_websocket_message(room_id, user_id, username, role, data)

    except WebSocketDisconnect:
        _handle_disconnect(websocket, room_id, user_id, username)
    except Exception:
        # M1 fix: Handle non-WebSocketDisconnect exceptions to avoid connection leak
        _handle_disconnect(websocket, room_id, user_id, username)


def _handle_disconnect(websocket, room_id, user_id, username):
    """Common disconnect logic for both WebSocketDisconnect and other exceptions"""
    room_id, user_id, username, is_last = manager.disconnect(websocket)
    if room_id and is_last:
        import asyncio
        asyncio.ensure_future(_write_log(room_id, user_id, f"{username} 离开了房间"))
        asyncio.ensure_future(manager.broadcast_to_room(room_id, {
            "type": "user_left",
            "user_id": user_id,
            "username": username,
            "message": f"{username} 离开了房间"
        }))
    if room_id:
        asyncio.ensure_future(manager.broadcast_online_users(room_id))


async def handle_websocket_message(room_id: int, user_id: int, username: str, role: str, data: dict):
    """处理 WebSocket 消息 — C2 fix: check role for GM-only operations"""
    message_type = data.get("type")

    # C2 fix: Reject GM-only messages from non-GM users
    if message_type in GM_ONLY_MESSAGES and role != "gm":
        return  # Silently ignore unauthorized messages

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

    elif message_type == "character_created":
        await manager.broadcast_to_room(room_id, {
            "type": "character_created",
            "character": data.get("character"),
            "created_by": username
        })

    elif message_type == "character_deleted":
        await manager.broadcast_to_room(room_id, {
            "type": "character_deleted",
            "character_id": data.get("character_id"),
            "character_name": data.get("character_name"),
            "deleted_by": username
        })

    elif message_type == "block_toggled":
        await manager.broadcast_to_room(room_id, {
            "type": "block_toggled",
            "resource_id": data.get("resource_id"),
            "block_index": data.get("block_index"),
            "is_revealed": data.get("is_revealed"),
            "changed_by": username
        })
