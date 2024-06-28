import pygame

# Helper function to scale image
def scale_img(image: pygame.Surface, scale: int):
    w = image.get_width()
    h = image.get_height()
    return pygame.transform.scale(image, (w * scale, h * scale))