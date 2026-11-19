# Named styles: DOS observations

Alt+F8, Create (3) opens the style form. Name (1) sets the name;
Codes (4) opens a separate editor. F6 adds Bold, then F7 returns
to the form and a second F7 commits the definition. Attempting to
name another style `wptest` when `WPTEST` exists shows
`ERROR: Style name already exists`.

The original session with its bundled library is retained as
[STYLE.WP](STYLE.WP). The isolated [BOLD.WP](BOLD.WP) was created
with Fast Save disabled and without the bundled library in the
private guest copy. Its compact prefix contains the definition
packet, and the document body embeds linked style on/off owners
and their Bold codes. Its [Standard Printer stream](BOLD.PRN)
matches Wordling.

Wordling creates and applies this compact paired Bold profile.
It retains the names and cached words in existing files and writes
zero cache words for newly created definitions. DOS retrieved a
Wordling save and listed EMPHASIS as Paired. The broader library,
other style types and operations, and styles with arbitrary codes
remain open.

[Name](named.txt) · [Code editor](codes.txt) · [Style list](created.txt) ·
[Duplicate name](duplicate.txt)

Run the replay scripts with `PYTHONPATH=scripts/reference` from the
repository root. `replay-paired.py` writes its isolated result as
`STYLE.WP` in the run directory.
