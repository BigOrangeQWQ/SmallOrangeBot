"""
骰点相关，使用onedice协议
"""
from typing import Optional
import onedice

def random(statement: str = '1d100') -> int:
    """
    使用onedice进行骰点

    Args:
        statement (str, optional): onedice公式. Defaults to '1d100'.

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
        statement: str = '1d100' onedice骰子检定公式
        
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