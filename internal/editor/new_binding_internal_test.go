package editor

import (
	"errors"
	"github.com/lynncoleart/wordling/internal/storage"
	"testing"
)

func TestFirstErrorCaptureWholeTreeAndPublicDiagnosticCopies(t *testing.T) {
	no := &storage.Failure{Kind: storage.CandidateFailed, Stage: "candidate write/close", Cause: errors.Join(errors.New("write"), errors.New("cleanup"))}
	may := &storage.Failure{Kind: storage.PublicationUncertain, DestinationMayExist: true, Candidate: "residue"}
	for _, tc := range []struct {
		err  error
		want bool
	}{{no, false}, {errors.Join(no, errors.New("unknown outer")), true}, {errors.Join(no, may), true}, {&storage.Failure{Kind: storage.CandidateFailed, Cause: errors.Join(errors.New("write"), may)}, true}} {
		frozen, possible, _ := freezeFirstError(tc.err, true)
		if possible != tc.want {
			t.Fatalf("tree classification %v", tc.err)
		}
		var public *storage.Failure
		if !errors.As(frozen, &public) {
			t.Fatal("lost typed failure")
		}
		public.DestinationMayExist = !public.DestinationMayExist
		public.Candidate = "forged"
		var again *storage.Failure
		if !errors.As(frozen, &again) || again.Candidate == "forged" {
			t.Fatal("diagnostic retargeted private observation")
		}
	}
}
