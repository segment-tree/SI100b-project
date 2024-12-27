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
    eventType: str

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
        body.type = "UPDATE"
        return cls(_const.EventCode.UPDATE, body=body, prior=20)

    @classmethod
    def kill_event(cls, uuid: str) -> "EventLike":
        """
        创建KILL事件

        ---
        :param uuid: str
            被删除监听者的UUID
        :return: object
            一个初始化好的EventLike对象
        """
        body: _const.KillEventBody = {"suicide": uuid}
        body.type = "KILL"
        return cls(_const.EventCode.KILL, body=body, sender=uuid, prior=0)

    @classmethod
    def draw_event(
            cls,
            window: _pygame.Surface,
            *,
            receivers: _typing.Set[str] = None,
            camera: _typing.Tuple[int, int] = (0, 0)
    ):
        """

        :param window: pygame.Surface
            一般是pygame.display.set_mode(...)返回的Surface对象, 占满整个窗口的画布
        :param receivers: set[str], typing.Optional, default = {EVERYONE_RECEIVER}
            事件接收者, 默认是任何Listener
        :param camera: tuple[int, int], default = (0, 0)
            相机位置, 绘制偏移量
        :return: object
            一个初始化好的EventLike对象
        """
        body: _const.DrawEventBody = {"window": window, "camera": camera}
        body.type = "DRAW"
        return cls(_const.EventCode.DRAW, body=body, prior=300, receivers=receivers)

    def __init__(
        self,
        EventCode: int,
        *,
        prior: int = 10,
        sender: str = "",
        receivers: _typing.Set[str] = None,
        body: _typing.Optional[_typing.Dict[str, _typing.Any]] = None,
    ) -> None:
        """
        :param EventCode:
            事件代码 独一无二的
        :param prior:
            优先级
        :param sender:
            事件发送者（UUID）
        :param receivers:
            事件目标接收者（UUID集合） 默认参数提供一个空集合，接收者添加入其中
        :param body:
            事件附加信息
        """
        assert isinstance(EventCode, int)
        assert isinstance(prior, int)
        assert isinstance(sender, str)
        assert isinstance(receivers, (set, None.__class__))
        assert isinstance(body, (dict, None.__class__))
        self.EventCode: int = EventCode
        self.EventPrior: int = prior
        self.EventSender: str = sender
        self.EventReceivers: _typing.Set[str] = (
                receivers if receivers is not None else {_const.EVERYONE_RECEIVER}
        )

    def __lt__(self, other: "EventLike") -> bool:
        """
        运算符重载: `<`, 根据`prior`进行比较。
        """
        return self.EventPrior < other.EventPrior
    def __gt__(self, other: "EventLike") -> bool:
        """
        运算符重载: `>`, 根据`prior`进行比较。
        """
        return self.EventPrior > other.EventPrior


PostEventAPILike: _typing.TypeAlias = _typing.Callable[
    [EventLike], None
]  # 事件发布函数类型注释, 一般使用`Core`的`add_event`函数
class ListenerLike:
    """
    监听者

    1. ‘self.listen(event)’函数监听事件
        (1) 首先检查事件类型和接收者集(`EventLike.code`, `EventLike.receivers`)
        (2) 根据事件类型`EventLike.code`, 将事件传递到对应的被`listening`(basetools模块提供)装饰过的函数。
    2. `self.post(event)`函数可以发布事件 (发布位置取决初始化时传入的`post_api`, 推荐使用`Core().add_event`作为`post_api`)

    :param listen_receivers: set[str]
    """
    __post_api: _typing.Optional[PostEventAPILike]
    __listen_receivers: _typing.Set[str]
    __listen_methods: _typing.Dict[
        int, _typing.Set[_typing.Callable[[EventLike], None]]
    ]

    def __init__(
        self,
        *,
        listen_receivers: _typing.Optional[_typing.Set[str]],
        post_api: _typing.Optional[PostEventAPILike] = None,
    ) -> None:
        """
        :param listen_receivers:
            监听者接收者集合，默认有自己和EVERYONE_RECEIVER
        :param post_api:
            事件发布函数，一般使用Core类的add_event
        """
        self.__post_api: _typing.Optional[PostEventAPILike] = post_api
        self.__listen_receivers: _typing.Set[str] = (
            listen_receivers | {_const.EVERYONE_RECEIVER, self.uuid}
            if listen_receivers is not None
            else {_const.EVERYONE_RECEIVER, self.uuid}
        )
        self.__listen_methods: _typing.Dict[
            int, _typing.Set[_typing.Callable[[EventLike], None]]
        ] = _tools.find_listening_methods(self)
