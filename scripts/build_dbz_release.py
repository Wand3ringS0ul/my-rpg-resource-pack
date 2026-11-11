#!/usr/bin/env python3
"""Create a hosted RPG Companion 5e resource pack using the official compiled 5e system."""
import argparse
import gzip
import io
import json
import tarfile
import urllib.request
import uuid
from pathlib import Path

BASE = "https://d2dmd8x0lyn9l8.cloudfront.net/5e/system.rpg"

def jbytes(obj):
    return (json.dumps(obj, indent=2, ensure_ascii=False) + "\n").encode("utf-8")

def gzip_json(obj):
    return gzip.compress(jbytes(obj), compresslevel=9, mtime=0)

def build(source, output, official_file=None):
    files = sorted(source.glob("*.rpg.json"))
    assert len(files) == 542, f"Expected 542 source resources; got {len(files)}"
    if official_file:
        official = Path(official_file).read_bytes()
    else:
        req = urllib.request.Request(BASE, headers={"User-Agent": "RPG-Companion-Resource-Pack"})
        with urllib.request.urlopen(req, timeout=45) as response:
            official = response.read()
    if not official.startswith(bytes((31, 139))):
        raise RuntimeError("Official system file is not a gzip-encoded .rpg file")
    system = json.loads(gzip.decompress(official))
    if system.get("id") != "5e":
        raise RuntimeError("Official RPG file does not contain the 5e system")
    meta = {k: system[k] for k in ("id", "name", "abbreviation", "version", "min_app_version")}
    meta["path"] = "5e"
    (output / "5e" / "resources").mkdir(parents=True, exist_ok=True)
    (output / "5e" / "system.rpg").write_bytes(official)
    (output / "systems.json").write_bytes(jbytes({"systems": [meta]}))
    (output / "systems.rpg").write_bytes(gzip_json({"systems": [meta]}))
    (output / ".nojekyll").touch()
    resources = []
    known_ids = set()
    collisions = []
    for file in files:
        entry = json.loads(file.read_text(encoding="utf-8"))
        if entry.get("resource_id") not in {"race", "class", "feat", "item", "weapon", "armor"}:
            raise RuntimeError(f"Unknown resource type in {file.name}")
        if entry.get("system") not in ("5e", None):
            raise RuntimeError(f"Wrong system for {file.name}")
        entry["system"] = "5e"
        stats = entry.get("stats") or {}
        name = (stats.get("name") or {}).get("value")
        if not isinstance(name, str) or not name.strip():
            raise RuntimeError(f"Missing name for {file.name}")
        resource_id = stats.get("id")
        if not isinstance(resource_id, str) or not resource_id.strip():
            raise RuntimeError(f"Invalid ID for {file.name}")
        if resource_id in known_ids:
            collisions.append({"file": file.name, "old_id": resource_id})
            resource_id = str(uuid.uuid5(uuid.NAMESPACE_URL, "dndbz-v3/5e/" + file.name))
            stats["id"] = resource_id
        if resource_id in known_ids:
            raise RuntimeError("Unable to resolve resource ID conflict")
        known_ids.add(resource_id)
        rel = "resources/" + file.name.removesuffix(".json") 
        target = output / "5e" / rel
        target.write_bytes(gzip_json(entry))
        timestamp = (stats.get("updated_at") or {}).get("value", "2026-11-11T00:00:00")
        timestamp = timestamp.removesuffix("Z")
        resources.append({"id": resource_id, "name": name, "path": rel, "updated_at": timestamp})

    index = {"resources": resources}
    (output / "5e" / "resources.json").write_bytes(jbytes(index))
    (output / "5e" / "resources.rpg").write_bytes(gzip_json(index))
    with tarfile.open(output / "5e" / "resources.rpg.gzip", "w:gz", format=tarfile.USTAR_FORMAT) as archive:
        for item in resources:
            p = output / "5e" / item["path"]
            blob = p.read_bytes()
            info = tarfile.TarInfo(item["path"])
            info.size = len(blob)
            info.mode = 0o644
            info.mtime = 0
            archive.addfile(info, io.BytesIO(blob))

    back = json.loads(gzip.decompress((output / "5e" / "resources.rpg").read_bytes()))
    assert len(back["resources"]) == len(files)
    for item in resources:
        dest = output / "5e" / item["path"]
        assert dest.is_file()
        loaded = json.loads(gzip.decompress(dest.read_bytes()))
        assert loaded["stats"]["id"] == item["id"]
    with tarfile.open(output / "5e" / "resources.rpg.gzip", "r:gz") as tar:
        assert len(tar.getmembers()) == len(files)
    print(f"RELEASE PASS: {len(files)} resources; system version {meta['version']}; {len(collisions)} duplicate IDs corrected")
    print("Resource counts by type:", {t: sum(1 for f in files if json.loads(f.read_text()).get("resource_id") == t) for t in ("race","class","feat","item","weapon","armor")})
    if collisions:
        print("Resolved duplicate IDs:", collisions)
    print("Static release ready at", output.resolve())

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default="systems/5e/resource_instances")
    parser.add_argument("--output", default="release-site")
    parser.add_argument("--official-system", default=None)
    args = parser.parse_args()
    build(Path(args.source), Path(args.output), args.official_system)
