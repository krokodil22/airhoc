import pygame as pg
from pygame.math import Vector2

class BasePlayer:
    def __init__(self, x, y, radius=28, color=(200, 200, 200), bounds=(0, 9999)):
        self.pos = Vector2(x, y)
        self.vel = Vector2(0, 0)
        self.radius = radius
        self.color = color
        self.bounds = bounds
        self.max_speed = 520
        self.last_action = (0.0, 0.0)

    def clamp_bounds(self, height):
        self.pos.x = max(self.bounds[0]+self.radius, min(self.pos.x, self.bounds[1]-self.radius))
        self.pos.y = max(self.radius, min(self.pos.y, height - self.radius))

    def draw(self, surf):
        pg.draw.circle(surf, self.color, (int(self.pos.x), int(self.pos.y)), self.radius)

class HumanPlayer(BasePlayer):
    def update(self, dt):
        keys = pg.key.get_pressed()
        target = self.pos.copy()
        height = pg.display.get_surface().get_height()
        self.vel.update(0, 0)

        if pg.mouse.get_focused():
            mx, my = pg.mouse.get_pos()
            target.update(
                max(self.bounds[0] + self.radius, min(mx, self.bounds[1] - self.radius)),
                max(self.radius, min(my, height - self.radius)),
            )
            dir_vec = target - self.pos
            if dir_vec.length() > 0:
                desired_speed = min(self.max_speed, dir_vec.length() / max(dt, 1e-6))
                dir_vec.scale_to_length(desired_speed)
                self.vel = dir_vec

        self.pos += self.vel * dt
        self.clamp_bounds(height)
        action = self.vel.copy()
        if action.length() > 0:
            action.scale_to_length(1.0)
        self.last_action = (action.x, action.y)
