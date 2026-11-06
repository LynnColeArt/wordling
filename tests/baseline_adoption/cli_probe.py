"""Exercise the real CLI with a Linux PTY; no private model or synthetic I/O replies."""
import errno
import fcntl
import hashlib
import json
import os
from pathlib import Path
import pty
import select
import struct
import subprocess
import sys
import tempfile
import termios
import time


def run(binary):
    with tempfile.TemporaryDirectory(prefix="wordling-cli-") as root:
        master, slave = pty.openpty()
        fcntl.ioctl(slave, termios.TIOCSWINSZ, struct.pack("HHHH", 25, 80, 0, 0))
        before = termios.tcgetattr(slave)
        env = dict(os.environ, TERM="xterm-256color", COLORTERM="truecolor")
        proc = subprocess.Popen([binary, "-root", root, "-profile", "local-flat"],
                                stdin=slave, stdout=slave, stderr=slave, env=env)
        transcript = bytearray()
        checkpoints = []

        def read_until(predicate, label, timeout=8):
            deadline = time.monotonic() + timeout
            while time.monotonic() < deadline:
                if predicate():
                    checkpoints.append(label)
                    return
                readable, _, _ = select.select([master], [], [], 0.05)
                if readable:
                    try:
                        chunk = os.read(master, 65536)
                    except OSError as exc:
                        if exc.errno == errno.EIO:
                            chunk = b""
                        else:
                            raise
                    transcript.extend(chunk)
                    # Deterministic minimal terminal replies for startup probes.
                    if b"\x1b[6n" in chunk:
                        os.write(master, b"\x1b[1;1R")
                    if b"\x1b[c" in chunk:
                        os.write(master, b"\x1b[?1;2c")
                if proc.poll() is not None and not predicate():
                    raise AssertionError(f"exited early at {label}: {transcript!r}")
            raise AssertionError(f"timeout at {label}: {transcript!r}")

        def key(data):
            offset = len(transcript)
            os.write(master, data)
            return offset

        try:
            read_until(lambda: b"Layout" in transcript, "startup menu")
            # Send each character independently, avoiding terminal bracketed-paste semantics.
            for char in b"CLIalpha":
                key(bytes([char]))
            key(b"\r")
            for char in b"CLIbeta":
                key(bytes([char]))
            read_until(lambda: b"CLIbeta" in transcript, "typed second paragraph")
            key(b"\x1b[21~")  # xterm F10
            read_until(lambda: b"Document to be saved:" in transcript, "candidate save prompt")
            key(b"PROBE.WP")
            save_offset = key(b"\r")
            path = Path(root, "PROBE.WP")
            read_until(path.exists, "native first publication")
            raw = path.read_bytes()
            assert raw.startswith(b"\xffWPC"), raw[:16]
            assert raw.endswith(b"CLIalpha\x0aCLIbeta"), raw[-40:]
            # Wait for binding/read verification, rather than exiting during actual I/O.
            read_until(lambda: b"Doc 1 Pg" in transcript[save_offset:], "returned document status")
            offset = key(b"\x1b[18~")  # xterm F7
            read_until(lambda: b"Save document" in transcript[offset:], "exit save question")
            offset = key(b"n")
            read_until(lambda: b"Exit" in transcript[offset:], "exit application question")
            key(b"y")
            read_until(lambda: proc.poll() is not None, "normal process exit")
            assert proc.returncode == 0, transcript
            assert termios.tcgetattr(slave) == before, "terminal modes not restored"
            assert b"\x1b[?1049h" in transcript and b"\x1b[?1049l" in transcript, "alternate screen not restored"
            assert path.read_bytes() == raw, "exit changed saved bytes"
            return {"checkpoints": checkpoints, "exit_code": proc.returncode,
                    "terminal_restored": True, "native_sha256": hashlib.sha256(raw).hexdigest(),
                    "native_body_hex": raw[-16:].hex()}
        finally:
            if proc.poll() is None:
                proc.kill()
                proc.wait()
            os.close(master)
            os.close(slave)


if __name__ == "__main__":
    print(json.dumps(run(sys.argv[1]), indent=2))
