import pygame as _pygame
import typing as _typing
from enum import IntEnum as _IntEnum

EVERYONE_RECEIVER: _typing.Final = "constants_everyone"  #

NOWMAP = 1  # 当前所在地图的编号

# event code
user_event_start: _typing.Final = _pygame.USEREVENT # 32866？ 32869

def get_unused_event_code() -> int:
    """
    获取一个尚未使用的事件代码

    :return:
    int
        尚未使用的事件代码
    """
    global user_event_start
    user_event_start += 1
    return user_event_start

class EventCode(_IntEnum): # members are all ints
    UPDATE = get_unused_event_code()  # 通知监听者已经过去了一个游戏刻
    DRAW = get_unused_event_code()  # 绘制事件
    KILL = get_unused_event_code()  # 删除监听者事件（从群组等中删除监听者）
    # 实质上三者功能相同 只是做了可读化命名


# event body

class UpdateEventBody(_typing.TypedDict):
    """
    UPDATE事件body模板
    """

    second: float  # 距离上一次游戏刻发生经过的时间（秒）

class DrawEventBody(_typing.TypedDict):
    """
    DRAW事件body模板
    """

    window: _pygame.Surface  # 画布
    camera: tuple[int, int]  # 镜头坐标（/负偏移量）


class KillEventBody(_typing.TypedDict):
    """
    KILL事件body模板
    """

    suicide: str  # 被删除监听者的UUID

abilityCount: int = 0  # 能力总数
ability: list = [
    ""
]  #能力表 TODO: 想名字



someDefine = {
    "渲染事件": 114514,
    "更新事件": 12701300,
}