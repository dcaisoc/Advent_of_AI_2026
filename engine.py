"""Santa's Sleigh engine. Pure standard library, so anyone can run it."""
import json, os, random

SALT = os.environ.get("AOAI_SALT", "practice")  # secret salt for real scoring
DIRS = {"U": (0, -1), "D": (0, 1), "L": (-1, 0), "R": (1, 0), "W": (0, 0)}


def load_challenge(cid):
    for ch in json.load(open("challenges.json")):
        if ch["id"] == cid:
            return ch
    raise KeyError(cid)


def make_world(cfg, seed):
    rng = random.Random(f"{SALT}-{cfg['id']}-{seed}")
    w, h = cfg["width"], cfg["height"]
    cells = [(x, y) for x in range(w) for y in range(h)]
    rng.shuffle(cells)
    start = cells.pop()
    n_obs = int(cfg["obstacles"] * w * h)
    obstacles = set(cells[:n_obs])
    cells = cells[n_obs:]
    houses = {c: rng.randint(1, cfg["max_value"]) for c in cells[: cfg["houses"]]}
    return start, obstacles, houses


def play(act, cfg, seed):
    """Run one episode. Returns score = value delivered (+ <1 bonus for finishing early)."""
    pos, obstacles, houses = make_world(cfg, seed)
    rng = random.Random(f"{SALT}-{cfg['id']}-{seed}-play")
    w, h, delivered = cfg["width"], cfg["height"], 0
    total = sum(houses.values())
    for step in range(cfg["steps"]):
        obs = {
            "pos": pos, "width": w, "height": h,
            "obstacles": sorted(obstacles),
            "houses": [(c, v) for c, v in sorted(houses.items())],
            "steps_left": cfg["steps"] - step, "delivered": delivered,
        }
        try:
            a = act(obs)
        except Exception:
            a = "W"
        if a not in DIRS:
            a = "W"
        if rng.random() < cfg["wind"]:
            a = rng.choice("UDLR")
        dx, dy = DIRS[a]
        nxt = (pos[0] + dx, pos[1] + dy)
        if 0 <= nxt[0] < w and 0 <= nxt[1] < h and nxt not in obstacles:
            pos = nxt
        if pos in houses:
            delivered += houses.pop(pos)
        if not houses:
            return delivered + (cfg["steps"] - step) / cfg["steps"]
    return float(delivered)
