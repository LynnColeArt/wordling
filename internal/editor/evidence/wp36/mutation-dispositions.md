# Finite mutation dispositions

The original12 numeric-epoch source mutations were killed before the stronger
unique transition token was introduced. Their logs remain historical. On the
unique-token source, omitting only the run-owner guard survived because the
independent unique-transition guard still rejected that public foreign session.
This is a redundant-guard survivor, not a claim that its omission was killed.
The compound omission of both guards represents the actual identity-protection
class and is killed by the same external API test.

The first compound variant replaced both predicates with false and was rejected
by Go vet as `redundant or: false || false`; it was NOT counted as a behavioral
kill. Its command/exit/non-kill record remains in the before-correction manifest.
The corrected variant removes both guard clauses, compiles and fails the actual
assertion. Final manifest joins that corrected row with12 unchanged compiling
behavioral kills from the same frozen source. Current mutated source archives
are inert .go.txt; no product or reference data was changed by these overlays.
