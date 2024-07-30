from dataclasses import dataclass

from sqlalchemy import insert

from app.logic.uow import SessionUow
from app.model.models import Level, LevelReward, Prize, Boost


@dataclass(eq=False)
class LevelRewardService:
    level: Level
    uow: SessionUow

    async def add_level(self, prize: Prize, boost: Boost) -> None:
        async with self.uow as session:
            async with session.begin():
                level = Level(title=self.level.title, order=self.level.order)
                session.add(level)
                await session.flush()
                
                prize = Prize(title=prize.title, level_reward_id=None)
                session.add(prize)
                await session.flush()
                

                boost = Boost(type=boost.type, duration=boost.duration, level_reward_id=None)
                session.add(boost)
                await session.flush()

                level_reward = LevelReward(level_id=level.id)
                session.add(level_reward)
                await session.flush()
                
                prize.level_reward_id = level_reward.id
                boost.level_reward_id = level_reward.id


                session.add(prize)
                session.add(boost)
                
                await session.commit() 
                return level_reward.id
