import csv
import numpy as np
def load_session_csv(path):
    X, Y = [], []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            X.append([float(row["px"]), float(row["py"]), float(row["vx"]), float(row["vy"]), float(row["hx"]), float(row["hy"])])
            Y.append([float(row["action_hx"]), float(row["action_hy"])])
    return np.array(X, dtype=np.float32), np.array(Y, dtype=np.float32)

def load_many(paths):
    Xs, Ys = [], []
    for p in paths:
        X, Y = load_session_csv(p)
        Xs.append(X); Ys.append(Y)
    X = np.concatenate(Xs, axis=0)
    Y = np.concatenate(Ys, axis=0)
    return X, Y
