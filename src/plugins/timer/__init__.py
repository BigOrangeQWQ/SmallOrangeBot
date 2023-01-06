

from random import sample
from typing import Dict, Literal

import mcstatus
from nonebot.adapters.onebot.v11.event import MessageEvent
from nonebot.adapters.onebot.v11.message import Message
from nonebot.plugin import PluginMetadata, on_command

from nonebot.matcher import Matcher
from nonebot.adapters import Bot
from nonebot.plugin import require
from nonebot.params import ArgStr
from nonebot.typing import T_State

require('nonebot_plugin_apscheduler')
from nonebot_plugin_apscheduler import scheduler


__player_list__file_ = "player_list.json"
"""
{'teamA': ['A','B','C','D','F']}
"""
__player_data_file__ = "player_data.json"
"""
{'team':{'teamA': time, 'teamB': time}, 'player': {'playerA': time}}
"""

__time_data__: Dict[Literal['team','player'], Dict[str, int]] = {}
__server_ip__ = ''


async def get_player_list() -> list[str]:
    server = await mcstatus.JavaServer.async_lookup(__server_ip__)
    sample = server.status().players.sample
    if sample is not None:
        return [i.name for i in sample]
    else:
        return []
    
@scheduler.scheduled_job("cron", second='*')
async def add():
    # __sign_data__.clear()
    player_list = await get_player_list()
    for i in player_list:
        pass

timelist = on_command(cmd='timelist', aliases={'时间排行榜'}, priority=5)
