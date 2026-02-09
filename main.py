import os, csv, time, pygame as pg, numpy as np
from game.board import Board
from game.player import HumanPlayer
from game.ai_player import AIPlayer
from game.ui import draw_hud

WIDTH, HEIGHT = 900, 500
FPS = 60
LOG_DIR = os.path.join("data", "sessions")
os.makedirs(LOG_DIR, exist_ok=True)

def norm(x, a, b): return (x - a) / (b - a)

def main():
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("Air Hockey — NN Project")
    clock = pg.time.Clock()
    board = Board(WIDTH, HEIGHT)
    human = HumanPlayer(x=40, y=HEIGHT//2, radius=28, color=(30, 144, 255), bounds=(0, WIDTH//2))
    ai = AIPlayer(x=WIDTH-40, y=HEIGHT//2, radius=28, color=(255, 99, 71), bounds=(WIDTH//2, WIDTH))
    session_path = os.path.join(LOG_DIR, f"session_{int(time.time())}.csv")
    log_file = open(session_path, "w", newline="", encoding="utf-8")
    logger = csv.writer(log_file)
    logger.writerow(["t","px","py","vx","vy","hx","hy","ax","ay","action_hx","action_hy"])
    running, score_left, score_right = True, 0, 0
    match_time = 120
    start_ts = time.time()
    while running:
        dt = clock.tick(FPS) / 1000.0
        for event in pg.event.get():
            if event.type == pg.QUIT: running = False
        human.update(dt)
        puck = board.puck
        state = np.array([norm(puck.pos.x,0,WIDTH), norm(puck.pos.y,0,HEIGHT), norm(puck.vel.x,-800,800), norm(puck.vel.y,-800,800), norm(human.pos.x,0,WIDTH), norm(human.pos.y,0,HEIGHT)], dtype=np.float32)
        ax, ay = ai.decide(state, puck)
        ai.apply_action(ax, ay, dt)
        board.update(dt, [human, ai])
        hx, hy = human.last_action
        logger.writerow([f"{time.time()-start_ts:.3f}",f"{state[0]:.6f}",f"{state[1]:.6f}",f"{state[2]:.6f}",f"{state[3]:.6f}",f"{state[4]:.6f}",f"{state[5]:.6f}",f"{norm(ai.pos.x,0,WIDTH):.6f}",f"{norm(ai.pos.y,0,HEIGHT):.6f}",f"{hx:.6f}",f"{hy:.6f}"])
        goal = board.check_goal()
        if goal == "left":
            score_left += 1; board.reset()
        elif goal == "right":
            score_right += 1; board.reset()
        screen.fill((18,18,22))
        board.draw(screen); human.draw(screen); ai.draw(screen)
        draw_hud(screen, score_left, score_right, start_ts, match_time)
        pg.display.flip()
        if time.time()-start_ts >= match_time: running = False
    log_file.close()
    pg.quit()

if __name__ == "__main__":
    main()
