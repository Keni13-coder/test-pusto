from datetime import datetime
from uuid import UUID, uuid4
import pytest
from sqlalchemy import insert
from app.logic.uow import SessionUow
from app.logic.level import LevelRewardService
from app.model.models import Level, Boost, Prize, Player, PlayerPoint
from app.model.enums import BoostType

@pytest.fixture(scope='session')
async def get_session():
    return SessionUow()

@pytest.fixture(scope='session')
async def create_level(get_session) -> UUID:
    level = Level(title='title', order=1)
    reward = LevelRewardService(uow=get_session, level=level)
    boost = Boost(type=BoostType.type, duration=datetime.now())
    prize = Prize(title='title')
    return await reward.add_level(boost=boost, prize=prize)


@pytest.fixture(scope='session')
async def create_player(get_session: SessionUow):
    # игрока тоже созаем агрегируя PlayerPoint, создаем вместе, но нам для задаче не к чему реализовывать сейчас   
    async with get_session as session:
        async with session.begin():
            stmt_player_point = insert(PlayerPoint).values(
                last_entry_date=datetime.now(),
                point_id=uuid4(),
                sum=0,
                ).returning(PlayerPoint.id)
            
            player_point_result = await session.execute(stmt_player_point)
            player_point_id = player_point_result.scalar_one()
            
            stmt_player = insert(Player).values(
                name='name',
                player_point_id=player_point_id,
            ).returning(Player)
            player_result = await session.execute(stmt_player)
            return player_result.scalar_one()