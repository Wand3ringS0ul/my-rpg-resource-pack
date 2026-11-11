# Dungeons and Dragon Ballz V3 — RPG Companion 5e expansion

## Status
Conversion workspace prepared; **not yet compiled or hosted**. This public repository does **not** currently contain a working RPG Companion release.

The conversion contains 542 5e resource candidates (18 races, 10 classes, 473 feats/reference entries, 23 items, 12 weapons, 6 armor). JSON syntax checks passed; compilation and app imports are unverified.

## How to finish publishing

1. Download the **DBZ V3 GitHub Publishing Kit ZIP** from the ChatGPT conversation and extract it.
2. Read its `PUBLISHING_STEPS.md`. On Windows, run `01_prepare_workspace.ps1` to combine the official 5e system with the converted resources (or manually copy the resource files into the official source's `systems/5e/resource_instances/` directory).
3. In the official RPG Companion Dev Tool, select the prepared `systems` folder and choose **Create Release Package**.
4. Check the generated output root contains `systems.json`, `systems.rpg`, and `5e/`.
5. Upload those **compiled output contents** to this GitHub repository root. Alternatively, run the kit's `02_publish_release.ps1` after reviewing its safety check.
6. Enable GitHub Pages under Settings > Pages, branch `main`, folder `/(root)`.
7. In RPG Companion settings, add the deployed GitHub Pages URL as a resource repository and fetch resources.

Official guide: https://docs.rpg-companion.app/GettingStarted/HostingAResourceRepo

## Rights and limitations

This is derived from a third-party fan rulebook and Dragon Ball media. **Confirm permission to redistribute the source creator's descriptions before uploading them publicly.** The publishing kit omits the original PDF and complete extracted book. The source conversion does not automate all Ki, Stamina, transformations or alternate combat mechanics within stock 5e.
