# Standard Printer disk output

The reference was WordPerfect 5.1 US DOS, March 9, 1992, with Standard Printer (STANPRIN.PRS, Courier 10 cpi, US Letter). In the original, press Shift+F7, S, 3, 2, 8, enter the disk filename, then press Enter and F7 twice. Select 1 for Full Document or 2 for Page. The fixtures were copied from the guest disk after stopping the guest.

| Fixture | Original input and action |
| --- | --- |
| disk.PRN | Type `Hello print`, Enter, and `Second line`. Print Full Document. |
| attrs.PRN | Type `A `, F6, `B`, F8, `C`, F6, `D`, F8, then ` E  `. Print Full Document. |
| pages.PRN | Type `One`, Ctrl+Enter, and `Two`. Print Full Document. |
| current.PRN | Use the same two pages and select Page with the cursor on page 2. |

The driver emits 66 CRLF line advances per Letter sheet. Bold and Underline use separate carriage-return overstrikes. The Wordling terminal replay compares the full output files and exercises page navigation in the terminal View Document. The original View Document uses a graphics display. Wordling's initial view uses fixed-width character cells.

```sh
run_dir=$(mktemp -d /tmp/wordling-print.XXXXXX)
go build -o "$run_dir/wordling" ./cmd/wordling
for case in disk attrs pages current; do
  python3 tests/everyday_qualification/printing.py "$PWD" "$run_dir/wordling" "$run_dir/$case" "$case"
done
```

The implemented scope is the Standard Printer profile, an unused disk filename in the workspace, full document and current page. Hardware printing, other printer definitions, print jobs and graphics preview remain open.
