"""Usage: python play_one.py <team> <challenge_id>  -> prints JSON. Run in a subprocess by score.py."""
import sys, json, importlib.util
from engine import load_challenge, play

team, cid = sys.argv[1], sys.argv[2]
cfg = load_challenge(cid)
spec = importlib.util.spec_from_file_location("agent", f"submissions/{team}/agent.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
params, cap = getattr(mod, "NUM_PARAMS", None), cfg.get("param_cap")
if cap is not None and (params is None or params > cap):
    print(json.dumps({"score": 0, "note": f"needs NUM_PARAMS <= {cap}"}))
else:
    s = [play(mod.act, cfg, i) for i in range(cfg["seeds"])]
    print(json.dumps({"score": round(sum(s) / len(s), 3)}))
