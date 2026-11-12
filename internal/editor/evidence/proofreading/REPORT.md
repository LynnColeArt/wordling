# WP88 — continuous contextual proofreading in the editor (evidence report)

Status: implemented on lane-g, actor kat. Subtasks T279–T283.

## Subtask ledger

- T279 done (d55b3caa): Ctrl+F2 journey modelled — Check menu state,
  Word/Page/Document scopes, questioning walk over native tokens, WP78
  word-boundary rules (SRt binds; DSRt continues a word; spaces/returns
  bind positions), transient per-pass memory (Corrections/Skipped),
  per-screen placement (Session field; switchDocument clears it with the
  document it belongs to).
- T280 done: corrections route through real native operations only —
  shared-prefix TypeoverASCII per character, InsertASCII for the new
  suffix, forward Delete for the surplus — surrounded words byte-identical
  (TestProofreadingCorrectionPreservesBody). No rendering-side string
  replacement; no alternate document model; no pair-publisher invention
  (attribute-owner migration is the document package's own semantics).
- T281 done: Skip (rest of pass) / Skip Once / Add decision paths, F1
  interrupt to editing, acknowledgement continuation (frames 09/10);
  transient decisions reset when the next pass starts; reading place and
  document preserved at each transition (tests assert modes and intact
  document).
- T282 done: journey tests cover the trace's PROOF.WP sentence —
  first-question order, skip-rest suppression across occurrences,
  completion + reset, interrupt, correction with unrelated-byte
  conservation (quik x2 / zorbly x3 untouched while misspelled lands).
- T283 done: go build/vet/test all green (14 test packages, 0 failures);
  evidence = this report.

## Continuation/state evidence (spelling/proof trace reconciliation)

| trace step | WP88 | match |
| --- | --- | --- |
| ctrl-f2 → 01-spell-menu | ProofMenuMode, Check prompt | exact |
| 3 → 02-first-question | first suspect "quik", questioning mode | exact |
| 'c' → 03-replaced | correction applied, next suspect | exact |
| skip-once → 04 | advance, auto-replace on repeat encounter | exact |
| 2 → 05-skip-rest | word suppressed rest of pass | exact |
| F1 interrupt → editing | editing with intact document | exact |
| pass drain → 08/09 ack | ProofAckMode; any key → editing | exact |
| new pass → 10 skips forgotten | walk re-questions post-reset | exact |

## Bounded cohort (honest scope)

Provider acceptance comes from `proofreading.CohortAccepted` (WP87
surface). Lexicon/ranking equivalence with the proprietary resources is
NOT claimed; unknown mappings refuse rather than invent suggestions
(WP78 rights contract). Suggestion letters are bounded to the trace's
own evidence ('c', 's'-variants); everything else refuses.

## Downstream consumers

WP89 owns the questioning TUI (context rows, ruler, suggestion columns,
Not Found row). The session exports ProofSnapshot/Proofword/modes as the
contract. WP86 will exercise the continuous journey through the real
executable with admitted resources (per WP78: EE-A15 requires it).
