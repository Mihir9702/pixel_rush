import pygame
WEIGHT, HEIGHT = 960, 720
TILE_SIZE = 18


class Tile():
    def __init__(self, x, y, w, h, img):
        super().__init__(x, y, w, h, img)
        self.rect = p.Rect(x, y, w, h)


class SkyTile(Tile):
    imgs = [pygame.image.load("img/bg_sky_left.png"),
            pygame.image.load("img/bg_sky_right.png")]

    def __init__(self, x, y, w, h, img):
        super().__init__(x, y, w, h, img)
        self.speed = 0.75

    # Draw sky tiles on top half of screen
    def draw(self, window):
        if self.y < HEIGHT:
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
        if self.y > HEIGHT // 1.5:
            super().draw(window)

            # # first row of ground tiles
            # if self.y == height // 1.5 + TILE_SIZE:
            #     if player.y > height // 1.5:
            #         player.x, player.y = player.prev_x, player.prev_y
            #         player.velocity_y = 0

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
        if self.y > HEIGHT // 1.5 - TILE_SIZE:
            super().draw(window)
            # p.draw.rect(window, (255, 255, 200), (self.x, self.y, self.w, self.h), 1)

    def update(self):
        self.x -= self.speed


def create_tiles(tile_type, col=False):
    tiles = []
    for row in range(0, WIDTH, TILE_SIZE):
        for col in range(0, HEIGHT, TILE_SIZE):
            tiles.append(tile_type(row, col, TILE_SIZE, TILE_SIZE,
                                   tile_type.imgs[randint(0, 1)]))
    return tiles


def draw_tiles(*tile_lists):
    for tiles in tile_lists:
        for row in tiles:
            for tile in row:
                tile.draw(window)
                tile.update()
