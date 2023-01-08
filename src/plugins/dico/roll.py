"""
骰点相关，使用onedice协议
"""
from typing import Optional
import onedice

from .card import get_card

def random(statement: str = '1d100') -> int:
    """
    使用onedice进行骰点

    Args:
        statement (str, optional): [onedice]公式. Defaults to '1d100'.

    Returns:
        int: 骰点后结果
    """
    result = onedice.RD(statement)
    result.roll()
    if result.resError is not None:
        return 0
    return result.resInt #type:ignore

def RD(player_name: Optional[str], item: Optional[str], statement: str = '1d100') -> str:
    """
    进行骰点并返回骰点消息
    
    Args:
        player_name: Optional[str] 玩家名字
        item: Optional[str] 检定技能
        statement: str = '1d100' [onedice]骰子检定公式
        
    Return:
        str 检定后信息
        
    Example:
        [in].rd测试 
        fun('测试','PlayerName','1D100')
        [out]进行了[测试]检定1D100=result
        
        [in].r
        fun('PlayerName')
        [out]进行了检定1D100=result
    """
    result = random(statement)
    if item != None:
        return f"{player_name}进行了[{item}]检定{statement.upper()}={result}"
    return f"{player_name}进行了检定{statement.upper()}={result}"

def RA(player_name: str, user_id: int, item: str, attr: Optional[int]) -> str:
    """进行检定并返回骰点信息

    Args:
        player_name (str): 玩家名字
        user_id (int): QQ号
        item (str): 检定技能
        attr (int): 技能值

    Returns:
        str: 检定后信息
    
    Example:
        [in].ra测试
        fun('name', 110, '测试')
        [out]name[attr]进行了[测试]检定1D100=result [msg]
        
        [in].ra测试100
        fun('name', 110, '测试', 100)
        [out]name[100]进行了[测试]检定1D100=result [msg]
    """
    attrs: int = get_card(user_id).get(item, 0) 
    if attr is not None:
        attrs = attr
    result: int = random()
    msg = '失败~'
    if(result > 95):
        msg = "大失败~"
    if(result < attrs):
        msg = '成功！'
    if(result < attrs*0.5):
        msg = '困难成功！'
    if(result < attrs*0.2):
        msg = "极限成功！"
    if(result < 5):
        msg = "大成功！！"
    if(result == 0):
        return f'{player_name}没有这个属性'
    return f"{player_name}[{attrs}]进行了[{item}]检定1D100={result} {msg}"