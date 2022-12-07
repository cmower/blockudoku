import abc
import time
import pygame as pg
from PIL import Image

AGENTBUTTONDOWN = '__agent_button_down__'
AGENTBUTTONUP = '__agent_button_up__'

class AgentEvent:

    button = 1

    def __init__(self, type):
        self.type = type

class Agent(abc.ABC):

    def __init__(self):
        self.screen_np = None
        self._mouse_pressed = False
        self._last_state_button_was_pressed = False
        pg.mouse.set_pos([0, 0])

    def reset(self, screen_np):
        self.screen_np = screen_np
        self._reset()

    def save_screen_as_png(self):
        Image.fromarray(self.screen_np).save(f"screen_{time.time_ns()}.png")

    @abc.abstractmethod
    def set_score(self, score):
        pass

    @abc.abstractmethod
    def _reset(self):
        pass

    @abc.abstractmethod
    def mouse_position(self):
        pass

    def mouse_pressed(self):
        return self._mouse_pressed

    def get_events(self):
        events = pg.event.get()

        self._mouse_pressed = self.mouse_pressed()

        if self._mouse_pressed and not self._last_state_button_was_pressed:
            events.append(AgentEvent(AGENTBUTTONDOWN))

        if not self._mouse_pressed and self._last_state_button_was_pressed:
            events.append(AgentEvent(AGENTBUTTONUP))

        self._last_state_button_was_pressed = self._mouse_pressed

        return events

class Human(Agent):

    def _reset(self):
        self._mouse_pressed = pg.mouse.get_pressed()[0]

    def mouse_position(self):
        return pg.mouse.get_pos()

    def set_score(self, score):
        pass

class AI(Agent):

    def _reset(self):
        pass

    def mouse_position(self):
        pass
