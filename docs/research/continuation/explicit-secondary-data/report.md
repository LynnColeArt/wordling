---
status: ready-for-independent-code-review
work_package: WP67
review_cycle: 2
scope: explicit-field-DATA-only
---
# WP67 F1 correction — implementation cycle 2

F1 is acknowledged and corrected. Independent cycle1 review found that the new
launcher bound local GoFiles but merely recorded other compiled source kinds.
A real build-valid68-byte empty assembly member in the frozen native package
passed audit and replaced a genuine prior workflow report. This was an approved
source-custody failure, even though DATA/native behavior otherwise passed. No
malicious assembly or native-document corruption was observed or claimed.

This is an implementer handoff for the same independent reviewer, not approval.
The full generated33-line fix prompt, preferred review-feedback-1.md and complete
independent report were read. No manual feedback/frontmatter/status mutation was
used; this report records the acknowledgment under the normal generated fix mode.

## Narrow correction

One shared roster now governs both source admission and source reporting for all
production source/asset kinds exposed by the pinned Go tool: GoFiles,
CompiledGoFiles, CgoFiles, CFiles, CXXFiles, MFiles, HFiles, FFiles, SFiles,
SwigFiles, SwigCXXFiles, SysoFiles and EmbedFiles. Ignored/test-only files are not
production compilation inputs. Go list is requested with -compiled so the actual
Go compiler input set is visible rather than inferred. For every local package,
CompiledGoFiles must equal GoFiles under the approved Go-only closure; both sets
are checked against exact reviewed manifest paths/bytes. Every other nonempty
local source/asset kind refuses. Recording a source hash never authorizes an
otherwise unapproved member. The approved source set was not enlarged.

Only launcher source and its public regression test changed. All4 Go source/test
files, module files, DATA API and221 frozen native/wp51/WP53 members remain exact.
No old53 helper/authority/report, native decoder, interpreter or writer was edited.

## Actual red and green

The new public regression ran before the fix. In a disposable tree all260 copied
inputs were exact, all30 native inputs remained exact, and the only added provider
source was the same68-byte empty assembly cohort used by the independent review.
An actual go build succeeded and go list showed SFiles=[unreviewed.s]. The public
audit then exited0 and replaced the prior report: the test failed its runtime
nonzero assertion. This is a genuine reproduced F1 red, not a construction or
compile failure.

With the correction the same build-valid source addition is refused by the public
launcher with UnapprovedLocalCompiledSourceKind:SFiles. The genuine prior report,
all copied provider/native inputs and the added assembly bytes remain unchanged.
The final regression also observes actual CompiledGoFiles matching GoFiles.
Raw arguments, cwd, statuses/stdout/stderr, source counts, hashes and assertions
are retained in cycle2/source-gate-red.*, source-gate-green.* and
source-gate-final.*. The initial12-kind fix and intermediate qualifications remain
historical; the final13-kind source point is separately identified.

The final actual30-image audit and separate fresh Clara inspection both complete
successfully through the corrected production launcher/API. Results remain
24records/36explicit fields/6explicit empties/six opaque cohorts; Clara is a fresh
synthetic structural DATA value, not a generated original result. Both native
inputs and the public original remain unchanged. The actual closure is102packages,
4local packages,6 unique local production Go files and751 unique per-package
source members. GoFiles/CompiledGoFiles associations are both checked and recorded;
their repeated membership does not mean twice as many distinct sources.

Four affected existing Python public tests pass: real API/diagnostic qualification,
source-substitution refusal, failure preserving a genuine prior report, and
successful fresh-value report replacement after complete checks. The new actual
assembly regression passes separately. Python compilation and changed-source
whitespace checks complete0. Exact raw commands and outputs, including final
launcher/source closure identities, are in cycle2/verification-final.json and its
two qualification reports. Unchanged Go/configured/race/fuzz suites were not
repeated solely for this Python correction; their author and independent cycle1
results remain explicitly historical. Historical raw evidence whitespace2 is
retained; no whole-history clean-lint or complete-raw-history claim is introduced.

## Custody and retained history

The normal cycle2 host claim produced9569aabc49a24a4f356c5d510c04493b2666f7cc by
its recorded planning-only merge of prior be000145 and ceb22ee5. ROOT independently
verified all178 changed planning paths; all94 original owned bytes were exact
before this fix. Canonical branch currency returned None, so no additional merge,
rebase, overlay or source-provider reentry was performed. All59 immutable Git pins,
221 working/Git/mode-semantic bindings and the actual pinned Go/compiler bytes
were reverified before editing.

The first frozen CURRENT/report/seals are retained byte-for-byte as inert
history/cycle1 copies, with original names/Git identities mapped explicitly in
cycle2/history-map.json. Their old e99 seal describes the original set at
be000145, not the changed current namespace or renamed archive. All other prior
qualification/raw receipts remain literal historical evidence. The independent
counterexample/report/raw files remain intact in canonical review cycle1 and are
pinned in place, not relabeled successful or executed as product code. Old missing
child-output/transient-mutant raw-history limitations and absolute shared-cache
measurement remain disclosed by the archived first report. No new cache delta or
exclusive ownership is claimed.

No native/companion format, program admission, formatter/count/tail interpretation,
merge evaluator/PAGE/nesting effect, result writer, app Merge route, original
launch/private resource/VM/grant or PDF authority follows. Generic Secondary
Supported/Admit remains blocked. All38 requirements/91groups/36lessons/nested M1
and SC001–005 remain OPEN. Normal root-coordinated lifecycle and independent
cycle2 code review are still required.
