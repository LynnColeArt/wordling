# Preparation diagnostics

The following bounded observer mistakes occurred during source discovery. Their
returned error lines are transcribed here, not described as original byte-for-byte
PTY recordings. No product code was imported/executed by these reads, no private
asset/cache/reference path was inspected and no host change was attempted.

- In the retained task proposal directory, `cat research-inputs/assessment.md`
  exited1: `cat: research-inputs/assessment.md: No such file or directory`.
  Correct locator was then read: research-inputs/assessment/assessment.md.
- In lane-y, `cat internal/wp51/image.go` emitted
  `cat: internal/wp51/image.go: No such file or directory`.
  Subsequent reads of reader.go/types.go emitted
  `sed: can't read internal/wp51/reader.go: No such file or directory` and
  `sed: can't read internal/wp51/types.go: No such file or directory`.
  `go list` resolved the actual pinned native.go and its full source was read.
- A scoped `rg --files internal/wp51` issued in the task proposal cwd emitted
  `rg: internal/wp51: IO error for operation on internal/wp51: No such file or directory (os error 2)`.
  The actual lane-y compiler/module locations were then verified explicitly.
- A combined read in the proposal cwd attempted the lane-relative
  consumer-first.stderr/exit files and emitted No such file or directory for
  both. They were then read from actual lane-y. The command also read successful
  governance/research text; its overall exit was0 from the last successful read.
- A lane-y contract lookup used missing top-level `contracts`:
  `rg: contracts: IO error for operation on contracts: No such file or directory (os error 2)`;
  `cat: contracts/merge-native.md: No such file or directory`;
  `cat: contracts/native-framing.md: No such file or directory`.
  The primary shared mission contract directory was then located. There is no
  merge-native.md; its attempted primary sed also emitted No such file or directory.
  Applicable native-framing/automation and boundaries were read there, and all15
  contracts separately matched the earlier canonical7ce5b703 snapshot exactly.

Runtime/governance output reports teamspace logged-out warning, retained whole
in profile.txt. No authentication, hosted publication or host/cache repair is
claimed. Missing charter Terminology Canon and Code Review Checklist sections
are retained as returned diagnostics; no unsolicited charter edits were made.

Exploratory library/consumer runs preceded the final prose resource proof; their
full raw stdout/stderr/exits remain. Post-proof qualification and final configured
checks are separate. RED is an expected compile failure before new APIs existed.
First mutation roster has10 genuine kills and one redundant-owner-check survivor;
its compound replacement is separately compiled and killed. All original raw
failures and assertions remain; no survivor is relabeled as a kill.

The initial no-index whitespace sweep printed no errors but returned1 (ordinary
no-index diff status); its exact stdout/stderr/status remain under source-lint.
The final index-aware nine-source-path whitespace sweep exits0. The whole raw
packet whitespace sweep exits2 with10,358B of diagnostics, retained unchanged;
that result is not source lint failure and is not relabeled green.

The first actual-binary negative wrapper checked combined output after
communicate; source-fixed stdout<=1MiB and bounded stderr kept actual runs
inside2MiB, but this did not demonstrate a live capture guard. Its complete
history remains. The corrected second wrapper enforces the2MiB bound before
retained append with selectors and owned timeout/reap handling. It reruns only
those actual-binary negatives/removal checks whose capture mechanism changed;
all ten negatives and the compiled removal control pass qualification there.
No product change or old output overwrite occurred. Both exact scripts remain.
