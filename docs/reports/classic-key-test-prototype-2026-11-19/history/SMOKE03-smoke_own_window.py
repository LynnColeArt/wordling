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
    from gi.repository import Gdk, GLib, Gtk
    results = []
    state = {'step': 0, 'failed': False, 'start': time.monotonic()}

    def drive(window):
        state['window'] = window
        window.present()

        def fail(reason):
            window.escape_probe_armed = False
            state['failed'] = True
            results.append({'check': 'failure', 'reason': reason,
                            'fixed_candidate_receipts': window.escape_probe_observations[:]})
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
                elif step in (1, 3, 5, 7):
                    if not window.captured:
                        return fail('actual GDK capture did not remain successful at step ' + str(step))
                    results.append({'check': 'actual_capture_' + str(step), 'result': 'PASS'})
                    if step == 1:
                        window.release_button.clicked()  # Exact visible Release signal path.
                    elif step in (3, 5):
                        # Fixed candidate only. Avoid XSendEvent's documented XI2 limitation.
                        own = window.get_window() if step == 3 else window.terminal.get_window()
                        window.escape_probe_observations.clear()
                        window.escape_probe_armed = True
                        mods = Gdk.ModifierType.CONTROL_MASK | Gdk.ModifierType.MOD1_MASK
                        for kind in (Gdk.EventType.KEY_PRESS, Gdk.EventType.KEY_RELEASE):
                            event = Gdk.Event.new(kind)
                            event.window = own
                            event.send_event = True
                            event.time = Gdk.CURRENT_TIME
                            event.state = mods
                            event.keyval = Gdk.KEY_g
                            event.hardware_keycode = 0
                            event.group = 0
                            event.set_device(window.seat.get_keyboard())
                            Gtk.main_do_event(event)
                    else:
                        window.hide()
                elif step in (2, 4, 6, 8):
                    if window.captured:
                        return fail('capture remained ON after release path at step ' + str(step))
                    label = {2: 'visible_Release_signal', 4: 'synthetic_GTK_CtrlAltG_toplevel_target',
                             6: 'synthetic_GTK_CtrlAltG_focused_VTE_target', 8: 'hide_unmap_release'}[step]
                    check = {'check': label, 'result': 'PASS'}
                    if step in (4, 6):
                        window.escape_probe_armed = False
                        receipts = window.escape_probe_observations[:]
                        if not any(item['phase'] == 'press' and item['handler'] == 'Window' and item['control_alt'] for item in receipts):
                            return fail('fixed candidate did not establish the Window host escape receipt route')
                        check['observed_receipts'] = receipts
                    results.append(check)
                    if step == 8:
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
    completed = state['step'] == 8 and not state['failed'] and cleanup_ok
    print(json.dumps({'result': 'PASS_SYNTHETIC_SMOKE_ONLY' if completed else 'FAIL_SYNTHETIC_SMOKE',
                      'physical_key_delivery': 'NOT_TESTED', 'checks': results,
                      'synthetic_transport': 'GTK_main_do_event_only; native_X11_XI2_delivery_NOT_TESTED',
                      'elapsed_seconds': round(time.monotonic() - state['start'], 3)}, indent=2))
    return 0 if completed else 1


if __name__ == '__main__':
    raise SystemExit(run())
