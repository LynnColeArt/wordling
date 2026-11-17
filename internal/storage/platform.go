//go:build linux || darwin || windows

package storage

// PlatformSupport describes the native save protocol implemented by this build.
// Successful file publication does not certify power-loss behavior on a volume.
type PlatformSupport struct {
	AtomicReplacement bool
	DirectorySync     bool
	Notice            string
}

func CurrentPlatform() PlatformSupport {
	if !platformAtomicExchange() {
		return PlatformSupport{Notice: "Windows prerelease: save to new names; crash durability is unqualified."}
	}
	return PlatformSupport{AtomicReplacement: true, DirectorySync: true}
}
