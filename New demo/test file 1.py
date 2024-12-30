import typing as _typing
import game_collections as _col
import game_constants as _const
import game_tools as _tools

print(_const.user_event_start)

c = _col.Core()

print(_const.user_event_start)

a = _col.EntityLike(listen_receivers=None)
b = _col.EventLike(
            EventCode=_const.get_unused_event_code(),
            sender=self.uuid,
        )
a.post(b)

print(_const.user_event_start)




