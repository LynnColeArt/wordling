# Pre-qualification finite source proof

All ceilings are Linux requested/copy-byte accounting, not RSS or original capacities.
Go1.26.4 amd64 pinned actual types: Token32, Command136, Finding56, Record136,
Field88, Span24. Native Inspect copies Tokens<=65536, Commands<=Tokens,
Findings<=1024, Records<=4096, Fields total<=16384, Interstitial<=Tokens.
Their actual copied sum14,639,104B. append-from-nil allocation rounding bounded
by twice requested payload plus per-slice rounding (Records<=4096 =><1MiB
small-slice rounding). 48MiB comfortably covers that (<31MiB). Work precharge
348160 covers 4 traversals of all token/field/record/finding cardinalities;
commands/interstitial each bounded by tokens; no nested quadratic traversal.
Compile reserves48MiB BEFORE its only Inspect; remaining16MiB covers <=4096
literal refs32B, <=4096 one-byte Bytes copies and <=4 command/operand copies,
private proof and bounded arrays. Every source-byte/read/next/append request
is charged before effect. Actual compile/eval measurement is separate.

Evaluator requests at most2 Value.Provenance copies; authentic explicit proof
limits each to2 Fields +2 Interstitial. Each request is precharged before call.
Then field.Content Bounds is read BEFORE Value.Bytes. Sum body<=65536,
trace<=4098, each48B; Access<=2 with bounded slices. Precharge output, field
copy, trace, access and result <=~264KiB. Result accessors defensively copy
<=~264KiB. Fixed4MiB accounts for these and source proof captures. The
maximal possible selected work includes <=4096 literal traversals and <=65536
field bytes three times, below1Mi units. Tiny WorkUnits that cannot pay the
348160 inspection reservation reject at Compile, not a fake eval exhaustion.

Consumer read/decode precharges32MiB allocation/12Mi work. io.ReadAll3MiB+1
sentinel has cumulative geometric buffer requests<20MiB. Raw JSON plus decoded
base64 payload<=2MiB and decoder copies/token strings fit remaining12MiB.
Two exact keys only; overlong key strings still bounded by request cap.
Before either Parse, each source precharges512*n+4MiB allocation,256*n+1Mi
work. From pinned wp51/native/explicit closure: outer packet/index arrays and
sort extents/map (bounded by source length/10) <32n+1MiB; token growth32B per
one-byte token with geometric cumulative requests<128n; command growth136B
per minimum8-byte command <68n; record/field growth plus inspection copies
<160n; copied whole input/field byte requests<24n; stack, finding strings and
remaining provenance/temporary rounding fit remaining100n+3MiB. Primary
includes Parse+View, secondary includes Parse+View+explicit.Admit. The
admission proof may refuse, never exceeds this conservative reservation.
Native admission limits themselves remain unchanged. Sources that cannot
fit this cumulative reservation refuse BEFORE Parse even if <1MiB.

Compile precharges64MiB/1Miwork. One report envelope8MiB/4Miwork covers staging,
fixed-schema JSON upper bound<=1MiB including marshaler buffer growth, trace
projection, final bytes and hash formatting. Each record BEFORE Evaluate
precharges5MiB allocation/2Miwork: fixed4MiB evaluator plus1MiB accessor and
projection. All reservations decrement ONE ledger256MiB/64Miwork. The
record ceiling32 is not a promise all32maximal records fit: insufficient
remaining reservation refuses atomically. Original two-record pairs fit with
wide margin (~115MiB allocations/<24Miwork). All bodies/traces staged privately,
then preflight encoded bound1024 +sum(256+4*ceil(body/3)+128*traces+1024*accesses)
BEFORE marshaling. Decimal offsets<=1MiB, output offsets<=65536, constant tags,
recordordinal<=32 and fixed metadata schema fit these per-entry allowances.
Bounds/body/trace/encoded checks precede row append/JSON encoding. OS short
writes return failure; diagnostics may be partially written and are not rolled
back. No native document writer or new canonical format exists.

Chronology: initial RED compile failure and exploratory library/consumer tests
preceded this complete prose proof; those raw runs are retained as exploratory,
not the final post-proof qualification. The type-size proof was measured in
those exploratory tests. Final tests/binary campaigns begin only after this file.
