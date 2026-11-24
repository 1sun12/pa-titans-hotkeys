"""Snapshot the live BAR keymap + the game's own keybind and build-grid data into this repo.

Writes uikeys.txt (the keymap the game loads), game_defaults.json (keybind catalog, the
shipped profile the active one is based on, and every factory/builder grid menu, read from
the installed game package), then renders KEYS.md and BUILD_GRID.md.
Safe to run while the game is open: it only reads.
"""
import gzip, json, os, re, shutil, subprocess

BAR_DATA = os.path.expanduser("~/.var/app/info.beyondallreason.bar/data")
HERE = os.path.dirname(os.path.abspath(__file__))

# Runs gridmenu_layouts.lua with default mod options and prints one TSV line per grid slot.
LUA_DUMP = r"""
Spring = { GetModOptions = function() return {} end }
BAR = { Utilities = { Gametype = { IsScavengers = function() return false end } } }
local g = dofile(arg[1])
for lab, units in pairs(g.LabGrids) do
  for i, u in pairs(units) do if u ~= "" then print("lab", lab, i, u) end end
end
for b, cats in pairs(g.UnitGrids) do
  for c, rows in pairs(cats) do for r, cols in pairs(rows) do for k, u in pairs(cols) do
    if type(u) == "string" and u ~= "" then print("builder", b, c, r, k, u) end
  end end end
end
"""


def game_package():
    """Return (name, file -> pool md5) for the newest installed BAR game version."""
    versions = f"{BAR_DATA}/rapid/repos-cdn.beyondallreason.dev/byar/versions.gz"
    line = next(l for l in gzip.open(versions, "rt") if l.startswith("byar:test,"))
    _, md5, _, name = line.strip().split(",", 3)
    b, i, idx = gzip.open(f"{BAR_DATA}/packages/{md5}.sdp").read(), 0, {}
    while i < len(b):
        n = b[i]; idx[b[i + 1:i + 1 + n].decode()] = b[i + 1 + n:i + 17 + n].hex(); i += 25 + n
    return name, idx


def main():
    name, idx = game_package()
    read = lambda f: gzip.open(f"{BAR_DATA}/pool/{idx[f][:2]}/{idx[f][2:]}.gz").read()
    lang = json.loads(read("language/en/commands.json"))
    lang["ui"] = json.loads(read("language/en/interface.json"))["ui"]  # grid menu category names
    units = json.loads(read("language/en/units.json"))["units"]["names"]
    catalog = json.loads(read("common/configs/keybind_catalog.json"))
    profiles = json.loads(read("common/configs/keybind_defaults.json"))["profiles"]

    def label(key):
        node = lang
        for part in (key or "").split("."):
            node = node.get(part) if isinstance(node, dict) else None
        return node if isinstance(node, str) else None

    store = json.load(open(f"{BAR_DATA}/LuaUI/Config/keybind_profiles.json"))
    active = store.get("active")
    mine = {p["name"]: p for p in store.get("profiles", [])}
    base = mine[active].get("basedOn") if active in mine else active
    shipped = next((p for p in profiles if p["name"] == base), profiles[0])

    categories = []
    for cat in catalog[1:]:
        items = [dict(i, label=label(i.get("label")) or i.get("label")) for i in cat["items"]]
        categories.append({"name": label(cat["category"]), "items": items})

    layout = f"{HERE}/.gridmenu_layouts.lua"
    open(layout, "wb").write(read("luaui/configs/gridmenu_layouts.lua"))
    try:
        rows = subprocess.run(["lua", "-", layout], input=LUA_DUMP, capture_output=True, text=True,
                              check=True).stdout.splitlines()
    finally:
        os.remove(layout)
    labs, builders = {}, {}
    for r in rows:
        f = r.split("\t")
        if f[0] == "lab":
            labs.setdefault(f[1], {})[int(f[2])] = f[3]
        else:
            builders.setdefault(f[1], {})[f"{f[2]}.{f[3]}.{f[4]}"] = f[5]
    used = {u for g in [*labs.values(), *builders.values()] for u in g.values()} | set(labs) | set(builders)
    assert labs and builders, "grid layout dump came back empty"

    out = {"game": name, "profile": shipped["name"], "active_profile": active,
           "hidden": catalog[0]["hidden"], "categories": categories, "default_binds": shipped["binds"],
           "labs": labs, "builders": builders, "names": {u: units[u] for u in sorted(used) if u in units}}
    json.dump(out, open(f"{HERE}/game_defaults.json", "w"), indent=1, sort_keys=True)
    shutil.copy(f"{BAR_DATA}/uikeys.txt", f"{HERE}/uikeys.txt")
    import render
    render.main()


if __name__ == "__main__":
    main()
