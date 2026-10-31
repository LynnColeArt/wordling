package main

import (
	"encoding/json"
	"os"
	"testing"
)

// Same timer/counter boundary as the phase collector; not subtracted from data.
func TestCollectorOverheadCalibration(t *testing.T) {
	p := measure("empty_callback_timer_baseline", 31, 3, func() error { return nil })
	if path := os.Getenv("WORDLING_MEASUREMENT_CALIBRATION"); path != "" {
		raw, e := json.MarshalIndent(p, "", "  ")
		if e != nil {
			t.Fatal(e)
		}
		if e = os.WriteFile(path, append(raw, '\n'), 0600); e != nil {
			t.Fatal(e)
		}
	}
	for _, s := range p.Samples {
		if s.NS < 0 || s.Error != "" {
			t.Fatal(s)
		}
	}
}
