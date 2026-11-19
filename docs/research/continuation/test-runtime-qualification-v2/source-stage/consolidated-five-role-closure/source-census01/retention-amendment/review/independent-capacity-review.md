# WP108 retained-file capacity review

**APPROVE** the conditional retention plan from **1,024 to 1,176 files**, for final six-file manifest `efa6cfaefec85eb058e9d63a3a93f3b7c5907f430682b6f7ee188c0ce008d808` / design `1b12326a44a32334e403690d19b2c65c087f258189b9cdefae17213d7aea9293`. No blocking capacity finding. This verdict does not approve census source, TDD execution, SOURCE capture, actual runtime admission or full WP108.

All five manifest members and the manifest itself are pinned; all seven frozen source pins match Git `9037451df84b6d6c7b71116a88d5737b0294400b`. Independent bounded prefix census verifies **804 files / 6,135,812 bytes**, with every blob hashed; the prefix Git tree is identical at `072bad82`.

The roster contains **368 distinct future paths**, none overlapping the 804 retained paths: 86 census + 76 later-context + 9 amendment governance/review + 175 historical R2 + 22 additional runtime. Thus 804+368=1,172 concrete files; four unassigned retention slots give **1,176**, exactly 152 above the current quota. Four slots are not writer authority: the packet still requires precise amendment before any extra path/attempt. No archive, pruning, refund or hidden bundled path count is used.

Reserved future bytes recompute as 27,393,024 source/governance + 275,021,824 R2 + 2,801,664 additional runtime = **305,216,512**. The maximum allowable current retained bytes is **231,654,400**. Actual retained plus future reservations is **311,352,324**, leaving **225,518,588** under the unchanged **536,870,912-byte** ceiling. Shared raw-group byte maxima are charged once while every physical writer path is counted individually.

All **197 runtime paths** recompute exactly against the proposed per-class table and fit the unchanged canonical 17 classes. AST-only inspection verifies intrinsic **4GiB / 10,240 files**, class-max sum **1,829,830,656 bytes / 6,506 files**. `SOURCE_METADATA` is a planning retention category, never a new runtime class or permission to borrow another class's budget.

The conservative global proof remains explicitly conditional:

- 1,176 + 6,506 + OTHERbaseline files ≤ 10,240: **OTHER ≤ 2,558 files**.
- 536,870,912 + 1,829,830,656 + OTHERbaseline bytes ≤ 4,294,967,296: **OTHER ≤ 1,928,265,728 bytes**.

Actual OTHER remains **UNKNOWN**, and no full runtime admission is claimed. Normal task/Op/event stores and physical governance originals outside the retained/reserved namespace are not free: they remain OTHERbaseline and must be measured before genuine admission. Three governance contexts plus the actual planner dispatch fit their four explicit 65,536-byte reservations. The real PLAN Op is OPEN at `072bad82`; its named close capsule is **uncreated**, correctly reserved rather than fabricated.

Only the retention quota wording at canonical WP108 lines112/137 and its explicit supersession/decision link may adopt this plan; preserve historical512/1024 artifacts. No dependency, owner, lane, execution metadata, status or planning-base refresh follows. The current task remains1,024 until ROOT's actual adoption. The separate candidate inventory1,024 and every intrinsic/class/runtime/case/memory/clock/source/authority limit remain unchanged. Missing context, REF01/REF02, source, argv, descendant and live-owner closure is still pending. The35logical/14knownOS inventory retains unresolved REF02OS classification.

Exactly three scratch proofs were produced, each≤262,144 bytes: this review, its JSON and combined-checks.json. No primary/index/Op/status mutation, operational import/test/prototype, public/BASE lookup, census/qualification/clock/P/TEST/Mac action occurred. FullWP108/M1/ticket7/Original and all49families remain pending; Mac is deferred to milestone end.

Final plan-address check: `fixed_repository_plan` exactly matches the allocated `source-census01/design/reader-plan.json` writer; final plan SHA-256 `36c8a705b53e6f08bc2fa52f47dea9bed731de1b7f34400ec0f079c7d24cf4c0`. The corrected final six-file manifest is fully reverified; capacity/design numbers are unchanged.
