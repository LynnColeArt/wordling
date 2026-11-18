# Corrected WP104 pre-CONTROL review — REQUEST CHANGES

Fixed HEAD: **59a665acacb50e23249a2a5dc7761e9bb4c1ccca**, production source checkpoint **d00fe267**. Source manifest SHA256 **869a15c39fe4fc39c68c8e88f93891158148de303af5e684a29ce3c7fb3f0fc8**; finite campaign SHA256 **cb128b5ffc179b6ff2fcdc5e2b5afd1d635bc956661d79bf02274f5472e2f57f**. Independent reviewer-renata context remains the resolver-produced review-governance.json, hash9cc878b18c35b303. This review performs no lifecycle verdict event and authorizes no ROOT/admin/P/CONTROL/TEST/ORIGINAL/Mac action.

**R1, R2 and R4 are corrected. R3 is substantially improved but the exact campaign is not ready to accept or execute.** Two demonstrated feasibility defects and the separate TEST qualification prerequisite remain. Do not add accepted review refs to any B yet.

## Accepted corrections and inspected closure

- The two CONTROL fault/cleanup methods now belong to the actual OriginalLeaf class. They retain literal CONTROL/case restrictions. The installed class regression directly catches the previous placement fault without manufacturing a grant.
- Actual ledger states are now canonical AUTHORIZED and RUNNING. Diagnostic facts retain AUTHORIZED_UNREADY/OWNED_UNREADY, ready=false, unresolved hold and physical_released=false. Unowned records.py is unchanged; the installed schema/fact test uses that actual module. RUNNING is written only after retained P ownership/identity checks.
- Administration now invokes the shared registered-source identity comparator before creating effects, after bounded nonempty file/read phases, after each complete group and around the receipt. The funded leaf verifier uses the same comparator; the admin DATA checker grants no authority. The actual disposable-source phase refusal and nonvacuous structural bypass regression are appropriate pre-control evidence. The81 source phases ×27 identities and1530 other syscall reservations give3717, within4096; declared10278 work is conservative.91 files,129 directories and29381237 IO bytes fit the unchanged bounds. Actual successful administration remains UNRUN.
- All nine ordinary candidates have independently checked source-to-installed bytes, exact listed semantic edit sequences, code/data/deployment evidence pins, complete inventory members/directories, absent archive and no symlink/cache addition. **6804 inventory entries /921720316 bytes total**,756 per candidate, largest179361-byte inventory; zero integrity discrepancies. This includes all mutant postimages rather than trusting that compilation alone establishes deployability. All B reviews=[] remain unaccepted. No old candidate was repaired or moved by this review.
- Same canonical issuer, permanent stable IDs, durable hold before grant, exact live grant/plan binding, retained physical guard and actual P route remain. The reviewed private memory-only128-syscall handoff still keeps the original1024 issuer cap and earlier2s end. No new generic account/ownership/P API or alternate authority was introduced.
- The source-stamped M01–M08 namespaces are fixed before deployment and disjoint from baseline. Each has its own C/K/P/R/D/B and no-clobber admin. M08 genuinely changes both hold inventory refusal and later hold creation; it can reach the intended second-ID target without the earlier EEXIST false kill. M02/M03/M05/M06/M07/M08 intended witnesses now distinguish the relevant safety property from unrelated failure. Actual semantic kills are all UNRUN.
- The finite manifest has333 unique case IDs,285 PASS data/cold/static cases,46 UNRUN operational cases and2 BLOCKED TEST CLI cases.38 ROOT actions and9 admins are separately counted. Reservation groups sum4520s. These counts are honest, not evidence that operational cases passed.

## Blocking finding A — genuine TEST boundary's positive activation cannot fit its unchanged issuer cap

`tests/test_original_admission.py:48–69` loads **OriginalSourcePolicy**, with27 verified identity rows, then uses unchanged TestIssuer.issue/activate. Its baseline expects post-original-refusal activation to succeed. That expectation is infeasible under the unchanged1024 issuer check cap.

Static source accounting for the exact fresh TEST root/two metadata entries and normal complete first marker write:

| Stage | Issuer check/syscall charge count |
|---|---:|
| Reserve's actual coordinator sample |18|
| Explicit issue source verification |3n|
| TicketStore.open, including first validation |3n+78|
| Store inventory charge/two entry work checks |5|
| Pre-marker validation |3n+27|
| Marker open/fstat/flock plus binding's37 charge checks |46|
| Write and read charge/calls plus two fsync calls |14|
| Five post-marker validations, three retained files |5×(3n+33)|
| Final publication check |1|
| **Issue total** |**24n+354**|

For n=27, publication consumes1002, leaving22. `TestIssuer.activate` at issuance.py:579–580 marks the genuine grant used and immediately validates the retained store. Its source verification alone needs81 before the rest of store/coordinator validation. It must hit OperationLimit, even with healthy OS input. For the canonical TEST20 policy, the same accounting is834 plus a fitting activation tail; this is why the unchanged route worked with its actual source set. The count is derived from `PhaseReservation.check/charge`, ownership._call, actual source identity loop, store topology and binding cardinality; no fake meter/grant or operational call was used.

Consequences: baseline post-refusal activation cannot pass; M01 cannot claim the intended clean-baseline comparison from its current recipe. OperationLimit alone is not an unrelated-refusal kill.

Minimal reviewed correction: retain the genuine issued TestGrant but narrow this package's boundary target to the actual public original gate—exact SourcePrelaunchBlocked before hostile source/plan access and no inappropriate grant consumption—rather than promising a successful later TEST activation in this27-source runtime. Define a precise causal M01 witness for its unauthorized actual activation/consumption attempt (including the intended call/used-state observation), not generic exception matching. Observational grant state may supplement real public behavior; no private key, fake grant or registry injection. Recount/review the revised target and manifest. Alternatively a genuine separately qualified same-interpreter TEST20 arrangement would need its own concrete supported source/layout plan; a grant from another process cannot be transferred across the exact live registry/type boundary. **Do not enlarge TEST's1024 cap or weaken its guards.** The full public TEST CLI positive is a separate requirement below.

## Blocking finding B — proposed1200s namespace reservation omits live baseline actions

The1150s baseline figure includes only23 ROOT actions ×(30s action +10s observation +10s preflight). But the baseline namespace also must run these after administration and before destructive final SOURCE:

- genuine-TEST:baseline:30s;
- raw-after-admin:30s;
- causal observations for those two public groups:20s.

That gives **1230s** assigned work in the namespace, not1150. Even crediting the first admin preflight10s before the namespace origin leaves1220 >1200. The claimed50s unallocated is already less than the two required30s public groups, before observations.

The7200s global proposal has room above4520s of reservations, but it does not repair this tighter live predicate. Correct the full namespace schedule and either prove genuinely shared smaller phase reservations or request a precise finite namespace extension with matching source/admin-receipt/issuer checks and fresh repinned candidates. Do not renew an expired clock, delete/re-administer the root or omit a target after starting. Root should retain one external whole-campaign budget/start/remaining record and require room for the complete next action/observation/preflight before each individually deliberate invocation; this adds no batch authority. The revised complete finite extension needs review before first admin.

## Required causal manifest annotation

C104-CONTENTION and C104-MISSING currently list raw BlockingIOError:errno11 and FileNotFoundError:errno2 as allowed outcomes. Actual `_Guard.call` uses unchanged `ownership._call:18–20`, which wraps those OSErrors as **Refusal FilesystemFailure, partial=true**, with the exact errno exception as cause. Name that real top-level result plus intended causal phase/errno witness. Do not accept any earlier unrelated FilesystemFailure. This is a manifest correction, not a reason to weaken or change the production wrapper.

## Disposition of the separate unchanged TEST positive

**The scoped public TEST compatibility obligation does not intrinsically require replaying the retired188-path campaign.** Actual source proves a supported noncampaign deployment branch exists:

- `controller_deployment.deploy:185–191` creates real Preparation with no campaign by default; it is not an invented mode flag.
- Same routine freezes TEST20 source members, the canonical0.2.0 TEST wheel, original harmless_fixture.c and30720-byte source-defined master, verifies wheel/install members/RECORD/source/data and actual copied interpreter/class/provider/import observations.
- Exact188 inventory is conditional at the campaign helper and inventory selection. The actual noncampaign branch at363–370 accepts a complete <=1024 inventory after the same strict normal copied3.12.14 layout/flags/origin checks. It ends in actual preflight and input custody checks.
- Installed `bootstrap.load_policy` retains SourcePolicyData/exact TEST20/data/package/module checks. Public `cli.leaf_transaction` uses genuine TestIssuer.reserve/issue, ReferenceController.open_leaf, run_leaf and actual close. Neither this CLI nor run_leaf requires a campaign/188 object. Thus a correctly qualified current ordinary TEST runtime plus real public test-admin/test-leaf healthy evidence can satisfy this specific compatibility regression; it would not requalify the old campaign or its provenance.

**That legitimate contract does not make the current helper runnable without its prerequisites.** Default noncampaign deploy still calls load_expected at the missing V19 path. Preparation/admit_capacity require the exact capacity baseline, expected closed roots, evidence/reference custody, tool selection and current file/right pins; check_selection_records also preserves the historical20279 external subset and explicit tool records. strict_layout/compare_observation retain the real3.12.14 base/prefix/features. A newly observed ORIGINAL756 tree, arbitrary expected dict or choosing context=None does not replace these inputs.

There is also a concrete current-provider provenance difference: noncampaign `Preparation.provider_rows:3103` returns the old PROVIDERS literal with lifetime.py commit eba8382f (SHAba82bf709a6c6eb39f40197ce284f3d144a58802e925ff316c8720638acb709d). Current approved source equals7869159b (SHA3a6130bef6516648189f61ba4dd2dbc8cdf3360249307b71d062ef4c5ce98050). Only genuine campaign/cold-qualified paths select that newer row. Do not label current bytes as the old approved blob.

If exact historical inputs cannot be recovered with correct custody/current postimages, a **separately owned, source-reviewed TEST deployment qualification prerequisite** is legitimate and necessary. Its bounded scope is a fresh immutable current TEST20 + original TEST fixture/master + approved current P closure; ordinary copied runtime with mandatory features/normal isolated prefix/imports/no customization; exact tools/native dependency/right inventories frozen before effects; source/expected/provider provenance and resource/clock/output/evidence/cleanup accounting; complete preflight; then genuine public TEST CLI admin/healthy run_leaf and actual P stop/export/containment receipts. It must explicitly select current approved provider bytes without claiming old campaign qualification. Preserve operational TEST source/data/type/owner/cap/P guards, do not modify old expected inputs/approvals, and do not use ORIGINAL policy/fixture as the full TEST-positive substitute. Any qualifier/helper amendment needs its own owned scope/review, not an unowned WP104 edit. No new package number or execution is assigned by this report.

The current960s existing-TEST reservation is an allowance, not this missing source/runtime plan. Freeze the actual candidate/recipe/prerequisite before accepting the complete campaign. TEST type-boundary work in finding A does not satisfy the public healthy run_leaf requirement.

## Final disposition

REQUEST CHANGES for accepting/executing the exact current campaign. R1/R2/R4 source corrections and nine immutable candidate closures are sound on this read-only recheck. Correct findings A/B and the errno annotation; bind the actual separately qualified TEST-positive recipe or an independently reviewed prerequisite/staging disposition that preserves its mandatory completion gate; then request a new exact pre-execution review. No B has been accepted and all48 operational compatibility/control cases remain unrun/blocked. No semantic survivor/kill or original/M1/Mac result is asserted.

Independent artifact: `/tmp/wordling-mission1-closeout-20261118/wp104-review-clean-independent-evidence.json`. Source/evidence/candidate hashing, AST/static budget arithmetic and public tracked API inspection only; no operational modules imported, no ROOT/TEST/CONTROL/P/Original action, and no repo/index/runtime change.
