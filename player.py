# import spritesheet
import pygame.time

import world
from pygame.locals import *
from world import *

win = pygame.display.set_mode((width, height))  # Size of window
pygame.init()

world = World(world_data)
p = 0
p2 = 0


class Player():
    def __init__(self, x, y, width, height, color, health, health_x, health_y):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = pygame.Rect(x, y, width, height)
        self.vel_y = 0
        self.jumped = False
        self.current_health = health
        self.maximum_health = health
        self.health_bar_length = 250
        self.health_ratio = self.maximum_health / self.health_bar_length
        self.health_x = health_x
        self.health_y = health_y
        self.keys = pygame.key.get_pressed()
        self.action = 0
        self.frame = 0
        self.last_update = pygame.time.get_ticks()

    def draw_character(self, win, animation_list):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update >= 125:
            self.frame += 1
            self.last_update = current_time
            if self.frame >= len(animation_list[self.action]):
                self.frame = 0
        win.blit(animation_list[self.action][self.frame], (self.x - 10, self.y - 10))

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

    def move(self, player, player2):
        dx = 0
        dy = 0
        self.action = 0

        # get key presses
        self.keys = pygame.key.get_pressed()
        if self.keys[pygame.K_a] or self.keys[pygame.K_LEFT]:
            dx -= 5
            self.frame = 0

        if self.keys[pygame.K_d] or self.keys[pygame.K_RIGHT]:
            dx += 5
            self.action = 1
            self.frame = 0

        if (self.keys[pygame.K_w] or self.keys[pygame.K_UP]) and self.jumped == False:
            self.vel_y = -15
            self.jumped = True
            self.action = 7
            self.frame = 0

        if not (self.keys[pygame.K_w] or self.keys[pygame.K_UP]):
            self.jumped = False

        # this is the gravity
        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        # collision
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

        # coord
        self.x += dx
        self.y += dy

        self.update()

    def attack(self, player, player2):

        if self.keys[pygame.K_j]:
            self.action = 2
            self.frame = 0

        if self.keys[pygame.K_k]:
            self.action = 5
            self.frame = 0

        if player.rect.colliderect(player2.rect) and player2.keys[pygame.K_j]:
            player.get_damage(50)
            player.action = 3
            self.frame = 0

        if player.rect.colliderect(player2.rect) and player2.keys[pygame.K_k]:
            player.get_damage(100)
            player.action = 3
            self.frame = 0

    def update(self):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.display_health()
        # pygame.draw.rect(win, (255, 255, 255), self.rect, 2)
