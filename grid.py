import pygame as pg
from copy import deepcopy
from block import GridBlock, BlockState, block_colors

class Grid:

    nrow = 9
    ncol = nrow

    block_pos_ref = [
        (0, 0), (0, 1), (0, 2),
        (1, 0), (1, 1), (1, 2),
        (2, 0), (2, 1), (2, 2),
    ]

    def __init__(self, agent):

        self.agent = agent

        self.last_selected_item = None
        self.pattern = [['O']*self.ncol for _ in range(self.nrow)]

        # Init blocks
        self.blocks = [[None]*self.ncol for _ in range(self.nrow)]
        for i in range(self.nrow):
            for j in range(self.ncol):
                self.blocks[i][j] = GridBlock(i, j)

    def is_item_inside(self, item):
        if item is None: return False
        for pos in item.positions():

            inside = []
            for i in range(self.nrow):
                for j in range(self.ncol):
                    b = self.blocks[i][j]
                    inside_block = b.inside(pos)
                    if inside_block:
                        if self.pattern[i][j] == 'X':
                            return False
                    inside.append(inside_block)

            if not any(inside):
                return False

        return True

    def fill_item(self, item):
        for pos in item.positions():
            for i in range(self.nrow):
                for j in range(self.ncol):
                    b = self.blocks[i][j]
                    if b.inside(pos):
                        self.pattern[i][j] = 'X'

    def draw(self, surface, selected_item):

        self.last_selected_item = selected_item

        for i in range(self.nrow):
            for j in range(self.ncol):
                if self.pattern[i][j] == 'X':
                    c = block_colors[BlockState.FILLED]
                else:
                    c = block_colors[BlockState.UNFILLED]
                self.blocks[i][j].draw(surface, c)

        if selected_item:
            if self.can_selected_item_fit_in_user_selection(selected_item):
                c = block_colors[BlockState.READY_TO_BE_FILLED]
            else:
                c = block_colors[BlockState.CANT_BE_FILLED]

            for pos in selected_item.positions():
                for i in range(self.nrow):
                    for j in range(self.ncol):
                        b = self.blocks[i][j]
                        if b.inside(pos):
                            b.draw(surface, c)

    def can_selected_item_fit_in_user_selection(self, item):
        for pos in item.positions():
            for i in range(self.nrow):
                for j in range(self.ncol):
                    b = self.blocks[i][j]
                    if b.inside(pos) and self.pattern[i][j] == 'X':
                        return False
        return True

    def handle_block(self, ii, jj):
        update_score = 0
        n = 0
        for (i, j) in self.block_pos_ref:
            i += ii
            j += jj
            if self.pattern[i][j] == 'X':
                n += 1
        if n == self.nrow:
            update_score += self.nrow
            for (i, j) in self.block_pos_ref:
                i += ii
                j += jj
                self.positions_to_make_blank.append((i, j))
        return update_score


    def handle_full_areas(self):

        self.positions_to_make_blank = []

        update_score = 0

        for i in range(self.nrow):

            n = 0
            for j in range(self.ncol):
                if self.pattern[i][j] == 'X':
                    n += 1

            if n == self.ncol:
                update_score += self.ncol
                for j in range(self.ncol):
                    self.positions_to_make_blank.append((i, j))

        for j in range(self.ncol):

            n = 0
            for i in range(self.nrow):
                if self.pattern[i][j] == 'X':
                    n += 1

            if n == self.nrow:
                update_score += self.nrow
                for i in range(self.nrow):
                    self.positions_to_make_blank.append((i, j))



        update_score += self.handle_block(0, 0)
        update_score += self.handle_block(3, 0)
        update_score += self.handle_block(6, 0)

        update_score += self.handle_block(0, 3)
        update_score += self.handle_block(3, 3)
        update_score += self.handle_block(6, 3)

        update_score += self.handle_block(0, 6)
        update_score += self.handle_block(3, 6)
        update_score += self.handle_block(6, 6)

        for i, j in self.positions_to_make_blank:
            self.pattern[i][j] = 'O'

        return update_score
