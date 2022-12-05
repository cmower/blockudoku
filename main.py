import sys
import time

import pygame as pg
pg.init()

from grid import Grid, GridBlock

from items import get_random_item

class Game:

    framerate = 20
    num_item_opts = 1

    def __init__(self, args):
        self.score = 0
        pannel_height = 300
        self.height = Grid.nrow*GridBlock.height + GridBlock.yoffset + pannel_height
        self.width = Grid.ncol*GridBlock.width+GridBlock.xoffset*2
        self.screen = pg.display.set_mode((self.width, self.height))
        pg.display.set_caption('Blockudoku')
        self.clock = pg.time.Clock()
        self.grid = Grid()
        self.running = True
        self.event_action_map = {
            pg.QUIT: self.quit_game,
            pg.MOUSEBUTTONUP: self.handle_grid,
        }
        self.sound = '--nosound' not in args
        if self.sound:

            if '--altmusic' not in args:
                pg.mixer.music.load('audio/night-run-125181.mp3')
            else:
                pg.mixer.music.load('audio/stranger-things-124008.mp3')

            pg.mixer.music.play(-1)

        self.item_options = [
            get_random_item('left', self.width),
            get_random_item('center', self.width),
            get_random_item('right', self.width),
        ]

    def handle_events(self):
        for event in pg.event.get():
            handler = self.event_action_map.get(event.type)
            if handler:
                handler(event)

    def handle_grid(self, event):
        if event.button!=1: return

        if self.grid.is_item_inside(self.grid.last_selected_item):
            self.grid.fill_item(self.grid.last_selected_item)
            idx = self.item_options.index(self.grid.last_selected_item)
            if idx == 0:
                loc = 'left'
            elif idx == 1:
                loc = 'center'
            elif idx == 2:
                loc = 'right'
            else:
                raise ValueError(f"index '{idx}' not recognized!")
            self.item_options[idx] = get_random_item(loc, self.width)
            self.grid.last_selected_item = None

            self.score += self.grid.handle_full_areas()

    def draw_goodbye(self):
        c = pg.Color(255, 0, 0) # red
        surface = pg.font.SysFont(None, 100).render('Goodbye!', True, c)
        rect = surface.get_rect()
        rect.center = (int(0.5*float(self.width)), 200)
        self.screen.blit(surface, rect)
        self.update_screen()

    def quit_game(self, event=None):
        self.draw_goodbye()
        self.running = False
        if self.sound:
            pg.mixer.music.fadeout(1000)
            time.sleep(1)
        pg.quit()

    def draw_score(self):
        c = pg.Color(255, 255, 255)  # white
        surface = pg.font.SysFont(None, 50).render(str(self.score), True, c)
        rect = surface.get_rect()
        rect.center = (int(0.5*float(self.width)), 35)
        self.screen.blit(surface, rect)

    def draw(self):
        self.screen.fill(pg.Color(0, 0, 0))

        selected_item = None
        for item in self.item_options:
            if item.selected:
                selected_item = item
                break

        self.grid.draw(self.screen, selected_item)
        self.draw_score()
        for item in self.item_options:
            item.draw(self.screen)

    def update_screen(self):
        pg.display.flip()
        pg.display.update()

    def tick(self):
        self.clock.tick(Game.framerate)

    def spin(self):
        try:
            while self.running:
                self.draw()
                self.update_screen()
                self.tick()
                self.handle_events()
        except KeyboardInterrupt:
            self.quit_game()

def main():
    Game(sys.argv).spin()

if __name__ == '__main__':
    main()
