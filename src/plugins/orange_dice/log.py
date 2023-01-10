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
        """
        使用json文件储存数据
        """
        with open(plugin_config.log_file, 'w', encoding='utf-8') as f:
            dump(self._cache_log_, f)
        
    def read_json(self):
        """
        读取json文件数据
        若文件不存在则创建
        """
        if exists(plugin_config.log_file):
            with open(plugin_config.log_file, 'r', encoding='utf-8') as f:
                self._cache_log_ = load(f)
        else:
            self.save_json()
        
    def is_loging(self, group_id: int) -> bool:
        """
        检测某群是否正在记录日志

        Args:
            group_id (int): 群号

        Returns:
            bool: 记录中返回True
        """
        return self._cache_log_[str(group_id)].get('log',)
    
    def log_on(self, group_id: int):
        """
        开启某群的日志记录功能

        Args:
            group_id (int): 群号
        """
        self._cache_log_[str(group_id)]['log'] = True
    
    def log_off(self, group_id: int):
        """
        关闭某群的日志记录功能

        Args:
            group_id (int): 群号
        """
        self._cache_log_[str(group_id)]['log'] = False
    
    def log_add_message(self, group_id: int , message: str):
        """
        为日志增加消息

        Args:
            message (str): 需增加的消息
        """
        self._cache_log_[str(group_id)]['msg'].append(message)
