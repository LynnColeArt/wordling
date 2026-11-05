"""Black-box resize/conservation probe against a supplied built Wordling executable."""
import fcntl
import hashlib
import json
import os
from pathlib import Path
import pty
import select
import signal
import struct
import subprocess
import sys
import tempfile
import termios
import time


def probe(executable, modal):
    with tempfile.TemporaryDirectory(prefix="wp90-cli-") as folder:
        master, slave = pty.openpty()
        fcntl.ioctl(slave, termios.TIOCSWINSZ, struct.pack("HHHH", 25, 80, 0, 0))
        initial_terminal = termios.tcgetattr(slave)
        child = subprocess.Popen([executable, "-root", folder, "-profile", "local-flat"],
                                 stdin=slave, stdout=slave, stderr=slave,
                                 env=dict(os.environ, TERM="xterm-256color", COLORTERM="truecolor"))
        output = bytearray()
        steps = []

        def pump(seconds=0.05):
            ready, _, _ = select.select([master], [], [], seconds)
            if ready:
                chunk = os.read(master, 65536)
                output.extend(chunk)
                if b"\x1b[6n" in chunk:
                    os.write(master, b"\x1b[1;1R")
                if b"\x1b[c" in chunk:
                    os.write(master, b"\x1b[?1;2c")

        def until(predicate, label):
            deadline = time.monotonic() + 8
            while not predicate():
                if time.monotonic() > deadline or child.poll() is not None:
                    raise AssertionError(f"{modal}: {label}: {output!r}")
                pump()
            steps.append(label)

        def send(data):
            start = len(output)
            os.write(master, data)
            return start

        def settle():
            # Input with no visible effect cannot use a renderer marker. Queue
            # ordering plus the public Model regression covers those exact steps.
            deadline = time.monotonic() + 0.15
            while time.monotonic() < deadline:
                pump(0.02)

        def resize(rows):
            start = len(output)
            fcntl.ioctl(slave, termios.TIOCSWINSZ, struct.pack("HHHH", rows, 80, 0, 0))
            os.kill(child.pid, signal.SIGWINCH)
            until(lambda: len(output) > start, f"render at {rows} rows")
            settle()
            return bytes(output[start:])

        try:
            until(lambda: b"Graphics Help" in output, "startup")
            send(b"BASE")
            until(lambda: b"BASE" in output, "document typed")
            offset = send(b"\x1b[15~" if modal == "files" else b"\x1b=")
            until(lambda: (b"Directory" if modal == "files" else b"File") in output[offset:], "modal opened")
            send(b"x")
            settle()
            small = resize(11)
            send(b"x")
            settle()
            restored = resize(25)
            assert (b"Directory" if modal == "files" else b"File") in restored, "modal did not return"
            send(b"\x1b[18~")  # F7 leaves modal, not the application.
            settle()
            offset = send(b"\x1b[21~")  # F10
            until(lambda: b"Document to be saved:" in output[offset:], "save prompt")
            send(b"RESULT.WP")
            offset = send(b"\r")
            saved = Path(folder, "RESULT.WP")
            until(lambda: saved.exists() and b"Doc 1 Pg" in output[offset:], "actual native publication")
            native = saved.read_bytes()
            body_offset = int.from_bytes(native[4:8], "little")
            body = native[body_offset:]
            offset = send(b"\x1b[18~")
            until(lambda: b"Save document?" in output[offset:], "exit save question")
            offset = send(b"n")
            until(lambda: b"Exit WP?" in output[offset:], "exit confirmation")
            send(b"y")
            until(lambda: child.poll() is not None, "process exit")
            assert child.returncode == 0, output
            assert termios.tcgetattr(slave) == initial_terminal, "terminal attributes not restored"
            assert b"\x1b[?1049l" in output, "alternate screen not restored"
            return {"modal": modal, "steps": steps, "conserved": body == b"BASE",
                    "native_body_hex": body.hex(), "native_sha256": hashlib.sha256(native).hexdigest(),
                    "small_screen_output": small.decode("utf8", "backslashreplace"),
                    "restored_screen_output": restored.decode("utf8", "backslashreplace"),
                    "exit_code": child.returncode, "terminal_restored": True}
        finally:
            if child.poll() is None:
                child.kill()
                child.wait()
            os.close(master)
            os.close(slave)


if __name__ == "__main__":
    results = [probe(sys.argv[1], mode) for mode in ("files", "menu")]
    print(json.dumps({"executable_sha256": hashlib.sha256(Path(sys.argv[1]).read_bytes()).hexdigest(),
                      "results": results}, indent=2))
    sys.exit(0 if all(r["conserved"] for r in results) else 1)
