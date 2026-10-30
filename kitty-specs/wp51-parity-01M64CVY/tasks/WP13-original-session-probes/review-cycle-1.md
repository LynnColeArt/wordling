---
affected_files: []
cycle_number: 1
mission_slug: wp51-parity-01M64CVY
reproduction_command:
reviewed_at: '2026-10-30T23:17:41Z'
reviewer_agent: reviewer-renata
wp_id: WP13
---

# WP13 changes requested

Reviewer: reviewer-renata. Reviewed lane-c commit5994bcc. One blocking evidence-completeness finding; no observed original exit-behavior defect.

## I1 — Archive the final DOS state for all dedicated quit repetitions (P2)

Affected source: scripts/reference/session1.py lines253–258; canonical CMD51-244 session1_subcases, accepted-branches.json/state-index.json/pair-audit.json and corresponding report rows.

The runner sends y, captures exit-choice-result immediately after Exit WP disappears, then waits for C:\WP51> without another capture. All eight accepted dedicated quit exit-choice-result screens lack C:\WP51>. Named runs retain stale ABCD/CHANGEDABCD at the top with no editing status; unnamed changed retains UNNAMED; empty context is blank. Their sealed runner and successful result support that the later DOS wait completed, but do not archive that terminal state's screen/VRAM/raster/cursor. Thus CMD51-244 currently associates its claimed returned-DOS state with an earlier transition capture. This fails T038's intermediate/resulting-state capture and acceptance's exact accepted prompt/cursor/name/buffer-state evidence requirement. The generic pair/hash checks pass because both repetitions capture the same incomplete transition.

Affected branches/run IDs:

- named-unchanged-quit:2026-10-31-session1-b08-r1 and-b08-r2.
- named-changed-quit:2026-10-31-session1-b14-r1 and-b14-r2.
- unnamed-unchanged-quit:2026-10-31-session1-b20-r1 and-b20-r2.
- unnamed-changed-quit:2026-10-31-session1-b26-r1 and-b26-r2.

Required fix: capture and assert the actual final DOS state after wait_for(DOS), recording raw screen/VRAM/raster/hardware cursor through the existing evidence path. Preserve these eight attempts unchanged. Schedule two new fresh-copy runs per affected context under the shared VM coordinator after WP14 releases it; no concurrent guest or rewriting old evidence. Select those new repetitions explicitly, regenerate derived reports/index and update CMD51-244 exact state-label/manifest links and owned rendered views. Keep old successful waits described honestly as superseded evidence with incomplete terminal captures. Add a semantic negative audit requiring that CMD51-244's accepted terminal state contains the DOS prompt and is linked to that post-wait capture; substituting exit-choice-result must fail even if its hashes/pair equality are valid. Rerun existing offline audits and actual lane gate. Other accepted branches need not be repeated absent a new concern.

Independent reproduction without VM: inspect state-index.json branches ending -quit, read each states.exit-choice-result screen_path and test 'C:\\WP51>' membership; all8 are false. Inspect the archived runner sequence and current lines253–258. This is missing archived observation, not proof that exit failed or that the original retained an active document after exit.
