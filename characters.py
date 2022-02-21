import pygame
import spritesheet

sprite_sheet_image_doux = pygame.image.load('doux.png').convert_alpha()
sprite_sheet_image_doux2 = pygame.image.load('doux2.png').convert_alpha()
sprite_sheet_doux = spritesheet.SpriteSheet(sprite_sheet_image_doux)
sprite_sheet_doux2 = spritesheet.SpriteSheet(sprite_sheet_image_doux2)

sprite_sheet_image_mort = pygame.image.load('mort.png').convert_alpha()
sprite_sheet_image_mort2 = pygame.image.load('mort2.png').convert_alpha()
sprite_sheet_mort = spritesheet.SpriteSheet(sprite_sheet_image_mort)
sprite_sheet_mort2 = spritesheet.SpriteSheet(sprite_sheet_image_mort2)

sprite_sheet_image_tard = pygame.image.load('tard.png').convert_alpha()
sprite_sheet_image_tard2 = pygame.image.load('tard2.png').convert_alpha()
sprite_sheet_tard = spritesheet.SpriteSheet(sprite_sheet_image_tard)
sprite_sheet_tard2 = spritesheet.SpriteSheet(sprite_sheet_image_tard2)

sprite_sheet_image_vita = pygame.image.load('vita.png').convert_alpha()
sprite_sheet_image_vita2 = pygame.image.load('vita2.png').convert_alpha()
sprite_sheet_vita = spritesheet.SpriteSheet(sprite_sheet_image_vita)
sprite_sheet_vita2 = spritesheet.SpriteSheet(sprite_sheet_image_vita2)

# create animation list
animation_list_doux = []
animation_list_mort = []
animation_list_tard = []
animation_list_vita = []

animation_steps = [4, 6, 3, 4, 7]
animation_steps2 = [4, 4, 4, 11]


def get_animations_right(sprite_sheet, animation_list, animation_steps):
    step_counter = 0
    for animation in animation_steps:
        temp_img_list = []
        for _ in range(animation):
            temp_img_list.append(
                pygame.transform.flip(sprite_sheet.get_image(step_counter, 24, 24, 3, (0, 0, 0)), False, False))
            step_counter += 1
        animation_list.append(temp_img_list)


def get_animations_left(sprite_sheet, animation_list, animation_steps):
    step_counter = 0
    for animation in animation_steps:
        temp_img_list = []
        for _ in range(animation):
            temp_img_list.append(
                pygame.transform.flip(sprite_sheet.get_image(step_counter, 24, 24, 3, (0, 0, 0)), True, False))
            step_counter += 1
        animation_list.append(temp_img_list)


get_animations_right(sprite_sheet_doux, animation_list_doux, animation_steps)
get_animations_right(sprite_sheet_doux2, animation_list_doux, animation_steps2)
get_animations_left(sprite_sheet_doux, animation_list_doux, animation_steps)
get_animations_left(sprite_sheet_doux2, animation_list_doux, animation_steps2)

get_animations_right(sprite_sheet_mort, animation_list_mort, animation_steps)
get_animations_right(sprite_sheet_mort2, animation_list_mort, animation_steps2)
get_animations_left(sprite_sheet_mort, animation_list_mort, animation_steps)
get_animations_left(sprite_sheet_mort2, animation_list_mort, animation_steps2)

get_animations_right(sprite_sheet_tard, animation_list_tard, animation_steps)
get_animations_right(sprite_sheet_tard2, animation_list_tard, animation_steps2)
get_animations_left(sprite_sheet_tard, animation_list_tard, animation_steps)
get_animations_left(sprite_sheet_tard2, animation_list_tard, animation_steps2)

get_animations_right(sprite_sheet_vita, animation_list_vita, animation_steps)
get_animations_right(sprite_sheet_vita2, animation_list_vita, animation_steps2)
get_animations_left(sprite_sheet_vita, animation_list_vita, animation_steps)
get_animations_left(sprite_sheet_vita2, animation_list_vita, animation_steps2)

characters = [animation_list_doux, animation_list_mort, animation_list_tard, animation_list_vita]
