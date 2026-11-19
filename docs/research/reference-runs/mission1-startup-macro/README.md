# Starting with a macro: DOS observations

`WP /m-TESTMAC` starts the pinned DOS release and immediately
runs the [recorded TESTMAC.WPM](TESTMAC.WPM) in the WP program
directory. The macro writes `ABC` on the untouched first document.
F10 produces a native save with the same three-byte body.
[Startup screen](startup.txt) · [Native save](START.WP)

Wordling Linux accepts `wordling /m-TESTMAC` and
`wordling -macro TESTMAC`. It uses its existing workspace macro
resolver and runtime. The terminal replay passes without changing
the source macro and matches the original native document body.

Other startup switches, historical resource search paths, and
macros outside the admitted runtime profile remain open. Run
`replay.py` from the repository root with `PYTHONPATH=scripts/reference`.
