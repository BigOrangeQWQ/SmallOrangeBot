players = dict[str, dict[str, int]]

from . import _cache_player_, plugin_config
from json import dump
from re import findall

def get_card(user_id: int) -> dict[str,int]:
    """获取车卡数据

    Args:
        user_id (int): QQ号

    Returns:
        dict[str,int]: 属性及数据
    """
    return _cache_player_.get(str(user_id), {})
    
def set_card(user_id: int, attr: str):
    """
    解析并储存玩家数据

    Args:
        user_id (int): QQ号
        attr (str): 未处理的属性字符串  
    """
    find: list[tuple[str,int]] = findall(r"(\D{2,4})(\d{1,3})", attr)
    attrs: dict[str, int] = {}
    for i in find:
        a, b = i
        attrs[str(a)] = int(b)
    _cache_player_[str(user_id)] = attrs
    
def save_card_json():
    """
    储存玩家数据
    """
    with open(plugin_config.card_file,'w',encoding='utf-8') as f:
        dump(_cache_player_, open(plugin_config.card_file,'w',encoding='utf-8'))

def save_card_sqlite():
    ...
