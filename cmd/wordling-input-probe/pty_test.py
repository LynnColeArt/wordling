#!/usr/bin/env python3
"""Linux synthetic PTY integration evidence, never physical qualification.

Usage: python3 cmd/wordling-input-probe/pty_test.py /tmp/probe NEW_OUTPUT_DIR
The output directory is retained, including raw-byte/event journals.
"""
import errno
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
import termios
import threading
import time


def run_probe(binary, root, name, enhanced, chunks, stop_early=False):
    master, slave = pty.openpty()
    fcntl.ioctl(slave, termios.TIOCSWINSZ, struct.pack("HHHH", 25, 80, 0, 0))
    initial = termios.tcgetattr(slave)
    env = dict(os.environ, TERM="xterm-256color", LANG="C.UTF-8")
    argv = [str(binary), "-output", str(root/name), "-duration", "2500ms",
            "-transport", "synthetic-pty", "-profile", name,
            "-keyboard-layout", "synthetic bytes; no physical layout",
            "-enhanced="+str(enhanced).lower()]
    proc = subprocess.Popen(argv, stdin=slave, stdout=slave, stderr=subprocess.PIPE, env=env)
    wire = bytearray()
    stop = threading.Event()

    def drain():
        while not stop.is_set():
            if select.select([master], [], [], .05)[0]:
                try:
                    raw = os.read(master, 65536)
                    if not raw:
                        break
                    wire.extend(raw)
                except OSError as exc:
                    if exc.errno == errno.EIO:
                        break
                    raise

    reader = threading.Thread(target=drain)
    reader.start()
    sent = []
    try:
        # Wait for negotiation request/output before injecting candidate input.
        until = time.monotonic()+1
        while not wire and time.monotonic() < until:
            time.sleep(.01)
        for delay, raw in chunks:
            time.sleep(delay)
            os.write(master, raw)
            sent.append({"delay_seconds": delay, "hex": raw.hex()})
        fcntl.ioctl(slave, termios.TIOCSWINSZ, struct.pack("HHHH", 30, 100, 0, 0))
        proc.send_signal(signal.SIGWINCH)
        if stop_early:
            time.sleep(.1)
            proc.send_signal(signal.SIGTERM)
        _, stderr = proc.communicate(timeout=7)
        if stop_early:
            assert proc.returncode != 0 and b"before probe deadline" in stderr, stderr
        else:
            assert proc.returncode == 0, stderr.decode(errors="replace")
        assert termios.tcgetattr(slave) == initial, "terminal state not restored"
        original_journal = (root/name/"journal.jsonl").read_bytes()
        refused = subprocess.run(argv, stdin=slave, stdout=slave, stderr=subprocess.PIPE, env=env, timeout=2)
        assert refused.returncode != 0, "existing capture overwritten"
        assert (root/name/"journal.jsonl").read_bytes() == original_journal
    finally:
        if proc.poll() is None:
            proc.kill()
            proc.wait()
        stop.set()
        reader.join()
        os.close(master)
        os.close(slave)
    rows = [json.loads(x) for x in (root/name/"journal.jsonl").read_text().splitlines()]
    captured = b"".join(bytes.fromhex(x["value"]) for x in rows if x["kind"] == "raw-input")
    assert captured == b"".join(bytes.fromhex(x["hex"]) for x in sent), "input tee lost bytes"
    assert rows[-1]["kind"] == "end" and rows[-1]["value"]["terminal_state_restored"]
    assert rows[-1]["value"]["deadline_reached"] != stop_early
    assert any(r["kind"] == "event" and r["value"]["kind"] == "resize"
               and r["value"].get("width") == 100 and r["value"].get("height") == 30
               for r in rows), "actual resize was not delivered"
    assert [r["sequence"] for r in rows] == list(range(1, len(rows)+1))
    (root/name/"injected.json").write_text(json.dumps(sent, indent=2)+"\n")
    (root/name/"wire-output.bin").write_bytes(wire)
    return [x["value"] for x in rows if x["kind"] == "event"]


def key_events(events):
    return [(x["kind"], x["key"]) for x in events if "key" in x]


def main():
    binary = Path(sys.argv[1]).resolve()
    root = Path(sys.argv[2]).resolve()
    root.mkdir()  # Refuse overwrite.
    # Enhanced response and Kitty-encoded keys, including distinct Ctrl/legacy
    # collision partners, repeats, release, and an unknown control sequence.
    enhanced = run_probe(binary, root, "synthetic-enhanced", True, [
        (.05, b"\x1b[?31u\x1bP>|synthetic-test-terminal\x1b\\"),
        (.05, b"\x1b[57364u\x1b[57366u\x1b[57370u\x1b[57373u"),
        (.05, b"\x1b[57366;3u\x1b[57373;2u\x1b[61;3u\x1b[57356u\x1b[57351u"),
        (.05, b"\x1b[105;5u\x1b[9u\x1b[109;5u\x1b[13u\x1b[91;5u\x1b[27u"),
        (.05, b"\x1b[32;5u\x1b[64;5u\x1b[127u\x1b[57349u"),
        (.05, b"\x1b[120;1:2;120u\x1b[120;1:3u"),
        (.05, b"\x1b[200~\x1bOPq\x13\x1b[201~\x1b[999~"),
        (.05, b"\x1b[I\x1b[O\x1b[<0;4;5M\x1b[<0;4;5m"),
        (.05, b"\x1b["), (.005, b"57364u"),
    ])
    caps = [e["support"] for e in enhanced if e["kind"] == "keyboard-capabilities"]
    assert caps and caps[0]["flags"] == 31 and caps[0]["event_types"]
    keys = key_events(enhanced)
    # Pinned v2/UV numeric key identities. These are decoded values, not Kitty
    # protocol numbers. Go tests separately compare the symbolic tea constants.
    expected = [(1114156, 0), (1114158, 0), (1114162, 0), (1114165, 0),
                (1114158, 2), (1114165, 1), (61, 2), (1114124, 0), (1114115, 0),
                (105, 4), (9, 0), (109, 4), (13, 0), (91, 4), (27, 0),
                (32, 4), (64, 4), (127, 0), (1114120, 0)]
    assert [(k["code"], k["mod"]) for _, k in keys[:len(expected)]] == expected
    assert any(kind == "release" for kind, _ in keys)
    assert any(k["is_repeat"] for _, k in keys)
    assert any(e["kind"] == "paste" and "\x1bOPq\x13" == e.get("text") for e in enhanced)
    assert any(e["kind"] == "unknown" and e["source_type"] == "uv.UnknownCsiEvent" for e in enhanced)
    for kind in ["focus", "blur", "mouse-click", "mouse-release"]:
        assert any(e["kind"] == kind for e in enhanced), kind
    legacy = run_probe(binary, root, "synthetic-legacy-fast", False, [
        (.05, b"\x1bOP\x1bOR\x1b[18~\x1b[21~\x1b[1;3R\x1b[21;2~\x1b=\x1b[H\x1b[C"),
        (.05, b"\t\r\x00\x7f\x1b[3~"),
        (.05, b"\x1b"), (.005, b"5x"),
    ])
    slow = run_probe(binary, root, "synthetic-legacy-slow", False, [
        (.05, b"\x1b"), (.150, b"5"), (.05, b"x"),
        (.05, b"\x1b["), (.150, b"C"),
    ])
    # Delayed ESC must stay an Escape, not application-inferred Alt+5.
    fast_keys = key_events(legacy)
    slow_keys = key_events(slow)
    assert [(k["code"], k["mod"]) for _, k in fast_keys[:9]] == expected[:9]
    assert any(k["code"] == 27 and k["mod"] == 0 for _, k in slow_keys)
    assert any(k["code"] == ord("5") and k["mod"] != 0 for _, k in fast_keys)
    assert any(k["code"] == ord("5") and k["mod"] == 0 for _, k in slow_keys)
    run_probe(binary, root, "synthetic-host-sigterm", False, [(.05, b"x")], stop_early=True)
    negative = subprocess.run([str(binary), "-output", str(root/"not-a-tty")],
                              input=b"", capture_output=True)
    assert negative.returncode != 0 and not (root/"not-a-tty").exists()
    report = {"scope": "synthetic-pty-only", "physical_qualified": False,
              "binary_sha256": hashlib.sha256(binary.read_bytes()).hexdigest(),
              "driver_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "checks": ["exact raw capture", "negotiation response", "repeat/release",
                         "paste isolation", "unknown preservation", "split/delayed ESC distinction",
                         "terminal restoration", "non-TTY refusal", "existing capture refusal",
                         "SIGTERM is abnormal with restored terminal"], "files": []}
    for p in sorted(root.rglob("*")):
        if p.is_file():
            raw = p.read_bytes()
            report["files"].append({"path": str(p.relative_to(root)), "bytes": len(raw),
                                    "sha256": hashlib.sha256(raw).hexdigest()})
    (root/"manifest.json").write_text(json.dumps(report, indent=2)+"\n")
    print("synthetic PTY checks passed; physical delivery remains unqualified")


if __name__ == "__main__":
    main()
