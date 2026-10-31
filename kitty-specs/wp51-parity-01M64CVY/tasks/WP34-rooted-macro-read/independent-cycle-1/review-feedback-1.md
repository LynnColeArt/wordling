# WP34 review feedback, cycle1

## Issue1 — P2: returned Image pointer permits rebinding the owned snapshot

- **Location:** internal/storage/macro_linux.go:15, Macro.Image.
- **Contract:** Macro/ReadMacro immutable source snapshot and exact source identity,
  WP32 additions-to-storage API; T100/T101 copy/identity boundary.
- **Trigger:** ReadMacro successfully acquires an original WPM, then a caller uses
  legal Go assignment `*macro.Image() = wpm.Image{}` or assigns a second valid
  parsed Image through that pointer.
- **Observed:** Macro.Export/image hash changes, but Macro.Identity continues to
  report the original acquired file/hash. Both independent public-API tests fail
  against source0793933. This is not a future filesystem freshness guarantee.
- **Fix:** retain the approved signature, but return an independent Image value
  wrapper/copy so replacing a returned pointer's whole value cannot change the
  owned snapshot. Keep codec/storage acquisition/publication contracts unchanged.
- **Validation:** add public-API zero assignment and valid-image substitution tests
  and assert original Export, Identity, Name/DirectoryID and subsequent Image views
  remain unchanged. Reproducer/source bindings and passing baseline checks are in
  independent-cycle-1/. Rerun meaningful changed tests, real build/test/vet/race and
  configured checks. No redundant parser fuzz/VM is required for this wrapper fix.

No other actionable finding. Full macro execution and FR/M1 completion remain open.
