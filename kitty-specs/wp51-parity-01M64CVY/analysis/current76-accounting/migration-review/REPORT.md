# Independent native capture v2 and one-shot migration static review

**APPROVE_EXACT_NATIVE_CAPTURE_V2_AND_ONE_SHOT_MIGRATION_STATIC_ONLY.** No actionable static findings remain against these exact artifacts. Audience: ROOT and the phase-two operator. This is source/migration readiness review only; it grants no helper operation, migration, phase2 publication, native command, product parser/DATA/TCB execution, WP CODE approval or mission acceptance.

I am Reviewer Renata, different from the source author. I reuse my personally resolved review context retained in the prior resolver-captures.json.gz SHA48beb26d33d7539405ff148e7b84d8fdfa7caf61ae6514921b5fd6307d223430. No new resolver invocation or another agent's context is claimed. This<=5file/96KiB packet consumes the existing REVIEW disposition16/512KiB allocation alongside the prior four-file helper review; its canonical copy also consumes the existing CURRENT26 allowance.

## Exact source and full delta

V2 root /tmp/wordling-WP70-native-capture-helper-v2 is exactly three regular0600/uid1000/gid1000 files,54,286B:

- capture.py46,577B/SHA9cc3fac98ace24f1bad75e99d696e1d909d37844ee2e191262d6a749fb337155.
- config.json3,698B/SHA32295139e18e5040b6475e7adda5dce143f287003760af527b4ec1c6e9bc1980.
- source-checkpoint.json4,011B/SHA958f5809cf9b23b247a110a3690e91fa261d75d56099596f5a78640795806f6c.

All remain inside source56KiB/config4KiB/checkpoint4KiB and total64KiB. I independently pinned the unchanged v1 sourceb530531..., configc836447... and checkpoint1c0d758... from their original root. No old file, approval or phase-one receipt was overwritten.

full-source.diff is the entire literal delta against those immutable bytes:13,050B/SHA74b72dca3fd47ab26f5f94ef80bfc3479095e0b8f7b0324c45160705d5cae900, using the checkpoint's explicit absolute old_path/new_path headers. I read every delta and the affected complete constructor/scan/migration/publication/main bodies. Independent AST comparison verifies every global helper unchanged, all imports unchanged, and every shared Writer method unchanged except __init__,scan,publish; init is removed and migrate added. Native-family, capture/drain/wait, budget, save/begin/finish, metadata serialization/copies, task-update, stop/close methods remain exactly the same AST. No raw, command, guard, resource or runtime-role weakening hides in the delta.

The source remains an ordinary standalone __main__ script. Only previously reviewed stdlib imports occur; no product/q import, custom loader/sys.path/module alias, dynamic code producer or callback is introduced. ROOT must invoke the exact pinned v2 script path/interpreter/checkpoint/plan in a later grant; this review does not authorize an alternate source copy or cached imported entry point.

## Missed v1 integration case and concrete accepted carrier

I missed the v1 integration coupling: publish always prepended a nonempty packet label, but native_family requires root-level CURRENT_root/analysis.md. Phase-two read-only preflight found this before any phase2 plan, staging, native call or canonical write. It was an implementation gap, not an exercised failed native run. My old approval remains literal history; I do not rewrite it or claim the case had been tested.

V2 permits an empty label ONLY when publication family is CURRENT and phase is2. Nonempty labels still pass the original strict safe_relative path check; relative member paths always remain strict, execute suffixes become inert.txt, duplicate destinations and reserved ADOPTION/map/outer names refuse before writes. No traversal, wrapper alias, duplicate carrier or different record path is used.

I fully verified the actual accepted /tmp/wordling-current76-accounting-analysis packet:18files/114,938B; seal411511974559b600e3492cb5a0d5d0f118877ee6d37325ef7685d71228bef9a0; analysis.md19,975B/SHAaf8a9c36994b143b84a7e3d52b560f6214f69d35e57ae05e3f93f78d8276dd83. Every declared member hash/rights and the exact closed filename set match. It has no reserved wrapper-name collision. With its empty label, the unchanged original analysis.md bytes resolve to:

/home/lynn/projects/wordling/kitty-specs/wp51-parity-01M64CVY/analysis/current76-accounting/analysis.md

That is exactly the configured CURRENT root and native record-analysis input path. verify.py becomes verify.py.txt; the already inert verify-first.py.txt stays unchanged. All18 literal members, including prior analyst failure evidence, remain present. This is an independent metadata destination calculation against the real inputs, not a call/test of the authored publisher.

This five-file review must be a second, nonempty-labelled migration-review packet in the same publication. It must not also be rootless: shared filenames such as seal.json/verification.json would collide. ROOT will freeze and verify the exact label/manifest before publication.18+5+3outer files=26, within CURRENT26; old canonical58+phase1amendment46+CURRENT26=130 within160/four roots. The third v2 metadata root is CAT, not an extra canonical-publication root.

## Exact old binding, ownership and migration order

The original shared STATE is still26,913B/SHAd3a09e9834f9ff19ef8a95309f2be25cd65d7ebc1b30f48c8a5eb6ebfa6b3834, regular0600/uid1000/gid1000. It is ready phase1, command index3, pending[], task_doneTrue, plan89fd0e57433ef7eddfc526a8ca1172360a3897ef3a293a048f917558f7c72fb4 and v1checkpoint1c0d758.... I independently resolved ALL73 existing pins/rights and the complete old owned directory closure, including the canonical phase1 publication; all78 old highwater entries remain unchanged. STATE.next,STOP,FINAL, task stage, v2snapshot and migration receipt are absent. No transition or phase2 effect occurred.

Both pre-lock and post-lock constructors allow the old binding only when the explicit operation is migrate. Default v2 operations require its own checkpoint and migration.completeTrue. The existing nonblocking original LOCK is reused; no second owner lock, init/bootstrap/reset or generic active recovery exists. Migration also checks exact old STATE SHA, ready/phase/index/task facts, original plan with exactly three commands, all three old source/config/checkpoint pins, whole closure, current task-after pin, all old charges and absence of inherited failure/temporary paths. A nonmatching or active/stopped/partial input is not a migration source.

The static write order is precise:

1. Validate all old/v2 pins and exact three prepared v2 files; calculate budget for the five declared new paths before writing.
2. O_EXCL-write and verify the literal old STATE-v1.json snapshot, then recheck the still-old shared STATE. Snapshot precedes the binding transition.
3. Preserve all old highwater values and old phase/index/plan; add the new source pins/snapshot, mark active migration.completeFalse, activate the new checkpoint through the existing charged STATE.next→STATE atomic save.
4. Write the<=32KiB MIGRATION receipt describing the OBSERVED ACTIVE transition, source pins, snapshot and separately named old/new highwater digests. It does not pretend to contain an already-final ready-state proof.
5. Pin that receipt, set migration.completeTrue and use the unchanged finish/save/check path to publish ready state.

The snapshot and receipt have fixed names and O_EXCL/lexists no-partial-retry guards. New-root scan allows only the three source files plus STATE-v1.json and MIGRATION.json, flat regular files; unknown members refuse. No commands0–2 are replayed and no phase/index/plan assignment occurs in migrate. V2's retained existing phase2 method can begin only after ready migration and a separately pinned new ROOT phase2 plan.

After the active new-checkpoint STATE save, unchanged v1 fails its strict StateBinding inequality. Default v2 also rejects an incomplete migration; for_migration rejects the now-new binding, preventing replay. Before activation, a partial snapshot likewise prevents a second migrate via its no-partial guard, while default v2 rejects the old binding; the old phase1 grant remains spent and supplies no phase2 authority. A failure is retained as UNKNOWN/STOP or incomplete state, not automatic recovery permission. I did not execute v1 to demonstrate refusal; this is the exact source comparison and binding proof.

## Same budget, bounded memory and unchanged failure semantics

Only five new CAT paths are admitted: three source checkpoint files, old-state snapshot<=32KiB and receipt<=32KiB. Actual source54,286 + old snapshot26,913 + full receipt reservation32,768 =113,967B; the conservative complete maximum remains131,072B. All78 old entries remain identical and exactly five entries are added, giving83 highwater paths before phase2. Static current family sums remain within their existing caps; CAT includes the charged task-stage slot even while absent.

The checkpoint's prior complete-cycle projection81files/12,796,765B plus five/131,072 yields86/12,927,837, within the SAME96/16MiB by10files/3,849,379B. This is the stated preflight projection, not independently minted future pins or a promise of completion. ROOT must remeasure the exact phase2 plan/output set after this review seals. Canonical families64/2MiB and CURRENT26/2,359,296B remain unchanged; no extra class/root/loop credit is created.

Both existing coexisting262,144B STATE slots, STOP65,536 and FINAL262,144 remain charged; no migration resets their maxima. Old-state retention/snapshot/receipt each have an explicit32KiB bound; state/input nodes/depth, chunking, per-file metadata3MiB and raw shared<=1MiB are unchanged. Receipt content is bounded metadata with finite source pins/digests, not a decoded copy of all historical catalogs. Serialization is still measured before writes. Existing descriptor-relative nofollow walking, no-clobber writes, fsync/atomic save and exact task overwrite boundary remain intact.

Because capture/native methods are unchanged AST, the reviewed ordinary overflow EOF-drain, catastrophic unusable-owned-pipe UNKNOWN+actualwait, constructor-failure launchUNKNOWN, no signal/kill/timeout/retry/foreign-proc, stopped-state and final-state semantics remain exact. This preserves static conclusions only; no new failure-path test or whole capture is claimed. A failed intermediate migration cannot become a successful ready receipt or another native authority.

## Own verification and limitations

My corrected independent checker completed1,795checks, whole exit0/empty stderr in0.113556212s, reading4,621,253B. It nofollow-hashes the exact source/config/checkpoints, all73 old pins, current STATE/task and all18 accepted carrier members; walks old closed roots; checks class sums; reproduces the full diff; compares unchanged AST bodies; examines the migration operation/binding/order/no-replay guards and the actual carrier destination. verification.json retains literal argv/cwd/stdout/stderr/exit/wall. It never imports, compiles, calls or executes authored helpers, migrations, publisher functions, native commands, product code, models or tests. Snapshot/receipt future pins remain UNKNOWN.

My first own checker used shorthand diff headers old/capture.py→v2/capture.py from prose instead of the explicit absolute old_path/new_path fields. That produced a different header-only digest. I corrected only my checker; the explicit-field reproduction is exactly13,050B/74b72dca as declared. The complete failed checker source and literal failed capture remain in verification.json. This was a reader error, not an author/source defect or runtime retry.

ROOT must now fully read/verify this closed review and freeze exact migration/phase2 plans and current pins before issuing any separate operation grant. The unchanged H-time CURRENT carrier is not silently rewritten; the v2 delta travels as this separate reviewed packet. All v1 evidence, prior approvals/refusals/spent grants/UNKNOWNs remain literal. No M1 completion, Bold CODE handoff, M2/PDF or product compatibility claim follows.
