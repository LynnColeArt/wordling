#!/usr/bin/env python3
"""Small QMP driver for the isolated Wordling reference guest (not the host UI)."""

import argparse
import json
from pathlib import Path
import socket
import time

ROOT = Path(__file__).resolve().parents[2]
RUNTIME = ROOT / "research/cache/reference/runtime"
SOCKET = RUNTIME / "qmp.sock"


class QMP:
    def __enter__(self):
        self.socket = socket.socket(socket.AF_UNIX)
        self.socket.settimeout(10)
        self.socket.connect(str(SOCKET))
        self.stream = self.socket.makefile("rwb")
        self.read()
        self.execute("qmp_capabilities")
        return self

    def read(self):
        while True:
            line = self.stream.readline()
            if not line:
                raise RuntimeError("QMP disconnected")
            result = json.loads(line)
            if "event" not in result:
                return result

    def execute(self, command, arguments=None):
        message = {"execute": command}
        if arguments is not None:
            message["arguments"] = arguments
        self.stream.write(json.dumps(message).encode() + b"\n")
        self.stream.flush()
        result = self.read()
        if "error" in result:
            raise RuntimeError(result["error"])
        return result["return"]

    def hmp(self, command):
        return self.execute("human-monitor-command", {"command-line": command})

    def key(self, chord):
        result = self.hmp("sendkey " + chord + " 80")
        if result:
            raise RuntimeError(result)
        time.sleep(0.13)

    def wait_for(self, needle, timeout=20):
        return self.wait_until(lambda screen: needle in screen, repr(needle), timeout)

    def wait_absent(self, needle, timeout=20):
        return self.wait_until(lambda screen: needle not in screen, "absence of " + repr(needle), timeout)

    def wait_until(self, predicate, description, timeout=20):
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            screen = self.text(RUNTIME / "inspect")
            if predicate(screen):
                return screen
            time.sleep(0.1)
        raise TimeoutError(f"Guest did not reach {description}:\n{screen}")

    def type(self, value):
        punctuation = {" ": "spc", ":": "shift-semicolon", "\\": "backslash",
                       "/": "slash", ".": "dot", "-": "minus", "_": "shift-minus",
                       "=": "equal", "+": "shift-equal", ",": "comma", "\n": "ret",
                       '{': "shift-bracket_left", '}': "shift-bracket_right",
                       '"': "shift-apostrophe", "~": "shift-grave_accent", ";": "semicolon",
                       "<": "shift-comma", ">": "shift-dot"}
        for char in value:
            if char in punctuation:
                self.key(punctuation[char])
            elif char.isascii() and char.isalnum():
                self.key("shift-" + char.lower() if char.isupper() else char)
            else:
                raise ValueError(f"Unmapped reference input character {char!r}")

    def text(self, directory):
        directory = Path(directory).resolve()
        directory.mkdir(parents=True, exist_ok=True)
        raw = directory / "vram.bin"
        result = self.hmp(f'pmemsave 0xb8000 4000 "{raw}"')
        if result:
            raise RuntimeError(result)
        data = raw.read_bytes()
        rows = [data[i:i+160:2].replace(b"\x00", b" ").decode("cp437").rstrip() for i in range(0, 4000, 160)]
        text = "\n".join(rows) + "\n"
        (directory / "screen.txt").write_text(text)
        return text

    def capture(self, directory):
        directory = Path(directory).resolve()
        directory.mkdir(parents=True, exist_ok=True)
        running = self.execute("query-status")["running"]
        if running:
            self.execute("stop")
        try:
            self.execute("screendump", {"filename": str(directory / "screen.ppm")})
            from PIL import Image
            with Image.open(directory / "screen.ppm") as im:
                im.save(directory / "screen.png")
            text = self.text(directory)
            (directory / "guest-status.json").write_text(json.dumps(self.execute("query-status"), indent=2) + "\n")
            return text
        finally:
            if running:
                self.execute("cont")

    def __exit__(self, *unused):
        self.stream.close()
        self.socket.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["key", "type", "text", "capture", "hmp", "quit"])
    parser.add_argument("value", nargs="?", default="")
    args = parser.parse_args()
    with QMP() as q:
        if args.action == "key":
            for key in args.value.split(","):
                q.key(key.strip())
        elif args.action == "type":
            q.type(args.value)
        elif args.action == "text":
            print(q.text(RUNTIME / "inspect"))
        elif args.action == "capture":
            print(q.capture(args.value))
        elif args.action == "hmp":
            print(q.hmp(args.value))
        else:
            q.execute("quit")


if __name__ == "__main__":
    main()
