import sys

import pygame
from collections import *
import constants as _const

test = 1




if __name__ == "__main__":
    pygame.init()
    core = Core()
    player = PlayerLike(listen_receivers=_const.EVERYONE_RECEIVER, post_api=core.add_event)
    if test:
        player.suicide()

    pygame.quit()
    sys.exit()