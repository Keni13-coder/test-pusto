from uuid import UUID

from app.model.models import Player
from app.logic.player import PlayerLevelService




class TestPlayerLevelService:
    
    id_playerlevel = {'id': None}
    
    async def test_add_player_level(self, get_session, create_player: Player, create_level: UUID):
       player_level_service = PlayerLevelService(uow=get_session)
       result_id = await player_level_service.add_player_level(level_reward_id=create_level, player_id=create_player.id)
       assert result_id
       
       self.id_playerlevel['id'] = result_id

        
    async def test_completed_player_lavel(self, get_session):
        assert self.id_playerlevel['id']
        player_level_service = PlayerLevelService(uow=get_session)
        assert not await player_level_service.completed_player_lavel(player_level_id=self.id_playerlevel['id'], scope=1)
    
    async def test_get_player_level(self, get_session):
        player_level_service = PlayerLevelService(uow=get_session)
        assert await player_level_service.get_player_level()