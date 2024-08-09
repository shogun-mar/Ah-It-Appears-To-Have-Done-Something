import pygame as pg
from settings import *

class Tilemap:
    def __init__(self):
        self.tilemaps = []
        self.offgrid_tiles = []
        self.current_level = 0
        self.load_tilemaps()

    def load_tilemaps(self):
        #Start menu
        tiles = pg.sprite.Group()
        tiles.add(Tile("ground", (0, 7)))
        self.tilemaps.append(tiles)

        tiles = pg.sprite.Group()

    def render(self, screen, level_num):
        self.tilemaps[level_num].draw(screen)

class Tile(pg.sprite.Sprite):
    def __init__(self, tile_type, grid_pos):
        super().__init__()
        self.tile_type = tile_type
        self.image = pg.image.load(f"graphics/assets/tiles/{tile_type}_1.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=(grid_pos[0] * TILE_SIZE, grid_pos[1] * TILE_SIZE))