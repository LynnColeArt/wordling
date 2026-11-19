#!/usr/bin/python3
"""Fixed-binary, private-workspace Wordling keyboard test; capture starts OFF."""
import hashlib
import json
import os
from pathlib import Path
import signal
import sys
import tempfile
import time

BINARY = Path('/tmp/wordling-linux-keys-f6cea1cc-dlsi4ix9/wordling')
BINARY_SHA256 = '4789d95f166a42f2bffa6565919143f21d272c81e0446e58fb5d762eae48ce1f'
SOURCE_COMMIT = 'f6cea1cc'
BASE = Path(__file__).resolve().parent
CAPTURE_SECONDS = 60
SESSION_SECONDS = 15 * 60
SPAWN_TIMEOUT_MS = 5000


def verify_binary():
    if BINARY.is_symlink() or not BINARY.is_file() or not os.access(BINARY, os.X_OK):
        raise RuntimeError('Fixed Wordling executable is missing or not a regular executable')
    actual = hashlib.sha256(BINARY.read_bytes()).hexdigest()
    if actual != BINARY_SHA256:
        raise RuntimeError('Fixed Wordling executable SHA256 does not match reviewed binary')
    return actual


def argv_for(workspace):
    return [str(BINARY), '-root', str(workspace), '-profile', 'macro-cout', '-control-keys']


def main():
    if len(sys.argv) != 1:
        raise RuntimeError('This launcher takes no arguments; it cannot run arbitrary commands')
    if BASE != Path('/tmp/wordling-classic-key-test-prototype'):
        raise RuntimeError('This review prototype must remain in its owned /tmp directory')
    verify_binary()
    # Imports do not create a window. No init, process spawn, or grab occurs on import.
    import gi
    gi.require_version('Gtk', '3.0')
    gi.require_version('Gdk', '3.0')
    gi.require_version('GdkX11', '3.0')
    gi.require_version('Vte', '2.91')
    from gi.repository import Gdk, GdkX11, Gio, GLib, Gtk, Vte

    if not Gtk.init_check()[0]:
        raise RuntimeError('No GTK display available')
    display = Gdk.Display.get_default()
    if not isinstance(display, GdkX11.X11Display):
        raise RuntimeError('This prototype only supports an X11 session; no Wayland grab attempted')
    session = Path(tempfile.mkdtemp(prefix='session-', dir=BASE))
    workspace = session / 'workspace'
    workspace.mkdir(mode=0o700)
    log = (session / 'special-keys.jsonl').open('x', encoding='utf-8')
    os.chmod(log.name, 0o600)

    class TestWindow(Gtk.Window):
        def __init__(self):
            super().__init__(title='Wordling classic keyboard test — capture OFF')
            self.set_default_size(1050, 760)
            self.pid = None
            self.child_finished = False
            self.spawning = True
            self.closing = False
            self.captured = False
            self.capture_timer = None
            self.cancellable = Gio.Cancellable()
            self.seat = display.get_default_seat()
            self.add_events(Gdk.EventMask.FOCUS_CHANGE_MASK | Gdk.EventMask.LEAVE_NOTIFY_MASK |
                            Gdk.EventMask.KEY_PRESS_MASK | Gdk.EventMask.KEY_RELEASE_MASK)
            box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
            box.set_border_width(8)
            self.add(box)
            notice = Gtk.Label(label='Private scratch Wordling • Capture starts OFF • Ctrl+Alt+G releases capture')
            box.pack_start(notice, False, False, 0)
            controls = Gtk.Box(spacing=10)
            box.pack_start(controls, False, False, 0)
            self.enable = Gtk.Button(label='Enable classic keyboard capture (60 seconds)')
            self.enable.set_can_focus(False)
            self.enable.set_sensitive(False)
            self.enable.connect('clicked', self.capture)
            controls.pack_start(self.enable, False, False, 0)
            self.release_button = Gtk.Button(label='Release keyboard')
            self.release_button.set_can_focus(False)
            self.release_button.connect('clicked', lambda *_: self.release('mouse Release'))
            controls.pack_start(self.release_button, False, False, 0)
            close = Gtk.Button(label='Close test')
            close.set_can_focus(False)
            close.connect('clicked', lambda *_: self.shutdown('mouse Close'))
            controls.pack_start(close, False, False, 0)
            self.status = Gtk.Label(label='Starting reviewed Wordling binary; capture OFF')
            self.status.set_xalign(0)
            box.pack_start(self.status, False, False, 0)
            self.terminal = Vte.Terminal()
            self.terminal.set_scrollback_lines(300)
            self.terminal.set_audible_bell(False)
            self.terminal.set_size(100, 30)
            box.pack_start(self.terminal, True, True, 0)
            foot = Gtk.Label(label='Capture also releases on focus loss, pointer leaving this window, hide, child exit, or after 60 seconds.\n'
                                  'No media-key remapping. Test closes after 15 minutes. Scratch data stays in: ' + str(session))
            foot.set_xalign(0)
            foot.set_selectable(True)
            box.pack_start(foot, False, False, 0)
            self.connect('focus-out-event', self.focus_out)
            self.connect('notify::is-active', self.active_changed)
            self.connect('leave-notify-event', self.pointer_left)
            self.connect('grab-broken-event', lambda *_: self.release('grab broken'))
            self.connect('unmap', lambda *_: self.release('window hidden'))
            self.connect('delete-event', self.delete_event)
            self.connect('key-press-event', self.key_event, 'press')
            self.connect('key-release-event', self.key_event, 'release')
            self.terminal.connect('child-exited', self.child_exited)
            self.show_all()
            self.terminal.grab_focus()
            self.record('session', binary_sha256=BINARY_SHA256, source_commit=SOURCE_COMMIT,
                        workspace=str(workspace), capture_default='off')
            # Keep the normal environment, except opt out of inherited raw key tracing.
            envv = ['TEA_TRACE=', 'TERM=xterm-256color', 'COLORTERM=truecolor']
            self.terminal.spawn_async(Vte.PtyFlags.DEFAULT, str(workspace), argv_for(workspace),
                                      envv, GLib.SpawnFlags.DEFAULT, None, SPAWN_TIMEOUT_MS,
                                      self.cancellable, self.spawned, None)
            GLib.timeout_add_seconds(SESSION_SECONDS, self.session_expired)

        def record(self, event, **fields):
            log.write(json.dumps(dict(event=event, elapsed_seconds=round(time.monotonic() - started, 3), **fields)) + '\n')
            log.flush()

        def capture(self, *_):
            if self.closing or self.pid is None or not self.is_active() or not self.get_mapped():
                self.release('capture refused: window not active or child not running')
                return
            self.terminal.grab_focus()
            result = self.seat.grab(self.get_window(), Gdk.SeatCapabilities.KEYBOARD,
                                    True, None, Gtk.get_current_event(), None, None)
            if result != Gdk.GrabStatus.SUCCESS:
                self.status.set_text('Capture OFF — keyboard grab refused: ' + result.value_nick)
                self.record('capture-refused', status=result.value_nick)
                return
            self.captured = True
            self.enable.set_sensitive(False)
            self.set_title('Wordling classic keyboard test — CAPTURE ON — Ctrl+Alt+G releases')
            self.status.set_text('CAPTURE ON (60-second lease) — Release button or Ctrl+Alt+G returns keyboard to desktop')
            self.record('capture-on')
            self.capture_timer = GLib.timeout_add_seconds(CAPTURE_SECONDS, self.capture_expired)

        def release(self, reason):
            was_captured = self.captured
            self.captured = False
            # Call ungrab on every release path, including broken-grab notifications.
            self.seat.ungrab()
            if self.capture_timer is not None:
                GLib.source_remove(self.capture_timer)
                self.capture_timer = None
            self.enable.set_sensitive(self.pid is not None and not self.closing)
            self.set_title('Wordling classic keyboard test — capture OFF')
            self.status.set_text('Capture OFF — ' + reason)
            if was_captured:
                self.record('capture-off', reason=reason)
            return False

        def capture_expired(self):
            self.capture_timer = None
            return self.release('60-second lease expired')

        def focus_out(self, *_):
            return self.release('window lost keyboard focus')

        def active_changed(self, *_):
            if not self.is_active():
                self.release('window no longer active')

        def pointer_left(self, _widget, event):
            # Ignore crossings from the top-level to its own child widgets.
            if event.window == self.get_window() and event.detail != Gdk.NotifyType.INFERIOR:
                self.release('pointer left test window')
            return False

        def key_event(self, _widget, event, phase):
            if not self.is_active():
                if self.captured:
                    self.release('key refused while test window inactive')
                    return True
                return False
            control_alt = Gdk.ModifierType.CONTROL_MASK | Gdk.ModifierType.MOD1_MASK
            if event.state & control_alt == control_alt and event.keyval in (Gdk.KEY_g, Gdk.KEY_G):
                if phase == 'press':
                    self.release('Ctrl+Alt+G host escape')
                return True
            name = Gdk.keyval_name(event.keyval) or ''
            function = name.startswith('F') and name[1:].isdigit() and 1 <= int(name[1:]) <= 35
            modifier = name in {'Shift_L', 'Shift_R', 'Control_L', 'Control_R', 'Alt_L', 'Alt_R',
                                'Meta_L', 'Meta_R', 'Super_L', 'Super_R', 'ISO_Level3_Shift', 'Caps_Lock'}
            if function or modifier or name.startswith('XF86'):
                mods = [label for mask, label in ((Gdk.ModifierType.SHIFT_MASK, 'Shift'),
                        (Gdk.ModifierType.CONTROL_MASK, 'Control'), (Gdk.ModifierType.MOD1_MASK, 'Alt'),
                        (Gdk.ModifierType.SUPER_MASK, 'Super')) if event.state & mask]
                self.record('special-key', phase=phase, key=name, modifiers=mods, capture=self.captured)
            # GTK/VTE translates all normal keys. No synthetic sequences or media remap.
            return False

        def spawned(self, _terminal, pid, error, _data=None):
            self.spawning = False
            if error is not None:
                self.record('spawn-failed', error=str(error))
                self.release('Wordling launch failed: ' + str(error))
                if self.closing:
                    Gtk.main_quit()
                return
            # Do not revive a stale child identity if an immediate exit was delivered first.
            if self.child_finished:
                return
            self.pid = pid
            self.record('child-start', pid=pid)
            if self.closing:
                self.stop_child(signal.SIGHUP)
            else:
                self.enable.set_sensitive(True)
                self.status.set_text('Capture OFF — Wordling ready; use mouse Enable to test desktop-conflicting keys')

        def child_exited(self, _terminal, status):
            self.pid = None
            self.child_finished = True
            self.spawning = False
            self.release('Wordling exited; close this test window')
            self.record('child-exit', wait_status=status)
            if self.closing:
                Gtk.main_quit()

        def stop_child(self, sig):
            if self.pid is not None:
                try:
                    os.kill(self.pid, sig)
                except ProcessLookupError:
                    pass

        def delete_event(self, *_):
            self.shutdown('window Close')
            return True

        def session_expired(self):
            self.shutdown('15-minute session limit')
            return False

        def shutdown(self, reason):
            if self.closing:
                return
            self.closing = True
            self.release(reason)
            self.record('shutdown', reason=reason)
            self.hide()
            self.cancellable.cancel()
            self.stop_child(signal.SIGHUP)
            GLib.timeout_add(2000, self.force_stop)
            if self.pid is None and not self.spawning:
                Gtk.main_quit()

        def force_stop(self):
            self.stop_child(signal.SIGKILL)
            GLib.timeout_add(1000, Gtk.main_quit)
            return False

    started = time.monotonic()
    window = TestWindow()
    for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP):
        GLib.unix_signal_add(GLib.PRIORITY_DEFAULT, sig, lambda s=sig: (window.shutdown('host signal ' + str(s)), False)[1])
    try:
        Gtk.main()
    finally:
        window.release('main loop ended')
        window.stop_child(signal.SIGKILL)
        window.destroy()
        log.close()
    print('Private scratch and special-key-only diagnostics:', session)


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print('Classic keyboard test:', exc, file=sys.stderr)
        sys.exit(1)
