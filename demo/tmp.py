import pygame

# 初始化 Pygame
pygame.init()

# 创建一个 42x42 的 Surface
width, height = 42, 42
surface = pygame.Surface((width, height))

# 填充粉色 (RGB 值为 (255, 192, 203))
pink_color = (255, 192, 203)
surface.fill(pink_color)

# 保存图片为 PNG 文件
pygame.image.save(surface, "pink_image.png")

print("图片已保存为 pink_image.png")
