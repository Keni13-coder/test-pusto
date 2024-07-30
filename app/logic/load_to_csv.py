import pandas as pd

from app.logic.player import PlayerLevelService
from app.model.models import PlayerLevel

async def save_player_levels_to_csv(player_service: PlayerLevelService, limit: int = 1000):
    offset = 0
    while True:
        data = []
        print(offset)
        player_levels = await player_service.get_player_level(limit, offset)
        if not player_levels:
            break

        for pl in player_levels:
            level_reward = pl.level_reward
            if not level_reward:
                continue
            pl: PlayerLevel
            data.append({
                'player_id': pl.player_id,
                'level_reward_id': pl.level_reward_id,
                'is_completed': pl.is_completed,
                'prize_title': [prize.title for prize in pl.level_reward.prizes] if pl.level_reward.prizes else None,
                'boost_type': [boost.type for boost in pl.level_reward.boosts] if pl.level_reward.boosts else None,
                'level_title': pl.level_reward.level.title if pl.level_reward.level else None,
            })

        df = pd.DataFrame(data)
        df.to_csv('player_level.csv', mode='a', header=not bool(offset), index=False)
        offset += limit