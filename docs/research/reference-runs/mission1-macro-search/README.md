# Forward search during a WordPerfect 5.1 macro

- The original [failed search](../2026-10-29-advanced-04/CMD51-178)
  stops after typing `BEFORE`. The operator types `READY` after the
  stop to confirm that control has returned to the editor.
- The original [ON NOT FOUND macro](../2026-10-29-advanced-04/CMD51-206)
  jumps to the handler and saves `BEFOREHANDLED` when `ABSENT` cannot
  be found.
- To repeat the same macro with a real match, type `ABSENT tail`,
  press Home, Home, Up and run `HANDLER.WPM` with Alt+F10. It inserts
  `BEFORE`, finds `ABSENT` and continues by typing `SHOULDNOT`.
  Type `X` at the resulting cursor and save. [FOUND.WP](FOUND.WP)
  contains `BEFOREABSENTSHOULDNOTX tail`. [DOS screen](found.txt)

Wordling reproduces these native document bodies through its ordinary
forward search. The qualification compares the body bytes and verifies
that the WPMs remain unchanged. [Linux terminal qualification](../../../../tests/everyday_qualification/macro_control.py)
