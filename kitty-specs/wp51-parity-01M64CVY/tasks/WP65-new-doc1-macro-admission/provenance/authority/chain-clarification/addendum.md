# Supplementary design/task clarification — static refusal typing

Status: **READY_FOR_INDEPENDENT_SUPPLEMENTARY_REVIEW_ONLY**. This corrects a narrower source/type assumption in approved-for-design revision2; it does not rewrite/reseal R2, reserve tasks/IDs, authorize code or change its other normative boundaries.

R2 correctly distinguishes already compilable NEST runtime refusal from CHAIN static refusal. Its design11/effect-table CHAIN row, acceptance G8, package-boundaries16 and README5 nevertheless name CHAIN's exact error as `UnsupportedInstruction`. Public source does not justify that exact native-input claim:

- `contracts/macro-framing.md:185–186` marks CHAIN/CALL/other commands documentary-only; the current20-case/46-source corpus does not bind a CHAIN opcode/input fixture. No opcode may be guessed from a table name or invented from an opaque word.
- `wpm/image.go:264–269` classifies every FCxx outside its explicit admitted list as Opaque/UnqualifiedMacro. Parse preserves such words and records findings, rather than granting execution.
- `runtime/compiler.go:68–74` rejects nonempty Image findings as `UnsupportedImage` before statement compilation. Only a finding-free admitted Image reaching an unsupported statement falls through `compiler.go:505–506` to `UnsupportedInstruction`. The latter source default proves no CHAIN admission exists; it does not prove every purported CHAIN native input reaches that default.
- Existing `negative_test.go`'s `unknown-dead` control uses a genuinely typed static-unknown source and expects UnsupportedImage before effects. It is an UNKNOWN/ineligible-image control, not an original or invented CHAIN fixture.

Proposed precise correction to every coupled clause:

> CHAIN stays outside the admitted native/VM grammar and is statically refused before all sink effects, including preceding literals. There is no execution driver, runtime ProgramRequest, Resolve callback, child IO or partial-applied-text expectation. Assert the exact typed refusal only for a real source-backed input/path; WPM findings may cause UnsupportedImage before any statement-level UnsupportedInstruction. Do not invent a CHAIN encoding/fixture, relabel an opaque FCxx control as CHAIN, broaden reader/compiler/grammar or fabricate a runtime test. Root WPM acquisition may already have occurred.

Future acceptance separates two honest proofs. Retain source inspection of CHAIN's documentary-only/unadmitted status and unchanged guards, without an executable CHAIN fixture claim. Run existing actually typed UNKNOWN/static-preflight controls with truthful classifications and exact observed codes/zero effects; they must be named UNKNOWN, not CHAIN. If a named executable CHAIN test is later required, its exact public native encoding/provenance is a missing prerequisite—report it rather than accessing private manuals/originals or guessing a word.

The NEST contract is unchanged: admitted FC18 compiles and reaches existing Resolve; the proposed New root-only resolver returns typed host-error before child-name lookup/read/IO, existing VM maps failed/HostFailure, earlier actually applied ASCII remains, and no CommandError/NotFound/handler success is injected. A compile failure cannot satisfy that runtime negative.

Every other R2 boundary remains exact: genuine pristine New Doc1/default Repeat1/capture before MacroName; opaque Birth/genesis/native/buffer/screen/issued/ready/current/source/receipt proofs; actual H once-only current UI/IO/worker and G persistent-fork truth; unchanged New Repeat/switch and loaded behaviors; ordinary ASCII/DISPLAY/history/partial errors/budgets; same native writer and raw indexed packet06 bit08 policy; actual future full-native/first-save/cancel/unknown readback and unexplained-difference halts. No new native equality, product/runtime test or original permission follows. Full M1 stays open; M2/PDF gated.
