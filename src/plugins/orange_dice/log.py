from os.path import exists
from json import load, dump
from typing import TypedDict
from nonebot import get_driver

from .config import Config

plugin_config = Config.parse_obj(get_driver().config)

LogType = TypedDict('Log', {'msg': list[str], 'log': bool})
class Log:
    
    def __init__(self) -> None:
        self._cache_log_: dict[str, LogType] = {}
        """
        {"group_id": {'msgs': ['msg'], 'log': bool}}

        (nickname: msg)
        nickname: msg
        """
    
    def save_json(self):
        with open(plugin_config.log_file, 'w', encoding='utf-8') as f:
            dump(self._cache_log_, f)
        
    def read_json(self):
        if exists(plugin_config.log_file):
            with open(plugin_config.log_file, 'r', encoding='utf-8') as f:
                self._cache_log_ = load(f)
        else:
            self.save_json()
        
    def is_loging(self, group_id: int) -> bool:
        """检测某群是否正在记录日志

        Args:
            group_id (int): 群号

        Returns:
            bool: 记录中返回True
        """
        return self._cache_log_[str(group_id)].get('log',)
    
    def log_on(self, group_id: int):
        """开启某群

        Args:
            group_id (int): _description_
        """
        ...
