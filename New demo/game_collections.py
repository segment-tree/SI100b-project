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

import game_constants as _const
import game_tools as _tools
import makescene as _makescene

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
        return cls(_const.EventCode.DRAW, body=body, prior=300, receivers=receivers)

    def __init__(
        self,
        code: int,
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
        assert isinstance(code, int)
        assert isinstance(prior, int)
        assert isinstance(sender, str)
        assert isinstance(receivers, (set, None.__class__))
        assert isinstance(body, (dict, None.__class__))
        self.code: int = code
        self.prior: int = prior
        self.sender: str = sender
        self.receivers: _typing.Set[str] = (
                receivers if receivers is not None else {_const.EVERYONE_RECEIVER}
        )
        self.body: _typing.Dict[str, _typing.Any] = body if body is not None else {}

    def __lt__(self, other: "EventLike") -> bool:
        """
        运算符重载: `<`, 根据`prior`进行比较。
        """
        return self.prior < other.prior
    def __gt__(self, other: "EventLike") -> bool:
        """
        运算符重载: `>`, 根据`prior`进行比较。
        """
        return self.prior > other.prior


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
        获取该监听者监听的事件代码集合
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
        listen_receivers: _typing.Optional[_typing.Set[str]] = None,
        post_api: _typing.Optional[PostEventAPILike] = None,
    ) -> None:
        """
        :param listen_receivers:
            监听者接收者集合，默认有自己和EVERYONE_RECEIVER
        :param post_api:
            事件发布函数，一般使用Core类的add_event
        """
        self.__post_api: _typing.Optional[PostEventAPILike] = post_api
        self.__listen_receivers = (
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

    def side_post(self, event: EventLike) -> None:
        pass

    def listen(self, event: EventLike) -> None:
        """
        根据事件code，分配至对应的被listening装饰过的函数处理 iff 事件接收者在监听者的监听接收者集合中
        :param event: EventLike
            待处理事件
        """
        listen_receivers = self.__listen_receivers
        if not event.receivers & listen_receivers:  # 等价于 event.receiver.isdisjoint(listen_receivers)
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

@_typing.final
@_tools.singleton
class SceneLike(ListenerLike):
    """

    """
    @_tools.listening()

    pass

class EntityLike(ListenerLike):
    """
    实体类

    """
    __attributes: _typing.Dict[str, _typing.Any]
    __image: _typing.Optional[_pygame.Surface]
    __pos: _typing.List[int]
    __map: int  # 当前处于哪张地图

    @property
    def attributes(self):
        """
        实体的游戏内数值属性，如hp atk
        :return:
        """
        return self.__attributes

    @attributes.setter
    def attributes(self, attributes: _typing.Dict[str, _typing.Any]):
        self.__attributes = attributes

    @property
    def hp(self) -> int:
        return self.__attributes["hp"]

    @hp.setter
    def hp(self, value: int) -> None:
        self.__attributes["hp"] = value

    @property
    def image(self) -> _typing.Optional[_pygame.Surface]:
        """
        实体图像
        :return:
        """
        return self.__image

    @property
    def pos(self) -> _typing.List[int]:
        """
        实体坐标
        :return:
        """
        return self.__pos

    @pos.setter
    def pos(self, position: _typing.List[int]) -> None:
        self.__pos = position

    def modify_single_attributes(self, key: str, value: _typing.Any) -> None:
        self.__attributes[key] = value

    def __init__(
        self,
        *,
        image: _typing.Optional[_pygame.Surface],
        listen_receivers: _typing.Optional[_typing.Set[str]],
        post_api: _typing.Optional[PostEventAPILike] = None,
    ) -> None:
        super().__init__(
            listen_receivers=listen_receivers,
            post_api=post_api
    )
        _pygame.sprite.Sprite.__init__(self)

        self.__image: _typing.Optional[_pygame.Surface] = image

    @_tools.listening(_const.EventCode.DRAW)
    def draw(self, event: EventLike) -> None:
        """
        绘制自己
        TODO: 坐标和像素的对应
        :param event:
        :return:
        """
        body: _const.DrawEventBody = event.body
        window: _pygame.Surface = body["window"]
        camera: _typing.Tuple[int, int] = body["camera"]
        window.blit(self.image, self.pos, camera)


class PlayerLike(EntityLike):
    """
    玩家类
    实现一些常用操作
    :param __ability: typing.List[bool]
        持有的能力（非数值的）
        TODO: 几号位放什么能力？
    """
    __ability: _typing.List[bool]
    # TODO: 一些和捡掉落物相关的方法，需要知道有哪些掉落物

    @property
    def bomb(self) -> _typing.Dict[str, _typing.Any]:
        return self.__attributes["bomb"]

    @bomb.setter
    def bomb(self, value: _typing.Dict[str, _typing.Any]) -> None:
        self.__attributes["bomb"] = value

    @property
    def bomb_count(self) -> int:
        return self.__attributes["bomb"]["count"]

    @bomb_count.setter
    def bomb_count(self, value: int) -> None:
        self.__attributes["bomb"]["count"] = value

    @property
    def bomb_power(self) -> int:
        return self.__attributes["bomb"]["power"]

    @bomb_power.setter
    def bomb_power(self, value: int) -> None:
        self.__attributes["bomb"]["power"] = value

    # @property
    # def speed(self) -> int:
    #     return self.__attributes["speed"]
    #
    # @speed.setter
    # def speed(self):
    #     self.__attributes["speed"] = value
    # TODO: 加不加这个？

    @property
    def ability(self) -> _typing.List[str]:
        return [_const.ability[x] for x in range(_const.abilityCount) if self.__ability[x]]

    def learn_ability(self, ability: int):
        self.__ability[ability] = True

    @_tools.listening(_pygame.KEYDOWN)
    def move(self, event: EventLike):
        keys = _pygame.key.get_pressed()

    # # def forget_ability(self, ability: int):
    #     self.__ability[ability] = False




class MonsterLike(EntityLike):
    pass

# class MapLike(ListenerLike):
#     """
#     地图类
#
#     :param __mapDetails: typing.List[typing.List[typing.Dict[str, typing.Any]]]
#
#     """
#     __mapDetails: _typing.List[_typing.List[_typing.Dict[str, _typing.Any]]]
#     __isActive: bool
#     __sizeColumn: int
#     __sizeRow: int
#
#     def __init__(self, mapId: int):
#         match mapId:
#             case 1:
#                 _makescene.mapGener1(self)
#                 pass
#             case 2:
#                 _makescene.mapGener2()
#
#     @property
#     def details(self) -> _typing.List[_typing.List[_typing.Dict[str, _typing.Any]]]:
#         return self.__mapDetails
#
#
#
#     pass
# TODO: 改成全局变量



@_typing.final
@_tools.singleton
class Core:
    """
    核心
        管理事件队列，窗口，刻，pygame api
        单例类
    """

    def __init__(self):
        def get_prior(event: EventLike) -> int:
            return event.prior

        self.__winsize: _typing.Tuple[int, int] = (800, 600)
        self.__title: str = "1"  # TODO: title
        self.__rate: float = 0
        self.__window: _pygame.Surface = _pygame.display.set_mode(
            self.winsize, _pygame.RESIZABLE
        )
        self.__clock: _pygame.time.Clock = _pygame.time.Clock()
        self.__event_queue: _tools.BarrelQueue[EventLike] = _tools.BarrelQueue(
            get_prior
        )

        self.init()
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

    def add_event(self, event: EventLike) -> None:
        """
        向事件队列添加事件
        :param event: EventLike
            待添加事件
        """
        self.__event_queue.append(event)

    def clear_event(self) -> None:
        """
        清空事件队列 包括pygame队列
        """
        _pygame.event.clear()
        self.__event_queue.clear()

    def get_update_event(self) -> EventLike:
        """
        调用tick() 并生成UPDATE事件
        :return: EventLike
            UPDATE事件
        """
        return EventLike.update_event(self.__clock.tick() / 1000)

    @property
    def winsize(self) -> _typing.Tuple[int, int]:
        """
        :return:
            窗口大小
        """
        return self.__winsize

    @winsize.setter
    def winsize(self, winsize: _typing.Tuple[int, int]):
        """
        :param winsize: tuple[int, int]
            窗口大小
        """
        self.__winsize = winsize
        self.__window = _pygame.display.set_mode(self.__winsize, _pygame.RESIZABLE)

    @property
    def title(self) -> str:
        """
        :return:
            窗口标题
        """
        return self.__title

    @title.setter
    def title(self, title: str):
        """
        :param title: str
            窗口标题
        """
        self.__title = title
        _pygame.display.set_caption(self.__title)

    @property
    def window(self) -> _pygame.Surface:
        """
        :return:
            窗口(画布)
        """
        return self.__window

    @window.setter
    def window(self, window: _pygame.Surface):
        raise AttributeError("Setting attribute `window` is denied.")

    @property
    def clock(self) -> _pygame.time.Clock:
        """
        :return:
            主时钟
        """
        return self.__clock

    @clock.setter
    def clock(self, clock: _pygame.time.Clock):
        raise AttributeError("Setting attribute `clock` is denied.")

    @property
    def rate(self) -> float:
        """
        :return:
            tick rate
        """
        return self.__rate

    @rate.setter
    def rate(self, rate: float):
        raise AttributeError("Setting attribute `rate` is denied.")

    def tick(self, tick_rate: float = None) -> int:
        """
        时钟调用tick
        :param tick_rate:
        :return:
            距离上一次调用tick经过的时间 (ms)
        """
        if tick_rate is None:
            tick_rate = self.__rate
        return self.__clock.tick(tick_rate)

    # pygame api
    @staticmethod
    def flip() -> None:
        """
        将`self.window`上画的内容输出的屏幕上
        """
        return _pygame.display.flip()

    @staticmethod
    def init() -> None:
        """
        初始化pygame
        """
        _pygame.init()
        _pygame.mixer.init()

    @staticmethod
    def exit() -> None:
        """
        结束程序
        """
        _pygame.quit()
        _sys.exit()

    def blit(
            self,
            source: _pygame.Surface,
            dest,
            area=None,
            special_flags: int = 0,
    ) -> _pygame.Rect:
        """
        在self.windows上绘制
        :param source:
        :param dest:
        :param area:
        :param special_flags:
        :return:
        """
        self.window.blit(source, dest, area, special_flags)

    @staticmethod
    def play_music(path: str, loop: int = -1, monotone: bool = True) -> None:
        """
        播放音乐

        Parameters
        ---
        path : str
            音乐路径
        loop : int, default = -1
            循环次数, `-1`为无限循环
        monotone : bool, default = True
            是否仅播放该音乐
        """
        if monotone:
            _pygame.mixer.music.stop()
        _pygame.mixer.music.load(path)
        _pygame.mixer.music.play(loop)

    @staticmethod
    def stop_music() -> None:
        """
        停止音乐
        """
        _pygame.mixer.music.stop()

class SideCore:
    """
    处理跨帧事件
    """
    __across_frame_event: _typing.Deque[_typing.List[EventLike]]
    def __init__(self):
        self.__across_frame_event = _typing.Deque[_typing.List[EventLike]]()

    @property
    def across_frame_event(self) -> _typing.Deque[_typing.List[EventLike]]:
        return self.__across_frame_event

    def add_across_event(self, i: int, event: EventLike) -> None:
        """
        向当前帧之后的第i帧加入事件。

        :param i: int
            放置在之后的第几帧
        :param event: EventLike
            等待置入之后某一帧事件队列的事件
        :return:
        """
        while len(self.__across_frame_event) < i+1:
            self.__across_frame_event.append([])
        self.__across_frame_event[i].append(event)

    def frame_end(self, core: Core) -> None:
        for event in self.__across_frame_event[0]:
            core.add_event(event)
        self.__across_frame_event.popleft()
    pass

