import pygame as p
import math
from random import randint
from pytmx.util_pygame import load_pygame

p.init()

run = True
width = 1080
height = 720
TILE_SIZE = 18
CLOCK = p.time.Clock()

window = p.display.set_mode((width, height))
p.display.set_caption("Tiles")


class Tile:
    def __init__(self, x, y, w, h, img):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.img = img

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))


class SkyTile(Tile):
    imgs = [p.image.load("img/bg_sky_left.png"),
            p.image.load("img/bg_sky_right.png")]

    def __init__(self, x, y, w, h, img):
        super().__init__(x, y, w, h, img)
        self.speed = 0.75

    # Draw sky tiles on top half of screen
    def draw(self, window):
        if self.y < height:
            super().draw(window)
            # p.draw.rect(window, (255, 200, 255), (self.x, self.y, self.w, self.h), 1)

    def update(self):
        self.x -= self.speed


class GroundTile(Tile):
    imgs = [p.image.load("img/bg_ground_left.png"),
            p.image.load("img/bg_ground_right.png")]

    def __init__(self, x, y, w, h, img):
        super().__init__(x, y, w, h, img)
        self.speed = 0.25

    # Draw ground tiles on bottom half of screen
    def draw(self, window):
        if self.y > height // 1.5:
            super().draw(window)

            # first row of ground tiles
            if self.y == height // 1.5 + TILE_SIZE:
                if player.y > height // 1.5:
                    player.x, player.y = player.prev_x, player.prev_y
                    player.velocity_y = 0

    def update(self):
        self.x -= self.speed


class ViewTile(Tile):
    imgs = [p.image.load("img/bg_view_left.png"),
            p.image.load("img/bg_view_right.png")]

    def __init__(self, x, y, w, h, img):
        super().__init__(x, y, w, h, img)
        self.speed = 0.5

    # draw view tiles right above ground tiles
    def draw(self, window):
        if self.y > height // 1.5 - TILE_SIZE:
            super().draw(window)
            # p.draw.rect(window, (255, 255, 200), (self.x, self.y, self.w, self.h), 1)

    def update(self):
        self.x -= self.speed


def create_tiles(tile_type, col=False):
    tiles = []
    for row in range(0, width, TILE_SIZE):
        for col in range(0, height, TILE_SIZE):
            tiles.append(tile_type(row, col, TILE_SIZE, TILE_SIZE,
                                   tile_type.imgs[randint(0, 1)]))
    return tiles


def draw_tiles(*tile_lists):
    for tiles in tile_lists:
        for row in tiles:
            for tile in row:
                tile.draw(window)
                tile.update()


sky_tiles = [create_tiles(SkyTile)]
view_tiles = [create_tiles(ViewTile)]
ground_tiles = [create_tiles(GroundTile)]


class GameSprite:
    def __init__(self, x, y, w, h, img):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.img = img


class Player(GameSprite):
    imgs = {
        'left': p.image.load('img/player_left.png'),
        'right': p.image.load('img/player_right.png'),
        'left_jump': p.image.load('img/player_left_jump.png'),
        'right_jump': p.image.load('img/player_right_jump.png')
    }

    def __init__(self, x, y, w, h, img):
        super().__init__(x, y, w, h, img)
        self.rect = p.Rect(x, y, w, h)
        self.speed = 7
        self.prev_x = x
        self.prev_y = y
        self.gravity = 1  # gravity constant
        self.jump_height = 20
        self.velocity_y = self.jump_height
        self.jumping = False

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))
        # p.draw.rect(window, (255, 0, 0), (self.x, self.y, self.w, self.h), 1)

    def move(self):
        self.prev_x, self.prev_y = self.x, self.y  # save previous position

        self.rect.topleft = (self.x, self.y)

        # check if player is out of bounds
        if self.rect.left < 0:
            self.x = 0
        elif self.rect.right > width:
            self.x = width - self.w

        # check if player is jumping
        if self.jumping:
            if self.img == self.imgs['left']:
                self.img = self.imgs['left_jump']
            elif self.img == self.imgs['right']:
                self.img = self.imgs['right_jump']

            self.y -= self.velocity_y
            self.velocity_y -= self.gravity
            if self.velocity_y < -self.jump_height:
                self.jumping = False
                self.velocity_y = self.jump_height


player = Player(width // 4 - TILE_SIZE * 2, height // 1.5, TILE_SIZE, TILE_SIZE,
                p.image.load('img/player_right.png'))


TILES_AHEAD = 5

while True:
    window.fill((0, 0, 0))

    for e in p.event.get():
        if e.type == p.QUIT:
            p.quit()

    draw_tiles(sky_tiles, view_tiles, ground_tiles)

    for row in sky_tiles:
        if row[0].x < 0:
            sky_tiles.remove(row)
            sky_tiles.append(create_tiles(SkyTile))

    for row in view_tiles:
        if row[0].x < 0:
            view_tiles.remove(row)
            view_tiles.append(create_tiles(ViewTile))

    for row in ground_tiles:
        if row[0].x < 0:
            ground_tiles.remove(row)
            ground_tiles.append(create_tiles(GroundTile))

    keys_pressed = p.key.get_pressed()

    if keys_pressed[119]:  # up
        player.jumping = True
    elif keys_pressed[115]:  # down
        pass

    player.draw(window)
    player.move()

    CLOCK.tick(60)
    p.display.update()
