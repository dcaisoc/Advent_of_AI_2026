"""Starter bot: walk toward the nearest house, ignoring obstacles. Copy this folder, rename it to
your team name, and make it better (path-finding with BFS is the obvious next step)."""
NUM_PARAMS = 0  # declare learned parameters (0 for hand-written logic). Required on capped days.


def act(obs):
    x, y = obs["pos"]
    if not obs["houses"]:
        return "W"
    (hx, hy), _ = min(obs["houses"], key=lambda h: abs(h[0][0] - x) + abs(h[0][1] - y))
    if hx != x:
        return "R" if hx > x else "L"
    return "D" if hy > y else "U"
