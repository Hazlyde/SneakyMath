"""Tile classes file"""

import random

import pygame

import data.constants as c

from data.textures import TEXTURES as textures


class Tile:
    """Tile class"""

    def __init__(self, grid, pos):
        self.grid = grid
        self.rect = pygame.Rect(0, 0, c.T_W, c.T_H)
        self.x = None
        self.y = None
        if pos is not None:
            self.spawn(pos)

    def spawn(self, pos):
        """Spawn tile"""
        self.x, self.y = pos
        self.grid[self.x][self.y] = self


class BodyPart(Tile):
    """Body Part of the snake class"""

    def __init__(self, grid, pos, ope=None):

        super().__init__(grid, pos)

        self.image = textures.body_part(ope)

        self.prev_x, self.prev_y = self.x, self.y
        self.dir = None

    def move(self, direction, remove=True):
        """Move"""
        self.prev_x, self.prev_y = self.x, self.y

        self.dir = direction

        self.x, self.y = self.grid.new_pos(self.dir, (self.x, self.y))

        self.grid[self.x][self.y] = self

    def get_coords(self, progress, dead=False):
        """Get the coordinates"""
        if not dead:
            offset = round(progress * c.T_W)
        else:
            offset = round(0.5 * (-((progress * 2 - 1) ** 2) + 1) * c.T_W)
        self.rect.x = (
            self.x * c.T_W + ((self.dir == "right") - (self.dir == "left")) * offset
        )
        self.rect.y = (
            self.y * c.T_H + ((self.dir == "down") - (self.dir == "up")) * offset
        )

        return self.rect.topleft


class Block(Tile):
    """Block"""

    def __init__(self, grid, pos):
        super().__init__(grid, pos)

    def get_coords(self, progress=None):
        """Get the coordinates"""
        self.rect.x = self.x * c.T_W
        self.rect.y = self.y * c.T_H
        return self.rect.topleft


class Number(Block):
    """Number"""

    def __init__(self, grid, pos=None, value=None):
        super().__init__(grid, pos)

        if value is None:
            self.value = random.randint(1, 9)
        else:
            self.value = value

        self.image = textures.number(self.value)


class Operation(Block):
    """Operation"""

    def __init__(self, grid, ope, pos=None):
        super().__init__(grid, pos)

        self.ope = ope

        self.image = textures.operation(self.ope)
