# BAR hotkeys

Versioned backup of my Beyond All Reason keymap (Flatpak install, `~/.var/app/info.beyondallreason.bar/data`).

- `uikeys.txt` is the keymap the game loads. Apply it in game with the keybind editor's Import,
  or copy it over the game's `uikeys.txt` while BAR is closed (the game keeps a hand-edited file as a profile of its own).
- `KEYS.md` is the readable view: every bindable action, the shipped default vs current.
- `BUILD_GRID.md` lists what each factory and builder puts on the Z/X/C/V, A/S/D/F, Q/W/E/R grid keys.
- `game_defaults.json` is the game's keybind catalog, shipped profile and grid layouts, read from the install.

## Scripts

- `python3 BAR/sync_from_game.py` snapshots the live keymap and the game's data into this repo (safe while the game runs; needs `lua`).
- `python3 BAR/render.py` rebuilds `KEYS.md` and `BUILD_GRID.md` after `uikeys.txt` is edited.
