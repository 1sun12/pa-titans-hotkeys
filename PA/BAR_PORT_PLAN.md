# Plan: the PA layout, BAR style

Status: parked (2026-11-24). Nothing built yet. The BAR reference lives in [`../BAR/`](../BAR/README.md).

## Goal

Bring the ideas of this PA layout to BAR without fighting BAR's own design. Start from BAR's stock **Grid**
profile, keep everything its designers put there, and add binds only on keys it leaves free. Each PA feature
either maps to a BAR default that already does the job, or goes on a free key.

## Findings

- BAR is the Flatpak install at `~/.var/app/info.beyondallreason.bar/data`. The live keymap is `uikeys.txt`
  there, and it is exactly the stock Grid profile (no customisation yet).
- [`BAR/KEYS.md`](../BAR/KEYS.md) lists every bindable action (248 bound) by category, default vs current.
- [`BAR/BUILD_GRID.md`](../BAR/BUILD_GRID.md) lists what all 54 factories and 97 builders put on the grid keys.
- **Grid uses every letter.** Orders sit on letters (A attack, G stop, H patrol, O guard, E reclaim, R repair,
  F fight, D D-gun...). The grid keys Q W E R / A S D F / Z X C V are bound as `Any+`, so they own every modifier
  combination too.
- **The grid menu is BAR's Hotbuild.** With a builder selected: Z/X/C/V picks a category (Economy, Combat,
  Utility, Build), then a grid key picks the unit. Factories skip the category step.
- **`` ` `` is map draw / ping**, and the engine forces it to fire with any modifier held, so `` Shift+` `` etc. are
  not really free. **Space is the Meta key.**
- **Keys Grid leaves free:** CapsLock (with any modifier), F9, Ctrl + H J L M O P T U, Alt + H I J L M N P U.
- Selection filters can use unit categories BAR assigns in `gamedata/alldefs_post.lua`: `Category_SHIP`,
  `Category_VTOL`, `Category_MOBILE`, `Category_COMMANDER`, plus the engine's `Builder`, `Building`, `Aircraft`,
  `Weapons`, `Idle`.
- Editing the Grid profile in game forks it into a profile of your own. A fork stops receiving updates to Grid,
  which is another reason to keep the additions small: easy to re-apply on a fresh Grid after a game update.

## PA feature → BAR style

| PA layout | BAR style | Why |
|---|---|---|
| Groups 0-8 on 1 2 3 Q W E A S D | Groups 0-9 on the number row (Grid default) | Q-D are orders and grid keys in BAR |
| Alt+group saves | Ctrl+number saves (Grid default) | Alt+number is BAR's autogroups, worth keeping |
| Shift+group recalls camera | Double-tap the group number (Grid default) | BAR already jumps the camera to the group |
| Alt+Shift+group saves camera | Ctrl+F1-F4 save, F1-F4 jump (Grid default) | Four camera anchors already on F keys |
| F1-F6 stop / attack / patrol / assist / reclaim / repair | G / A / H / O / E / R (Grid default) | Letters are where BAR puts orders; F1-F4 are anchors |
| Hotbuild2 keys C V Z B F G Y H T R X | Grid menu, see below | It is BAR's built-in equivalent |
| Tab commander | Tab (Grid default) | Same key already |
| Shift+Space idle fabbers | Ctrl+Tab (Grid default) | Space is BAR's Meta key |
| Space acknowledge alert | F5 jump to last message (Grid default) | Space is BAR's Meta key |
| CapsLock all factories | **CapsLock** (new) | Free in Grid |
| `` ` `` all air | **Ctrl+CapsLock** (new) | `` ` `` is BAR's map draw / ping |
| `` Shift+` `` entire army | **Shift+CapsLock** (new) | Same modifier as PA |
| `` Alt+` `` all navy | **Alt+CapsLock** (new) | Same modifier as PA |

So the whole custom layout is Grid plus four binds. Draft lines for `uikeys.txt`:

```
bind capslock       select AllMap+_Builder_Building+_ClearSelection_SelectAll+
bind Ctrl+capslock  select AllMap+_Not_Builder_Aircraft_Weapons+_ClearSelection_SelectAll+
bind Shift+capslock select AllMap+_Not_Builder_Not_Building_Weapons+_ClearSelection_SelectAll+
bind Alt+capslock   select AllMap+_Not_Builder_Category_SHIP_Weapons+_ClearSelection_SelectAll+
```

`Not_Builder` keeps the commander and constructors out of army selections.

## Hotbuild habits on the grid

PA hotbuild slots and where the same job sits on BAR's grid, using the T1 bot constructor (`armck`) as the
example (category key, then grid key):

| PA key | Job | BAR grid |
|---|---|---|
| R | Metal extractor | Z, Z |
| T | Energy | Z, X (solar) · Z, C (wind) |
| Z | Storage | Z, Q (energy) · Z, W (metal) |
| F | Vehicle / bot factory | V, X (vehicle) · V, Z (bot) |
| G | Air / naval factory | V, C (air) · V, V (shipyard) |
| H | T2 factory | V, S (advanced bot lab) |
| C | Anti-air | X, A |
| X | Point defense | X, Z (Sentry) · X, C (Overwatch) |
| V | Artillery | X, W (Gauntlet) |
| Y | Radar | C, Z |
| B | Construction helper | V, A (construction turret) |

Other builders follow the same pattern; [`BAR/BUILD_GRID.md`](../BAR/BUILD_GRID.md) has them all.

## Open questions (test in game)

- Does BAR register CapsLock as a bindable key, and does it leave caps-lock on for chat? Fallback: the same
  family on F9, or on Ctrl+T / Ctrl+U.
- Does `_Builder_Building` grab construction turrets along with factories? If so, exclude them by unit name.
- Does `Category_SHIP` catch hovercraft and amphibious units the way PA's navy select did?

## Next steps

1. Add the four binds to a copy of Grid in `BAR/uikeys.txt`, then `python3 BAR/render.py`.
2. Import it in game and work through the open questions.
3. Play a few games on the grid menu before deciding anything should move.
