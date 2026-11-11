---
work_package_id: WP95
title: Admit the licensed ESDB lexicon and publish native supplementary dictionaries
dependencies:
- WP87
- WP98
requirement_refs:
- FR-004
- FR-005
- FR-014
- NFR-001
- NFR-002
- NFR-003
- NFR-004
planning_base_branch: feat/wp51-parity
merge_target_branch: feat/wp51-parity
branch_strategy: Planning artifacts for this mission were generated on feat/wp51-parity. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/wp51-parity unless the human explicitly redirects the landing branch.
subtasks:
- T312
- T313
- T314
phase: Everyday editing corrective integration within M1
history: []
agent_profile: implementer-ivan
authoritative_surface: internal/proofreading/provider.go
create_intent:
- internal/proofreading/lexicon.go
- internal/proofreading/lexicon_test.go
- internal/proofreading/supplementary.go
- internal/proofreading/supplementary_test.go
- internal/proofreading/resources/en_US.txt
- internal/proofreading/resources/README.txt
- internal/proofreading/resources/README_en_US.txt
execution_mode: code_change
owned_files:
- internal/proofreading/provider.go
- internal/proofreading/provider_test.go
- internal/proofreading/README.md
- internal/proofreading/lexicon.go
- internal/proofreading/lexicon_test.go
- internal/proofreading/supplementary.go
- internal/proofreading/supplementary_test.go
- internal/proofreading/resources/en_US.txt
- internal/proofreading/resources/README.txt
- internal/proofreading/resources/README_en_US.txt
role: implementer
tags: []
task_type: implementation
tracker_refs: []
---

# WP95 — Admit the licensed ESDB lexicon and publish native supplementary dictionaries

Use the issued prompt, WP78 original evidence and milestone EE-013/EE-015 acceptance. The current provider/session source audit found demonstration behavior in production. Preserve prior verdicts and source boundaries. Proofreading must work generally through admitted resources and observed contextual behavior. Exact original lexical ranking remains outside the approved Linux adaptation.

## T312

Implement an immutable real provider for the reviewed linux-esdb-en-us-2026.02.25-plain-v1 profile. Embed exact en_US.txt and both archive notices from the hash-verified release; check the approved raw hash and parse declared CRLF, with bounded strict resource admission, no case or encoding loss during admission and no network or fixture fallback. Expose explicit acceptance, ranked bounded suggestions and lookup with deterministic output; document ASCII and case policy, limits and original_lexical_equivalence=false. General dictionary witnesses must cover unrelated words and common typo/wildcard cases. Keep only source compatibility required by the existing WP88 consumer until WP96 switches it to the real provider.

## T313

Implement uncompressed native SUP admission and persistence using WP78 user-authored specimens: exact supported prefix family, HRt-terminated lexical entries, bounded sizes and duplicate handling; reject compressed, mixed, malformed or unsupported resources before mutation. Support default WP{WP}US.SUP and selected custom exact DOS filenames. Use a live pinned WorkspaceDirectory with Observe/Read and existing PrepareSave/PrepareNewSave/PublishSave/PublishNewSave with WP98 preserve-backup policy, fresh operation identity and exact expected source/target snapshots. Do not bypass publication checks or fabricate success. A pre-publication failure preserves prior bytes, uncertainty is reported with no adopted vocabulary, and restart rereads actual published bytes. Exercise missing/new, existing, duplicate, alias/stale and permission/fault cases.

## T314

Expose provider and supplementary operations to WP96, with a copied immutable supplementary snapshot and context-aware cancellation before publication. Verify provenance against reviewed adaptation and native SUP fixtures; test original DOS opens an authored SUP result. Run focused tests and full Go build/test/vet, format/diff checks, commit scoped changes and request independent review.
