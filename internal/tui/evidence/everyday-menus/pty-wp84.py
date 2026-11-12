#!/usr/bin/env python3
"""Run the frozen WP84 assertions with an observer for added menu glyphs."""
import codecs
import importlib.util
import sys
from pathlib import Path
from types import SimpleNamespace


class MenuDecoder:
    cells = str.maketrans({"├": "+", "┤": "+", "└": "+", "┘": "+",
                           "┌": "+", "┐": "+", "─": "-", "┬": "+",
                           "┴": "+", "►": ">", "║": "|", "═": "-",
                           "╔": "+", "╗": "+", "╚": "+", "╝": "+",
                           "╤": "+", "╧": "+"})

    def __init__(self):
        self.decoder = codecs.getincrementaldecoder("utf-8")()

    def decode(self, wire):
        return self.decoder.decode(wire).translate(self.cells)


def main():
    repo = Path(sys.argv[1]).resolve()
    driver = repo / "internal/tui/evidence/everyday/pty-everyday.py"
    spec = importlib.util.spec_from_file_location("wp84_pty_driver", driver)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.codecs = SimpleNamespace(getincrementaldecoder=lambda encoding: MenuDecoder)
    module.main()


if __name__ == "__main__":
    main()
