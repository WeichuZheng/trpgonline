import asyncio
from backend.database import engine, Base
from backend.models.models import User, Module, Resource, Room, RoomParticipant, RoomResource, CharacterCard, GameLog, Map, MapUnit, CharacterTemplate

async def init():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print('Database tables created successfully')

asyncio.run(init())
