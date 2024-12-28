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
        second: float
            距离上次UPDATE事件经过的时间(s)
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
]  # 事件发布函数类型注释, 一般使用`Core`的`add_event`函数 接受EventLike类型的形参 返回None
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

    @property
    def listen_receivers(self) -> _typing.Set[str]:
        return self.__listen_receivers
    @listen_receivers.setter
    def listen_receivers(self, listen_receivers: _typing.Set[str]):
        self.__listen_receivers = listen_receivers

    @property
    def listen_codes(self) -> _typing.Set[int]:
        """
        获取监听者监听的事件代码集合
        :return:
            所有被tools.listening装饰过的函数中包含的事件代码
        """
        return set(self.__listen_methods)
    @listen_codes.setter
    def listen_codes(self, listen_codes: _typing.Set[int]):
        raise AttributeError("Setting attribute `listen_codes` is denied.")

    @property
    def post_api(self) -> _typing.Optional[PostEventAPILike]:
        return self.__post_api
    @post_api.setter
    def post_api(self, post_api: _typing.Optional[PostEventAPILike]):
        self.__post_api = post_api

    @property
    def uuid(self) -> str:
        """
        监听者的UUID
        使用对象实例的内存地址作为UUID
        :return:
        """
        return str(id(self))

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

    def post(self, event: EventLike) -> None:
        """
        通过post_api发布事件
        :param event: EventLike
            待发布事件
        :raise AttributeError:
            如果没有设置post_api，则抛出
        """
        if self.__post_api is None:
            raise AttributeError("Post API is not set.")
        self.__post_api(event)  # __post_api是EventLike对象的实例

    def listen(self, event: EventLike) -> None:
        """
        根据事件code，分配至对应的被listening装饰过的函数处理 iff 事件接收者在监听者的监听接收者集合中
        :param event: EventLike
            待处理事件
        """
        listen_receivers = self.__listen_receivers
        if not event.receiver & listen_receivers:  # 等价于 event.receiver.isdisjoint(listen_receivers)
            return
        listen_code_methods = self.__listen_methods
        if not event.code in listen_code_methods:
            return
        for method_ in listen_code_methods[event.code]:
            method_(event)
        """
        这一段的思路是：listening函数
        """

class GroupLike(ListenerLike):
    """
    Listener群组 群组内共用post_api和receivers
    :param listeners: _tools.DoubleKeyBarrel[ListenerLike]
        群组内成员
    :param listen_receivers: set[str]
        群组接收者集合
    :param listen_codes: set[int]
        监听事件类型, 是群组监听类型与所有成员监听类型的并集
    :method
    """
    __listeners: _tools.DoubleKeyBarrel[ListenerLike]  # 双键桶存储的Listener实例

    # 双键桶键1是listen_code 键2是receivers' UUID
    @property
    def listen_codes(self) -> _typing.Set[int]:
        """
        监听事件类型, 是群组监听类型与所有成员监听类型的并集 (只读)
        :return:
        """
        return self.__listeners.keys1 | super().listen_codes

    @listen_codes.setter
    def listen_codes(self, listen_codes: _typing.Set[int]):
        raise AttributeError("Setting attribute `listen_codes` is denied.")

    @property
    def listen_receivers(self) -> _typing.Set[str]:
        """
        监听者接收者集合 是群组接收者集合与所有成员接收者集合的并集 (只读)
        :return:
        """
        return self.__listeners.keys2 | super().listen_receivers

    @listen_receivers.setter
    def listen_receivers(self, listen_receivers: _typing.Set[str]):
        raise AttributeError("Setting attribute `listen_receivers` is denied.")

    @property
    def listeners(self) -> _typing.Set[ListenerLike]:
        """
        :return: typing.Set[ListenerLike]
            群组中所有成员
        """
        return set(self.__listeners)

    @listeners.setter
    def listeners(self, listeners: _tools.DoubleKeyBarrel[ListenerLike]):
        raise AttributeError("Setting attribute `listeners` is denied. Please use other methods.")

    def __init__(
        self,
        *,
        post_api: _typing.Optional[PostEventAPILike] = None,
        listen_receivers: _typing.Optional[_typing.Set[str]] = None,
    ):
        """

        :param post_api: (EventLike) -> None, optional, default = None
            发布事件函数, 一般使用`Core`的`add_event`
        :param listen_receivers: set[str], optional, default = {EVERYONE_RECEIVER, self.uuid}
            监听的接收者集合
        """
        super().__init__(listen_receivers=listen_receivers, post_api=post_api)

        def __get_key1(listener: ListenerLike) -> _typing.Set[int]:
            return listener.listen_codes
        def __get_key2(listener: ListenerLike) -> _typing.Set[str]:
            return listener.listen_receivers

        self.__listeners: _tools.DoubleKeyBarrel[ListenerLike] = _tools.DoubleKeyBarrel(
            __get_key1, __get_key2
        )
        # 用listen_codes和listen_receivers作为键1和键2构建桶 此时桶里还是空的

    def group_listen(self, event: EventLike) -> None:
        """
        根据事件的`code`, 分配到对应的被`listening`装饰过的函数 (属于GroupLike的函数) 进行处理。
        (除非事件的`receivers`中, 不包括此监听者。)
        :param event: EventLike
            待处理事件
        """
        super().listen(event)

    def member_listen(self, event: EventLike) -> None:
        """
        将事件传递到群组内所有ListenerLike的listen中。
        (如果事件代码event.code和事件接收者event.receivers合适的话)
        :param event: EventLike
            待处理事件
        """
        for l in self.get_listener({event.code}, event.receivers):
            l.listen(event)

    def get_listener(
        self,
        codes: _typing.Set[int],
        receivers: _typing.Set[str],
    ) -> _typing.Set[ListenerLike]:
        """
        获取群组内的所有监听者，并根据给定事件代码和接收者进行筛选
        :param codes: set[int]
            事件代码集合
        :param receivers: set[str]
            事件接收者集合
        :return: typing.Set[ListenerLike]
            筛选后的监听者集合
        """
        return self.__listeners.get(codes, receivers)

    def add_listener(self, listener: ListenerLike) -> None:
        """
        添加监听者
        :param listener: ListenerLike
            待添加监听者
        """
        self.__listeners.add(listener)

    def remove_listener(self, listener: ListenerLike) -> None:
        """
        移除监听者
        :param listener: ListenerLike
            待移除监听者
        """
        self.__listeners.remove(listener)

    def clear_listener(self) -> None:
        """
        清空监听者
        """
        self.__listeners.clear()

    def listen(self, event: EventLike) -> None:
        """
        群组处理事件, 且群组成员处理事件
        :param event: EventLike
            待处理事件
        """
        self.group_listen(event)
        self.member_listen(event)

    @_tools.listening(_const.EventCode.KILL)
    def kill(self, event: EventLike) -> None:
        """
        根据`event.body["suicide"]`提供的UUID, 从群组中删除该成员
        :param event: EventLike
            待处理事件
        """
        body: _const.KillEventBody = event.body
        uuid: str = body["suicide"]
        for i in filter(lambda x: x.uuid == uuid, self.listeners):
            self.remove_listener(i)

class EntityLike(ListenerLike):
    pass

class PlayerLike(EntityLike):
    pass

class MonsterLike(EntityLike):
    pass

class MapLike(EntityLike):
    pass

@_typing.Final
@_tools.singleton
class Core:
    """
    核心
        管理事件队列，窗口，刻，pygame api
        单例类
    """

    def __init__(self, winsize: _typing.Tuple[int, int]):
        def get_prior(event: EventLike) -> int:
            return event.prior

        self.__winsize: _typing.Tuple[int, int] = winsize
        self.__title: str = ""  # TODO: title
        self.__rate: float = 60
        self.__window: _pygame.Surface = _pygame.display.set_mode(
            self.winsize, _pygame.RESIZABLE
        )
        self.__clock: _pygame.time.Clock = _pygame.time.Clock()
        self.__event_queue: _tools.BarrelQueue[EventLike] = _tools.BarrelQueue(
            get_prior
        )

        self.__init__()
        _pygame.display.set_caption(self.__title)

    def yield_events(
            self,
            *,
            add_pygame_event: bool = True,
            add_update_event: bool = True,
            add_draw_event: bool = True,
    ) -> _typing.Generator[EventLike, None, None]:
        """
        生成事件

        将事件队列的所有事件都yield出来 (根据优先级), 直到事件队列为空

        :param add_pygame_event: bool, optional, default = True
            是否自动加入pygame事件
        :param add_update_event: bool, optional, default = True
            是否自动加入UPDATE事件
        :param add_draw_event: bool, optional, default = True
            是否自动加入DRAW事件
        :return: typing.Generator[EventLike, None, None]
            生成器
        """
        if add_pygame_event:
            pygame_events = [
                EventLike.from_pygame_event(i) for i in _pygame.event.get()
            ]
            self.__event_queue.extend(pygame_events)
            # for event in filter(lambda x: x.code == _pygame.VIDEORESIZE, pygame_events):
            #     self.winsize = (event.w, event.h)
        if add_update_event:
            self.__event_queue.append(self.get_update_event())
        if add_draw_event:
            self.__event_queue.append(EventLike.draw_event(self.window))
        while self.__event_queue:
            yield self.__event_queue.popleft()


    def winsize(self) -> float:
        pass


