import pygame


class SpriteSheet():
    def __init__(self, image):
        self.sheet = image

    # Turn spritesheet into a form that can be easily animated by taking snippets of the sheet
    def get_frames(self, frame, width, height, scale, colour):
        image = pygame.Surface((width, height)).convert()
        image.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(colour)

        return image
