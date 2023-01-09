from json import load
from nonebot import get_driver
from nonebot.plugin import on_startswith, on_message
from nonebot.adapters.onebot.v11 import GroupMessageEvent

from .card import Card
from .log import Log
from .config import Config

help = on_startswith(".help")           #获取插件帮助
roll = on_startswith(".r", priority=5)  #roll点
log  = on_startswith(".log", priority=5) #日志相关指令
log_msg = on_message()                  #记录日志
card = on_startswith(".st", priority=5) #造成人物卡
roll_card = on_startswith(".ra", priority=4) #人物技能roll点

driver = get_driver()
plugin_config = Config.parse_obj(driver.config)

cards = Card()
logs = Log()

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


