#!/usr/bin/env python3
"""Real Linux terminal qualification. Keep failures and raw observations."""
import argparse
import codecs
import fcntl
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import signal
import struct
import subprocess
import termios
import time

F1, F2, F5, F6, F7, F8, F10, F11 = (
    b"\x1bOP", b"\x1bOQ", b"\x1b[15~", b"\x1b[17~",
    b"\x1b[18~", b"\x1b[19~", b"\x1b[21~", b"\x1b[23~",
)
SWITCH, RETRIEVE, PROOF = b"\x1b[13;2~", b"\x1b[21;2~", b"\x1b[1;5Q"
ENTER, HOME, UP = b"\r", b"\x1bOH", b"\x1b[A"
SETUP = b"\x1b[1;2P"
REF = "docs/research/everyday-contract-2026-11-05/qualification"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def native(path):
    data = path.read_bytes()
    assert data[:4] == b"\xffWPC", (path, "missing native WP signature")
    offset = int.from_bytes(data[4:8], "little")
    assert 16 <= offset <= len(data), (path, offset, len(data))
    return data, offset, data[offset:]


def native_info(path):
    data, offset, body = native(path)
    return {"bytes": len(data), "body_offset": offset, "sha256": sha(data),
            "body_sha256": sha(body)}


def load(repo, path, name):
    spec = importlib.util.spec_from_file_location(name, repo / path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Run:
    def __init__(self, repo, binary, folder):
        self.repo, self.binary, self.folder = repo, binary, folder
        old = load(repo, "internal/tui/evidence/wp52/run_pty.py", "wp86_transport")
        self.p = old.old.PTY(binary, folder, {"profile": "local-flat"})

        class Terminal(old.Styled):
            def __init__(self):
                super().__init__()
                self.decoder = codecs.getincrementaldecoder("utf-8")()

            def feed(self, wire):
                # The inherited parser handles control sequences in ASCII.
                # Known VGA substitutes are single-cell terminal glyphs.
                text = self.decoder.decode(wire)
                for part in re.split(r"([^\x00-\x7f])", text):
                    if part.isascii():
                        super().feed(part.encode("ascii"))
                    elif part in "│─┌┐└┘├┤┬┴┼║═╔╗╚╝╟╢╠╣╤╧╪╦╩╬╞╡▲▼◀▶►◄←→↑↓":
                        assert not self.pending, "Unicode inside unfinished ANSI sequence"
                        self.put(part)
                    else:
                        raise ValueError(("unqualified terminal glyph", part))

        self.p.terminal = Terminal()
        self.p.env["COLORTERM"] = "truecolor"
        self.p.env.pop("NO_COLOR", None)
        config = folder / "config"
        config.mkdir()
        self.p.env["XDG_CONFIG_HOME"] = str(config)
        self.frames = []
        self.files = {}
        fcntl.ioctl(self.p.slave, termios.TIOCSWINSZ, struct.pack("HHHH", 25, 80, 0, 0))

    def launch(self, wait_bar=True):
        self.p.proc = subprocess.Popen(
            self.p.argv, cwd=self.repo, stdin=self.p.slave, stdout=self.p.slave,
            stderr=subprocess.PIPE, env=self.p.env,
        )
        self.wait("Doc 1 Pg")
        if wait_bar:
            self.wait("Graphics Help", 0)
        self.step(b"\x1b[?31u", "synthetic keyboard capability response")

    def rows(self):
        return self.p.terminal.rows()

    def wait(self, cue, row=None, timeout=3):
        limit = time.monotonic() + timeout
        while True:
            rows = self.rows()
            if cue in ("\n".join(rows) if row is None else rows[row]):
                return rows
            if time.monotonic() >= limit or self.p.proc.poll() is not None:
                raise AssertionError((cue, row, rows))
            self.p.collect(.025)

    def until(self, condition, label, timeout=4):
        limit = time.monotonic() + timeout
        while not condition():
            if time.monotonic() >= limit or self.p.proc.poll() is not None:
                raise AssertionError((label, self.rows()))
            self.p.collect(.025)

    def capture(self, label, checks=()):
        terminal = self.p.terminal
        self.frames.append({
            "label": label, "checks": list(checks),
            "rows": self.rows(), "cursor": [terminal.x, terminal.y],
            "styles": [[list(cell) for cell in row] for row in terminal.styles],
            "wire_bytes": len(self.p.wire),
        })

    def step(self, keys, label, cue=None, row=None, checks=()):
        if isinstance(keys, str):
            keys = keys.encode("ascii")
        self.p.send(keys, label, .07)
        if cue:
            self.wait(cue, row)
        self.capture(label, checks)

    def seed(self, source, name):
        data = source.read_bytes()
        (self.p.work / name).write_bytes(data)
        self.files[name] = {"seed": str(source), "initial_sha256": sha(data)}

    def start_of_document(self):
        self.step(HOME, "Home prefix")
        self.step(HOME, "second Home prefix")
        self.step(UP, "Home Home Up to document start", 'Pos 1"')

    def retrieve(self, name):
        self.step(RETRIEVE, "Shift+F10 Retrieve", "Document to be retrieved:")
        self.step(name, "type source filename")
        self.step(ENTER, "retrieve the exact named native file")
        self.until(lambda: "Document to be retrieved:" not in "\n".join(self.rows()), "retrieval settled")

    def save(self, name, *, replace=False, prefill=False, body_fragment=None, expected_offset=324):
        path = self.p.work / name
        before = path.read_bytes() if path.is_file() else None
        self.step(F10, "F10 native Save", "Document to be saved:")
        if not prefill:
            self.step(name, "type destination")
        self.step(ENTER, "commit destination")
        if replace:
            self.wait("Replace " + name)
            self.step("y", "confirm replacement")
        self.until(lambda: path.is_file() and path.read_bytes() != before,
                   f"exact changed output at {name}")
        self.wait("Doc ")
        self.p.collect(.12)
        data, offset, body = native(path)
        assert offset == expected_offset, (path, offset)
        if body_fragment is not None:
            assert body_fragment in body, (path, body_fragment, body)
        self.files[name] = native_info(path)
        self.capture("published " + name, ("native header and body",))
        return data

    def exit_application(self):
        self.step(F7, "F7 Exit", "Save document?")
        self.step("n", "decline another save", "Exit WP?")
        self.step("y", "confirm normal application exit")
        self.p.proc.wait(timeout=4)
        assert self.p.proc.returncode == 0, self.p.proc.returncode

    def finish(self, failure, case):
        try:
            restored = self.p.close()
        except Exception as error:
            restored = False
            failure = failure or repr(error)
        record = {
            "schema": 1, "case": case, "result": "fail" if failure or not restored else "pass",
            "failure": failure, "termios_restored": restored,
            "returncode": self.p.proc.returncode if self.p.proc else None,
            "binary_sha256": sha(self.binary.read_bytes()), "argv": self.p.argv,
            "config_dir": self.p.env["XDG_CONFIG_HOME"],
            "source_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=self.repo, text=True).strip(),
            "wire_sha256": sha(bytes(self.p.wire)), "files": self.files, "steps": self.frames,
            "terminal_scope": "synthetic Linux PTY with actual key bytes and cell attributes",
        }
        (self.folder / "qualification.json").write_text(json.dumps(record, indent=2) + "\n")
        if failure or not restored:
            raise AssertionError(failure or "terminal state was not restored")


def continuous(run, preflight):
    flow = run.repo / "internal/tui/evidence/everyday/FLOW.WP"
    other = run.repo / REF / "files/exports/A.WP"
    run.seed(flow, "FLOW.WP")
    run.seed(other, "ZZ.WP")
    run.launch()
    run.step(F5, "F5 lists the current directory", "Dir C:\\*.*", 24, ("EE-A10",))
    run.step(ENTER, "confirm pinned directory", "Directory C:\\*.*", 0)
    run.step("n", "Name Search", "Name Search", 24)
    run.step("FLOW.WP", "locate original FLOW")
    run.step(ENTER, "settle selected row", "6 Look", 24)
    run.step("6", "Look without acquiring", "File: C:\\FLOW.WP", 0)
    run.step("1", "Look Next", "File: C:\\ZZ.WP", 0)
    run.step("2", "Look Previous", "File: C:\\FLOW.WP", 0)
    run.step(F7, "return from Look", "Directory C:\\*.*", 0)
    run.step("1", "retrieve original selected row", "A faithful reconstruction")
    copied = run.save("COPY.WP")
    assert copied == flow.read_bytes(), "no-edit native Save As changed original bytes"
    run.start_of_document()
    run.step(F6, "begin Bold", checks=("EE-A07",))
    run.step("quik", "write suspect within Bold", "quik")
    run.step(F6, "close Bold")
    run.step(" ", "separate attributes")
    run.step(F8, "begin Underline")
    run.step("review", "write within Underline", "review")
    run.step(F8, "close Underline")
    run.step(ENTER, "write a hard return", checks=("EE-A04",))
    run.step("A long paragraph keeps the line moving across the right margin and retains every native character. ",
             "write through a physical wrap")
    run.step(ENTER, "separate the authored paragraph from the original")
    run.start_of_document()
    run.step(F11, "Reveal on", "Press Reveal Codes", 24, ("EE-A08",))
    run.wait("[BOLD]quik[bold]")
    run.wait("[UND]review[und]")
    run.step(F2, "forward search on the same revision", "Srch:", checks=("EE-A09",))
    run.step("quik", "enter query")
    run.step(F2, "find suspect at its native boundary")
    run.step(F11, "close Reveal")
    if not preflight:
        run.start_of_document()
        run.step(PROOF, "Ctrl+F2 contextual proof", "New Sup. Dictionary", checks=("EE-A15",))
        run.step("1", "check Word at the located spelling", "Not Found")
        choose_suggestion(run, "quick")
        run.wait("Check:")
        run.wait("quick")
        run.step(F7, "leave Word-scope Check and return to ordinary editing")
        run.until(lambda: "Check:" not in "\n".join(run.rows()), "proof menu closed")
    expected = b"quik" if preflight else b"quick"
    first = run.save("WPLIVE.WP", body_fragment=expected)
    run.step(HOME, "first Home before document start")
    run.step(HOME, "second Home before document start")
    run.step(UP, "return to document start")
    run.step("Wordling ", "second authored change")
    second = run.save("WPLIVE.WP", replace=True, prefill=True, body_fragment=b"Wordling ")
    assert first != second and (run.p.work / "FLOW.WP").read_bytes() == flow.read_bytes()
    backup = run.p.work / "WPLIVE.BK!"
    if backup.exists():
        assert backup.read_bytes() == first, "backup does not contain the prior destination"
        run.files[backup.name] = native_info(backup)
    run.step(SWITCH, "Shift+F3 opens independent Doc 2", "Doc 2 Pg", checks=("EE-A12",))
    run.retrieve("WPLIVE.WP")
    run.wait("Wordling")
    run.step(SWITCH, "switch back to saved Doc 1", "Doc 1 Pg")
    run.wait("Wordling")
    run.step(SWITCH, "return to Doc 2 for its separate close", "Doc 2 Pg")
    run.step(F7, "F7 on Doc 2", "Save document?")
    run.step("n", "decline save of reloaded Doc 2", "Exit doc 2?")
    run.step("y", "close only Doc 2 and restore Doc 1", "Doc 1 Pg")
    run.exit_application()


def choose_suggestion(run, word):
    pattern = re.compile(r"(?:^|\s)([A-Xa-x])[.) :]+\s*" + re.escape(word) + r"\b")
    for attempt in range(4):
        if match := pattern.search("\n".join(run.rows())):
            run.step(match[1], "choose the actual displayed ESDB suggestion " + word)
            return
        run.step(ENTER, "advance suggestion page " + str(attempt + 1))
    raise AssertionError(("suggestion label not visible", word, run.rows()))


def reopen(run, source):
    _, _, prior_body = native(source)
    assert prior_body[:3] == b"\xc3\x0c\xc3", "preflight fixture must begin with the witnessed BoldOn"
    run.seed(source, "ROUND.WP")
    run.launch()
    run.retrieve("ROUND.WP")
    run.wait("Original")
    run.start_of_document()
    run.step("Continued ", "continue editing original-resaved native file")
    run.save("BACK.WP", body_fragment=b"Continued ")
    _, _, continued = native(run.p.work / "BACK.WP")
    assert continued == prior_body[:3] + b"Continued " + prior_body[3:], "reopen changed an unrelated native owner"
    run.exit_application()


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("repo", type=Path)
    p.add_argument("binary", type=Path)
    p.add_argument("output", type=Path)
    p.add_argument("--preflight-no-proof", action="store_true")
    p.add_argument("--reopen", type=Path)
    opts = p.parse_args()
    out = opts.output.resolve()
    if out.exists():
        p.error("output must be a fresh directory")
    run = Run(opts.repo.resolve(), opts.binary.resolve(), out)
    failure = None
    case = "original-roundtrip-reopen" if opts.reopen else "preflight" if opts.preflight_no_proof else "EE-A14"
    try:
        if opts.reopen:
            reopen(run, opts.reopen.resolve())
        else:
            continuous(run, opts.preflight_no_proof)
    except Exception as error:
        failure = repr(error)
    finally:
        run.finish(failure, case)


if __name__ == "__main__":
    main()
