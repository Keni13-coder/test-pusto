from app.logic.player import PlayerLevelService
from app.logic.load_to_csv import save_player_levels_to_csv

async def test_save_player_levels_to_csv(get_session):
    player_level_service = PlayerLevelService(uow=get_session)
    await save_player_levels_to_csv(player_service=player_level_service)