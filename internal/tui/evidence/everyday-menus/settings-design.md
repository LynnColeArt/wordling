# WP85 Linux menu preference mapping proposed for review

## Contract

D-EE-04 prefers the native SET file where a checked, format-preserving setter exists. The approved production interfaces expose native document, layout, workspace and backup operations. They have no admitted original SET setter. The smallest reviewed Linux mapping for EE-003 stores one app preference per Linux user through the normal historic editor. The existing startup profile chooses Yes when the file is absent. The document workspace is chosen independently, so the setting follows the user across document roots and ordinary F5 listings contain workspace entries.

Resolve the app directory with `os.UserConfigDir()` and append `wordling`. On Linux this uses the user's XDG config directory or its normal home fallback. The preference file is `settings`. Its entire version-1 format is ASCII:

```text
wordling-settings=1
menu_bar_remains_visible=yes
```

The same exact form with `no` is the only other accepted value. A fixed grammar rejects unknown keys, duplicates, missing values, extra bytes and unknown versions. Read a bounded regular file. A missing file or directory selects Yes without creating files. Malformed, inaccessible or unresolvable configuration produces a visible settings error while the editor uses its Yes default. The reader and writer operate only on this application config. Native documents and original SET files continue using their own existing authorities.

## Setup and atomic publication

The original sequence is Shift+F1 → Setup → 2 Display → 4 Menu Options → 8 Menu Bar Remains Visible → Yes or No. Opening the menu, moving focus, declining a change and startup perform no writes. A confirmed Yes/No choice updates the live preference after successful publication. Persistence is independent of whether the user later leaves Setup with F7 or exits the editor normally. A write failure stays in the setting context, retains the previous active preference and shows the actionable error. Existing malformed or unrecognized version files are refused on write, avoiding a destructive automatic reset.

Create the application config directory lazily with mode 0700. Pin it with Go's `os.OpenRoot`. Create an exclusive random-suffixed sibling temporary file mode 0600 under that root, write the complete bounded record, sync and close it, then atomically rename to `settings` inside the same directory. Clean up the temporary file on failures. Regular-file validation refuses a special or link destination. With one key, concurrent successful publications each contain one complete preference and the latest replacement sets the next startup state. No document backup behavior is invoked for settings.

## Verification

Use disposable `XDG_CONFIG_HOME` directories for settings tests and real CLI subprocesses. Unrelated historic-profile tests should also run against an empty temporary user config, so an existing user's No preference does not change test expectations. The Model/API coverage verifies absent defaults, exact wire record, Yes/No across a fresh Open and different document roots, malformed/version and publication errors, unchanged in-memory state on failure, cancellation without creation, and settings outside the ordinary F5 list. The terminal probe verifies the actual Shift+F1 sequence, both startup preferences, distinct menu visibility/focus and continued typing. The existing document format, ordinary Save/Backup seam and source bytes stay under their approved owners.

TUI source lives in the issued WP85-owned settings/runtime/model/menu files. A shared test isolation change outside H, if required for external baseline expectations, uses the separately reviewed test-only lane. The design adds one persistent key. Any separately approved setup for Original Document Backup can continue using the editor's existing WithOriginalBackup operation.
