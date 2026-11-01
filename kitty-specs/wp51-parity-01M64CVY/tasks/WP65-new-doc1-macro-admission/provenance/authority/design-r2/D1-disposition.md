# D1/P2 correction disposition — proposed resolution

Review input: immutable report93ef094316a9413c875ee022f7a7c63a102cd05d64f9ad06eb4576aa400a6c35, actual closed seal519eb27c8f7e53bfa7f4d6f4a4eb9a0be1846ecc03d745ff306ae921c5c71654. Citation correction d7ac11db5cd4f78228f956f957649a03229271439d4ba8728c55bee634885d46 / seal581cc79b4cf7cd883e93cf07cab74003f074b70713af9075aee014ada9fb8b04 is preserved separately. The old review's514 citation is superseded only by that inert correction; neither old seal was rewritten.

The original design wrongly combined NEST/CHAIN as a runtime resolver request. Active revision2 design's opening root-only policy, effect table, G acceptance8 and README/package-boundary restatements now distinguish:

| Source | Existing approved admission | Proposed New target outcome | Earlier ASCII |
| --- | --- | --- | --- |
| Already compilable NEST FC18 | compiler.go:440–448 captures literal name; machine.go:371–380 dispatches to Resolve | Existing G Resolve checks New root-only policy before child-name lookup/read/IO; returns Resolution host-error/Refusal; existing machine.go:492–493 produces failed/HostFailure; no synthetic CommandError/NotFound/handler success | Only genuinely applied prefix effects survive and are receipted. |
| CHAIN | Exhaustive compiler statement switch has no CHAIN admission; compiler.go:505–506 defaults UnsupportedInstruction. Runtime README requires statically unknown instructions to refuse before any effect. | Unchanged Compile refusal, no execution driver, runtime ProgramRequest or Resolve callback. Root WPM acquisition/receipt may already exist; no child IO. No VM/compiler/evaluator/scanner widening. | No sink effects, including textually preceding literals; no partial-effect claim. |

The NEST partial-prefix/handler-noninterception runtime negative and CHAIN preflight/no-effects negative are separate required future tests. A compile failure cannot be counted as the NEST runtime negative. Source inspection and a textual regression control here verify design consistency only; no compiler or runtime was executed.

No other normative scope was relaxed: real pristine New Doc1/default Repeat1, captured admission before MacroName, opaque Birth/genesis/native/buffer/screen/issued/ready/current transition and authentic root source/receipts, private driver/H current-chain ownership, no global G fork revocation, unchanged New WithMacroRepeat/switch guards, ordinary ASCII/DISPLAY and limits, loaded behavior, history and genuine first publication/read-back remain. Raw indexed packet06 bit08 is an existing permitted difference, never normalized or cleared to force equality. Full-native future comparison and unexplained-difference halt remain. P61 and parallel P proposals are unrelated.

Disposition: **D1 addressed in proposed revision2; READY_FOR_INDEPENDENT_DESIGN_REVIEW_ONLY.** Independent reviewer must verify and decide; this document does not self-approve or authorize tasks/code.
