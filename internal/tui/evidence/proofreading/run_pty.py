#!/usr/bin/env python3
"""Run the original proofreading workflow through the production Linux PTY."""
from argparse import ArgumentParser
import codecs
from contextlib import contextmanager
import fcntl
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import signal
import struct
import termios
import time

CTRL_F2 = b"\x1b[1;5Q"
CTRL_F2_ENHANCED = b"\x1b[57365;5:1u"
F1 = b"\x1bOP"
F7 = b"\x1b[18~"
F10 = b"\x1b[21~"
RETRIEVE = b"\x1b[21;2~"
TEXT = b"The quik brown fox met a zorbly cat. The quik fox saw zorbly again. Zorbly follows a mispelled word."
EXPECTED = b"The quick brown fox met a zorbly cat. The quick fox saw zorbly again. Zorbly follows a misspelled word."


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def observer(repo):
    path = repo / "internal/tui/evidence/wp52/run_pty.py"
    spec = importlib.util.spec_from_file_location("wordling_proof_styled_observer", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def styled_proof_observer(module):
    class StyledProof(module.Styled):
        def __init__(self):
            super().__init__()
            self.decoder = codecs.getincrementaldecoder("utf-8")()

        def feed(self, raw):
            text = self.decoder.decode(raw)
            # The inherited observer is ASCII-only. Each displayed Unicode
            # ruler/resize glyph has a one-cell ASCII measurement surrogate.
            super().feed(text.translate(str.maketrans({"▲": "^", "×": "x", "─": "-", "│": "|", "┐": "+", "└": "+", "┘": "+", "├": "+", "┤": "+", "►": ">"})).encode("ascii"))

    return StyledProof()


class ProofPTY:
    def __init__(self, module, binary, out, config, workspace=None):
        self.module = module
        self.p = module.old.PTY(binary, out, {"profile": "local-flat"})
        self.p.terminal = styled_proof_observer(module)
        self.p.env.pop("NO_COLOR", None)
        self.p.env.update(COLORTERM="truecolor", XDG_CONFIG_HOME=str(config))
        fcntl.ioctl(self.p.slave, termios.TIOCSWINSZ, struct.pack("HHHH", 25, 80, 0, 0))
        if workspace is not None:
            self.p.argv[2] = str(workspace)
        self.frames = []

    def expect(self, marker, row=None, timeout=3):
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline and self.p.proc.poll() is None:
            lines = self.p.terminal.rows()
            if marker in ("\n".join(lines) if row is None else lines[row]):
                return lines
            self.p.collect(.03)
        raise AssertionError(f"missing {marker!r} at row {row}: {self.p.terminal.rows()!r}")

    def capture(self, label):
        term = self.p.terminal
        assert not term.unknown, term.unknown
        self.frames.append(dict(label=label, rows=term.rows(), cursor=[term.x, term.y],
                                roles=[term.roles(row) for row in range(25)]))

    def step(self, raw, label, marker=None, row=None):
        self.p.send(raw, label, .07)
        if marker is not None:
            self.expect(marker, row)
        self.capture(label)

    def launch(self):
        self.p.proc = self.module.old.subprocess.Popen(
            self.p.argv, stdin=self.p.slave, stdout=self.p.slave,
            stderr=self.module.old.subprocess.PIPE, env=self.p.env,
        )
        self.expect("Graphics Help", 0)
        self.step(b"\x1b[?31u", "keyboard capabilities response")

    def quit(self):
        self.step(F7, "F7 Exit", "Save document?", 24)
        self.step(b"n", "decline Save", "Exit WP?", 24)
        self.step(b"y", "confirm Exit")
        self.p.proc.wait(timeout=3)
        assert self.p.proc.returncode == 0

    def suggestion(self, word):
        for _ in range(4):
            for row in self.p.terminal.rows()[14:22]:
                choices = re.findall(r"\b([A-X])\. ([A-Za-z']+)", row)
                for label, text in choices:
                    if text.lower() == word.lower():
                        return label.lower().encode()
            assert "Press Enter for more words" in self.p.terminal.rows()[22]
            self.step(b"\r", "Enter shows more suggestions")
        raise AssertionError(f"missing displayed suggestion {word!r}")

    def resize(self, rows, columns):
        fcntl.ioctl(self.p.slave, termios.TIOCSWINSZ, struct.pack("HHHH", rows, columns, 0, 0))
        self.p.proc.send_signal(signal.SIGWINCH)
        self.p.collect(.16)

    def red(self, row):
        return [index for index, role in enumerate(self.p.terminal.roles(row)) if role == 0x47]


@contextmanager
def observed(module, binary, out, config, workspace=None):
    term = ProofPTY(module, binary, out, config, workspace)
    failure = None
    try:
        term.launch()
        yield term
    except Exception as err:
        failure = repr(err)
        raise
    finally:
        restored = term.p.close()
        result = dict(argv=term.p.argv, termios_restored=restored, failure=failure,
                      status=term.p.proc.returncode, wire_sha256=digest(term.p.wire),
                      frames=term.frames)
        (out / "proof-pty.json").write_text(json.dumps(result, indent=2) + "\n")
        assert restored, "terminal attributes were not restored"


def run(repo, binary, out, dos_resave=None):
    module = observer(repo)
    config = out / "config"
    original = repo / "docs/research/everyday-contract-2026-11-05/spelling"
    with observed(module, binary, out / "first", config) as term:
        workspace = term.p.work
        term.step(TEXT, "type original proofreading sentence", "mispelled word.")
        term.step(CTRL_F2, "physical Ctrl+F2 Check", "4 New Sup. Dictionary", 24)
        term.step(b"3", "Document scope", "Not Found:", 24)
        assert term.red(0) == list(range(4, 8)), term.red(0)
        raw = (original / "proof/02-first-question/vram.bin").read_bytes()
        assert term.p.terminal.roles(12) == list(raw[12*160+1:13*160:2])
        footer = raw[24*160:25*160]
        for index in range(80):
            if footer[index*2] != 32:
                assert term.p.terminal.rows()[24][index] == chr(footer[index*2])
                assert term.p.terminal.roles(24)[index] == footer[index*2+1]
        assert term.p.terminal.rows()[11][52:72] == "Doc 1 Pg 1 Ln 1\" Pos"
        assert [term.p.terminal.x, term.p.terminal.y] == [76, 24]
        term.resize(18, 55)
        term.expect("Proofreading active", 0)
        term.step(b"4", "hidden choices stay held")
        term.resize(25, 80)
        term.expect("Not Found:", 24)
        assert term.red(0) == list(range(4, 8))
        term.step(term.suggestion("quick"), "choose displayed quick", "The quick brown fox")
        term.step(b"1", "Skip Once and apply remembered correction", "The quick fox")
        term.step(b"2", "Skip remainder and case variants", "Not Found:", 24)
        term.step(b"4", "Edit in document context", "Spell Edit:", 24)
        assert "File Edit" not in term.p.terminal.rows()[0]
        term.step(b"\x1b[C", "Right in Spell Edit")
        term.step(b"\x1b[C", "second Right in Spell Edit")
        term.step(b"s", "type correction", "misspelled word.")
        term.step(F7, "F7 resumes Spell Edit", "Word count: 19", 24)
        term.step(b" ", "acknowledge completed count", "File Edit", 0)
        term.step(CTRL_F2, "fresh Check", "Check:", 24)
        term.step(b"3", "new pass questions zorbly again", "Not Found:", 24)
        before = term.p.terminal.rows()
        term.step(F7, "F7 leaves live question in place", "Not Found:", 24)
        assert before == term.p.terminal.rows()
        term.step(F1, "F1 interrupts current pass", "Word count: 7", 24)
        term.step(b" ", "acknowledge partial count", "File Edit", 0)
        term.step(CTRL_F2, "Check for persistent Add", "Check:", 24)
        term.step(b"3", "Document scope for Add", "Not Found:", 24)
        term.step(b"3", "checked native Add", "Word count: 19", 24)
        term.step(b" ", "acknowledge Add scan", "File Edit", 0)
        term.step(F10, "F10 native save", "Document to be saved:", 24)
        term.step(b"PROOF.WP", "native target")
        term.step(b"\r", "publish native document", "PROOF.WP", 24)
        written = (workspace / "PROOF.WP").read_bytes()
        offset = int.from_bytes(written[4:8], "little")
        assert written[offset:].replace(b"\x0d", b" ") == EXPECTED, written[offset:]
        original_native = (original / "proof/exports/PROOF.WP").read_bytes()
        original_offset = int.from_bytes(original_native[4:8], "little")
        assert written[offset:] == original_native[original_offset:]
        sup = (workspace / "WP{WP}US.SUP").read_bytes()
        assert sup == (original / "proof/supplementary/WP{WP}US.SUP").read_bytes()
        term.quit()

    with observed(module, binary, out / "restart", config, workspace) as term:
        term.step(RETRIEVE, "fresh executable Shift+F10", "Document to be retrieved:", 24)
        term.step(b"PROOF.WP", "read prior native output")
        term.step(b"\r", "reopen native document", "PROOF.WP", 24)
        term.step(CTRL_F2_ENHANCED, "enhanced physical Ctrl+F2", "Check:", 24)
        term.step(b"3", "reopened SUP accepts all zorbly variants", "Word count: 19", 24)
        term.step(b" ", "return to ordinary editing", "File Edit", 0)
        assert (workspace / "PROOF.WP").read_bytes() == written
        assert (workspace / "WP{WP}US.SUP").read_bytes() == sup
        term.quit()

    with observed(module, binary, out / "contexts", config) as term:
        term.step(b"the  the fox", "type original Double Word example", "the  the fox")
        term.step(b"\x1b=", "Alt+= opens pull-down focus")
        term.step(b"t", "Tools pull-down", "Spell")
        term.step(b"s", "Tools Spell starts Check", "Check:", 24)
        term.step(b"3", "Document checks both exact words", "Double Word:", 24)
        assert term.red(0) == [0, 1, 2, 5, 6, 7], term.red(0)
        term.step(b"3", "Delete 2nd", "Word count: 2", 24)
        assert term.p.terminal.rows()[0].startswith("the  fox")
        term.step(b" ", "return from Double Word", "File Edit", 0)
        term.step(CTRL_F2, "Check for standalone Look Up", "Check:", 24)
        term.step(b"5", "standalone Look Up", "Word or word pattern:", 24)
        term.step(b"qu?ck", "wildcard pattern", "qu?ck", 24)
        term.step(b"\r", "evaluate standalone pattern", "quick", 14)
        term.step(b"a", "A starts a new pattern", "Word or word pattern: a", 24)
        term.step(F1, "return to Check menu", "Check:", 24)
        term.step(F1, "return to ordinary editing", "File Edit", 0)
        term.step(b" quik", "append another correctable word", "the  fox quik")
        term.step(CTRL_F2, "Check for contextual Look Up", "Check:", 24)
        term.step(b"3", "check new suspect", "Not Found:", 24)
        original_page = term.p.terminal.rows()[14]
        term.expect("Press Enter for more words", 22)
        term.step(b"\r", "physical Enter pages actual suggestions", "  A. ", 14)
        assert term.p.terminal.rows()[14] != original_page
        term.step(b"5", "contextual lookup keeps the current issue", "Word or word pattern:", 24)
        term.step(b"qu?ck", "enter contextual wildcard", "qu?ck", 24)
        term.step(b"\r", "contextual result accepts an actual choice", "Select Word: 0", 24)
        term.step(term.suggestion("quick"), "select displayed lookup choice", "Word count: 3", 24)
        term.step(b" ", "settle contextual lookup", "File Edit", 0)
        term.expect("the  fox quick", 1)
        term.quit()

    pages = repo / "docs/research/everyday-contract-2026-11-05/qualification/proof-pages/exports"
    with observed(module, binary, out / "scopes", config) as term:
        term.step(b"\x1b[1;2P", "Shift+F1 Setup for the compact original comparison", "Setup", 0)
        term.step(b"3", "open Environment", "Setup: Environment", 0)
        term.step(b"5", "select Fast Save", "Selection: 5", 24)
        term.step(b"n", "select Fast Save No", "Selection: 0", 24)
        term.step(F7, "return to ordinary editing", "File Edit", 0)
        (term.p.work / "BEFORE.WP").write_bytes((pages / "BEFORE.WP").read_bytes())
        term.step(RETRIEVE, "Shift+F10 original attributed document", "Document to be retrieved:", 24)
        term.step(b"BEFORE.WP", "original formatted source name")
        term.step(b"\r", "retrieve original formatted source", "BEFORE.WP", 24)
        term.step(b"\x1bOQ", "F2 finds first questionable word", "Srch:", 24)
        term.step(b"quik", "enter Word-scope caret target", "quik", 24)
        term.step(b"\x1bOQ", "F2 places caret after first suspect", "BEFORE.WP", 24)
        term.step(CTRL_F2, "Check for Word scope", "Check:", 24)
        term.step(b"1", "check only the current native word", "Not Found:", 24)
        term.step(term.suggestion("quick"), "Word correction returns to Check", "Check:", 24)
        term.step(b"2", "Page checks current physical page", "Not Found:", 24)
        term.step(term.suggestion("misspelled"), "Page corrects and remembers within scope", "Word count:", 24)
        term.step(b" ", "acknowledge Page and return to Check", "Check:", 24)
        term.step(F7, "leave Check for ordinary editing", "File Edit", 0)
        term.step(F10, "F10 Save As original page-only output", "Document to be saved:", 24)
        term.step(b"PAGEONLY.WP", "native page-only target")
        term.step(b"\r", "publish scoped proofreading changes", "PAGEONLY.WP", 24)
        scoped = (term.p.work / "PAGEONLY.WP").read_bytes()
        assert scoped == (pages / "PAGEONLY.WP").read_bytes()
        term.quit()

    with observed(module, binary, out / "mnemonics", config) as term:
        term.step(b"The quik fox.", "type original mnemonic fixture", "The quik fox.")
        term.step(b"\x1b[H", "Home")
        term.step(b"\x1b[H", "Home again")
        term.step(b"\x1b[A", "Up reaches document start")
        for index in range(4):
            term.step(b"\x1b[C", f"Right to native column {index + 1}")
        term.step(CTRL_F2, "open original Check", "Check:", 24)
        term.step(b"w", "physical W selects Word", "Not Found:", 24)
        assert term.red(0) == [4, 5, 6, 7]
        term.step(F1, "Word F1 returns directly to Check", "Check:", 24)
        term.step(b"p", "physical P selects Page", "Not Found:", 24)
        term.step(F1, "Page F1 shows partial count", "Word count: 2", 24)
        term.step(b" ", "Page partial returns to Check", "Check:", 24)
        term.step(b"d", "physical D selects Document", "Not Found:", 24)
        term.step(F1, "Document F1 shows partial count", "Word count: 2", 24)
        term.step(b" ", "Document partial returns to the editor", "File Edit", 0)
        assert [term.p.terminal.x, term.p.terminal.y] == [4, 1]
        term.step(CTRL_F2, "reopen original Check", "Check:", 24)
        term.step(b"n", "physical N opens supplementary name", "Supplemental dictionary name:", 24)
        term.step(b"c", "C is literal within dictionary name", "Supplemental dictionary name: c", 24)
        term.step(F1, "cancel the name without creating a file", "Check:", 24)
        term.step(b"l", "physical L opens standalone Look Up", "Word or word pattern:", 24)
        term.step(b"n", "N is literal within lookup", "Word or word pattern: n", 24)
        term.step(F1, "cancel lookup", "Check:", 24)
        term.step(b"c", "physical C counts the whole document", "Word count: 3", 24)
        term.step(b" ", "Count returns to Check", "Check:", 24)
        term.step(F1, "Check cancellation returns to ordinary editing", "File Edit", 0)
        term.step(F10, "save exact unchanged mnemonic input", "Document to be saved:", 24)
        term.step(b"MENU.WP", "exact native witness basename")
        term.step(b"\r", "publish unchanged text", "MENU.WP", 24)
        menu = (term.p.work / "MENU.WP").read_bytes()
        assert menu[int.from_bytes(menu[4:8], "little"):] == b"The quik fox."
        assert not (term.p.work / "C").exists()
        term.quit()

    report = dict(binary_sha256=digest(binary.read_bytes()), document_sha256=digest(written),
                  original_document_sha256=digest((original / "proof/exports/PROOF.WP").read_bytes()),
                  supplementary_sha256=digest(sup), page_only_sha256=digest(scoped), menu_witness_sha256=digest(menu),
                  term="xterm-256color", processes=5)
    if dos_resave is not None:
        with observed(module, binary, out / "dos-reopen", config) as term:
            original_resave = dos_resave.read_bytes()
            (term.p.work / "REP89.WP").write_bytes(original_resave)
            term.step(RETRIEVE, "retrieve stopped original DOS resave", "Document to be retrieved:", 24)
            term.step(b"REP89.WP", "exact DOS resaved basename")
            term.step(b"\r", "reopen original DOS document", "REP89.WP", 24)
            term.expect("DOSEND")
            term.step(b"\x1b[H", "Home")
            term.step(b"\x1b[H", "Home again")
            term.step(b"\x1b[B", "Down reaches document end")
            term.step(b" GOEND", "continue editing original resave", "DOSEND GOEND")
            term.step(F10, "save the continued edit", "Document to be saved:", 24)
            term.step(b"CONT89.WP", "distinct native destination")
            term.step(b"\r", "publish edited original output", "CONT89.WP", 24)
            continued = (term.p.work / "CONT89.WP").read_bytes()
            assert continued.endswith(b" DOSEND GOEND")
            assert (term.p.work / "REP89.WP").read_bytes() == original_resave
            term.quit()
        report.update(dos_resave_sha256=digest(original_resave), continued_sha256=digest(continued), processes=6)
    (out / "result.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    for name in ("repo", "binary", "output"):
        parser.add_argument(name, type=Path)
    parser.add_argument("--dos-resave", type=Path)
    args = parser.parse_args()
    if args.output.exists():
        parser.error("output must be a fresh disposable directory")
    run(args.repo.resolve(), args.binary.resolve(), args.output.resolve(), args.dos_resave)
