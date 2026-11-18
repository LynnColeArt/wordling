---
type: reference
updated: 2026-11-18
audience: Wordling release operator
---
# Mission 1 recovery checkpoint

PR12 is merged into `fix/native-prerelease-builds` at `40ce35b86afc93710aa12fa12891c85e8360ffaa`; its reviewed production source is incorporated in `feat/wp51-parity`. The independent review and native Linux/Windows/macOS CI evidence are in `docs/reviews/pr12-2026-11-18/`. PowerShell defaults and Windows save-overwrite support are part of that merged baseline.

WP100 is now independently approved through Spec Kitty's durable review event `01M7Q8AXKV5THKECEEEQSEXJNV`. It admits authenticated nested macros on genuinely New documents, preserving existing text, native history, source provenance and first-save behavior. Source candidate `64025299`, evidence `4a232947`; review and baseline are under the canonical WP100 task directory. Full Linux tests, ownership race checks, build/vet and Windows app build/production vet passed. Four existing environment/platform test skips and the pre-existing broad Windows research-helper vet failure are explicitly recorded; the sixteen production dependencies vet cleanly.

Fresh engineering packages for Linux amd64 and Windows amd64/arm64 are in `bin/wp100-6b399840/`. Their normal app builds have no QA save-fault instrumentation; compiled inputs and package members have verified hashes. Packaged Linux filesystem/save/overwrite/recovery smoke tests and CLI startup passed, with the expected Windows-namespace test skipped on Linux. The Windows packages are cross-built here; no new native Windows execution is claimed for WP100. Package manifests are beside this report.

**Full Mission1 and ticket7 remain open.** The command audit remains186 verified /38 partial /20 unimplemented, and the canonical acceptance matrix remains pending. The four macro rows need fresh original unsaved-New comparisons and original reopen/edit/print/save evidence before promotion. The original controller currently admits TEST fixtures; the proposed genuine-original route needs a concrete ROOT release entry and closed CONTROL profile reviewed before source work and later original execution. WP101/102 are planned; WP104/105 remain unregistered proposals under architecture review. WP103's complete-coverage-index proposal is retained but unregistered because its late planning dependency produces a lane aggregation cycle. All49 remaining families stay in scope.

Bosslady2 is the Linux physical-keyboard host. GNOME currently binds Alt+F10 to window maximization, a configured collision with macro run; actual physical delivery remains to be checked. Pink Menace macOS testing is deferred until the end of the milestone at the owner's direction. No new Mac testing was performed for WP100. This checkpoint is not full parity acceptance or a production-release authorization.
