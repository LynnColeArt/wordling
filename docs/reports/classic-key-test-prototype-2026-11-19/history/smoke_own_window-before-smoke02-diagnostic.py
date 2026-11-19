#!/usr/bin/python3
"""DELIBERATE GUI launch. Synthetic own-window checks; never physical-key proof."""
import json
import time
import classic_key_test as prototype

# Importing this module alone does not launch a window; running it does.
def run():
    import gi
    gi.require_version('Gtk', '3.0')
    gi.require_version('Gdk', '3.0')
    from gi.repository import Gdk, GLib
    results = []
    state = {'step': 0, 'failed': False, 'start': time.monotonic()}

    def drive(window):
        state['window'] = window
        window.present()

        def fail(reason):
            state['failed'] = True
            results.append({'check': 'failure', 'reason': reason})
            window.shutdown('synthetic own-window smoke failed')
            return False

        def tick():
            try:
                if time.monotonic() - state['start'] >= 12:
                    return fail('12-second smoke deadline')
                step = state['step']
                if step == 0:
                    if window.pidfd is None or not window.is_active():
                        return True
                    if window.captured:
                        return fail('capture did not start OFF')
                    results.append({'check': 'default_OFF', 'result': 'PASS'})
                    window.enable.clicked()  # Synthetic activation of the visible Enable button.
                elif step in (1, 3, 5):
                    if not window.captured:
                        return fail('actual GDK capture did not remain successful at step ' + str(step))
                    results.append({'check': 'actual_capture_' + str(step), 'result': 'PASS'})
                    if step == 1:
                        window.release_button.clicked()  # Exact visible Release signal path.
                    elif step == 3:
                        own = window.get_window()
                        mods = Gdk.ModifierType.CONTROL_MASK | Gdk.ModifierType.MOD1_MASK
                        press = Gdk.test_simulate_key(own, 5, 5, Gdk.KEY_g, mods, Gdk.EventType.KEY_PRESS)
                        release = Gdk.test_simulate_key(own, 5, 5, Gdk.KEY_g, mods, Gdk.EventType.KEY_RELEASE)
                        if not press or not release:
                            return fail('GDK refused synthetic Ctrl+Alt+G to this exact test window')
                    else:
                        window.hide()
                elif step in (2, 4, 6):
                    if window.captured:
                        return fail('capture remained ON after release path at step ' + str(step))
                    label = {2: 'visible_Release_signal', 4: 'synthetic_CtrlAltG_event_route', 6: 'hide_unmap_release'}[step]
                    results.append({'check': label, 'result': 'PASS'})
                    if step == 6:
                        window.shutdown('synthetic own-window smoke complete')
                        return False
                    window.enable.clicked()
                state['step'] += 1
                return True
            except Exception as exc:
                return fail(type(exc).__name__ + ': ' + str(exc))

        GLib.timeout_add(200, tick)
        return False

    try:
        prototype.main(smoke_driver=drive)
    except Exception as exc:
        state['failed'] = True
        results.append({'check': 'launch_or_cleanup', 'reason': type(exc).__name__ + ': ' + str(exc)})
    window = state.get('window')
    cleanup_ok = window is not None and not window.captured and window.pidfd is None and window.child_finished
    results.append({'check': 'close_cleanup_child_exited_and_pidfd_closed', 'result': 'PASS' if cleanup_ok else 'FAIL'})
    completed = state['step'] == 6 and not state['failed'] and cleanup_ok
    print(json.dumps({'result': 'PASS_SYNTHETIC_SMOKE_ONLY' if completed else 'FAIL_SYNTHETIC_SMOKE',
                      'physical_key_delivery': 'NOT_TESTED', 'checks': results,
                      'elapsed_seconds': round(time.monotonic() - state['start'], 3)}, indent=2))
    return 0 if completed else 1


if __name__ == '__main__':
    raise SystemExit(run())
