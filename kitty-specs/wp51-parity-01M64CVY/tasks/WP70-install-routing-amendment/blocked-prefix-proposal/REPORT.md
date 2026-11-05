# STATIC09 — plain prefix BLOCKED; no source or runtime changes

The nine exact already-selected primary sources (211,619 bytes) prove that ordinary system pip `--prefix=<freshvenv> --ignore-installed` cannot meet the frozen installed layout. System sysconfig.py52–62,322–349 selects posix_local and installs under `<prefix>/local/lib/python3.12/dist-packages`; required layout remains `<venv>/lib/python3.12/site-packages`. No relocation, scheme monkeypatch, symlink overlay or changed checker is proposed.

Public prefix correctly bypasses the current-environment PEP668 check (install.py270–285); it disables user-install fallback (694–700). Ignore-installed reaches the selected resolver: factory.py122–129 empties installed distributions,610–614 yields no uninstall, resolver.py129–132 selects installation without entering already-installed-wheel skip branch. These are static source facts, not a qualified execution.

User scheme has the correct site-packages suffix and deterministic PYTHONUSERBASE, but `--user` alone does not bypass PEP668. A possible normal public `--user --root=/ --ignore-installed` route is explicitly UNRESOLVED, not a selected winning route or permission to use --break-system-packages. Exact root=/ identity source proof is separately requested; no unapproved payload read occurred.

Custody metadata preserves old190 files/11,684,080B plus prospective79/112,607,232B =269/124,291,312B; current256 file limit cannot fit. No task amendment/source grant/attempt assumed. Three full historical DATA inventories76+127+196=399 entries/nine exact roots and flat subsets remain mandatory before guardian. Old failed runtime trees never startup/code/provider inputs. Current E1281/25,461,100B and all old payloads/seals/UNKNOWNs stay literal.

All unchanged time/output/memory/family bounds remain conditional finite limits, not guaranteed successful fit. No source write/import/probe/command/runtime/P/Original/proc/network/native/canonical/commit effects. HOLD for ROOT and independent static review.
