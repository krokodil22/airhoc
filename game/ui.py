import time
import pygame as pg
FONT_CACHE = {}

def get_font(size=18):
    if size not in FONT_CACHE:
        FONT_CACHE[size] = pg.font.SysFont("consolas", size)
    return FONT_CACHE[size]

def draw_hud(screen, score_left, score_right, start_ts, match_time):
    now = time.time()
    remain = max(0, int(match_time - (now - start_ts)))
    mm, ss = divmod(remain, 60)
    text = f"L {score_left} : {score_right} R   |   {mm:02d}:{ss:02d}"
    surf = get_font(22).render(text, True, (230, 230, 240))
    screen.blit(surf, (screen.get_width()//2 - surf.get_width()//2, 10))
