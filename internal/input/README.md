# Typed input boundary

`Translate(tea.Msg) Event` wraps pinned `charm.land/bubbletea/v2 v2.1.1`.
It is used by `cmd/wordling-input-probe` and is the transport boundary for the
later session composition. It does not resolve WordPerfect commands. In
particular, Escape is a delivered key, not a global Cancel; F7 is not a probe
quit key; `q`, Ctrl+Q and Ctrl+S have no special bindings here.

`Event.Kind` is the discriminant. Only Press and Release carry Key. Both retain
Code, Mod, Text, ShiftedCode, BaseCode and IsRepeat without string matching,
modifier inference or normalization. A release is not a second press. An OS
repeat indication is separate from original WP Repeat Value semantics. The
adapter cannot restore distinctions already lost in a legacy terminal decoder.

Paste carries exact text and start/end events, never parsed keys. Mouse carries
its original coordinates/button/modifiers and specific event kind. Resize is
viewport input, not document layout. KeyboardCapabilities contains the actual
response Flags and pinned Supports method results; requesting enhancements does
not create a supported response. A zero-valued or absent alternate code is not
proof of a physical key's identity. Capability, terminal-version and focus/blur
remain separate from commands.

Ownership: every translated Key, Mouse and Support pointer refers to a fresh
value owned by the returned Event; the adapter keeps no state or aliases between
calls. Callers may mutate their own returned values. Strings are immutable Go
values. Original retains the received message itself, including unknown
messages, without a deep copy of arbitrary caller-defined pointer payloads;
callers must not concurrently mutate that original payload. Original is omitted
from JSON. SourceType identifies the original message type. Unknown values have
Kind Unknown and no Key, and must not dispatch editor commands. The probe's
separate raw-byte journal preserves unknown wire payloads; SourceType alone is
not a serialized replacement for unknown data.

This package does not read or write native files, map Unicode into WP character
identities, infer Alt from separately delivered Escape, or promise physical
keyboard delivery. See the terminal-input evidence report for the explicit
unqualified physical profile and reproducible synthetic PTY checks.
