import pygame as pg
from pygame.math import Vector2

class Puck:
    def __init__(self, x, y, radius=12, color=(240, 240, 240)):
        self.pos = Vector2(x, y)
        self.vel = Vector2(280, 120)
        self.radius = radius
        self.color = color

    def update(self, dt, width, height):
        self.pos += self.vel * dt
        self.vel *= 0.999
        if self.pos.y - self.radius <= 0 or self.pos.y + self.radius > height:
            self.vel.y *= -1
        if self.pos.y - self.radius <= 0:
            self.pos.y = 0 + self.radius
        if self.pos.y + self.radius >= height:
            self.pos.y = height - self.radius
        if self.pos.x - self.radius < 0 or self.pos.x + self.radius > width:
            self.vel.x *= -1

    def draw(self, surf):
        pg.draw.circle(surf, self.color, (int(self.pos.x), int(self.pos.y)), self.radius)

class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.center_line_color = (70, 70, 90)
        self.goal_size = 120
        self.goal_margin = (height - self.goal_size) // 2
        self.puck = Puck(width//2, height//2)

    def update(self, dt, players):
        for p in players:
            to_puck = self.puck.pos - p.pos
            dist = to_puck.length()
            if dist < self.puck.radius + p.radius:
                n = to_puck.normalize() if dist > 0 else Vector2(1, 0)
                rel = self.puck.vel - p.vel
                vn = rel.dot(n)
                if vn < 0:
                    rel -= 2 * vn * n
                    self.puck.vel = rel + p.vel
                overlap = (self.puck.radius + p.radius) - dist
                self.puck.pos += n * (overlap + 1)
        self.puck.update(dt, self.width, self.height)

    def check_goal(self):
        if self.puck.pos.x - self.puck.radius <= 0:
            if self.goal_margin <= self.puck.pos.y <= self.height - self.goal_margin:
                return "right"
        if self.puck.pos.x + self.puck.radius >= self.width:
            if self.goal_margin <= self.puck.pos.y <= self.height - self.goal_margin:
                return "left"
        return None

    def reset(self):
        self.puck.pos.update(self.width//2, self.height//2)
        self.puck.vel.update(-280, 120)

    def draw(self, surf):
        surf_w, surf_h = self.width, self.height
        pg.draw.line(surf, self.center_line_color, (surf_w//2, 0), (surf_w//2, surf_h), 2)
        pg.draw.rect(surf, (60, 80, 100), (0, self.goal_margin, 6, self.goal_size))
        pg.draw.rect(surf, (60, 80, 100), (surf_w-6, self.goal_margin, 6, self.goal_size))
        self.puck.draw(surf)
