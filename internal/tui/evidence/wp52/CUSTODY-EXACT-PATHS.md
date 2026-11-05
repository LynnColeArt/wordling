# Exact raw artifact paths

The final .gitattributes replaces the initial generic log whitespace setting with
seven exact raw paths: the two CPU benchmark outputs, two Go buildinfo outputs,
profile table/stderr and the retained failed lint containing those literal raw
lines. No source, Go tests, general logs, Python scripts or future paths receive
whitespace suppression. This attribute metadata is outside any frozen PTY raw
roster and never changes captured bytes. Previous202 and206-record manifests and
attributes remain exact in Git and history/custody-cycle1 andcycle2. The current
successor manifest explicitly binds both predecessors and all current paths.
Production/test/raw/binary source SHA values remain unchanged; only attributes,
this custody explanation, predecessor archives and manifest change.
