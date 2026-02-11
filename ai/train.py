import os, glob, json, time, numpy as np
from ai.dataset import load_many
from ai.model import MLP

DATA_DIR = os.path.join("../data", "sessions")
SAVE_PATH = os.path.join("../ai", "weights.npz")
META_PATH = os.path.join("../ai", "meta.json")
EPOCHS = 8
BATCH = 256
LR = 1e-3

def batches(X, Y, bs):
    n = X.shape[0]
    idx = np.random.permutation(n)
    for i in range(0, n, bs):
        ids = idx[i:i+bs]
        yield X[ids], Y[ids]

def main():
    files = sorted(glob.glob(os.path.join(DATA_DIR, "*.csv")))
    if not files:
        print("Нет данных — сыграйте несколько матчей.")
        return
    X, Y = load_many(files)
    n = X.shape[1]

    if os.path.exists(SAVE_PATH):
        model = MLP.load(SAVE_PATH)
        first_layer_inputs = model.W[0].shape[0]
        if first_layer_inputs != n:
            print(
                "Размер входных данных изменился, запускаю обучение с нуля "
                f"(ожидалось {first_layer_inputs}, получено {n})."
            )
            model = MLP([n, 64, 64, 2])
        else:
            print(f"Загружены предыдущие веса: {SAVE_PATH}")
    else:
        model = MLP([n, 64, 64, 2])
        print("Сохранённых весов не найдено, запускаю обучение с нуля.")

    for ep in range(1, EPOCHS+1):
        loss_sum, cnt = 0.0, 0
        for xb, yb in batches(X, Y, BATCH):
            grads_W, grads_b = model.backward(xb, yb)
            model.step(grads_W, grads_b, LR)
            pred = model.forward(xb)
            loss = np.mean((pred - yb)**2)
            loss_sum += loss; cnt += 1
        print(f"Epoch {ep}/{EPOCHS}: loss={loss_sum/cnt:.6f}")
    model.save(SAVE_PATH)
    meta = {"saved": int(time.time()), "samples": int(X.shape[0])}
    with open(META_PATH, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    print(f"Сохранено: {SAVE_PATH}")

if __name__ == "__main__":
    main()
