from json import load
from nonebot import get_driver
from nonebot.plugin import on_startswith, on_message
from nonebot.adapters.onebot.v11 import GroupMessageEvent

from plugins.dico.card import Card


from .config import Config

driver = get_driver()
roll_player = on_startswith(".ra", priority=4) #人物技能roll点
roll = on_startswith(".r", priority=5) #roll点
log = on_startswith(".log", priority=5) #日志相关指令
log_msg = on_message()
card = on_startswith(".st", priority=5) #造成人物卡
plugin_config = Config.parse_obj(driver.config)

# _cache_player_: dict[str, dict[str, int]] = {}
# """
# {"user_id": {"san": 50 ...}}
# """

# _cache_log_: dict[str, list[str]] = {}
# """
# {"group_id": ['message']}

# (nickname: msg)
# nickname: msg
# """
cards = Card()

@driver.on_startup
async def load_cache():
    """
    加载缓存文件
    """
    if plugin_config.save_type == 'file':
        cards.read_json()
    if plugin_config.save_type == 'sqlite':
        #TODO: need sqlite loading cache
        ...
        
@roll.handle()
async def roll_handle(event: GroupMessageEvent):
    ...


