import pygame

class State:
    def __init__(self):
        self.done = False
        self.next_state = None
        self.quit = False

    def handle_events(self, events): pass
    def update(self): pass
    def draw(self, surface):
        pass
    