#!/usr/bin/python3
"""Small non-GUI checks. Importing the target does not import GI or run main."""
import ast
import hashlib
import importlib.util
import json
from pathlib import Path
import stat
import tempfile

base = Path(__file__).resolve().parent
target = base / 'classic_key_test.py'
source = target.read_text()
compile(source, str(target), 'exec')
smoke = base / 'smoke_own_window.py'
compile(smoke.read_text(), str(smoke), 'exec')
tree = ast.parse(source)
spec = importlib.util.spec_from_file_location('classic_key_test', target)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
assert module.BASE == base
assert base.parent == Path('/tmp')
assert stat.S_IMODE(base.stat().st_mode) == 0o700
actual = module.verify_binary()
module.verify_pidfd_support()
assert module.CAPTURE_SECONDS == 60
assert module.SESSION_SECONDS == 900
assert module.SPAWN_TIMEOUT_MS == 5000
with tempfile.TemporaryDirectory(prefix='verify-', dir=base) as temp:
    root = Path(temp) / 'workspace'
    root.mkdir(mode=0o700)
    assert not list(root.iterdir())
    assert stat.S_IMODE(root.stat().st_mode) == 0o700
    assert module.argv_for(root) == [str(module.BINARY), '-root', str(root), '-profile', 'macro-cout', '-control-keys']
grab_calls = [node for node in ast.walk(tree) if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == 'grab']
assert len(grab_calls) == 1
assert ast.unparse(grab_calls[0].args[1]) == 'Gdk.SeatCapabilities.KEYBOARD'
assert 'self.captured = False' in source
assert "self.connect('focus-out-event'" in source
assert "self.connect('leave-notify-event'" in source
assert "self.connect('grab-broken-event'" in source
assert "self.connect('unmap'" in source
assert "name.startswith('XF86')" in source
assert "'TEA_TRACE='" in source
assert 'subprocess' not in source
assert 'os.kill(' not in source
assert 'signal.pidfd_send_signal(self.pidfd' in source
assert 'feed_child(' not in source
spawn_calls = [node for node in ast.walk(tree) if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == 'spawn_async']
assert len(spawn_calls) == 1
assert len(spawn_calls[0].args) == 7
assert all(isinstance(arg, ast.Constant) and arg.value is None for arg in spawn_calls[0].args[-2:])
assert [kw.arg for kw in spawn_calls[0].keywords] == ['timeout', 'cancellable', 'callback', 'user_data']
# No Gtk.init, Terminal constructor, display access, GUI, or genuine child spawn.
import gi
gi.require_version('Vte', '2.91')
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk, Gio, GLib, Vte
candidate = Gdk.Event.new(Gdk.EventType.KEY_PRESS)
candidate.send_event = True
candidate.time = Gdk.CURRENT_TIME
candidate.state = Gdk.ModifierType.CONTROL_MASK | Gdk.ModifierType.MOD1_MASK
candidate.keyval = Gdk.KEY_g
candidate.hardware_keycode = 0
candidate.group = 0
assert candidate.keyval == Gdk.KEY_g and int(candidate.state) == 12
assert 'Gdk.test_simulate_key' not in smoke.read_text()
assert 'Gtk.main_do_event(event)' in smoke.read_text()
assert 'self.escape_probe_armed = False' in source
raw_binding = [arg.get_name() for arg in Vte.Terminal.spawn_async.get_arguments()]
assert raw_binding[5:9] == ['child_setup', 'child_setup_data', 'child_setup_data_destroy', 'timeout']
try:
    Vte.Terminal.spawn_async(None, Vte.PtyFlags.DEFAULT, '/tmp', ['/definitely/not/run'], [],
                            GLib.SpawnFlags.DEFAULT, None, None, timeout=5000,
                            cancellable=Gio.Cancellable(), callback=None, user_data=None)
except TypeError as exc:
    inert_result = str(exc)
    assert inert_result == 'Argument 0 does not allow None as a value', inert_result
else:
    raise AssertionError('Inert None-self binding probe unexpectedly returned')
custody = json.loads((base / 'history/SMOKE01-custody.json').read_text())
assert all(hashlib.sha256((base / 'SMOKE01' / name).read_bytes()).hexdigest() == digest for name, digest in custody.items())
custody02 = json.loads((base / 'history/SMOKE02-custody.json').read_text())
assert all(hashlib.sha256((base / 'SMOKE02' / name).read_bytes()).hexdigest() == digest for name, digest in custody02.items())
report = dict(result='PASS_NON_GUI_ONLY', gui_started=False, child_started=False,
              keyboard_grab_activated=False, physical_key_delivery='NOT_TESTED',
              binary_sha256=actual, prototype_sha256=hashlib.sha256(target.read_bytes()).hexdigest(),
              unrun_smoke_sha256=hashlib.sha256(smoke.read_bytes()).hexdigest(),
              raw_vte_binding_arguments=raw_binding,
              inert_none_self_binding_result=inert_result,
              smoke01_preserved=True,
              smoke02_preserved=True,
              synthetic_candidate_fields_checked_without_dispatch=True,
              checks=['Python syntax', 'import without GTK', 'fixed binary SHA256', 'fixed argv',
                      'private empty workspace', 'bounded constants', 'keyboard-only grab', 'release hooks',
                      'owned pidfd available; no integer-PID signaling',
                      'explicit nullable child_setup_data and named VTE tail binding', 'SMOKE01 and SMOKE02 custody unchanged',
                      'fixed synthetic candidate GDK fields only; dispatch NOT_RUN'])
print(json.dumps(report, indent=2))
