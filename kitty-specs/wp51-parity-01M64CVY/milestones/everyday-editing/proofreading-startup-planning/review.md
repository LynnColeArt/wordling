# Independent WP89 startup ownership amendment review

Verdict: **APPROVE** this planning amendment only.

Reviewer: `/root/everyday_baseline_audit`, independent of author.
Reviewed patch SHA-256: `1920bf36ff66ed41963419036e817bb8d62f368c291a56f6049e1649faad7b38`.

The exact one-file patch adds existing `internal/tui/runtime.go` and genuinely new `internal/tui/proofreading_runtime_test.go` ownership, with only the latter added to create_intent. It establishes the missing production initialization/lifetime seam: normal tui.Open admits real resources, handles failure and cleanup, preserves existing settings, and proves supplemental additions survive a new application process. It forbids putting host I/O in View or a pure reducer. No new resource path or CLI flag is invented; an actual need for cmd changes requires a separate narrow amendment.

This matches inspected production flow cmd/wordling/main.go:37 → tui.Open → editor.New. WP85 already owns runtime.go and is an unchanged WP89 prerequisite. WP88 remains the other prerequisite. The amendment does not confer approval on a provider, resource equivalence, implementation or product milestone.

Independent verification used installed Spec Kitty modules, not the author's result file: exact diff bytes match planning.patch; git apply --check succeeds; both added ownership paths have correct existing/new status; all 90 frontmatters parsed; validate_all and validate_glob_matches return no errors; compute_lanes completes without cycle; the complete current 90-package lane map is identical, and all historical 76 mappings remain identical. Available branch/worktree identity fields compare unchanged. WP89 remains lane-h. No dependency, lifecycle/event, existing task identity, git ref, index or repository file was modified by this review. Pure computation does not replace canonical finalization and its normal pre/post identity checks.

No blocking finding. Apply only the exact reviewed patch, then perform canonical planning refresh and preserve prior approval/event identities. This review is not a WP89 lifecycle verdict.
