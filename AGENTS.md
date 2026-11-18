<!-- spec-kitty:orientation -->
**Spec Kitty v3.2.7** — project: unknown (healthy)

Two usage patterns:
- **Full mission** (spec → plan → tasks → implement → review → merge):
  trigger: "spec out", "create a mission", "write a spec", "plan this"
  → run `/spec-kitty.specify`
- **Lightweight dispatch** (ad-hoc fix, question, or advice — no mission created):
  trigger: "hey spec kitty", "use spec kitty to", "spec kitty <anything>"
  → **ALWAYS run `spec-kitty dispatch "<request verbatim>"` — do NOT answer directly.**
  If you know the right profile, pass it to skip routing:
  `spec-kitty dispatch "<request verbatim>" --profile <profile-id>`
  Reason: `spec-kitty dispatch` loads governance context, routes the request,
  and opens the Op. Skipping it produces ungoverned, untracked responses.
  After finishing the work, close the Op with the command printed in the capsule
  (`spec-kitty profile-invocation complete --invocation-id <id> --outcome <done|failed|abandoned>`).
<!-- /spec-kitty:orientation -->

## Wordling mission runtime

Mission commands use the independently reviewed local source repair:

```bash
env SPEC_KITTY_ENABLE_SAAS_SYNC=0 \
  PYTHONPATH=/tmp/wordling-spec-kitty-planning-epochs-20261118/src \
  /home/lynn/projects/spec-kitty/.venv/bin/python -m specify_cli <command>
```

Source head: `ec868755fa640238b4bdb98f957e948f28abdc0e` (approved executable
candidate `8315a288`). This contains the earlier large-WP-ID/retry repair and the
reviewed planning-stage repair. The installed distribution banner is3.2.6;
the selected source derives from3.2.7 plus these local repairs. Global/shared
installations are unchanged. Keep explicit per-process local mode; hosted v2
delivery is outside this repair.

The v2 planning-stage manifest deliberately refuses older readers, including the
previous b45 source. Preserve this source pin for live mission operations.
Exact source hashes, independent reviews, host checks and a clean-restore-tested
Git bundle are in `docs/reviews/spec-kitty-planning-stages-2026-11-18/`.
The tracked bundle restores the complete local repair history if `/tmp` is lost;
its required upstream base and MIT license are documented beside it.
