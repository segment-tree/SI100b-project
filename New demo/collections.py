"""
Classes
---
EventLike
    事件
ListenerLike
    监听器
GroupLike
    监听组
Core
    核心，管理事件队列, 窗口, 刻, pygame api


"""

import typing as _typing
import sys as _sys

import pygame as _pygame

from . import constants as _const
from . import tools as _tools

class EventLike:
    """
    事件类

    Attributes
    ---
    code : int
        事件代码
    sender: typing.Optional[str]
        发送者（记录UUID） (str或None)
    receiver: typing.Set[str]
        接收者（记录UUID） (str集合)
    prior: int
        优先级 （越小越高）
    body: typing.Dict[str, typing.Any]
        事件附加信息 (键为str 值为任意)

    Attribute ‘prior’
    ---
    10
        默认优先级
    20
        tick事件优先级
    30
        渲染事件优先级
    """

    # Attributes
    code: int
    sender: str
    receiver: _typing.Set[str]
    prior: int
    body: _typing.Dict[str, _typing.Any]

    key: _typing.Optional[int]

    @classmethod
    def from_pygame_event(cls, event: _pygame.event.Event) -> "EventLike":
        """
        将pygame.event.Event转换为EventLike
        使用object.__dict__继承pygame事件

        Parameters
        ---
        event: pygame.event.Event
            pygame事件
        """
        a = cls(event.type, sender="pygame", prior=10) # 利用pygame事件创建EventLike实例
        a.__dict__.update(event.__dict__) # 继承属性 得到一个字典
        return a

    @classmethod
    def update_event(cls, second: float) -> "EventLike":
        """
        创建UPDATE事件

        Parameters:
        ---
        ms: float
            距离上次UPDATE事件经过的时间
        """
        body: _const.UpdateEventBody = {"second": second}
        return cls(_const.Event)

