# Dungeons and Dragonballz V3 — RPG Companion 5e expansion

## Publication status

**Compiled release: STAGED on the [gh-pages branch](https://github.com/Wand3ringS0ul/my-rpg-resource-pack/tree/gh-pages).**

- The main branch contains 542 converted `.rpg.json` resources and the automated release builder.
- The `gh-pages` branch now contains all 542 gzip-encoded resource files, the compressed resource index and tar archive, `systems.json`, `systems.rpg`, and the **official 5e v0.9.1 system**.
- The builder corrected one duplicate resource ID in its generated release; source entries remain unchanged.
- All 542 JSON payloads passed packaging and structural tests. **An in-app import has not been tested.**
- **GitHub Pages is not yet enabled**, so do not treat the future site URL as live.

### One GitHub setting still required

Open **[Settings → Pages](https://github.com/Wand3ringS0ul/my-rpg-resource-pack/settings/pages)**. Under **Build and deployment**, choose:

1. **Source:** Deploy from a branch
2. **Branch:** `gh-pages`
3. **Folder:** `/(root)`
4. Click **Save**.

After GitHub confirms publication, your intended resource repository URL is:

https://wand3rings0ul.github.io/my-rpg-resource-pack/

Check `https://wand3rings0ul.github.io/my-rpg-resource-pack/systems.json` loads before adding the repository in RPG Companion.

### Build and update

Every time you modify `systems/5e/resource_instances/`, [Build and publish Dragonballz V3 RPG Companion pack](https://github.com/Wand3ringS0ul/my-rpg-resource-pack/actions/workflows/build-deploy-dbz.yml) rebuilds the compatible output and pushes it to `gh-pages`.

The `gh-pages` branch is automatically generated. **Do not manually edit compiled files on that branch.**

This release is packed using the publicly documented compressed JSON structure and the unmodified official compiled 5e system, rather than running the desktop Dev Tool. In-app testing is still required to verify that each custom resource is interpreted correctly. Rules such as alternate Ki/Stamina/Power tracking and transformations are not automatically enforced by the base 5e engine.

### Included converted entries

| Type | Count |
|---|---:|
| Races | 18 |
| Classes | 10 |
| Feats and other reference entries | 473 |
| Items | 23 |
| Weapons | 12 |
| Armor | 6 |
| **Total** | **542** |

## Attribution and rights

This conversion is based on a **third-party fan-created** Dungeons and Dragonballz V3 rulebook. The original creator and the relevant D&D and Dragon Ball rights holders retain their rights. Verify that you have permission to redistribute the original descriptions publicly. RPG Companion's official system sources and their licenses are available at https://github.com/blastervla/rpg-companion-app-systems.

Useful documentation: https://docs.rpg-companion.app/GettingStarted/HostingAResourceRepo.
