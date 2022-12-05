import random
import pygame as pg
from copy import deepcopy

from block import GridBlock

class Item:

    pattern = None
    preview_scale = 0.5
    init_xoffset = 40

    def __init__(self, initial_location, screen_width):
        self.selected = False
        self.y = 750
        if initial_location == 'left':
            self.x = int(round(0.25*float(screen_width))) - self.init_xoffset
        elif initial_location == 'center':
            self.x = int(round(0.5*float(screen_width)))
        elif initial_location == 'right':
            self.x = int(round(0.75*float(screen_width))) + self.init_xoffset
        else:
            raise ValueError(f"did not recognise the initial location '{initial_location}'")

        self.cx = deepcopy(self.x)
        self.cy = deepcopy(self.y)

    @property
    def nrow(self):
        return len(self.pattern)

    @property
    def ncol(self):
        return max(len(r) for r in self.pattern)

    def make_surface(self):
        surface = pg.Surface((self.ncol*GridBlock.width, self.nrow*GridBlock.height), pg.SRCALPHA)
        for i in range(self.nrow):
            for j in range(self.ncol):
                try:
                    if self.pattern[i][j] == 'X':
                        c = pg.Color(255, 94, 0)  # electric orange
                        xcenter = j*GridBlock.height+int(0.5*float(GridBlock.height))
                        ycenter = i*GridBlock.width+int(0.5*float(GridBlock.width))
                        center = (xcenter, ycenter)
                        pg.draw.circle(surface, c, center, int(0.5*GridBlock.width))
                except IndexError:
                    continue
        return surface

    def make_preview(self, surface):
        w, h = surface.get_size()
        w = int(round(self.preview_scale*float(w)))
        h = int(round(self.preview_scale*float(h)))
        return pg.transform.scale(surface, (w, h))

    def draw(self, surface):

        mouse_position = pg.mouse.get_pos()
        mouse_pressed = pg.mouse.get_pressed()[0]

        item = self.make_surface()
        preview = self.make_preview(item)

        preview_rect = preview.get_rect()
        preview_rect.center = (self.x, self.y)

        if preview_rect.collidepoint(mouse_position) and mouse_pressed:
            self.selected = True

        if not mouse_pressed:
            self.selected = False

        if self.selected:
            rect = item.get_rect()
            rect.center = mouse_position
            surface.blit(item, rect)
            self.cx, self.cy = mouse_position
        else:
            surface.blit(preview, preview_rect)
            self.cx, self.cy = deepcopy(self.x), deepcopy(self.y)

    def top_left_position(self):
        if not self.selected: return (0, 0)
        w = self.ncol*GridBlock.width
        h = self.nrow*GridBlock.height

        x = int(round(float(self.cx) - float(w)*0.5 + 0.5*float(GridBlock.width)))
        y = int(round(float(self.cy) - float(h)*0.5 + 0.5*float(GridBlock.height)))

        return x, y

    def positions(self):
        # Position in screen for all blocks in item
        xtl, ytl = self.top_left_position()
        positions = []
        for i in range(self.nrow):
            for j in range(self.ncol):

                try:
                    p = self.pattern[i][j]
                except IndexError:
                    continue

                if p == 'X':
                    x = xtl + j*GridBlock.width
                    y = ytl + i*GridBlock.height
                    yield (x, y)

class SingleSquare(Item):
    pattern = ['X']

class HorizontalTwoBlock(Item):
    pattern = ['XX']

class VerticleTwoBlock(Item):
    pattern = [
        'X',
        'X'
    ]

class HorizontalLine3(Item):
    pattern = ['XXX']

class VerticleLine3(Item):
    pattern = [
        'X',
        'X',
        'X',
    ]

class HorizontalLine4(Item):
    pattern = ['XXXX']

class VerticleLine4(Item):
    pattern = [
        'X',
        'X',
        'X',
        'X',
    ]

class HorizontalLine5(Item):
    pattern = ['XXXXX']

class VerticleLine5(Item):
    pattern = [
        'X',
        'X',
        'X',
        'X',
        'X',
    ]

class LShapeType1(Item):
    pattern = [
        '  X',
        'XXX',
    ]

class LShapeType2(Item):
    pattern = [
        'X',
        'X',
        'XX',
    ]

class LShapeType3(Item):
    pattern = [
        'XXX',
        'X'
    ]

class LShapeType4(Item):
    pattern = [
        'XX',
        ' X',
        ' X',
    ]

class BkwLShapeType1(Item):
    pattern = [
        'X  ',
        'XXX',
    ]

class BkwLShapeType2(Item):
    pattern = [
        'XX',
        'X',
        'X',
    ]

class BkwLShapeType3(Item):
    pattern = [
        'XXX',
        '  X',
    ]

class BkwLShapeType4(Item):
    pattern = [
        ' X',
        ' X',
        'XX',
    ]

class Block(Item):
    pattern = [
        'XX',
        'XX',
    ]

class SmallT1(Item):
    pattern = [
        'XXX',
        ' X',
    ]

class SmallT2(Item):
    pattern = [
        ' X',
        'XXX',
    ]

class SmallT3(Item):
    pattern = [
        'X',
        'XX',
        'X',
    ]

class SmallT4(Item):
    pattern = [
        ' X',
        'XX',
        ' X',
    ]


class LargeT1(Item):
    pattern = [
        'XXX',
        ' X',
        ' X',
    ]

class LargeT2(Item):
    pattern = [
        ' X',
        ' X',
        'XXX',
    ]

class LargeT3(Item):
    pattern = [
        'X',
        'XXX',
        'X',
    ]

class LargeT4(Item):
    pattern = [
        '  X',
        'XXX',
        '  X',
    ]


all_item_cls_handles = [
    SingleSquare,
    HorizontalTwoBlock,
    VerticleTwoBlock,
    HorizontalLine3,
    VerticleLine3,
    HorizontalLine4,
    VerticleLine4,
    HorizontalLine5,
    VerticleLine5,
    LShapeType1,
    LShapeType2,
    LShapeType3,
    LShapeType4,
    BkwLShapeType1,
    BkwLShapeType2,
    BkwLShapeType3,
    BkwLShapeType4,
    Block,
    SmallT1,
    SmallT2,
    SmallT3,
    SmallT4,
    LargeT1,
    LargeT2,
    LargeT3,
    LargeT4,
]

def get_random_item(location, screen_width):
    ItemCls = random.choice(all_item_cls_handles)
    return ItemCls(location, screen_width)
