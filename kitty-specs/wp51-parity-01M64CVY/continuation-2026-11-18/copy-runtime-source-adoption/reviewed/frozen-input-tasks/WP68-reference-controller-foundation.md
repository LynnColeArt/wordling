---
work_package_id: WP68
title: Finite reference authority foundation and real TEST transaction consumer
dependencies:
- WP55
- WP57
requirement_refs:
- NFR-002
- NFR-003
- NFR-004
- C-001
- C-004
- C-005
- C-006
planning_base_branch: feat/wp51-parity
merge_target_branch: feat/wp51-parity
branch_strategy: Planning artifacts for this mission were generated on feat/wp51-parity. During /spec-kitty.implement this WP may branch from a dependency-specific base, but completed changes must merge back into feat/wp51-parity unless the human explicitly redirects the landing branch.
subtasks:
- T202
- T203
- T204
phase: Harmless TEST only; production original route blocked
history: []
agent_profile: implementer-ivan
authoritative_surface: internal/document/evidence/reference_controller/
create_intent:
- internal/document/evidence/reference_controller/__init__.py
- internal/document/evidence/reference_controller/__main__.py
- internal/document/evidence/reference_controller/bootstrap.py
- internal/document/evidence/reference_controller/errors.py
- internal/document/evidence/reference_controller/account.py
- internal/document/evidence/reference_controller/ownership.py
- internal/document/evidence/reference_controller/records.py
- internal/document/evidence/reference_controller/issuance.py
- internal/document/evidence/reference_controller/cli.py
- internal/document/evidence/reference_controller/pyproject.toml
- internal/document/evidence/reference_controller/tests/
- internal/document/evidence/reference_controller/evidence/
execution_mode: code_change
owned_files:
- internal/document/evidence/reference_controller/__init__.py
- internal/document/evidence/reference_controller/__main__.py
- internal/document/evidence/reference_controller/bootstrap.py
- internal/document/evidence/reference_controller/errors.py
- internal/document/evidence/reference_controller/account.py
- internal/document/evidence/reference_controller/ownership.py
- internal/document/evidence/reference_controller/records.py
- internal/document/evidence/reference_controller/issuance.py
- internal/document/evidence/reference_controller/cli.py
- internal/document/evidence/reference_controller/pyproject.toml
- internal/document/evidence/reference_controller/tests/**
- internal/document/evidence/reference_controller/evidence/**
role: implementer
tags:
- m1-continuation
- one-leaf-reference-controller
- harmless-test-only
task_type: implementation
tracker_refs: []
---

# WP68 — finite authorities with a real installed TEST consumer

Audience: E implementer/reviewer. Implementation follows independent TASK review, normal canonical/CURRENT validation and the actual issued claim. It is deliberately the foundation part of the prior whole-controller task. WP70 delivers run_leaf; this package MUST NOT add a fake/BLOCKED0 run_leaf, claim controller/original qualification, or defer its own authority tests to70.

Read accompanying tasks/next-increments-68-69-70-task-proposal/COMMON-E-CONTRACT.md, approval/source-binding/current-guard/acceptance-matrix and preserved whole history. R3 newledger/permit/durableissuer/bootstrap precedence and R2 remaining contracts bind exactly; no new architecture is selected here. Originalresources/normalDOS/native/privatefit/prelaunch/NEW exactROOTgrant remain unknown/separate and productionentry disabled. No P/peer import/runtime dependency in this foundation; WP55/57 give actual historical ledger/ownership/safety semantic constraints, not oldclass runtime reuse.

## T202 — actual same-book permits, retained parent and finite ledger

Implement only errors/account/ownership/records in owned canonical namespace, with genuine typed LeafAccount/LedgerOperationPermit/ParentLease/OwnedLedger APIs and finite exact LedgerRecordV1, as common contract and R2 CONTRACT §§1–5. One-use issuer/live-object/account/source/leaf/parent/operation/end/maxima binding and fullspend before traversal/IO; account filesystem-effect-free and unauthorized before actual issuerhandoff. Preserve exact finite JSONschema/type/aliases/Unicode/int64/two-pass/work/buffer/syscall/chunk/readback rules. Retained root/componentfd/ancestorlink checks/no-clobber/foreignpreservation/currentclock/partialIOtruth/no rollback/cleanupfdidentity are required. No scalar permission/path+stat/callback/recordfacts authority. The account must also deliver the ALREADY reviewed full-phase cumulative reservation/book interface for frozen issuer/ledger/Eprotocol/P/helper/chunk/binarypublication/audit dimensions (integration-R2 ENVELOPE retained-authority contract), not a ledger-only budget dead end. The four LedgerOperationPermit kinds remain acquire-parent/create-ledger/update-record/cleanup-close; binarypublication stays a separate authority in70, no added ledgerkind or Pcredit factory. Source-owned transaction consumers must exercise genuine fullspend/bounds/remaining/no-refund reservations for these fixed categories, proving interface usability without pretending protocol/P/output effects occurred in68. Actual P enforcement/usage is70composition, never simulated authority.

Tests-first via actual new public TEST transaction consumer must demonstrate legitimate acquirepermit→ParentLease→createpermit→OwnedLedger→updatepermit→write→exactreadback→reservedclose, not an unusable abstract API. Actual permit/source/kind/root/owner generation copies/stale/consumed/wrongissuer/fieldidentical substitutes refuse before encoding/effect. Exact recordbytes and all meaningful finite/malformed/huge/custom/alias/cycle/Unicode/depth/work/IO/late/ancestor controls are intrinsic to68. Preserve raw failures and complete actual prior/partial bytes. New classes are not oldOwnedFile aliases/subclasses/extractions; old51/55/57 source/error/default/loaders/sets/hashes untouched.

## T203 — durable pregrant issuer and ordinary real TEST transaction CLI

Implement issuance.py actual TicketStore/RootTicketIssuer and disjoint TestTicketIssuer/TestGrant, separate bounded TEST administration/preprovisionedstore, stableID permanentO_EXCL→boundedwrite→filefsync→parentfsync→readback/currentidentityclock→privateCOMMITTED→opaqueactualgrant→consumehandoff→activateSAMEbook→parent/ledger. Implement real `-I -B -m reference_controller` ordinary sealed-wheel/venv bootstrap and source-defined finite public TEST ledger/issuer transaction CLI in cli.py, including explicit harmless TEST admin prerequisite and transaction result diagnostics. This is production maintainer TEST code, not a pytest-only helper. It must call every new consuming API legitimately, use the same actual source-owned issuer/account/activation path that70will consume, record initialcharge/finaltransactioncompletion, release/close truthfully and preserve permanentticket. No P Session/foreground/peer/QMP/controller/physicalreference-lock activity in68. Source-owned TEST transactions remain permanently original_qualification:false.

__init__ empty/__main__ minimalstdlibdelegate/bootstrap preimport flags/spec/origin/cache checks; trusted prelaunch exact regular pinnedcopiedinterpreter/venv/wheel/stdlib/sites/deployment exclusion. No loader/global/sys.path/module injection. Complete offline packaging/installmanifest proof from unrelatedcwd/hostilePYTHONPATH/cache/foreign origins and actual postimportclasses required. E70 may coordinate narrowly adding approved provider/peer closure and additional CLIroutes;68does not import them prematurely. pyproject is packagingmetadata only, no runtimeinstaller/network/proprietary source.

Issuer/store limits/trust/generation/bootquarantine/cap256/lock/stablekey/noGC/noIDreuse/fullspend/no capability recovery remain exact COMMON contract/R3 ISSUER. Originalissuerentry deliberately refuses before any original/private/grant effect pending separately reviewed gates; sourcevalidation/CLIboolean/SourcePolicyData cannot authorize it. Harmless TESTstoreadministration is explicit bounded prerequisite, not issue automaticmkdir. No actual original store/grant is provisioned.

## T204 — intrinsic real public authority, process-loss and custody acceptance

Run finite source-frozen public installed TEST transaction roster through genuine OS/files/permits/serialization, not mockedauthority/ticketmodel. Positive checks exactindependentlyexpected full ledgerbytes, alllegitimateAPIcalls, same earlierorigin/book/spend through issuer→parent→ledger→audit/close and genuine priorforeign bytes unchanged. Actual separate harmlessprocess losses after markercreate/bindingwrite/prefsyncloss/COMMITTEDbeforereturn/handoffbeforeparent/duringparent/beforeledger/aftercreatebeforecharge/afterdurableledgerbeforeresult/completehaltclose; freshprocess sameID with existing/spent/possiblycreated marker cannot gain fresh setup/parent/ledger effects; existingmarkerbytes unchanged. Before finalO_EXCL creates a marker, prove NO actual grant/downstreampermitcouldescape: absentmarker is not durableattemptdetection/proofrequestneverran, and no automaticretry/reconstruction is permitted. Any created empty/partial/foreign marker is permanentlyspent. Do not repeat the old overbroad historical 'secondprocess ALWAYSrefuses' assertion across the pre-first-effect boundary.

Real sameIDraces atmostone actualgrant, differentIDlock/cap256full refusal, changedsourceplanleafbudgettime binding underSAMEIDcollision, wrongkind/storegeneration/UID/bootquarantine/lockretarget/link/ancestorreplacement, fsync/zero/shortwrite/readback/clock/postblockinglate/descriptor/FDreuse controls. Fullspend/permit/encodebeforelimit/ancestorguard/durableorder/stablekey/replay/bootquarantine/sourcebootstrap semantic mutants must fail their actual public target, no construction-only substitutions. Source/evidence/wholehistory/oldprotectedsets/configuredlint/AST/compile/JUnit/cmd/env/binarycustody according to common finitebounds, honest no-root-Go skips. No source/runtime imports outside ownedchanged harness closure/no broad original/Go/fuzzcampaign. Each result remains TEST authorityfoundation only; controlleracceptance matrix explicitly marks70 NOT delivered.

Commit only actual ownedfiles. Request ROOTquietpoint before done/ONE ordinaryfor_review; independentotherreviewer, no selfapproval/otherWP claim/accept/merge/push/private/physical-lock/grant. Old38/91/36/nestedM1remainOPEN/M2gated. WP70 must consume ACTUAL independently approved68 source/classes, not this task/placeholder/currentmovingtree.
