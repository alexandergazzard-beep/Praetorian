"""Organize reference copies and catalogue, preserving originals and image bytes."""
import csv
import hashlib
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets/concepts/debris"
DEST = SOURCE / "by_size"
folders = {
    "small": ("01_small", "0.2-0.8 m"),
    "medium": ("02_medium", "1-3 m"),
    "large": ("03_large", "4-8 m"),
    "very_large": ("04_very_large", "12-25 m"),
    "enormous": ("05_enormous", "40-70 m"),
}
catalogue = []
checks = []

def copy(source, target):
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
    assert digest(source) == digest(target)
    checks.append({"source": str(source.relative_to(ROOT)), "copy": str(target.relative_to(ROOT)), "sha256": digest(target)})

def group(sheet, tier, entries, status, name=None):
    folder, size = folders[tier]
    filename = name or sheet
    copy(SOURCE / sheet, DEST / folder / filename)
    for ident, position, prop in entries:
        catalogue.append({"id": ident, "size_tier": tier, "proposed_longest_dimension": size,
                          "prop": prop, "reference_file": f"{folder}/{filename}",
                          "sheet_position": position, "design_status": status,
                          "model_status": "not generated", "geometry_rule": "visible shell, shallow damage; no full interiors"})

group("debris_d6_small_scatter_six_v1.png", "small", [
    ("S01", "top left", "Bent armor shard"), ("S02", "top middle", "Small electrical box"),
    ("S03", "top right", "Conduit elbow"), ("S04", "bottom left", "Vent grille"),
    ("S05", "bottom middle", "Broken keypad"), ("S06", "bottom right", "Mounting bracket and plate"),
], "new concept awaiting review")
group("debris_d7_medium_parts_six_v1.png", "medium", [
    ("M01", "top left", "Engine cowling"), ("M02", "top middle", "Floor grating panel"),
    ("M03", "top right", "Closed equipment cabinet"), ("M04", "bottom left", "Detached armored hatch panel"),
    ("M05", "bottom middle", "Snapped support beam"), ("M06", "bottom right", "Vented transport skin panel"),
], "new concept awaiting review")
group("debris_d2_ship_transport_six_pieces_v1.png", "medium", [
    ("M07", "top left", "Heavy hull plate"), ("M08", "top middle", "Interior wall panel"),
    ("M09", "top right", "Electrical assembly"), ("M10", "bottom left", "Broken console"),
], "D2 sheet approved; exact size proposed", "d2_USE_TOP_ROW_AND_BOTTOM_LEFT.png")
group("debris_d2_ship_transport_six_pieces_v1.png", "large", [
    ("L01", "bottom middle", "Transport wing fragment"), ("L02", "bottom right", "Transport engine section"),
], "D2 sheet approved; exact size proposed", "d2_USE_BOTTOM_MIDDLE_AND_RIGHT.png")
group("debris_d5_armored_exterior_engines_v1.png", "very_large", [
    ("VL01", "top left", "Detached engine nacelle"), ("VL02", "top right", "Broken nozzle casing"),
], "D5 revised sheet approved; exact size proposed", "d5_USE_TOP_ROW.png")
group("debris_d5_armored_exterior_engines_v1.png", "enormous", [
    ("E01", "bottom left", "Armored aft engine cluster"), ("E02", "bottom right", "Armored stern wreck"),
], "D5 revised sheet approved; exact size proposed", "d5_USE_BOTTOM_ROW.png")

group("debris_d8_medium_mechanical_six_v1.png", "medium", [
    ("M11", "top left", "Crushed armored crate"), ("M12", "top middle", "Engine intake cowling"),
    ("M13", "top right", "Curved hull corner"), ("M14", "bottom left", "Landing support strut"),
    ("M15", "bottom middle", "Paired conduit rack"), ("M16", "bottom right", "Damaged sensor unit"),
], "new concept awaiting review")

group("debris_d9_cargo_hangar_six_v1.png", "medium", [
    ("M17", "top left", "Infantry supply trunk"), ("M18", "top middle", "Cargo pallet"),
    ("M19", "top right", "Loading ramp section"), ("M20", "bottom left", "Reactor-service module"),
    ("M21", "bottom middle", "Cargo locking rail"), ("M22", "bottom right", "Broken troop seat"),
], "new concept awaiting review")

group("debris_d10_ground_electronics_six_v1.png", "small", [
    ("S07", "top left", "Ground cable harness"), ("S08", "top right", "Flat access cover"),
    ("S09", "bottom middle", "Fallen keyboard/control pad"), ("S10", "bottom right", "Circuit module on tray"),
], "new concept awaiting review", "d10_USE_TOP_LEFT_RIGHT_AND_BOTTOM_MIDDLE_RIGHT.png")
group("debris_d10_ground_electronics_six_v1.png", "medium", [
    ("M23", "top middle", "Fallen monitor"), ("M24", "bottom left", "Computer equipment chassis"),
], "new concept awaiting review", "d10_USE_TOP_MIDDLE_AND_BOTTOM_LEFT.png")
copy(SOURCE / "debris_d10_ground_electronics_six_v1.png", DEST / "06_ground_scatter" / "debris_d10_ground_electronics_six_v1.png")
ground = [r for r in catalogue if r["id"] in {"S07", "S08", "S09", "S10", "M23", "M24"}]
ground_lines = ["# Ground electronics scatter", "", "Low-profile fallen wires, monitors and computer parts. Also listed in small/medium folders; these are the same six catalogue entries, not extra models.", "", "| ID | Prop | Sheet position | Size tier |", "| --- | --- | --- | --- |"]
ground_lines += [f"| {r['id']} | {r['prop']} | {r['sheet_position']} | {r['size_tier']} |" for r in ground]
ground_lines += ["", "[Reference sheet](debris_d10_ground_electronics_six_v1.png). Concepts awaiting review. Use shallow backs and simple broad components. Fine circuit traces/pins belong primarily in texture/normal detail. One isolated prop per model task; no ground-plane/base mesh.", ""]
(DEST / "06_ground_scatter" / "README.md").write_text("\n".join(ground_lines), encoding="utf-8")

for sheet in SOURCE.glob("*.png"):
    copy(sheet, DEST / "00_master_sheets" / sheet.name)
for sheet in ["debris_d1_ship_starter_v1.png", "debris_d3_five_scale_tiers_v1.png", "debris_d4_aft_engine_wreckage_v1.png"]:
    copy(SOURCE / sheet, DEST / "99_earlier_explorations" / sheet)

for row in catalogue:
    if row['id'] in {'M17','S04'}:
        row['model_status']='Meshy generated; Blender prepared; imported and placed in Unreal; review pending'
fields = list(catalogue[0])
with (DEST / "asset_catalogue.csv").open("w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    writer.writerows(catalogue)

for tier, (folder, size) in folders.items():
    items = [r for r in catalogue if r["size_tier"] == tier]
    lines = [f"# {tier.replace('_', ' ').title()} debris references", "", f"Suggested longest dimension: **{size}**. These are planning ranges, not accepted or measured dimensions.", "",
             "Images remain full sheets to preserve the original art. Use only the positions listed below; the other objects may belong to another tier. Each eventual 3D job should use an isolated single-prop reference, not the entire sheet.", "",
             "| ID | Prop | Sheet position | Image | Review |", "| --- | --- | --- | --- | --- |"]
    lines += [f"| {r['id']} | {r['prop']} | {r['sheet_position']} | [{Path(r['reference_file']).name}]({Path(r['reference_file']).name}) | {r['design_status']} |" for r in items]
    lines += ["", "Keep mostly closed exterior shells with shallow backed damage and local electronics. No full rooms, doors/decks or hidden interiors. A detached hatch panel is a standalone prop, not an open doorway. Verify actual mesh counts, collision and scale after generation.", ""]
    (DEST / folder / "README.md").write_text("\n".join(lines), encoding="utf-8")

lines = ["# Debris reference library by size", "", "Created 2026-10-07. Originals are preserved in the parent directory. This library organizes byte-identical reference copies, not 3D models.", "",
         "| Folder | Proposed longest dimension | Catalogue candidates |", "| --- | --- | --- |"]
lines += [f"| [{folder}]({folder}/README.md) | {size} | {sum(r['size_tier'] == tier for r in catalogue)} |" for tier, (folder, size) in folders.items()]
lines += ["", f"[Asset catalogue](asset_catalogue.csv) identifies each prop and its position in the full sheet. There are {len(catalogue)} reference candidates, including {sum(r['design_status'] == 'new concept awaiting review' for r in catalogue)} new small/medium concepts awaiting review. Exact dimensions and geometry budgets remain open.", "",
          "00_master_sheets contains all original sheet copies for context. 99_earlier_explorations preserves earlier concepts; D3/D4 enormous room/deck cutaways are superseded by the exterior-only D5 direction. D1 is earlier exploration history, not a separate current production queue.", "",
          "For modeling: isolate one chosen prop, confirm scale, generate/prepare it, then inspect topology, visible silhouette, collision and materials. Keep outer armor; show shallow electronics at damage rather than rooms or deep internals. Use texture/normal detail where practical. No assets have been generated or imported by this organizing step.", ""]
lines += ["[Ground scatter collection](06_ground_scatter/README.md) cross-references fallen electronics from the small and medium folders.", "", "Production update 2026-10-08: M17 supply trunk and S04 grille have actual Meshy models, separate Blender sources/game exports, and Unreal imports. See docs/DEBRIS_FIRST_PAIR_BUILD_REPORT.md in the project root for QA; all other candidates remain references.", ""]
(DEST / "README.md").write_text("\n".join(lines), encoding="utf-8")
report = {"catalogue_candidates": len(catalogue), "copied_images": len(checks), "all_copy_hashes_verified": True, "originals_preserved": True, "checks": checks}
(ROOT / "reports/debris_library_organization.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps({k: report[k] for k in ["catalogue_candidates", "copied_images", "all_copy_hashes_verified", "originals_preserved"]}))
