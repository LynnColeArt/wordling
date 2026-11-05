# Allocation interpretation after measurement

The original `budget-plan.json` is retained as the pre-execution checkpoint.
Its phrase “Admission only copies <=65536 bytes plus fixed native metadata”
describes mutation-admitted inputs, but was too broad as a description of all
refusal paths. `mutationAdmission` calls the existing immutable reader's `Inspect`
before rejecting large/unqualified inputs. Inspect copies metadata bounded by
the unchanged WP02 limits of4096 blocks and16384 packet entries. This is inherited
read-only inspection cost, not a new unbounded traversal or an admitted writer
shape. No production source, input/token policy or fuzz budget changed to optimize
or conceal that cost.

`measure/main.go` uses labelled synthetic safety fixtures through the actual
public APIs. With2 matched pairs,16384 tokens derive16716 bytes and65540 bytes of
gap index for this closed prefix schema. These are combined qualification bounds,
not universal original offsets or DOS limits. On this host admission allocated
19128 B/op (9 allocs,31815ns), and changed typeover187136 B/op (37 allocs,114256ns).

The separate broad read-only fixture has204817 bytes,4096 blocks,16384 zero-length
opaque/deleted entries and one ASCII body token. Actual Parse/Export is lossless;
mutation returns typed MutationLimit. That refusal allocated786488 B/op (3 allocs,
88944ns), including its inherited metadata clones. This disproves any reading of
the original phrase as a smaller universal refusal-allocation cap. B/op is total
allocated bytes per call, not peak live memory, process RSS or a hard cap. The
external process/RSS log includes Go build/runtime/harness costs. No benchmark
selects a product SLO, establishes an original maximum, or broadens the writer.
