import pygame as pg
from settings import *

class Tilemap:
    def __init__(self, tile_size = TILE_SIZE):
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid_tiles = []

        for i in range(0, SCREEN_WIDTH, tile_size):
            for j in range(0, SCREEN_HEIGHT, tile_size):
                self.tilemap[(i, j)] = Tile("grass", (i, j))

class Tile:
    def __init__(self, tile_type, grid_pos):
        self.tile_type = tile_type
        self.sprite = pg.image.load(f"graphics/assets/tiles/{tile_type}_1.png")
        self.pos = grid_pos * TILE_SIZE