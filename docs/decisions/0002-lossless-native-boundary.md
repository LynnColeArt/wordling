# ADR 0002: Preserve native bytes before semantic mutation

Date: 2026-10-30. Status: Accepted for M1 planning.

The permanent compatibility contract requires byte-identical no-edit saves and preservation of unrelated/unknown data during edits. SDK51 framing includes linked prefix packets and nested function content; a flat text/style representation cannot account for all original bytes. Existing original fixtures already expose command-dependent code and packet behavior.

Use an immutable owned native byte image with validated spans as the preservation authority. Decode semantic structure separately and advertise exactly which mutations are supported. No-edit export returns byte-for-byte original content; unsafe mutation is refused before filesystem replacement. Terminal rendering and layout never own serialization.

This lets a small reader/preservation slice be tested against original-produced fixtures without pretending it supports general editing. It costs memory proportional to retained original bytes and requires deliberate span/semantic reconciliation for later edits. Set input/resource limits explicitly in the framing contract; do not hide them as parity exclusions. A rewritten normalized format or Unicode-only canonical image would violate the owner-approved contract.

Evidence: `docs/compatibility.md`, `docs/research/findings.md`, `kitty-specs/wp51-parity-01M64CVY/research.md`. This decision does not select a future piece table/rope, permit a general native writer, or establish layout fidelity.
