# Resolved personal-setup byte variation

The differing byte at file offset **1366 (`0x556`)** is the low byte of the
**cached printer modification-time word**, not a random identifier or an
unexplained format change. Original setup files and immutable masters have not
been normalized or altered.

## Documentary and independent binary evidence

The checksum-pinned [WordPerfect Developer’s Toolkit, Appendix A p. 8,
PDF 507](https://mendelson.org/wpdos/WP51DevelopersToolkit.pdf#page=507) describes
Default Printer packet **54h**. It places the printer filename at packet offset
37, the Date word at 237, and the Time word at 239. Appendix A starts at PDF
500; the main WordPerfect section's printed/PDF offset does **not** apply here.
This later toolkit is corroborated against the actual March executable's files.

The SET index chain places packet 54h at **1127**, so its Time word starts at
`1127 + 239 = 1366`. The packet names `STANPRIN.PRS`. An independent FAT16 reader
locates that file's directory entry, reads its modification date/time, and hashes
its contents without relying on host extraction timestamps.

| Installation | SET Time word | Decoded time | Printer FAT time |
| --- | --- | --- | --- |
| Original master | `0x608A` | `12:04:20` | `12:04:20` |
| Independent rebuild | `0x6009` | `12:00:18` | `12:00:18` |

Both dates are `0x1869`, or 1992-03-09. The time-word high byte is `60` in both
files, explaining why only one SET byte differed. DOS time stores hours in bits
15–11, minutes in 10–5, and seconds divided by two in 4–0. Both printer files have
SHA-256 `5bbb555348f91642e3229b4ea37e18bdd2c7e42b7cc095f82a53fd109ec2f74e`.
The discrepancy tracks the time the installer generated the printer definition;
it does not imply different printer contents.

## Controlled experiment

[Machine-readable report and captured exits](setup-timestamp-02/report.json).
The experiment creates three new disposable copies of the pinned master. The
control changes no bytes. The treatment changes only the printer's FAT directory
modification-time field to `0x60E0` (`12:07:00`); its date, name, contents, the
initial SET, and boot clock remain unchanged. All copies run the original WP
and exit normally to DOS before offline inspection. Each input image and emulator
profile is fingerprinted; scripts and captures are archived with the report.

The second treatment explicitly reselects Standard Printer using Shift+F7,
S, 1, F7 before exit. The results distinguish three cases:

| Trial | Cached time after normal exit |
| --- | --- |
| Unmodified control | `12:04:20`, unchanged |
| Printer FAT time changed; idle session | `12:04:20`, unchanged and now stale |
| Same FAT change; explicit printer selection | **`12:07:00`**, matching the changed file |

The selection treatment changes only SET byte 1366, from `8A` to `E0`; file size,
printer contents and the immutable master remain unchanged. The report records
all SET byte differences rather than filtering them to the expected field.
This confirms both the field interpretation and the observed refresh trigger.
It does not claim that selection is the only operation capable of refreshing it.
The initial hypothesis that an idle launch/exit refreshes the cache was refuted;
that negative result is reproduced as a treatment in the published experiment.

Reproduce with a new ID, with no reference guest already running:

```sh
python3 scripts/reference/setup_experiment.py setup-timestamp-your-unique-id
```

Inspect any stopped reference image independently:

```sh
python3 scripts/reference/inspect_setup.py path/to/harddisk.img
```

## Consequences

Keep exact SET fingerprints as part of each mutable profile. Installer execution
time need not be bit-identical for the installed program and resources to match.
This is an explained cache-field variation, not permission to ignore arbitrary
SET differences or weaken Wordling's untouched-input byte-preservation contract.
