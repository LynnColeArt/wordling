# Runner custody and reproduction

Every raw run archives native_edits.py and all scripts/reference Python modules
before guest launch. run.json pins their SHA/length, profile/master hashes, actual
QEMU argv, shared short runtime/socket/lock, source resources, action trace,
checks/settings, exports and raw captures. These are immutable original evidence.

The initial `wp23-a-*` suite used the external serial `run_pairs.py` scheduling
wrapper. That wrapper was recorded in its launch command but was not copied into
each initial raw run. No prelaunch wrapper hash is claimed. Its actions were:
parse prefix/optional recipe list; call archived `native_edits.configure()` once;
iterate the declared recipes and repetitions1,2; call
`native_edits.execute(prefix+'-'+recipe+'-r'+str(repetition), recipe)`; accumulate
observed/incomplete results and exit nonzero if any failed. It supplied no custom
recipe, extra guest command, direct disk mutation or semantic monkey patch.
`configure()` is the archived idempotent binding of guest/qmp runtime/socket,
master and profile to the primary private reference directory. execute's
exclusive context repeats that binding before actual launch. Actual run argv,
shared runtime metadata and source trace retain its effect; it is not omitted
as an assumed irrelevant global action.

Reproduce an initial per-run invocation from the recorded recipe/run identity:

```python
# In the actual code checkout, with root's exclusive reference VM authorization.
import sys
sys.path.insert(0, 'scripts/reference')
import native_edits
native_edits.configure()
native_edits.execute('NEW_DISTINCT_RUN_ID', 'modes') # exact recorded recipe
```

Use a fresh identity and private master copy for every run. To reproduce an old
recipe revision, use its archived native_edits.py plus all archived transitive
reference modules as the runner source. The default current source may contain
subsequent captured fixes. The saved action trace and exact native/output/state
checks establish which behavior actually occurred; scheduler omission does not
become an invented prelaunch artifact.

The focused `wp23-b-*` suite additionally archives every owned Python helper,
including scheduler and custom followups, before each VM. Its custom function is
the exact RECIPES[recipe] in archived wp23-followups.py. These files include
extra offline audit/test helpers as snapshots; their presence does not claim
every helper executed inside the guest. The actual guest entry remains archived
native_edits.execute, guest.start, MutationProbe/SessionProbe/LayoutProbe,
qmp commands, selected print_disk and clean_exit. Candidate mode similarly
archives source/inputs before launch and records its read-only B: seed drive.

Initial failed normal-delete attempts are immutable. Their diagnostic native
source files were extracted later from each stopped private image into a separate
diagnostic directory, with original manifest/image/native hashes in
`diagnostic-extractions.json`. No failed attempt was relabelled or completed by
retrofitting raw files. Initial menu/Block-name calibrations remain excluded.
