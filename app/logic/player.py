from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import insert, select, update
from sqlalchemy.orm import selectinload


from app.logic.uow import SessionUow
from app.model.models import LevelReward, PlayerLevel


@dataclass(eq=False)
class PlayerLevelService:
    uow: SessionUow
    
    async def add_player_level(self, player_id, level_reward_id: UUID):
        async with self.uow as session:
            async with session.begin():
                stmt_player_level = insert(PlayerLevel).values(level_reward_id=level_reward_id, player_id=player_id).returning(PlayerLevel.id)
                player_level_result = await session.execute(stmt_player_level)
                await session.commit()
                return player_level_result.scalar_one()
    
    async def completed_player_lavel(self, player_level_id: UUID, scope: int):
        async with self.uow as session:
            async with session.begin():
                stmt = (
                    update(PlayerLevel)
                    .filter_by(id=player_level_id)
                    .values(
                        completed_at=datetime.now(tz=timezone.utc),
                        is_completed=True,
                        score=scope
                    )
                )
                await session.execute(stmt)
                await session.commit()
                
                
    async def get_player_level(self, limit: int = 1000, offset: int = 0):
        async with self.uow as session:
            async with session.begin():
                stmt = (
                select(PlayerLevel)
                .options(
                    selectinload(PlayerLevel.level_reward)
                        .selectinload(LevelReward.prizes),
                    selectinload(PlayerLevel.level_reward)
                        .selectinload(LevelReward.boosts),
                    selectinload(PlayerLevel.level_reward)
                        .joinedload(LevelReward.level),
                    selectinload(PlayerLevel.player)
                )
                .offset(offset)
                .limit(limit)
            )
                result = await session.execute(stmt)
                return result.scalars().all()

