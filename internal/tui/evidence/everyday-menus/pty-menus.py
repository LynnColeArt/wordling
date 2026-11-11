#!/usr/bin/env python3
"""Verify original menu cells, direct commands, Help, Setup and fresh startup."""
from argparse import ArgumentParser
import fcntl
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import termios
import time


def import_path(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run(repo, binary, output):
    base = repo / "internal/tui/evidence"
    old = import_path("wp85_observer", base / "wp52/run_pty.py")
    adapter = import_path("wp85_single_cell", base / "everyday-menus/pty-wp84.py")
    reference = repo / "docs/research/everyday-contract-2026-11-05/qualification"
    config = output / "user-config"
    config.mkdir(parents=True)
    settings = config / "wordling/settings"
    header = b"wordling-settings=1\nmenu_bar_remains_visible="
    runs = []

    class Terminal(old.Styled):
        def __init__(self):
            super().__init__()
            self.decoder = adapter.MenuDecoder()

        def feed(self, wire):
            cells = self.decoder.decode(wire).replace("▲", "^").replace("│", "|")
            super().feed(cells.encode("ascii"))

        def roles(self, y):
            roles = super().roles(y)
            for x, (fg, bg, bold) in enumerate(self.styles[y]):
                if (fg, bg, bold) == (34, 47, False):
                    roles[x] = 0x71
                if (fg, bg, bold) == (31, 47, False):
                    roles[x] = 0x74
                if bg == 49:
                    roles[x] = 0x1F if fg == 97 or bold else 0x17
            return roles

    def exercise(name, visible, set_value):
        process = old.old.PTY(binary, output / name, {"profile": "local-flat"})
        process.env.pop("NO_COLOR", None)
        process.env.update(COLORTERM="truecolor", XDG_CONFIG_HOME=str(config))
        process.terminal = Terminal()
        fcntl.ioctl(process.slave, termios.TIOCSWINSZ, struct.pack("HHHH", 25, 80, 0, 0))
        observations = []

        def expect(marker, row=None):
            deadline = time.monotonic() + 3
            while True:
                rows = process.terminal.rows()
                if marker in ("\n".join(rows) if row is None else rows[row]):
                    return
                if process.proc.poll() is not None or time.monotonic() >= deadline:
                    raise AssertionError((marker, row, rows))
                process.collect(.02)

        def step(raw, label, marker=None, row=None):
            process.send(raw, label)
            if marker is not None:
                expect(marker, row)
            observations.append({"label": label, "cursor": [process.terminal.x, process.terminal.y]})

        def compare(frame, x, y, w, h):
            original = (reference / frame / "vram.bin").read_bytes()
            rows = process.terminal.rows()
            for line in range(y, y+h):
                raw = original[line*160:(line+1)*160]
                text = raw[::2].replace(b"\x10", b">").decode("cp437")
                text = text.translate(adapter.MenuDecoder.cells).replace("│", "|")
                assert rows[line][x:x+w] == text[x:x+w], (frame, line, rows[line], text)
                assert process.terminal.roles(line)[x:x+w] == list(raw[1::2][x:x+w]), (frame, line, process.terminal.roles(line), list(raw[1::2]))

        try:
            process.proc = old.old.subprocess.Popen(process.argv, stdin=process.slave,
                stdout=process.slave, stderr=old.old.subprocess.PIPE, env=process.env)
            expect("Doc 1 Pg 1", 24)
            assert ("File Edit" in process.terminal.rows()[0]) == visible
            step(b"\x1b[?31u", "keyboard enhancement response")
            step(b"EDIT", "typing goes to the document", "EDIT", 1 if visible else 0)
            step(b"\x1b=", "Alt+= focuses the menu bar", "File Edit", 0)
            compare("menus/14-focused-bar", 0, 0, 80, 1)
            step(b"l", "Layout menu", "Line", 1)
            step(b"j", "Justify child", "Left", 14)
            compare("menus/21-layout-justify", 35, 13, 10, 6)
            step(b"\x1bOP", "F1 retains drawn child")
            compare("focus-r1/02-f1-after", 35, 13, 10, 6)
            step(b"\x1b[A", "Up opens Endnote child", "Create", 12)
            step(b"\x1b[18~", "F7 leaves menus")
            if visible:
                step(b"\x1b[<0;1;1M", "SGR File selection", "Retrieve", 1)
                compare("menus/18-file-menu", 0, 1, 23, 16)
                step(b"\x1b[18~", "F7 returns from mouse menu")
            step(b"\x1b=", "keyboard bar focus", "File Edit", 0)
            step(b"o", "Font mnemonic is o", "Base Font", 1)
            step(b"\x1b[17~", "F6 leaves menu and starts native Bold")
            step(b"B", "bold text reaches editor", "EDITB", 1 if visible else 0)
            step(b"\x1b[17~", "F6 closes native Bold")
            step(b"\x1bOR", "F3 Help", "WP 5.1   03/09/92", 0)
            step(b"\x1bOR", "F3 keyboard template", "WordPerfect 5.1 Template", 0)
            step(b"\x1b[21~", "F10 help topic", "Save", 0)
            step(b"\r", "Enter returns from Help", "EDITB", 1 if visible else 0)
            if set_value is not None:
                step(b"\x1b[1;2P", "Shift+F1 Setup", "Setup", 0)
                step(b"2", "Display", "Setup: Display", 0)
                step(b"4", "Menu Options", "Setup: Menu Options", 0)
                step(b"8", "Menu Bar Remains Visible question", "Selection: 8", 24)
                step(b"y" if set_value else b"n", "publish chosen preference", "Selection: 0", 24)
                expected = header + (b"yes\n" if set_value else b"no\n")
                assert settings.read_bytes() == expected
                assert settings.stat().st_mode & 0o777 == 0o600
                step(b"\x1b[18~", "leave Setup", "EDITB", 1 if set_value else 0)
                assert ("File Edit" in process.terminal.rows()[0]) == set_value
            step(b"\x1b[15~", "F5 lists the document workspace", "Dir C:\\*.*", 24)
            step(b"\r", "list only document workspace entries", "Directory C:\\*.*", 0)
            assert "settings" not in "\n".join(process.terminal.rows()).lower()
            step(b"\x1b[18~", "leave browser")
            step(b"\x1b[21~", "save the native document", "Document to be saved:", 24)
            step(b"MENU.WP", "native filename")
            step(b"\r", "publish original-format document", "MENU.WP", 24)
            saved = process.work / "MENU.WP"
            deadline = time.monotonic() + 3
            while not saved.exists() and time.monotonic() < deadline:
                process.collect(.02)
            assert saved.read_bytes().endswith(b"EDIT\xc3\x0c\xc3B\xc4\x0c\xc4")
            step(b"\x1b[18~", "F7 original exit", "Save document?", 24)
            step(b"n", "decline exit save", "Exit WP?", 24)
            step(b"y", "confirm exit")
            process.proc.wait(timeout=3)
            assert process.proc.returncode == 0
        finally:
            restored = process.close()
            runs.append({"name": name, "observations": observations, "termios_restored": restored})
            (output / "results.json").write_text(json.dumps(runs, indent=2) + "\n")
            assert restored

    assert not settings.exists()
    exercise("default-yes", True, False)
    exercise("fresh-no", False, True)
    exercise("fresh-yes", True, None)
    digest = hashlib.sha256(binary.read_bytes()).hexdigest()
    print(f"Three actual executable processes passed, binary SHA-256 {digest}")


def main():
    parser = ArgumentParser(__doc__)
    parser.add_argument("repo", type=Path)
    parser.add_argument("binary", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    run(args.repo.resolve(), args.binary.resolve(), args.output.resolve())


if __name__ == "__main__":
    main()
