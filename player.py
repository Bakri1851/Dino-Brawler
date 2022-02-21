import pygame.time
import world
from world import World, world_data, width, height

win = pygame.display.set_mode((width, height))  # Size of window
pygame.init()

world = World(world_data)


class Player():
    def __init__(self, x, y, width, height, lives, health, health_x, health_y, direction):
        self.ready = False
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.vel_y = 0
        self.jumped = False
        self.in_air = True

        self.lives = lives

        self.current_health = health
        self.maximum_health = health
        self.health_bar_length = 250
        self.health_ratio = self.maximum_health / self.health_bar_length
        self.health_x = health_x
        self.health_y = health_y
        self.lives = 3

        self.keys = pygame.key.get_pressed()

        self.action = 0
        self.frame = 0

        self.direction = direction


    def get_damage(self, amount):
        if self.current_health > 0:
            self.current_health -= amount
        if self.current_health <= 0:
            self.current_health = 0

    def get_health(self, amount):
        if self.current_health < self.maximum_health:
            self.current_health += amount
        if self.current_health >= self.maximum_health:
            self.current_health = self.maximum_health

    def display_health(self):
        pygame.draw.rect(win, (255, 0, 0), (self.health_x, self.health_y, self.current_health / self.health_ratio, 15))
        pygame.draw.rect(win, (255, 255, 255), (self.health_x, self.health_y, self.health_bar_length, 15), 5)
        # if want health bar above player swap health.x with x - 30 and health.y with y - 30

    def move(self):
        dx = 0
        dy = 0

        # get key presses
        self.keys = pygame.key.get_pressed()
        if self.keys[pygame.K_a] or self.keys[pygame.K_LEFT]:
            dx -= 5

        if self.keys[pygame.K_d] or self.keys[pygame.K_RIGHT]:
            dx += 5

        if (self.keys[pygame.K_w] or self.keys[pygame.K_UP]) and self.jumped == False and self.in_air == False:
            self.vel_y = -15
            self.jumped = True

        if not (self.keys[pygame.K_w] or self.keys[pygame.K_UP]):
            self.jumped = False

        # this is the gravity
        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        # collision
        self.in_air = True
        for tile in world.tile_list:
            # check for collision in x direction
            if tile[1].colliderect(self.x + dx, self.y, self.width, self.height):
                dx = 0
            # check for collision is y direction
            if tile[1].colliderect(self.x, self.y + dy, self.width, self.height):
                # check if below the ground
                if self.vel_y < 0:
                    dy = tile[1].bottom - self.rect.top
                    self.vel_y = 0
                # check if above the ground
                elif self.vel_y >= 0:
                    dy = tile[1].top - self.rect.bottom
                    self.vel_y = 0
                    self.in_air = False


        # coord
        self.x += dx
        self.y += dy

        self.update()

    def attack(self, player, player2):

        if player.rect.colliderect(player2.rect) and player2.keys[pygame.K_j] and not player2.keys[pygame.K_k]:
            player.get_damage(50)

        if player.rect.colliderect(player2.rect) and player2.keys[pygame.K_k] and not player2.keys[pygame.K_j]:
            player.get_damage(100)

    def update(self):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.display_health()
