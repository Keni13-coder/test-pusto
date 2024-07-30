from datetime import datetime
from app.logic.level import LevelRewardService
from app.model.models import Level, Boost, Prize
from app.model.enums import BoostType

class TestLevelRewardService:
    
    async def test_add_level(self, get_session):
        level = Level(title='test_title', order=0)
        reward = LevelRewardService(uow=get_session, level=level)
        boost = Boost(type=BoostType.type, duration=datetime.now())
        prize = Prize(title='prize')
        assert await reward.add_level(boost=boost, prize=prize)