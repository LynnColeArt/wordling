# Native Windows candidate evidence

Run44402388644 passes at fixedf6cea1cc, with Linux build/regression and Windows amd64 only. verification.json binds downloaded artifacts, package members, every compiled local source and production-tree object to that exact commit. Windows ARM64 is cross-built only.

Native logs and console transcripts retain their exact original CRLF, terminal spacing and bytes as deterministic gzip files. raw-evidence-preservation.json maps raw paths, sizes and hashes to their stored gzip representation, including the two exact R3 chronology diffs. The initial whitespace-check failure is preserved; no evidence was normalized and no whitespace rule was disabled.

The verifier is stored inert as verify-artifacts.py.txt. Reproduction needs the exact two downloaded artifact archives beside the script and the pinned Git source. This result is native engineering-test evidence, not original compatibility, physical keyboard or full Mission1 acceptance. Mac testing remains deferred.
