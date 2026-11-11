#!/usr/bin/env python3
"""Run ordinary cmd/wordling input through an 80×25 Linux PTY."""
from argparse import ArgumentParser
import codecs
import fcntl
import hashlib
import importlib.util
import json
from pathlib import Path
import signal
import struct
import termios
import time


def observer_module(repo):
    source = repo / "internal/tui/evidence/wp52/run_pty.py"
    spec = importlib.util.spec_from_file_location("wp84_styled_observer", source)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def run(repo, binary, output):
    previous = observer_module(repo)
    process = previous.old.PTY(binary, output, {"profile": "local-flat"})
    process.env.pop("NO_COLOR", None)
    process.env["COLORTERM"] = "truecolor"
    class EverydayTerminal(previous.Styled):
        """Keep the pinned ANSI observer and translate two single-cell glyphs."""

        def __init__(self):
            super().__init__()
            self.decoder = codecs.getincrementaldecoder("utf-8")()

        def feed(self, wire):
            cells = self.decoder.decode(wire)
            super().feed(cells.replace("▲", "^").replace("│", "|").encode("ascii"))

        def roles(self, row):
            roles = super().roles(row)
            for column, (fg, bg, bold) in enumerate(self.styles[row]):
                if bg == 49:
                    roles[column] = 0x1F if fg == 97 or bold else 0x17
                elif (fg, bg, bold) == (34, 47, False):
                    roles[column] = 0x71
                elif (fg, bg, bold) == (97, 47, False):
                    roles[column] = 0x7F
            return roles

    process.terminal = EverydayTerminal()
    fcntl.ioctl(process.slave, termios.TIOCSWINSZ, struct.pack("HHHH", 25, 80, 0, 0))
    original = repo / "internal/tui/evidence/everyday/FLOW.WP"
    raw = original.read_bytes()
    (process.work / "FLOW.WP").write_bytes(raw)
    look = repo / "docs/research/everyday-contract-2026-11-05/qualification/files/exports/A.WP"
    (process.work / "ZZ.WP").write_bytes(look.read_bytes())
    result = {
        "binary_sha256": sha(binary.read_bytes()),
        "reference": str(original.relative_to(repo)),
        "reference_sha256": sha(raw),
        "argv": process.argv,
        "TERM": process.env["TERM"],
        "COLORTERM": process.env["COLORTERM"],
        "frames": [],
    }

    def expect(marker, row=None, timeout=2):
        deadline = time.monotonic() + timeout
        while True:
            rows = process.terminal.rows()
            if marker in ("\n".join(rows) if row is None else rows[row]):
                return rows
            if time.monotonic() >= deadline or process.proc.poll() is not None:
                raise AssertionError(f"missing {marker!r} at row {row!r}: {rows!r}")
            process.collect(.02)

    def step(data, label, marker=None, row=None):
        process.send(data, label)
        if marker is not None:
            expect(marker, row)
        result["frames"].append({
            "label": label,
            "rows": process.terminal.rows(),
            "cursor": [process.terminal.x, process.terminal.y],
            "roles": [process.terminal.roles(y) for y in range(25)],
        })

    def resize(rows):
        fcntl.ioctl(process.slave, termios.TIOCSWINSZ, struct.pack("HHHH", rows, 80, 0, 0))
        process.proc.send_signal(signal.SIGWINCH)
        process.collect(.12)

    failure = None
    try:
        process.proc = previous.old.subprocess.Popen(
            process.argv, stdin=process.slave, stdout=process.slave,
            stderr=previous.old.subprocess.PIPE, env=process.env,
        )
        expect("Graphics Help", 0)
        step(b"\x1b[?31u", "synthetic keyboard enhancement response")
        step(b"\x1b=", "physical Alt+= menu focus")
        step(b"\x1b[B", "open File from keyboard", "Retrieve")
        step(b"\x1b[18~", "F7 returns from keyboard menu")
        step(b"\x1b[<0;1;1M", "SGR click on File menu", "Retrieve")
        resize(12)
        step(b"x", "12-row menu input stays with menu", "Retrieve")
        resize(11)
        expect("Menu active")
        step(b"x", "11-row menu input stays with menu")
        resize(25)
        expect("Retrieve")
        step(b"\x1b[18~", "F7 returns from File menu")
        step(b"\x1b[15~", "physical F5", "Dir C:\\*.*", 24)
        resize(12)
        expect("Dir C:\\*.*", 11)
        resize(11)
        expect("List Files active")
        step(b"x", "input held by narrow directory prompt")
        resize(25)
        expect("Dir C:\\*.*", 24)
        step(b"\r", "confirm directory template", "Directory C:\\*.*", 0)
        resize(12)
        step(b"x", "12-row listing input stays with browser")
        resize(11)
        expect("List Files active")
        step(b"x", "11-row listing input stays with browser")
        resize(25)
        expect("Directory C:\\*.*", 0)
        step(b"5", "choose Short/Long Display", "1 Short Display; 2 Long Display: 2", 24)
        assert [process.terminal.x, process.terminal.y] == [33, 24]
        step(b"2", "Long choice opens directory confirmation", "Dir C:\\*.*", 24)
        assert [process.terminal.x, process.terminal.y] == [4, 24]
        assert process.terminal.roles(24)[:len("Dir C:\\*.*")] == [0x1F] * len("Dir C:\\*.*")
        assert "Descriptive Name" not in process.terminal.rows()[2]
        step(b"\x1bOP", "F1 cancels Long without changing the list", "N Name Search:", 24)
        assert "Descriptive Name" not in process.terminal.rows()[2]
        step(b"5", "open display choice again", "1 Short Display", 24)
        step(b"\r", "accept default Long and request its directory", "Dir C:\\*.*", 24)
        step(b"\x1b[18~", "F7 confirms visible Long directory", "Descriptive Name", 2)
        step(b"5", "choose Short from Long", "1 Short Display; 2 Long Display: 1", 24)
        step(b"1", "Short choice opens directory confirmation", "Dir C:\\*.*", 24)
        assert [process.terminal.x, process.terminal.y] == [4, 24]
        assert "Descriptive Name" in process.terminal.rows()[2]
        step(b"\x1b", "Escape preserves the confirmed Long list", "N Name Search:", 24)
        assert "Descriptive Name" in process.terminal.rows()[2]
        step(b"5", "choose Short again", "1 Short Display", 24)
        step(b"1", "Short opens the same pinned directory", "Dir C:\\*.*", 24)
        step(b"\r", "Enter confirms Short directory", "N Name Search:", 24)
        assert "Descriptive Name" not in process.terminal.rows()[2]
        assert process.terminal.rows()[3][39] == "|"
        step(b"n", "Name Search", "Name Search", 24)
        step(b"FLOW.WP", "type observed native filename")
        step(b"\r", "confirm file selection", "6 Look", 24)
        step(b"6", "Look selected file", "File: C:\\FLOW.WP", 0)
        step(b"1", "Look next native document", "File: C:\\ZZ.WP", 0)
        step(b"2", "Look previous native document", "File: C:\\FLOW.WP", 0)
        step(b"\x1b[18~", "return from Look", "Directory C:\\*.*", 0)
        step(b"1", "retrieve same selection", "A faithful reconstruction")
        step(b"\x1b[23~", "physical F11 Reveal", "Press Reveal Codes", 24)
        expect("Menus,[SRt]", 13)
        expect("Plain [UND]UNDER[und] after[HRt]", 16)
        expect("[Tab]Tab alpha alpha[HRt]", 17)
        compare_reveal(repo, process.terminal)
        step(b"\x1b[6~", "physical PageDown", "Doc 1 Pg 2 Ln 1", 11)
        step(b"\x1b[5~", "physical PageUp", "Doc 1 Pg 1 Ln 1", 11)
        step(b"\x1bOF", "physical End", "Pos 7.3", 11)
        step(b"\x1bOH", "first Home prefix")
        step(b"\x1bOH", "second Home prefix")
        step(b"\x1b[D", "Home Home Left returns to physical line start", 'Pos 1"', 11)
        step(b"\x1bOQ", "physical F2 Search", "Srch:", 11)
        step(b"unfindable", "type a missing query")
        step(b"\x1bOQ", "run search", "* Not found *", 11)
        expect("Doc 1 Pg 1", 11)
        step(b"\x1b[13;3~", "original Alt+F3 closes Reveal", "Doc 1 Pg 1", 24)
        step(b"\x1b[21~", "physical F10 native save", "Document to be saved:", 24)
        step(b"COPY.WP", "type a new native target")
        step(b"\r", "publish native copy")
        copy = process.work / "COPY.WP"
        deadline = time.monotonic() + 2
        while not copy.exists() and time.monotonic() < deadline:
            process.collect(.02)
        assert copy.read_bytes() == raw, "browse, Look, resize and search must preserve every native byte"
        assert (process.work / "FLOW.WP").read_bytes() == raw, "source file changed"
        step(b"\x1b[18~", "physical F7", "Save document?", 24)
        step(b"n", "decline exit save", "Exit WP?", 24)
        step(b"y", "confirm normal exit")
        process.proc.wait(timeout=3)
        assert process.proc.returncode == 0
        result["copy_sha256"] = sha(copy.read_bytes())
    except Exception as err:
        failure = repr(err)
    finally:
        try:
            result["termios_restored"] = process.close()
        except Exception as err:
            result["termios_restored"] = False
            failure = failure or repr(err)
        result["returncode"] = process.proc.returncode if process.proc is not None else None
        result["failure"] = failure
        (output / "everyday-pty-result.json").write_text(json.dumps(result, indent=2) + "\n")
    if failure or not result["termios_restored"]:
        raise AssertionError(failure or "terminal attributes were not restored")


def compare_reveal(repo, terminal):
    reference = repo / "docs/research/everyday-contract-2026-11-05/qualification/scroll-search-r1/03-reveal-start/vram.bin"
    raw = reference.read_bytes()
    assert len(raw) == 4000
    assert sha(raw) == "cf453e5c094e15e38a5f87e6a6403a388f99bc7410fed958d219d2c33e9dcae6"
    rows = terminal.rows()

    def compare(original_y, terminal_y, first=0, last=80):
        cells = raw[original_y*160:(original_y+1)*160]
        original = cells[::2].replace(b"\x1e", b"^").decode("ascii")
        roles = terminal.roles(terminal_y)
        for column in range(first, last):
            assert rows[terminal_y][column] == original[column], (original_y, terminal_y, column, rows[terminal_y], original)
            assert roles[column] == cells[column*2+1], (original_y, terminal_y, column, roles[column], cells[column*2+1])

    # The launched Linux profile displays a menu on row 0. The selected
    # original used the no-menu view, so the upper text is one row later.
    for row in (0, 1, 3, 4, 5, 6):
        compare(row, row+1, last=65)
    # Both profiles reserve the same physical status and code rows.
    compare(11, 11, first=52)
    compare(12, 12)
    for row in range(13, 23):
        compare(row, row)
    compare(24, 24)


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("repo", type=Path)
    parser.add_argument("binary", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    if args.output.exists():
        parser.error("output must be a fresh disposable directory")
    run(args.repo.resolve(), args.binary.resolve(), args.output.resolve())


if __name__ == "__main__":
    main()
