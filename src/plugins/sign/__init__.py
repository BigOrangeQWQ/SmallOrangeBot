
from typing import Dict

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

__plugin_meta__ = PluginMetadata(
    name="OrangeSign",
    description="一个普通的签到插件\n-> 特别致谢jinser[jetjinser]",
    usage="""
/jrrp[今日人品] 查询今日人品
/jrrpchange[人品变动] 近五次人品波动
/jrrptop[人品排行] 人品排行榜
""")

__sign_data__: Dict[int, int] = {}


@scheduler.scheduled_job("cron", day='*')
async def clear():
    __sign_data__.clear()


sign = on_command(cmd='jrrp', aliases={'今日人品'}, priority=5)

sign_top = on_command(cmd=('jrrp', 'top'), aliases={
    '今日人品排行', 'jrrptop', 'jrtop'}, priority=5)

sign_change = on_command(cmd=('jrrp', 'change'), aliases={
    '人品变动', 'jrrpchange', 'jrchange'}, priority=5)


@sign.handle()
async def sign_handle(matcher: Matcher, bot: Bot, event: MessageEvent):
    data = __sign_data__
    user_id = event.user_id
    if data.get(user_id):
        await sign.finish(f"你今日已打卡，人品值为：{data[user_id]}")
        
def handle_function(key):
    pass
    
@sign.got('key', prompt='请输入你的key')
async def handle(matcher: Matcher, bot: Bot, event: MessageEvent, state: T_State, key: str = ArgStr()):
    if key == 'end': #主动结束 或增加判断结束
        await sign.finish("完成全部事件")
    if key not in state['last']: #检测key是否有上次处理结果的一个选项
        await sign.reject("输入错误，请重新输入")
    else:
        result = handle_function(key) #业务函数 handle_function可sign.finish()
        state['last'] = result #将这次处理结果存入state
        await sign.reject(result) #倒回重新输入
        
    
from nonebot.adapters.onebot.v11.event import GroupMessageEvent
from random import random

word = on_command("s")


@word.handle()
async def _(event: GroupMessageEvent):
    if random() > 0.9:
        await word.finish("qwq")