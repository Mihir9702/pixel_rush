import pygame as p
import math
from random import randint
from pytmx.util_pygame import load_pygame
from pytmx import TiledTileLayer
from tiles import Tile

p.init()

run = True
width = 960
height = 720
TILE_SIZE = 18
CLOCK = p.time.Clock()

window = p.display.set_mode((width, height))
p.display.set_caption("Tiles")
p.transform.scale(window, (TILE_SIZE * 2, TILE_SIZE * 2))

tmx_map = load_pygame('map.tmx')


def key_handler():
    keys = p.key.get_pressed()

    if keys[p.K_a]:
        player.velocity_x -= player.speed
        player.img = player.imgs['left']
    elif keys[p.K_d]:
        player.velocity_x += player.speed
        player.img = player.imgs['right']
    else:
        player.velocity_x = 0

    if keys[p.K_w] and not player.jumping:
        player.jumping = True
        player.velocity_y = player.jump_height


class Player():
    imgs = {
        'left': p.image.load('img/player_left.png').convert_alpha(),
        'right': p.image.load('img/player_right.png').convert_alpha(),
        'left_jump': p.image.load('img/player_left_jump.png').convert_alpha(),
        'right_jump': p.image.load('img/player_right_jump.png').convert_alpha()
    }

    def __init__(self, x, y, w, h, img):
        super().__init__(x, y, w, h, img)
        self.rect = p.Rect(x, y, w, h)
        self.speed = 0.3
        self.prev_x = x
        self.prev_y = y
        self.gravity = 1  # gravity constant
        self.jump_height = 12
        self.velocity_x = 0
        self.velocity_y = self.jump_height
        self.jumping = False

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))
        # p.draw.rect(window, (255, 0, 0), (self.x, self.y, self.w, self.h), 1)

    def move(self):
        self.prev_x, self.prev_y = self.x, self.y  # save previous position

        self.velocity_x *= 0.9  # friction
        self.velocity_y += self.gravity

        self.x += self.velocity_x
        self.y += self.velocity_y

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


player = Player(TILE_SIZE * 2, 250,
                18, 18, Player.imgs['right'])
camera = Camera(width, height)


def draw_tiles(tiles):
    for tile in tiles:
        window.blit(tile.img, camera.apply(tile))


def load_map():
    tiles, grass_tiles = [], []

    for layer in tmx_map.visible_layers:
        if isinstance(layer, TiledTileLayer):
            for x, y, image in layer.tiles():
                if image:
                    if layer.name == 'grass':
                        tile = Tile(x * TILE_SIZE, y * TILE_SIZE,
                                    TILE_SIZE, TILE_SIZE, image)
                        grass_tiles.append(tile)
                    else:
                        tile = Tile(x * TILE_SIZE, y * TILE_SIZE,
                                    TILE_SIZE, TILE_SIZE, image)
                        tiles.append(tile)

    return tiles, grass_tiles


offset_x = 0
scroll_area_width = 200
all_tiles, grass_tiles = load_map()

while True:
    window.fill((0, 0, 0))

    for e in p.event.get():
        if e.type == p.QUIT:
            p.quit()

    key_handler()
    # draw_tiles(all_tiles)
    draw_tiles(grass_tiles)

    # Check if player is above the grass tiles (grass_tile.height = 40)

    # Scroll the background when the player moves to the right
    if ((player.rect.right - offset_x >= width - 200 and player.velocity_x > 0)
            or (player.rect.left - offset_x <= 200 and player.velocity_x < 0)):
        offset_x += player.velocity_x + 2

    for tile in grass_tiles:
        if player.y + player.h >= tile.y and player.y <= tile.y + tile.h:
            if player.x + player.w >= tile.x and player.x <= tile.x + tile.w:
                player.x, player.y = player.prev_x, player.prev_y
                player.velocity_y = 0
                player.jumping = False

    # Update the camera to follow the player
    camera.update(player)

    player.draw(window)
    player.move()

    CLOCK.tick(60)
    p.display.update()
