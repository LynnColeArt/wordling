# WP104 acceptance RED

Baseline e96b7a2896f26f626cf6c3b1b1215eb3e0040fa3; no production source changed. Actual offline ordinary TEST wheel was built from canonical E/P/peer source and installed into a copied isolated venv, without PYTHONPATH or source overlays. No ROOT coordinator invocation, CONTROL administration/leaf, original resource or VM occurred.

Command: `/usr/bin/python -B -m unittest discover -s internal/document/evidence/reference_controller/tests -p test_original_admission.py -v`. Exit1, two tests executed: existing TEST/raw and parameterless ROOT boundaries PASS; new installed original public entry fails because reference_controller.original is absent. This is the missing public interface, not evidence that its future refusal semantics already work. Raw stdout/stderr are retained.

An earlier harness-only zero-test error used the wrong canonical peer source location. Its raw logs are retained as initial-harness-red.*; the helper now uses actual retrieve-field-observations peer/boundaries. It is not counted as acceptance RED. The real two-test RED above follows that correction.

The test preparation helper currently stages the existing TEST wheel solely for this pre-implementation RED. Production delivery must switch to the separate exact original ordinary-wheel map and keep the old TEST wheel recipe untouched. Positive CONTROL execution remains prohibited until frozen closure review and ROOT decision.
