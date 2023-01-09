from nonebot import get_driver
from nonebot.plugin import on_startswith, on_message
from nonebot.adapters.onebot.v11 import GroupMessageEvent
from nonebot.matcher import Matcher
from re import search


from .card import Card
from .log import Log
from .config import Config
from .roll import RA, RD

help = on_startswith(".help")  # 获取插件帮助
roll = on_startswith(".r", priority=5)  # roll点
log = on_startswith(".log", priority=5)  # 日志相关指令
log_msg = on_message()  # 记录日志
card = on_startswith(".st", priority=5)  # 造成人物卡
roll_card = on_startswith(".ra", priority=4)  # 人物技能roll点

driver = get_driver()
plugin_config = Config.parse_obj(driver.config)
cards = Card()
logs = Log()


@driver.on_startup
async def load_cache():
    """
    加载缓存文件
    """
    if plugin_config.save_type.lower() == 'file':
        cards.read_json()
        logs.read_json()
    if plugin_config.save_type.lower() == 'sqlite':
        # TODO:
        ...


@roll.handle()
async def roll_handle(matcher: Matcher, event: GroupMessageEvent):
    """
    处理骰点检定

    Example:
        [in].rd测试
        RD('测试','PlayerName','1D100')
        [out]进行了[测试]检定1D100=result

        [in].r
        RD('PlayerName',None, '')
        [out]进行了检定1D100=result

        [in].rd测试50
        [error out]进行了检定1D100=0
    """
    msg = str(event.message)[2:].replace(' ', '').lower()
    name = event.sender.card if event.sender.card else event.sender.nickname
    matches = search(r"[\u4e00-\u9fa5]{1,100}", msg)
    if matches is None:
        await matcher.finish(RD(name, msg))
    else:
        await matcher.finish(RD(name, msg.replace(matches.group(), ''), matches.group()))

@roll_card.handle()
async def roll_card_handle(matcher: Matcher, event: GroupMessageEvent):
    """处理玩家属性骰点

    Example:
        [in].ra测试
        RA('name', 110, '测试')
        [out]name[attr]进行了[测试]检定1D100=result [msg]

        [in].ra测试100
        RA('name', 110, '测试', 100)
        [out]name[100]进行了[测试]检定1D100=result [msg]
    """
    user_id = event.user_id
    card = cards.get_card(user_id)
    msg = str(event.message)[3:].replace(' ','').lower()
    name = event.sender.card if event.sender.card else event.sender.nickname
    #正则匹配
    matches = search(r"[\u4e00-\u9fa5]{1,100}", msg) #搜索 测试
    matches_have_num = search(r"[\u4e00-\u9fa5]{1,100}\d{1,3}", msg) #搜索 测试100
    
    if matches is None:
        await matcher.finish('没有找到需要检定的属性')
    if matches_have_num is not None:
        result = RA(name, user_id, matches.group(), int(matches_have_num.group().replace(matches.group(),'')), card)
    else:
        result = RA(name, user_id, matches.group() , None, card)
    await matcher.finish(result)
