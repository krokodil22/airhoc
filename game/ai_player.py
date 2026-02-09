import os
import numpy as np
import pygame as pg
from pygame.math import Vector2
from ai.model import MLP
from game.player import BasePlayer


class AIPlayer(BasePlayer):
    def __init__(self, x, y, radius=28, color=(230, 180, 60), bounds=(0, 9999)):
        super().__init__(x, y, radius, color, bounds)
        self.max_speed = 500
        self.model = None
        weights_path = os.path.join("ai", "weights.npz")
        if os.path.exists(weights_path):
            try:
                self.model = MLP.load(weights_path)
            except Exception:
                print("Weights file not found")
                self.model = None

    def decide(self, state, puck):
        if self.model is not None:
            out = self.model.forward(state.reshape(1, -1))[0]
            norm = np.linalg.norm(out) + 1e-6
            out = out / norm
            print(float(out[0]), float(out[1]))
            return float(out[0]), float(out[1])
        else:
            target = Vector2(self.bounds[0] + (self.bounds[1]-self.bounds[0]) * 0.8, puck.pos.y)
            dir_vec = target - self.pos
            if dir_vec.length() > 0:
                dir_vec.scale_to_length(1)
            return dir_vec.x, dir_vec.y

    def apply_action(self, ax, ay, dt):
        self.vel.update(ax, ay)
        if self.vel.length() > 0:
            self.vel.scale_to_length(self.max_speed)
        self.pos += self.vel * dt
        self.clamp_bounds(pg.display.get_surface().get_height())


