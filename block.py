import pygame as pg
from enum import Enum

class BlockState(Enum):
    UNFILLED=0
    READY_TO_BE_FILLED=1
    FILLED=2
    CANT_BE_FILLED=3

block_colors = {
    BlockState.UNFILLED: pg.Color(135, 206, 250), # lightskyblue
    BlockState.READY_TO_BE_FILLED: pg.Color(255, 255, 51),  # electric yellow
    BlockState.CANT_BE_FILLED: pg.Color(255, 0, 0),  # red
    BlockState.FILLED: pg.Color(255, 0, 255), # magenta
}

class GridBlock:

    width = 60
    height = 60

    xoffset=10
    yoffset=70

    border_radius = 15  # see: https://www.pygame.org/docs/ref/draw.html#pygame.draw.rect

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.state = BlockState.UNFILLED
        self.rect = pg.Rect(
            x*self.width+self.xoffset, y*self.height+self.yoffset, self.width, self.height
        )

    def inside(self, mouse_position):
        x, y = mouse_position
        in_x = self.xoffset+self.x*self.width <= x <= self.x*self.width + self.width + self.xoffset
        in_y = self.yoffset+self.y*self.height <= y <= self.y*self.height + self.height + self.yoffset
        return in_x and in_y

    def draw(self, surface, color):
        pg.draw.rect(
            surface, color, self.rect, border_radius=self.border_radius
        )
