import pygame
import spritesheet

black = (0, 0, 0)

# load and store spritesheets and images whilst also applying class
sprite_sheet_image_doux = pygame.image.load('Characters/doux.png').convert_alpha()
sprite_sheet_image_doux2 = pygame.image.load('Characters/doux2.png').convert_alpha()
sprite_sheet_doux = spritesheet.SpriteSheet(sprite_sheet_image_doux)
sprite_sheet_doux2 = spritesheet.SpriteSheet(sprite_sheet_image_doux2)

sprite_sheet_image_mort = pygame.image.load('Characters/mort.png').convert_alpha()
sprite_sheet_image_mort2 = pygame.image.load('Characters/mort2.png').convert_alpha()
sprite_sheet_mort = spritesheet.SpriteSheet(sprite_sheet_image_mort)
sprite_sheet_mort2 = spritesheet.SpriteSheet(sprite_sheet_image_mort2)

sprite_sheet_image_tard = pygame.image.load('Characters/tard.png').convert_alpha()
sprite_sheet_image_tard2 = pygame.image.load('Characters/tard2.png').convert_alpha()
sprite_sheet_tard = spritesheet.SpriteSheet(sprite_sheet_image_tard)
sprite_sheet_tard2 = spritesheet.SpriteSheet(sprite_sheet_image_tard2)

sprite_sheet_image_vita = pygame.image.load('Characters/vita.png').convert_alpha()
sprite_sheet_image_vita2 = pygame.image.load('Characters/vita2.png').convert_alpha()
sprite_sheet_vita = spritesheet.SpriteSheet(sprite_sheet_image_vita)
sprite_sheet_vita2 = spritesheet.SpriteSheet(sprite_sheet_image_vita2)

# create animation list
animation_list_doux = []
animation_list_mort = []
animation_list_tard = []
animation_list_vita = []

# how many frames per action
animation_steps = [4, 6, 3, 4, 7]
animation_steps2 = [4, 4, 4, 11]


# to get animations for both directions
def get_character_animations_right(sprite_sheet, animation_list, animation_steps):
    step_counter = 0
    for animation in animation_steps:
        temp_img_list = []
        for _ in range(animation):
            temp_img_list.append(
                pygame.transform.flip(sprite_sheet.get_frames(step_counter, 24, 24, 3, black), False, False))
            step_counter += 1
        animation_list.append(temp_img_list)


def get_character_animations_left(sprite_sheet, animation_list, animation_steps):
    step_counter = 0
    for animation in animation_steps:
        temp_img_list = []
        for _ in range(animation):
            temp_img_list.append(
                pygame.transform.flip(sprite_sheet.get_frames(step_counter, 24, 24, 3, black), True, False))
            step_counter += 1
        animation_list.append(temp_img_list)


# get all animations

get_character_animations_right(sprite_sheet_doux, animation_list_doux, animation_steps)
get_character_animations_right(sprite_sheet_doux2, animation_list_doux, animation_steps2)
get_character_animations_left(sprite_sheet_doux, animation_list_doux, animation_steps)
get_character_animations_left(sprite_sheet_doux2, animation_list_doux, animation_steps2)

get_character_animations_right(sprite_sheet_mort, animation_list_mort, animation_steps)
get_character_animations_right(sprite_sheet_mort2, animation_list_mort, animation_steps2)
get_character_animations_left(sprite_sheet_mort, animation_list_mort, animation_steps)
get_character_animations_left(sprite_sheet_mort2, animation_list_mort, animation_steps2)

get_character_animations_right(sprite_sheet_tard, animation_list_tard, animation_steps)
get_character_animations_right(sprite_sheet_tard2, animation_list_tard, animation_steps2)
get_character_animations_left(sprite_sheet_tard, animation_list_tard, animation_steps)
get_character_animations_left(sprite_sheet_tard2, animation_list_tard, animation_steps2)

get_character_animations_right(sprite_sheet_vita, animation_list_vita, animation_steps)
get_character_animations_right(sprite_sheet_vita2, animation_list_vita, animation_steps2)
get_character_animations_left(sprite_sheet_vita, animation_list_vita, animation_steps)
get_character_animations_left(sprite_sheet_vita2, animation_list_vita, animation_steps2)

characters = [animation_list_doux, animation_list_mort, animation_list_tard, animation_list_vita]
