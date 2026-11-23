# PaTitansHotkeys

Versioned backup of my Planetary Annihilation: Titans keybinds and Hotbuild2 layout.

- `hotbuild2_layout.pas` holds the layout. Load it in game: Settings → Keyboard → Hotbuild2 Import/Export → Import.
  It restores the Hotbuild2 keys and every game keybind.
- `KEYS.md` is the readable view (Hotbuild2 keys plus all 233 game keybinds, default vs current).
- `game_default_keys.json` lists the game's stock keybinds, read from the install.

## Scripts

- `python3 sync_from_game.py` snapshots the live in-game settings into this repo (safe while the game runs).
- `python3 render.py` rebuilds `KEYS.md` after `hotbuild2_layout.pas` is edited.

Each change is a git commit, so `git log -p hotbuild2_layout.pas` shows the history.
