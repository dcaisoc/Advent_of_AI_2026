# Advent of AI: Downing

Build a bot for Santa's sleigh. A new challenge unlocks every other day from 1 December.

## Enter
1. Fork this repo, copy `submissions/starter_greedy` to `submissions/<your-team>`.
2. Edit `agent.py`. Your bot is `act(obs) -> "U"|"D"|"L"|"R"|"W"`. Set `NUM_PARAMS` honestly.
3. Test locally: `python play_one.py <your-team> d01`
4. Open a pull request. Once merged, the leaderboard updates.

## Rules
- The map is a grid. Walk onto a house to deliver. Obstacles block you. Wind can replace your move with a random one.
- Score = value delivered, plus a small bonus for finishing early. Averaged over 10 hidden maps.
- Daily points: 1st = 10, 2nd = 9 ... 10th = 1. Highest total wins on Christmas Eve.
- Capped days: `NUM_PARAMS` must be <= the cap. Heuristics-only days: it must be 0.
- Standard library only. 120 seconds per challenge. No reading other teams' files.

## Organisers
- Settings > Pages: deploy from `main` / `docs`. Settings > Secrets: add `AOAI_SALT` (any random string) so maps are hidden.
- Review every PR's `agent.py` before merging. It runs on the scorer, and the salt is in its environment.
- Local scoring: `TODAY=2026-12-23 python score.py`
