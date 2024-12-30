import sys

import pygame
from game_collections import *
import game_constants as _const
import utils

test = 0




if __name__ == "__main__":
    core = Core()
    player = PlayerLike(
        listen_receivers=None,
        post_api=core.add_event,
        image=utils.load_image_and_scale(
            r"../demo/assets/playerRight1.png",
            pygame.Rect(510, 330, 60, 60)
        )
    )
    entityGroup = GroupLike()
    entityGroup.add_listener(player)

    if test:
        pass

    while True:
        core.window.fill((0, 0, 0))
        for event in core.yield_events():
            entityGroup.listen(event)

        core.flip()

    pygame.quit()
    sys.exit()