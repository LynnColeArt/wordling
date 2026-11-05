# WP58 generic startup component

The new public component is `scripts/reference/startup_transport.py`. It is a
Linux-only standalone test transport; it does not delegate from or change legacy
`macro_session.fresh_start`, guest.py, qmp.py, or their callers. No original resource,
VM, QEMU, guard, ledger, program, manual, font, settings or private disk was read or
run. This package supplies no original grant, controller, safe original stop,
native writer or M1 acceptance. Full38/91/36/nested obligations stay open; M2 gated.

For component reviewers, start with CONTRACT.md, report.md, acceptance-inputs.json,
final-acceptance.xml/log, mutants.json and source-custody.json. The first contract,
development logs, two initial mutant survivors and their corrected probes, and
prior46-case/CLI captures are retained as history, not final-source results.

Public execution:

```
python -B scripts/reference/startup_transport.py fixture readiness
python -B tests/reference/startup-seam/run_suite.py --junit /tmp/startup-suite.xml
python -B tests/reference/startup-seam/mutate.py
```

The closed CLI accepts only8 named harmless disposable TEST cases. The Python API
accepts explicit lawful immutable specs. Before/after hooks are bounded subprocess
CommandSpecs with copied JSON stdin, not trusted in-process callbacks. See the
contract for single-threaded launching, exact limits and sampled-resource caveats.
An escaped daemon remains UNKNOWN even when the foreground command succeeds;
unknown ownership never authorizes commands/signals/unlink or original progression.

No Go source/module was changed. Actual configured runner7 records have4 executed
passes and3 no-package skips; nested archived WP33 Go files are isolated by their
own module, not overlaid or built by this package. No Go/race/fuzz verification is
claimed for nonexistent root packages or for unchanged native parsers.
