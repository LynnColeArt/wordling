//go:build !wordling_qa

package storage

// Normal binaries cannot activate qualification faults, regardless of environment.
func qualificationFault(stage, old, new string, flags uint) error { return nil }
