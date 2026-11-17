# Recovery decision regression

`python tests/everyday_qualification/recovery_decision.py REPO NORMAL_BINARY NEW_OUTPUT`

Fixture-free test using a real normal Wordling executable and local PTYs. It
creates FIRST/SECOND buffers, waits for durable autosave, and terminates only its
own child. It then cancels the unchecked-copy deletion warning with N, verifies
the old copies are byte-identical, selects all, restores, and immediately
terminates the restored session before any edit/save or timed autosave. Both
copies must be eligible for the next recovery decision with exact contents.
Restored buffers must still require explicit save/discard. After explicitly
discarding each on clean exit, a normal restart must not repeat recovery.

This adds cancellation and untouched immediate re-crash coverage to the existing
recovery.py tests, which cover confirmed unchecked deletion, save-before-recrash,
updated buffers, six tabs, and pre-publication interruption. No product semantics
changed. The existing UI says Enter Restore checked documents and D Uncheck all,
then confirmation for deletion; the test checks that implemented checklist flow,
not new literal button labels. Tabs and recovery are intentional modern behavior.

No proprietary fixtures, ptrace, test-build fault controls, or GNOME automation
are used. This proves PTY process/restart behavior and terminal state only. It
does not establish GNOME window-manager or desktop-session integration behavior.
