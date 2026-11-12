#!/usr/bin/env python3
"""Validate the curated game dataset. Uses Python stdlib only."""
from pathlib import Path
from collections import Counter
import json, csv

root = Path(__file__).resolve().parents[1]
d = json.loads((root/"data/games.json").read_text(encoding="utf-8"))
games = d["games"]
fields = ["id","name_zh","name_en","steam_year","category","scope",
          "pressure","companionship","low_distraction","description",
          "insight","tradeoff","source"]
assert len(games) == 32, "Unexpected count: update snapshot & validation when adding games"
assert len(d["categories"]) == 7
assert len({g["id"] for g in games}) == len(games)
for g in games:
    assert set(fields) == set(g), f"Missing/unexpected keys: {g}"
    assert g["id"].isdigit()
    assert g["category"] in d["categories"]
    assert g["scope"] in d["scopes"]
    assert 2000 <= g["steam_year"] <= 2030
    assert all(type(g[k]) is int and 0 <= g[k] <= 5
               for k in ("pressure","companionship","low_distraction"))
    assert g["source"] == f"https://store.steampowered.com/app/{g['id']}/"
    assert all(g[k].strip() for k in ("name_en","name_zh","description","insight","tradeoff"))
with (root/"data/games.csv").open(encoding="utf-8", newline="") as f:
    reader = csv.DictReader(f)
    assert reader.fieldnames == fields, "CSV schema mismatch"
    rows = list(reader)
assert len(rows) == len(games), "JSON/CSV length mismatch"
for i,(a,b) in enumerate(zip(games,rows)):
    for k in fields:
        assert str(a[k]) == b[k], f"row {i+1} mismatch for {k}"
print(f"VALID: {len(games)} games; {len(d['categories'])} categories")
print("categories:", dict(Counter(g["category"] for g in games)))
print("scopes:", dict(Counter(g["scope"] for g in games)))
