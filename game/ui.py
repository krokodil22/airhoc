import os
import pygame as pg
FONT_CACHE = {}

def get_font(size=18):
    if size not in FONT_CACHE:
        FONT_CACHE[size] = pg.font.SysFont("consolas", size)
    return FONT_CACHE[size]

def format_match_time(elapsed_s):
    minutes = int(elapsed_s) // 60
    seconds = int(elapsed_s) % 60
    return f"{minutes:02d}:{seconds:02d}"

def draw_hud(screen, score_left, score_right, target_score, field_width, elapsed_s):
    match_time = format_match_time(elapsed_s)
    text = f"L {score_left} : {score_right} R   |   до {target_score}   |   Время {match_time}"
    surf = get_font(22).render(text, True, (230, 230, 240))
    screen.blit(surf, (field_width//2 - surf.get_width()//2, 10))

def draw_training_panel(screen, rect, stats):
    pg.draw.rect(screen, (24, 26, 34), rect)
    pg.draw.line(screen, (60, 60, 80), (rect.left, rect.top), (rect.left, rect.bottom), 2)
    title = get_font(20).render("AI Статистика", True, (230, 230, 240))
    screen.blit(title, (rect.left + 12, rect.top + 12))
    lines = [
        f"Данные: {stats['samples'] if stats['has_data'] else 'нет'}",
        f"Весов: {'есть' if stats['weights_loaded'] else 'нет'}",
        f"Сохранено: {stats['last_saved']}",
        f"Средняя ошибка ИИ: {stats['ai_error_avg']}",
    ]
    y = rect.top + 44
    for line in lines:
        surf = get_font(16).render(line, True, (200, 200, 220))
        screen.blit(surf, (rect.left + 12, y))
        y += 22

def load_training_stats(meta_path, weights_loaded):
    stats = {
        "has_data": False,
        "samples": 0,
        "last_saved": "—",
        "weights_loaded": weights_loaded,
        "ai_error_avg": "—",
    }
    try:
        import json
        import time
        if os.path.exists(meta_path):
            with open(meta_path, "r", encoding="utf-8") as f:
                meta = json.load(f)
            stats["has_data"] = True
            stats["samples"] = int(meta.get("samples", 0))
            ts = int(meta.get("saved", 0))
            if ts > 0:
                stats["last_saved"] = time.strftime("%d.%m.%Y %H:%M", time.localtime(ts))
    except Exception:
        stats["last_saved"] = "ошибка"
    return stats
