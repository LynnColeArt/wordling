---
work_package_id: WP73
title: Bounded ordinary explicit-count character Repeat
dependencies:
- WP71
requirement_refs:
- FR-004
- FR-005
- NFR-001
- NFR-002
- NFR-003
- NFR-004
- C-001
- C-002
- C-003
- C-004
- C-005
- C-006
planning_base_branch: feat/wp51-parity
merge_target_branch: feat/wp51-parity
branch_strategy: Planning artifacts for this mission were generated on feat/wp51-parity. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/wp51-parity unless the human explicitly redirects the landing branch.
subtasks:
- T217
- T218
- T219
phase: Bounded pristine New Doc1 character Repeat; full Repeat and M1 remain open
history: []
authoritative_surface: internal/tui/
owned_files:
- internal/tui/**
create_intent:
- internal/tui/character_repeat.go
- internal/tui/character_repeat_test.go
- internal/tui/evidence/character-repeat/
execution_mode: code_change
agent_profile: implementer-ivan
role: implementer
task_type: implementation
---

# WP73 — ordinary character Repeat in pristine startup New Doc1

Audience: the issued implementer, ROOT, and independent CODE reviewer. WP73/T217–T219 are the mechanical identities for the independently approved revision2 TASK. Number-neutral/unreserved wording in retained proposal history retains its historical meaning. This is one H-only code-change package after actual CODE-approved WP71; inherited G65 is a source dependency, not a new G amendment. Normal canonical task gates, fresh actual CURRENT analysis and an issued claim remain mandatory.

The complete approved proposal is `tasks/next-increment-73-task-proposal/`, with its retained original/research/review history and original relative-name seal scopes. The DIFFERENT independent TASK approval/F1 closure is `tasks/next-increment-73-task-review/REPORT.md`. Basename annex/proof references in this body resolve from that proposal root: `ARCHITECTURE.md`, `ACCEPTANCE.md`, `BOUNDARIES.json`, `source-proof.json`, and their explicitly located history. Publication maps and outer seals bind archival destinations; they are provenance, never source/IO authority. WP71 and WP73 share H model/prompt/guard files: sequential lane-h coordination is required, with actual approved WP71 source retained and old tests byte-exact. No concurrent writer/source overlay or moving70/72 API is authorized.

## Routing metadata and CLOSED execution allowlist

`owned_files: [internal/tui/**]` is the existing H routing namespace, already declared by the approved BOUNDARIES.json `routing_owned_namespace`. It is NOT expanded source-write authority. The planning-only primary lacks the six old H files, whereas actual approved H71 contains them; namespace zero-match advisories must remain truthful. Do not disguise old files as new create_intent, copy source into planning, alter the host validator or use an overlay/skip. `create_intent` remains ONLY the two genuinely new Go files and own evidence namespace; dependency WP71 and actual H authoritative_surface remain unchanged.

The following CLOSED execution contract is copied semantically EXACT from the approved BOUNDARIES.json. Check actual changed/new/deleted/renamed pathSET against it at claim/commit/review; routing overlap never authorizes another inherited file, test, fixture or evidence amendment. All inherited paths outside these six explicit old amendments remain byte-exact. The three driver literals are limited to the already approved own bounded evidence namespace; no other executable literal without a reviewed amendment. No inherited test amendment is authorized. Grammar, APIs, allocation/work/evidence limits and host/original claims below and in the unchanged approved annexes remain unchanged.

```json
{
  "amend_existing": [
    "internal/tui/model.go",
    "internal/tui/macro_model.go",
    "internal/tui/menu_bar.go",
    "internal/tui/ascii_viewport.go",
    "internal/tui/reveal_inspection.go",
    "internal/tui/README.md"
  ],
  "create_files": [
    "internal/tui/character_repeat.go",
    "internal/tui/character_repeat_test.go"
  ],
  "create_namespaces": [
    "internal/tui/evidence/character-repeat/"
  ],
  "namespace_payload_drivers_exact": [
    "internal/tui/evidence/character-repeat/run_pty.py",
    "internal/tui/evidence/character-repeat/mutants.py",
    "internal/tui/evidence/character-repeat/collect.py"
  ],
  "namespace_other_payloads": "Bounded raw evidence/reports/JSON/text/native emitted outputs/history/nested seals only; no imported Go package/product Go file, hidden source/test edits or generic new tool framework. Drivers optional if existing approved read-only utility suffices; no other executable literal without reviewed amendment.",
  "old_test_amendments": [],
  "protected_no_change": [
    "cmd/",
    "internal/input/",
    "internal/editor/",
    "internal/document/",
    "internal/storage/",
    "internal/macro/",
    "go.mod",
    "go.sum",
    "all inherited tests/fixtures/evidence except none",
    "canonical planning/runtime/lifecycle"
  ]
}
```

## Outcome and evidence contract

In the genuine untouched constructor-created New Doc1, accept Escape, ONE explicit nonzero decimal digit, then ONE nonnumeric printable ASCII character key. Insert that character count times as ONE atomic real `editor.Text` transition. The original-backed positive is Escape →5 →x → final `xxxxx`. Additional counts/characters, one-shot consumption, cancellation, safety, intermediate UI, history and native conservation are Wordling host contracts, not newly observed March1992 semantics.

Use approved H71 `cd983c05401a90c1f0c912c60ab6ca23d8bd437b` and its inherited G65 `f110c5a7e113b063081879ea491c1dde5bf79aed`. No moving70/72 code, new native writer, document/editor/storage API, runtime framework, input decoder, module/dependency or command-line flag. Source locators and hashes are in source-proof.json. Read ARCHITECTURE.md, ACCEPTANCE.md, BOUNDARIES.json and both complete retained research packets before implementation. The small independent research review recommended design only; it is not TASK/CODE approval.

The June1992 Reference MNUS1WP51X1C-6/92, printed550–551/PDF567–568, is later than the selected March9 executable. Its ordinary nonnumeric one-operation Repeat description is documentary support, not an oracle for exact defaults/prompts/cancel/errors. The1989 Workbook WB03-LINE-04/05 count40 lead remains unobserved as a complete lesson. Two original CMD51-005 run associations have the same finalscreen; no prefix/default/cancel/native/history or next-key witness exists. Do not relabel them. Direct locators/hashes remain in retained research/manual-observations.json and original-observations.json.

## Frozen finite grammar and behavior

These narrow limits are deliberate HOST admission policy, not original limits:

| State/input | Result |
| --- | --- |
| Healthy pristine80x25 New Doc1 + ordinary unmodified Escape press | Enter separate character-count state with no default and no document/session/IO change |
| Pending, count absent + one delivered ASCII digit1..9 | Retain that one digit; show pending explicit value; no insertion |
| Pending, count present + one delivered character in ASCII0x21..0x7e excluding0..9 | Preflight, then one authoritative Text insertion of1..9 copies; consume count even if reducer refuses |
| Pending F1 or Escape, unmodified and nonrepeat | Cancel only this pending host state; consume key; report `Character Repeat cancelled (host policy)`; no native/session/IO command |
| Any other pending key, including0, a second digit, Enter, Space, AltF10, Alt+=, navigation, command modifiers or missing count before character | Cancel pending host state and report unsupported character Repeat input; consume offending key without dispatch/replay |
| Pending OS-repeat, paste/start/end, unknown/focus/blur/mouse/resize or asynchronous host completion/control message | Invalidate pending state before any old dispatch; preserve existing handling of actual asynchronous receipts/resize and their uncertainty; never replay Repeat or swallow a receipt |
| Key releases, keyboard/capability/terminal-version reports, EnvMsg/ColorProfileMsg | No Repeat effect; preserve old handling and pending state while the real context remains valid |

A text-bearing key must be an actual translated Press, non-IsRepeat, with exactly one byte of delivered Text, a printable ASCII Code, and modifiers limited to Shift/CapsLock for digit/character entry. Delivered text remains the identity; alternate/base codes are not guessed physical proof. Bare command Escape/F1 require empty Text and zero modifiers. There is no concatenation of Escape transport bytes, paste expansion, OS repeat alias, count digit insertion, automatic default8, leading-zero or multi-digit parsing, persistent setting, Enter commit, repeated numeric character, Space/command repetition or loaded/typeover/Reveal/Doc2 extension. A second digit is rejected BEFORE arithmetic: numeric overflow is structurally unreachable in this grammar, not a claim of general decimal parsing.

Cancellation/refusal consumes only the offending event, not future ordinary input. For separate presses Escape,9,9,9: native/session/history/IO remain unchanged through the offending SECOND9, which cancels Repeat; the separately delivered THIRD9 then follows ordinary Text exactly once, inserts one9 and inherits no count. A single delivered multi-character Text while pending is a distinct refusal and is not split or replayed. Cancellation/refusal notices are explicit host diagnostics, not copied DOS prompt claims. Do not clear preexisting unrelated notices to admit or continue Repeat. The pending display may use `Repeat Value = ` followed by the digit if present, with the prompt caret at its visible end in the existing legacy row2. This is bounded Linux composition, not an observed original prefix frame. Use existing width clipping/caret checks. State/View only observe; no setter, permit or telemetry is introduced. After success the next ordinary key goes through ordinary production dispatch once; it cannot inherit the count. The modified document is no longer this pristine cohort, so another character Repeat is outside this slice.

## T217 — ownership and finite expansion

Implement only the private H transient state and production hooks described in ARCHITECTURE.md. Its constant-size data carries stage/count and opaque actual native/genesis revision plus actual session revision/screen/gap baseline, not a Session/Document payload, source capability, cursor setter, map/history, worker, permit or public synthetic counter. Existing current `claimUI` ownership is checked FIRST on every Update. Persistent Model copies carry no right to execute after the authentic chain advances. No shared mutable count object may let a stale copied Model consume/change the authentic pending count.

Admission and every consuming pending Press must establish the SAME actual pristine constructor source and healthy current host context. Require real New Birth, source=nil, empty document, nonzero GenesisRevision==NativeRevision==captured owner, session Revision1, Gap0, Provenance0, screen1, NewUnpublished, Editing Insert, no selection/Reveal/HomePrefix, known qualified initial history and no mutation/publication/name/draft/receipt/prompt/notice. Require80x25, current nonstopping runtime, no prior issued/results/executed/first-ticket/macro-results work, active/ticket/CPU/deferred/frozen macro or nonzero MacroStatus, pending/unsettled/first IO, reconciliation, shown/diagnostic menu, legacy repeatEntry or MacroRepeat!=1. Read actual protected source predicates; ARCHITECTURE.md gives the complete mapping. An equal byte stream, empty-after-delete, published/bound New, independently created runtime/revision, copied snapshot or coincident gap/revision counter is not this source.

Before any repeated payload allocation, establish count1..9 and one allowed character, unchanged captured opaque owners/context, document total0, count<=MaxMutationTokens-total and native Export length<=MaxMutationBytes-count using bounded subtraction. The pristine profile is small; Export is the existing bounded native observation, not a writer replacement or source classifier. Do not allocate N bytes then check. Expansion is exactly count bytes (<=9), O(count), at most one new expansion string; no N separate Reduce edits, speculative publish/rollback or partial success. Perform ONE real `m.reduce(editor.Event{Command:editor.Text,Text:payload})` on the authentic current Session, keeping the downstream InsertASCII/admission/history receipt/revision path. The reducer's result/typed refusal is authoritative; no setting MacroRepeat1, session reset/fork, editing private fields, direct Document mutation or result fabrication. Count state is consumed before handing to the reducer; on failure retain its actual error and unchanged document, not a guessed retry.

Prospective new-expansion allocation ceiling is256 bytes total per operation including temporary payload conversion, excluding existing snapshot/native export/reducer/view costs. New transient state is constant-size, no retained payload. Public complete three-input Update sequence allocation<=1MiB at width80; pending View allocation<=128KiB/call; existing reducer/native/legacy render ceilings are not redefined. Measure bounded isolated expansion and public cold path, including count1 and9, at most100 measurement samples per case. These are proposed ceilings, not measured success; report a real mismatch before budget/scope widening. No new wall-clock production timeout.

## T218 — integration and protected behavior

Keep existing `repeatEntry` and Snapshot.MacroRepeat exclusively loaded Repeat3→Macro. Existing `WithMacroRepeat` New refusal and G Reduce non-Macro guard remain byte-exact. The new state does not set/clear/reset them. Existing loaded macro Esc3/AltF10, active/deferred/frozen work, New macro exclusions and actual New history/source/writer rules remain unchanged. Make the pending character state explicitly exclude pristine menu display, New macro admission, anchors, whole-ASCII viewport and partial inspection; it uses the old legacy prompt composition. Frozen DISPLAY OFF selection remains FIRST, unchanged. State/View cannot install/rearm/consume state or qualify a cache.

Use real Update integration, not a helper-only text expander. Handle pending character keys before menuPress so Alt+= cannot open/restore the menu or evade invalidation; preserve preexisting menu behavior when no character state exists. Admission Escape is after existing uncertainty/detached-IO/OS-repeat guards and before macroKey's legacy New-Escape refusal, and MUST decline loaded contexts so they continue to legacy macroKey. Pending handling checks those actual ownership/IO/macro gates itself before it can bypass later dispatch. Administrative and asynchronous invalidation cannot swallow a real receipt; no shortcut return before its original handler. Authentic returned Update still invalidates menu/prepares ASCII viewport in its existing order.

No old test amendment is needed or permitted. In particular preserve byte-exact:

- `new_macro_test.go` public `case "repeat": m = key(t,m,tea.KeyEscape,0,"")`, followed by AltF10 and the existing `nonpristine New admitted` assertion. It must STILL refuse with no IO/native change, because a pending character operation never admits Macro.
- `menu_bar_test.go` `"Repeat": {{Code:tea.KeyEscape}}` and its subsequent `context admitted` assertion. The pending character state must still exclude the pristine menu.

These assertions are NOT obsolete. All other inherited tests, fixtures, native samples and evidence remain exact. A necessary additional amendment is a precise prerequisite requiring independent TASK amendment before writes, not namespace authority.

## T219 — acceptance, evidence and independent review

Write meaningful failing public behavior tests before implementation; establish the intended failure, then implement without weakening inherited tests. Positive setup is actual `Open`, authentic returned Update/key chain and normal rooted IO continuations, never a forged Session/genesis/cursor/count. Supplemental private inconsistent-state negatives or pure expansion unit checks must be labeled and cannot replace public reachability. ACCEPTANCE.md fixes the matrix, semantic-mutant discriminators, commands and evidence limits.

Required two fresh unmodified `cmd/wordling`80x25 PTYs: (1) Esc5x → `xxxxx`, next q → `xxxxxq`; (2) Esc3= → `===`, next z → `===z`. Send Escape separately and await actual prompt before digit/character so decoder timing cannot be mistaken for Alt delivery. Observe intermediate pending native effects in Model tests, not fake PTY telemetry. Compare only the first final repeated text to both original005 screen text witnesses; the distinct count/character/next key and layout/caret are HOST acceptance. Actual F10 first publication/read binding, native file readback, no-edit preservation and safe F7 exit/termios restoration must occur, with no new cmd flag/test binary. Expected host bytes derive from genuine constructor plus approved ordinary Text path; do not synthesize/rewrite a prefix. Native conservation is not original native Repeat qualification.

At claim freeze actual clean claimed H HEAD, compiler/module/package source closure and ALL protected inherited paths, actual Git+working hashes and tests/fixtures/evidence set. source-proof.json is a reviewed approved-source design pin, not a stale eventual claim guard. Bind actual issued prompt, canonical task digest, compiler/version/go env/GOMOD/actual GoFiles/command cwd/env, product binary/build info and observer source to the final run. If approved source bytes differ, ROOT must classify exact differences before implementation; do not silently overlay/reset/rebase or import moving70/72 APIs. Late source hash change requires rebind/reverification of affected evidence. Keep all failed/initial attempts, survivors, setup failures, exact stdout/stderr/whole exit/elapsed, finite work/allocation measurements and cleanup outcomes. Inert history scripts never substitute for production.

One finite campaign: <=48 new Model cases, <=128 explicit events/case including IO, <=12 compiled semantic mutants, <=4 baseline PTYs INCLUDING the two retained failed observer attempts, plus at most1 integration-removal mutant PTY; combined PTY attempts remain<=5. The third and fourth baseline attempts are exactly one independently reviewed two-case replacement campaign, from a frozen corrected observer, permitted only by a separate ROOT grant after independent TASK-amendment approval. Both complete successful baseline cases remain required; another observer failure stops and is retained rather than retried. Each PTY30s+2s owned TERM/KILL/reap and combined wire/stderr<=2MiB checked before append. Each Go/configured command<=300s; total new evidence<=256 files/6MiB INCLUDING all failures/history/nested seals, no truncation presented as full evidence. Driver/observer/log overrun is a genuine retained failure; no silent discard or repeated retry-until-green. Test wall-clock/allocation bounds are host evidence, not DOS resources. No parser fuzz or new reference execution is required or authorized.

Run actual gofmt, cached-source lint on the CLOSED changed Go list, build, `go test ./...`, vet, focused race, meaningful allocation checks and configured7 against actual package discovery; preserve skips/failures honestly. Semantic mutants must compile, fail intended previously-green public targets, and production integration removal must fail both Model and real CLI (at least one of the two PTY cases). Setup/compile failure or unrelated timeout is not a kill. ROOT owns subsequent normal lifecycle/promotion/quietpoint and separate independent CODE review. No author native verdict, push/accept/merge/mission closure or source claim follows from this proposal.

The full37 M1 obligations, FC010/M2 gate,91 groups,36 lessons and SC001–005 remain open. General Repeat/default8/persistence/multidigit/range/zero/numeric/command/Space, loaded/Reveal/typeover/Doc2 behavior and original native/prefix/cancel/history effects remain explicit gaps. No native format changes; PDF stays M2-gated. Queue exhaustion is never parity.
