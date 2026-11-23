"""Snapshot the live PA Titans keybinds + Hotbuild2 layout into this repo.

Writes game_default_keys.json (from the game's UI source) and hotbuild2_layout.pas
(Hotbuild2 import format: hotbuild slots + every game keybind), then renders KEYS.md.
Safe to run while the game is open: it only reads a copy of the storage.
"""
import json, os, re, struct

PA_GAME = os.path.expanduser("~/.local/share/Steam/steamapps/common/Planetary Annihilation Titans")
PA_DATA = os.path.expanduser("~/.local/Uber Entertainment/Planetary Annihilation")
STORAGE = f"{PA_DATA}/localstore/cef/Default/Local Storage/leveldb"
HERE = os.path.dirname(os.path.abspath(__file__))


def game_defaults():
    text = open(f"{PA_GAME}/media/ui/main/shared/js/api/settings.js").read()
    out = {}
    for name, body in re.findall(r"\n {20}(\w+): \{(.*?)\n {20}\}", text, re.S):
        if "type: 'keybind'" not in body:
            continue
        get = lambda f: ((re.search(rf"{f}: '([^']*)'", body) or [None, ""])[1]).replace("!LOC:", "")
        out[name] = {"default": get("default"), "group": get("display_group"),
                     "sub_group": get("display_sub_group"), "title": get("title")}
    live = len(re.findall(r"^\s*type: 'keybind'", text, re.M))  # skips commented-out entries
    assert len(out) == live, (len(out), live)
    return out


def varint(b, i):
    r = s = 0
    while True:
        c = b[i]; i += 1; r |= (c & 0x7f) << s; s += 7
        if c < 0x80:
            return r, i


def local_storage():
    """Decode the newest localStorage values from the LevelDB write-ahead log."""
    # shortcut: reads only *.log, not the snappy-compressed *.ldb tables; fine while the game
    # keeps rewriting these keys on save, upgrade if the asserts below ever fire.
    kv = {}
    for log in sorted(f for f in os.listdir(STORAGE) if f.endswith(".log")):
        data, recs, buf, pos = open(f"{STORAGE}/{log}", "rb").read(), [], b"", 0
        while pos + 7 <= len(data):
            if 32768 - pos % 32768 < 7:
                pos += 32768 - pos % 32768; continue
            ln, typ = struct.unpack_from("<HB", data, pos + 4)
            frag = data[pos + 7:pos + 7 + ln]; pos += 7 + ln
            if typ == 0:
                continue
            buf = frag if typ in (1, 2) else buf + frag
            if typ in (1, 4):
                recs.append(buf); buf = b""
        for r in recs:
            i = 12
            for _ in range(struct.unpack_from("<I", r, 8)[0]):
                t = r[i]; i += 1
                kl, i = varint(r, i); k = r[i:i + kl]; i += kl
                if t == 1:
                    vl, i = varint(r, i); kv[k] = r[i:i + vl]; i += vl
                else:
                    kv.pop(k, None)
    dec = lambda v: v[1:].decode("utf-16le") if v[:1] == b"\x00" else v[1:].decode("latin-1")
    return {k.split(b"\x00\x01", 1)[1].decode("latin-1"): dec(v) for k, v in kv.items() if b"\x00\x01" in k}


if __name__ == "__main__":
    defaults = game_defaults()
    ls = local_storage()
    assert "hotbuildconfig" in ls and "hotbuildconfigkey" in ls, "hotbuild keys not in the .log"
    settings = [v for k, v in ls.items() if k.endswith(".paSettings")]
    assert len(settings) == 1, "expected one PA account's settings"
    saved = json.loads(settings[0]).get("keyboard", {})
    # the game stores only changed binds; everything else falls back to the default
    uber = [{"key": k, "value": saved.get(k, d["default"])} for k, d in defaults.items()]
    uber += [{"key": k, "value": v} for k, v in saved.items() if k not in defaults]
    layout = {"hotbuildglobalkey": json.loads(ls["hotbuildconfigkey"]),
              "hotbuildglobal": json.loads(ls["hotbuildconfig"]), "uber": uber}
    json.dump(defaults, open(f"{HERE}/game_default_keys.json", "w"), indent=1)
    json.dump(layout, open(f"{HERE}/hotbuild2_layout.pas", "w"), indent=1)
    import render
    render.main()
