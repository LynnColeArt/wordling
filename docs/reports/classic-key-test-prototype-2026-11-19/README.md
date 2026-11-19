# Wordling classic keyboard test prototype

Root's deliberate `SMOKE03` passed **synthetic GTK dispatch only** with the exact current source/smoke hashes. It passed default OFF, four actual GDK captures, the visible Release signal handler, fixed Ctrl+Alt+G receipt and release, hide/unmap, child exit, and pidfd closure. Parent exit was 0 after about 1.98 seconds with no timeout; stderr contained only the existing accessibility-bus warning. Both intended top-level/VTE targets produced `event_window=toplevel` receipts: their `get_window()` values apparently share the same native GdkWindow, so these do **not** prove two independent native event paths. Physical and native X11/XI2 key delivery remain **NOT_TESTED**. Exact provenance is in `smoke03-provenance.json`.

The earlier failures remain preserved: `SMOKE01` failed before Wordling launch/capture on VTE nullable-closure binding; `SMOKE02` passed actual capture, Release handler, and cleanup but failed the old XSendEvent synthetic escape test. All three raw attempts and exact source/smoke history are retained. No further GUI has been run while recording SMOKE03 evidence. This is a normal user-visible desktop aid, independent of Mission1 private runtime actors and qualification operations.

The only child is the existing verified Linux Wordling binary at `/tmp/wordling-linux-keys-f6cea1cc-dlsi4ix9/wordling`, source `f6cea1cc`, SHA256 `4789d95f166a42f2bffa6565919143f21d272c81e0446e58fb5d762eae48ce1f`. A changed binary is refused. There are no arguments or arbitrary command factory. Each run creates a new 0700 session and empty 0700 workspace under this prototype directory, then uses:

```
wordling -root NEW_PRIVATE_EMPTY_WORKSPACE -profile macro-cout -control-keys
```

The normal child environment is inherited, with `TEA_TRACE` disabled to avoid ordinary typed-text tracing and terminal identity set to `xterm-256color`/`truecolor`. No settings, keymaps, profiles, packages, kernel parameters, or files in a checkout are changed. No root privileges are needed. The mouse is never captured. Existing GTK3/GDK X11 and VTE 2.91 are the only non-stdlib dependencies. Wayland is explicitly refused.

## Root review and deliberate launch

Read `classic_key_test.py` first. The following command launches the GUI, so it has **not** been run during preparation:

```
/usr/bin/python3 /tmp/wordling-classic-key-test-prototype/classic_key_test.py
```

The visible title is **Wordling classic keyboard test**. Capture defaults **OFF**; it never enables itself automatically. Click **Enable classic keyboard capture (60 seconds)** after Wordling is ready. It uses GDK's keyboard-only seat grab while this window is active, without taking the pointer. Native keys flow through GTK/VTE's normal terminal translation; there are no invented function-key sequences. The grab may let keys bypass desktop passive shortcuts, but actual delivery on this desktop remains unverified.

Release with **Ctrl+Alt+G**, the visible **Release keyboard** mouse button, or the close button. Capture also releases on focus-out, loss of active status, top-level pointer exit, hide/unmap, broken grab, Wordling exit, and a 60-second lease. Moving between controls and VTE inside the window is excluded from top-level pointer-exit handling. The pointer exit release is deliberately conservative: moving the mouse outside releases even before a click elsewhere. Window-manager physical behavior still needs a supervised smoke test. If it fails to release as specified, close the window using the mouse and do not continue capture testing.

The entire session automatically closes after 15 minutes. Child spawn is limited to 5 seconds. Closing releases immediately, sends SIGHUP through the owned Wordling child pidfd, and sends SIGKILL through that same descriptor after 2 seconds if necessary; the loop ends no later than 3 seconds after shutdown. The pidfd comes only from VTE's genuine successful spawn callback and closes on child exit/finally. Integer PIDs are retained only for lifecycle/UI state; they are never used for signaling. Startup probes pidfd availability without sending a signal and refuses to spawn if support is absent. An unexpected ownership failure closes the child's PTY and exits on the same bounded cleanup schedule, with no PID-signaling fallback. No other process or process group is signaled.

## Diagnostics and physical testing

`session-*/special-keys.jsonl` records only this active window's function-key names, XF86 media-key names, modifier-key identities/modifier flags, capture state, lifecycle, and child wait status. The synthetic diagnostic can explicitly arm a maximum-eight-receipt observer for its fixed host-escape candidate: synthetic g/G or Ctrl+Alt+g/G only. That observer records handler identity, modifier state, synthetic flag, focus state, and own-window identity, and is OFF during ordinary manual use. Ordinary character events, document text, PTY bytes, clipboard contents, and other-app events are not recorded. Keyboard events only run through this application's GTK event handlers. There is no global event monitor. The log and scratch workspace are retained for root to inspect; they are never reused by the next launch.

There is **no Apple/media-row translation**. If the application receives an XF86 event it records the name and leaves it to VTE. The keyboard's media-row hypothesis remains unproven. Function/media names alone do not establish hardware causality.

Before any physical-key test, root should inspect this exact code and deliberately run a single GUI smoke to check: capture OFF at start; Enable/Release with mouse; Ctrl+Alt+G release; pointer leave; focus loss; window close; child exit; and timer release. Only then test physical F5/F10/Ctrl+F1 and relevant Alt+function keys, recording the visible Wordling result independently of the own-window special-key log. Non-GUI checks and synthetic events are **not** a physical PASS.

Use optional Ctrl+S/Ctrl+Q normally with capture OFF when useful. Ctrl+C is retained for the app's existing emergency handling. The test window itself reserves only Ctrl+Alt+G as a host escape.

## Synthetic own-window smoke (root SMOKE03 passed)

After reviewing both Python files, root may deliberately launch:

```
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 /tmp/wordling-classic-key-test-prototype/smoke_own_window.py
```

This starts the same fixed child/window with manual capture still OFF by default. It checks default OFF, actual GDK capture, and the visible Release button's exact signal handler. It then constructs a fixed Ctrl+Alt+G GdkEvent pair and uses `Gtk.main_do_event` first with the top-level widget's `get_window()`, then with the focused VTE widget's `get_window()`. Both produced Window-handler press receipts with the expected modifiers and actually released capture in SMOKE03; the receipt labels show these native window targets were shared, not independent. The VTE candidate observer does not intercept or change behavior. The smoke then checks another capture, hide/close, child exit, and pidfd closure. It never targets another application, changes XI2 settings, warps the pointer, or sends document text. Its 12-second deadline plus maximum 3-second shutdown keeps the normal bound below 20 seconds. Its result is `PASS_SYNTHETIC_SMOKE_ONLY`, with physical delivery `NOT_TESTED`. This bypasses the X11/XI2 synthetic transport layer and only proves GTK dispatch and handler behavior. A synthetic button signal proves its handler path, not a physical click. Pointer/focus/timer behavior still requires supervised observation separately.

The transport change has a concrete primary-source basis: [GNOME GTK3 test initialization source](https://github.com/GNOME/gtk/blob/gtk-3-24/gtk/gtktestutils.c#L86-L91) documents that `XSendEvent` test events do not work with XI2; [the GDK X11 test helper](https://github.com/GNOME/gtk/blob/gtk-3-24/gdk/x11/gdktestutils-x11.c) uses `XSendEvent`. This is a source-supported explanation consistent with SMOKE02, not proof of this machine's exact failure cause. We do not disable multidevice/XI2 to make the old test pass. [Gtk.Widget.event documentation](https://docs.gtk.org/gtk3/method.Widget.event.html) directs synthetic events to `Gtk.main_do_event` so they behave like queued events. [Gtk.main_do_event](https://docs.gtk.org/gtk3/func.main_do_event.html) and [Gdk.Event.set_device](https://docs.gtk.org/gdk3/method.Event.set_device.html) support the narrowly scoped replacement.

The pre-pidfd source and proof are preserved under `history/`; `history/classic_key_test-before-pidfd.py` has SHA256 `4a56408194545acaf2158933556988e6d838e154d13d6781b701f954ff7677d0`. Do not launch historical copies.

The exact SMOKE01 source and its prior non-GUI proof are also preserved as `history/classic_key_test-before-smoke01-fix.py` (SHA256 `0e25533324e5b16f667d6bfdcbff66b8ae5a5d55886fdbbce550369ea3e80d6e`) and `history/non-gui-before-smoke01-fix.json`. Current code explicitly supplies `child_setup=None, child_setup_data=None` positionally, then names `timeout`, `cancellable`, `callback`, and `user_data`. An inert `self=None` binding probe confirms argument-count/name acceptance and stops at the required non-null receiver check; it creates no widget and does not establish real spawn success. Assigned window construction, UI build, child start, and loop now sit inside `try/finally` with cancellable/window/log cleanup even if startup raises.

The exact SMOKE02 source/smoke/proof are preserved as `history/*before-smoke02-diagnostic*`; prior source SHA256 is `d6433a6bc9497adb863123bc4b10812c99acbe898995bc45e46cdbbc37a23d94`, prior smoke SHA256 is `bce30c78e338b7b3d3526f163744c32bbc800b2a8e51c04134297ac7689d6541`. `history/SMOKE02-custody.json` pins all four unchanged raw/result/command files.

## Supported API basis

The installed `/usr/share/gir-1.0/Gdk-3.0.gir` and `Gtk-3.0.gir` contain the same API contracts as the official GNOME docs below. Installed VTE 0.76 introspection verified the `spawn_async` signature before implementation.

- [Gdk.Seat.grab](https://docs.gtk.org/gdk3/method.Seat.grab.html): grabs only the supplied capabilities; hidden windows end the grab; handle broken-grab events. This prototype supplies **KEYBOARD**, never pointer/touch capabilities.
- [Gdk.Seat.ungrab](https://docs.gtk.org/gdk3/method.Seat.ungrab.html): releases a seat grab.
- [Gtk.Widget focus-out-event](https://docs.gtk.org/gtk3/signal.Widget.focus-out-event.html): focus leaves the widget's window; requires focus-change event mask.
- [Gtk.Widget leave-notify-event](https://docs.gtk.org/gtk3/signal.Widget.leave-notify-event.html) and [Gdk.EventCrossing](https://docs.gtk.org/gdk3/struct.EventCrossing.html): own-window pointer crossing details support excluding descendant crossings.
- [Gtk.Widget grab-broken-event](https://docs.gtk.org/gtk3/signal.Widget.grab-broken-event.html): keyboard/pointer grab loss notification, including an unviewable X11 window.
- [Vte.Terminal.spawn_async](https://gnome.pages.gitlab.gnome.org/vte/gtk3/method.Terminal.spawn_async.html): fixed child vector, cwd, environment additions, cancellable, and bounded timeout.
- [Python os.pidfd_open](https://docs.python.org/3/library/os.html#os.pidfd_open) and [signal.pidfd_send_signal](https://docs.python.org/3/library/signal.html#signal.pidfd_send_signal): descriptor-based child identity and signaling. Installed stdlib docstrings confirm the race-avoiding process descriptor semantics; non-GUI verification opens/closes a descriptor for this verifier itself without sending any signal.

These documented release mechanisms and SMOKE03 synthetic results do not substitute for supervised physical testing. Physical mouse-release behavior, physical Ctrl+Alt+G, native X11/XI2 function-key delivery, pointer/focus behavior, and timer release remain pending.

## Non-GUI verification and cleanup

Safe verification (creates no window, launches no Wordling child, and grabs no input; it imports VTE/GI metadata and performs an inert None-receiver binding check):

```
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 /tmp/wordling-classic-key-test-prototype/verify_no_gui.py
```

When root finishes testing, remove this owned directory and its scratch sessions. It is entirely under `/tmp`; no checkout/worktree was created or changed by this task.
