import pygame
from network import Network  # this will import the network class from network file
from world import World, map1, map2
from characters import characters

pygame.font.init()

width = 1250  # width of window
height = 800  # height of window
win = pygame.display.set_mode((width, height))  # Size of window
pygame.display.set_caption("MultiplayerTest")  # Cilent Name

# When connecting each player is allocated a different position on the map. The client will send new information and
# the other client position will be sent back to show movement

world = World(map1)

characters = {
    "Doux": characters[0],
    "Mort": characters[1],
    "Tard": characters[2],
    "Vita": characters[3],
}

animation_cooldown = 100


class Button:
    def __init__(self, text, x, y, color, text_color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.text_color = text_color
        self.width = 150
        self.height = 100

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("Agency FB", 40)
        text = font.render(self.text, True, self.text_color)
        win.blit(text, (self.x + round(self.width / 2) - round(text.get_width() / 2),
                        self.y + round(self.height / 2) - round(text.get_height() / 2)))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False


menu_buttons = (Button("Play Game", 525, 350, (255, 255, 255), (255, 0, 0)))

character_selection_buttons = (Button("Doux", 100, 200, (0, 156, 255), (0, 0, 0)),
                               Button("Mort", 400, 200, (255, 0, 0), (0, 0, 0)),
                               Button("Tard", 700, 200, (255, 174, 0), (0, 0, 0)),
                               Button("Vita", 1000, 200, (182, 255, 0), (0, 0, 0)))

play_again_button = Button("New Game?", 525, 550, (255, 255, 255), (0, 0, 255))


def update_screen(win, player, player2, chosen_animation_list, chosen_animation_list2):
    win.fill((193, 205, 205))

    if player.ready == True and player2.ready == True:

        # draws my tiles onto the screen
        world.draw()

        win.blit(chosen_animation_list[player.action][player.frame], (player.x - 10, player.y - 10))
        win.blit(chosen_animation_list2[player2.action][player2.frame], (player2.x - 10, player2.y - 10))

        font = pygame.font.SysFont("Agency FB", 80)

        text = font.render("P1", True, (255, 0, 0))
        win.blit(text, (25, 700))
        text = font.render("P2", True, (255, 0, 0))
        win.blit(text, (825, 700))

        player.update(player2)


    else:
        font = pygame.font.SysFont("Agency FB", 80)
        text = font.render("Waiting for Player...", True, (255, 0, 0))
        win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))

    pygame.display.update()


def main():
    run = True  # initiates while loop
    clock = pygame.time.Clock()

    n = Network()  # when we connect we will get the player starting position
    player = n.get_player()

    player.action = 0
    player.frame = 0
    last_update = pygame.time.get_ticks()

    chosen_animation_list = []
    chosen_animation_list2 = []

    while run:
        clock.tick(60)
        try:
            player2 = n.send(player)
        except:
            run = False
            print("Couldn't get game")
            break

        player.ready = True
        if player.ready == True and player.selected_char == False:
            select_character(player)
            chosen_animation_list = characters[player.chosen_char]

        if player2.ready == True and player2.selected_char == True:
            chosen_animation_list2 = characters[player2.chosen_char]

        current_time = pygame.time.get_ticks()
        if current_time - last_update >= animation_cooldown:
            player.frame += 1
            last_update = current_time
            if player.frame >= len(chosen_animation_list[player.action]):
                player.frame = 0

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False

                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    player.action = 1
                    player.frame = 0
                    player.direction = "RIGHT"

                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    player.action = 10
                    player.frame = 0
                    player.direction = "LEFT"

                if (event.key == pygame.K_w or event.key == pygame.K_UP) and player.jumped == False:
                    if player.direction == "RIGHT":
                        player.action = 7

                    elif player.direction == "LEFT":
                        player.action = 16

                    player.frame = 0

                if event.key == pygame.K_j:
                    player.tried_to_light_attack_this_frame = True
                    if player.direction == "RIGHT":
                        player.action = 2

                    elif player.direction == "LEFT":
                        player.action = 11

                    player.frame = 0

                if event.key == pygame.K_k:

                    if player.direction == "RIGHT":
                        player.action = 5

                    elif player.direction == "LEFT":
                        player.action = 14

                    player.frame = 0

            if event.type == pygame.KEYUP:
                player.tried_to_light_attack_this_frame = False
                if player.direction == "RIGHT":
                    player.action = 0

                elif player.direction == "LEFT":
                    player.action = 9

                player.frame = 0

            if player.current_lives == 0:
                loser_screen()
                run = False

            if player2.current_lives == 0:
                winner_screen()
                run = False

        if player.ready == True and player2.ready == True:
            player.move(player2)
            player.attack(player, player2)

        update_screen(win, player, player2, chosen_animation_list, chosen_animation_list2)


def loser_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        win.fill((0, 0, 0))
        font = pygame.font.SysFont("Agency FB", 60)
        loser_text = font.render("YOU LOSE!!!", True, (255, 0, 0))
        win.blit(loser_text, (525, 350))

        play_again_button.draw(win)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:

                pos = pygame.mouse.get_pos()
                if play_again_button.click(pos):
                    menu_screen()
                    run = False


def winner_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        win.fill((0, 0, 0))
        font = pygame.font.SysFont("Agency FB", 60)
        winner_text = font.render("YOU WIN!!!", True, (255, 255, 0))
        win.blit(winner_text, (525, 350))

        play_again_button.draw(win)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:

                pos = pygame.mouse.get_pos()
                if play_again_button.click(pos):
                    menu_screen()
                    run = False


def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        win.fill((128, 128, 128))

        menu_buttons.draw(win)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:

                pos = pygame.mouse.get_pos()
                if menu_buttons.click(pos):
                    run = False

    main()


def select_character(player):
    run = True
    clock = pygame.time.Clock()

    last_update = pygame.time.get_ticks()
    frame = 0
    while run:

        clock.tick(60)
        win.fill((0, 0, 0))

        current_time = pygame.time.get_ticks()
        if current_time - last_update >= animation_cooldown:
            frame += 1
            last_update = current_time
            if frame >= 6:
                frame = 0

        font = pygame.font.SysFont("Agency FB", 110)
        choose_character_text = font.render("CHOOSE YOUR CHARACTER", True, (255, 255, 255))
        win.blit(choose_character_text, (175, 25))

        font = pygame.font.SysFont("Agency FB", 40)

        doux_desc_health = font.render("Health: Normal", True, (0, 156, 255))
        doux_desc_attack = font.render("Attack: Normal", True, (0, 156, 255))
        doux_desc_speed = font.render("Speed: Normal ", True, (0, 156, 255))

        mort_desc_health = font.render("Health: Low", True, (255, 0, 0))
        mort_desc_attack = font.render("Attack: High", True, (255, 0, 0))
        mort_desc_speed = font.render("Speed: Normal", True, (255, 0, 0))

        tard_desc_health = font.render("Health: Low", True, (255, 174, 0))
        tard_desc_attack = font.render("Attack: Normal", True, (255, 174, 0))
        tard_desc_speed = font.render("Speed: High", True, (255, 174, 0))

        vita_desc_health = font.render("Health: High", True, (182, 255, 0))
        vita_desc_attack = font.render("Attack: Low", True, (182, 255, 0))
        vita_desc_speed = font.render("Speed: Low", True, (182, 255, 0))

        win.blit(doux_desc_health, (100, 450))
        win.blit(doux_desc_attack, (100, 500))
        win.blit(doux_desc_speed, (100, 550))

        win.blit(mort_desc_health, (400, 450))
        win.blit(mort_desc_attack, (400, 500))
        win.blit(mort_desc_speed, (400, 550))

        win.blit(tard_desc_health, (700, 450))
        win.blit(tard_desc_attack, (700, 500))
        win.blit(tard_desc_speed, (700, 550))

        win.blit(vita_desc_health, (1000, 450))
        win.blit(vita_desc_attack, (1000, 500))
        win.blit(vita_desc_speed, (1000, 550))

        win.blit(pygame.transform.scale(characters["Doux"][1][frame], (144, 144)), (105, 300))
        win.blit(pygame.transform.scale(characters["Mort"][1][frame], (144, 144)), (405, 300))
        win.blit(pygame.transform.scale(characters["Tard"][1][frame], (144, 144)), (705, 300))
        win.blit(pygame.transform.scale(characters["Vita"][1][frame], (144, 144)), (1005, 300))

        for button in character_selection_buttons:
            button.draw(win)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for character in character_selection_buttons:
                    if character.click(pos):
                        player.choose_character(character.text)
                        player.selected_char = True
                        run = False


while True:
    menu_screen()
