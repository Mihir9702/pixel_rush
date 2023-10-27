import pygame as p
from random import randint

p.init()

run = True
width = 960
height = 720
TILE_SIZE = 24
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

    # Draw sky tiles on top half of screen
    def draw(self, window):
        if self.y < height:
            super().draw(window)
            # p.draw.rect(window, (255, 200, 255), (self.x, self.y, self.w, self.h), 1)


class GroundTile(Tile):
    imgs = [p.image.load("img/bg_ground_left.png"),
            p.image.load("img/bg_ground_right.png")]

    def __init__(self, x, y, w, h, img):
        super().__init__(x, y, w, h, img)

    # Draw ground tiles on bottom half of screen
    def draw(self, window):
        if self.y > height // 1.5:
            super().draw(window)

            # first row of ground tiles
            if self.y == height // 1.5 + TILE_SIZE:
                if player.y > height // 1.5:
                    player.x, player.y = player.prev_x, player.prev_y
                    player.velocity_y = 0


class ViewTile(Tile):
    imgs = [p.image.load("img/bg_view_left.png"),
            p.image.load("img/bg_view_right.png")]

    def __init__(self, x, y, w, h, img):
        super().__init__(x, y, w, h, img)

    # draw view tiles right above ground tiles
    def draw(self, window):
        if self.y > height // 1.5 - TILE_SIZE:
            super().draw(window)
            # p.draw.rect(window, (255, 255, 200), (self.x, self.y, self.w, self.h), 1)


def create_tiles(tile_type):
    tiles = []
    for row in range(0, width, TILE_SIZE):
        for col in range(0, height, TILE_SIZE):
            tiles.append(tile_type(row, col, TILE_SIZE, TILE_SIZE,
                                   tile_type.imgs[randint(0, 1)]))
    return tiles


def draw_tiles(tiles):
    for row in tiles:
        for tile in row:
            tile.draw(window)


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
        'left': p.image.load('img/playerLeft.png'),
        'right': p.image.load('img/playerRight.png')
    }

    def __init__(self, x, y, w, h, img):
        super().__init__(x, y, w, h, img)
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

        # check if player is out of bounds
        if self.x < 0 or self.x > width - self.w:
            self.x = self.prev_x
        if self.y < 0 or self.y > height - self.h:
            self.y = self.prev_y
            self.velocity_y = 0

        if self.jumping:
            self.y -= self.velocity_y
            self.velocity_y -= self.gravity
            if self.velocity_y < -self.jump_height:
                self.jumping = False
                self.velocity_y = self.jump_height


player = Player(width // 2 - TILE_SIZE // 2, height // 1.5, TILE_SIZE, TILE_SIZE,
                p.image.load('img/playerRight.png'))


while True:
    window.fill((0, 0, 0))
    CLOCK.tick(60)

    for e in p.event.get():
        if e.type == p.QUIT:
            p.quit()

    # Draw tiles
    draw_tiles(sky_tiles)
    draw_tiles(view_tiles)
    draw_tiles(ground_tiles)

    # Get keys pressed
    keys_pressed = p.key.get_pressed()

    if keys_pressed[97]:  # left
        player.img = player.imgs['left']
        player.x -= player.speed
    elif keys_pressed[100]:  # right
        player.img = player.imgs['right']
        player.x += player.speed
    elif keys_pressed[119]:  # up
        player.jumping = True
    elif keys_pressed[115]:  # down
        pass

    player.draw(window)
    player.move()

    # Update window
    p.display.update()
