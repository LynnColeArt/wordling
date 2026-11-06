# WP26 typed API checkpoint for WP27

This is a document/history domain component, not another editor/session. Use the
actual existing Cursor, native Kind and private immutable document revision state.
Normal/Reveal are projections; cells, labels and inches never serialize identity.

- NewHistory(d) explicitly creates a fresh transient context. Do not call it as an
  assumed global history reset on retrieve, document clear, view changes or edits.
- d.Delete(c, direction, h) receives ForwardDelete or Backspace. Normal paired
  codes return an opaque Deletion question; Reveal bypasses only that question.
- d.DeleteBlock(anchor, end, h) admits only researched forward Reveal selections
  of the opening token, closing token or complete paired span. Other shapes refuse.
- d.AnswerDeletion(h, pending, answer) accepts Yes/No/F1/Escape at the exact bound
  document AND history state. Normal declines skip the code in deletion direction;
  block declines retain selection. d.CancelBlock(h, declined) is separateF1 cleanup.
- Deletion.Document() returns a fresh handle to captured immutable state; Cursor()
  and History() return immutable values. Pending, Applied, BodyChanged and
  NativeChanged are distinct. Kind identifies requested/performed command class,
  not success by itself. BlockActive/BlockRange/Prompt expose the exact context.
- History.Before/after generation is private; Revision() is a comparable opaque
  state identity. Whole-value public wrapper replacement cannot retarget accepted
  questions, previews, results or receipts. Errors publish no partial transaction.
- History.Separate(SavedBoundary/RightBoundary) reports only an actual successful
  Save or Right grouping barrier. The dispatcher must report real commands in
  order; failed keys/saves are not these events. InterruptGrouping() preserves
  entries and marks a non-deleting unqualified interleaving, refusing continued
  deletion until a known separator. It is not a generic key/router implementation.
- h.Open(c) returns inactive/no prompt when the known stack is empty. Preview is a
  captured read-only overlay; Previous cycles at most3 entries; no arrows/redo.
  h.CancelPreview(p) preserves bytes/order and invalidates stale preview use.
  Reopening starts newest. It does not prove unobserved continued-delete grouping.
- p.Present(start,count,reveal) returns bounded OverlayElements tagged current
  DocumentToken versus DeletionFragment. Only current document tokens have native
  spans; fragment spans are absent. FragmentStart/End describes virtual selection.
  The UI [Block] marker is not a native code. Preview can display a future
  three-pair overlay even when actual Restore must refuse the2-pair policy.
- d.Restore(h,p) inserts lawful stored native fragments relative to captured cursor
  and validates the prospective complete body before any publication/history
  update. Plain and opening-repair entry retention are proved. Full attributed
  first Restore is proved; its later history effect remains unqualified.
- h.AfterEdit(actual EditResult) accepts only a private immutable ASCII receipt,
  validates its real before/after state/cursor/Changed fields and captures state
  rather than exported result/Document pointers. Fabrication/rebinding refuses.
  Pure insertion with known empty history remains qualified. Typeover replacement
  or insertion after existing deletions preserves prior fragments but makes later
  unobserved history effects explicit: Qualified()==false and history/deletion
  operations refuse. The exact known Restore/reopen/cancel/X sequence is admitted
  through this seam; no post-X reopening is fabricated. No implicit clear/rebase.
- Count and Entry inspect preserved known storage; Entry.Native is a copy and
  Entry.Qualified distinguishes history-behavior qualification. Unknown history
  cannot become qualified by moving/saving. No persistent sidecar or global clear.

Approved40 now enables direct-pair/closing-repair completion only in the structural
seeded/pre-browsed/Right-separated qualification described by qualification.md.
CountKnown() is additive: Count() still inspects stored fragment knowledge, while
CountKnown()==false withholds actual stack cardinality. In bounded40 contexts
Preview.Index() is one of four observed browse positions; it does not imply that
four distinct entries exist. Fragment values/overlays come from actual native data.
Only one newest Restore plus observed post-Restore browse/cancel is enabled.
Extra Previous, repeat Restore, changed cursor/view, unbrowsed/uninterrupted/other
history setups refuse. Generic empty-history pair completion/EC045 intermediate
stays unsupported; there is no future-key compound operation or hidden clear.
Caller should adopt all successful result values atomically. On any error keep
its document/cursor/history/question/preview/selection unchanged. Pending/UI
operation identity, terminal commands, IO/save outcome and both document screens
remain the editor/session owner's responsibility. WP26 adds no hidden UI state.
