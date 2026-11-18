//go:build linux || darwin || windows

package storage

// PlatformSupport describes the native save protocol implemented by this build.
// Successful file publication does not certify power-loss behavior on a volume.
type PlatformSupport struct {
	Replacement       bool
	AtomicReplacement bool
	DirectorySync     bool
	Notice            string
}

func CurrentPlatform() PlatformSupport {
	if !platformAtomicExchange() {
		return PlatformSupport{Replacement: true, Notice: "Windows prerelease: namespace power-loss durability is unqualified."}
	}
	return PlatformSupport{Replacement: true, AtomicReplacement: true, DirectorySync: true}
}
