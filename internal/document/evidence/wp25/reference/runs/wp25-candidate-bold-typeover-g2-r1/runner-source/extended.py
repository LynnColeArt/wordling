"""Bounded code, save, macro and merge probes against the original application."""

import time


def position(p, value):
    p.trace.append({"wait_position":value,"settle_seconds":0.35})
    p.q.wait_for('Pos '+value+'"')
    time.sleep(.35)  # Allow the final same-position code-boundary key to redraw.


def save_as(p, name):
    p.key('f10'); p.q.wait_for('Document to be saved:')
    p.type('C:\\OUT\\'+name); p.key('ret')
    p.q.wait_absent('Document to be saved:')
    p.exports.append((name, name+'.WP5'))


def top(p):
    p.key('home,home,home,up'); position(p,'1')


def center_delete(p):
    p.key('shift-f6'); p.type('ABC'); p.q.wait_for('ABC')
    p.key('alt-f3'); p.q.wait_for('[Center]'); top(p)
    p.capture('before-delete'); p.key('delete'); p.q.wait_absent('[Center]')
    s=p.capture('after-delete')
    p.check('Center code removed; text preserved', 'ABC' in s and '[Center]' not in s)
    save_as(p,'CENTER')


def center_backspace(p):
    p.key('shift-f6'); p.type('ABC'); p.q.wait_for('ABC')
    p.key('alt-f3'); p.q.wait_for('[Center]'); top(p); p.key('right'); position(p,'4.1')
    p.capture('before-backspace'); p.key('backspace'); p.q.wait_absent('[Center]')
    s=p.capture('after-backspace')
    p.check('Backspace removes preceding Center code; text preserved', 'ABC' in s and '[Center]' not in s)
    save_as(p,'BACKSP')


def paired(p, backwards=False):
    p.type('A'); p.key('f6'); p.type('B'); p.key('f6'); p.type('C')
    p.q.wait_for('ABC'); p.key('alt-f3'); p.q.wait_for('A[BOLD]B[bold]C'); top(p)
    p.key('right')
    if backwards:
        p.key('right,right,right')
    position(p,'1.2' if backwards else '1.1')
    p.capture('before-boundary-delete')
    p.key('backspace' if backwards else 'delete')
    p.q.wait_absent('[BOLD]')
    s=p.capture('after-boundary-delete')
    p.check('Both paired bold codes removed and all three characters retained',
            s.splitlines()[0]=='ABC' and '[bold]' not in s and '[BOLD]' not in s)
    save_as(p,'PAIRED')


def overwrite(p):
    p.type('ORIGINAL'); p.q.wait_for('ORIGINAL'); save_as(p,'SAME')
    # Make the comparison copy through the guest, never read/write a live image.
    p.key('ctrl-f1'); p.q.wait_for('DOS Command'); p.key('2'); p.q.wait_for('DOS Command:')
    p.type('COPY C:\\OUT\\SAME C:\\OUT\\BEFORE'); p.key('ret')
    p.q.wait_for('Press any key'); p.capture('guest-copy'); p.key('spc'); p.q.wait_for('ORIGINAL')
    p.type('MODIFIED'); p.q.wait_for('ORIGINALMODIFIED')
    p.key('f10'); p.q.wait_for('Document to be saved:'); p.key('ret')
    p.q.wait_for('Replace'); p.capture('replace-prompt'); p.key('n')
    p.q.wait_for('Document to be saved:'); p.capture('different-filename-requested')
    p.key('f1'); p.q.wait_absent('Document to be saved:')
    s=p.capture('unsaved-buffer')
    p.check('Refusal returns to filename prompt and cancellation retains changed buffer', 'ORIGINALMODIFIED' in s)
    p.exports.append(('BEFORE','BEFORE.WP5'))
    p.identical.append(('SAME.WP5','BEFORE.WP5'))


def record_macro(p):
    p.key('ctrl-f10'); p.q.wait_for('Define macro:')
    p.type('C:\\OUT\\TESTMAC'); p.key('ret'); p.q.wait_for('Description:')
    p.type('Recorded test'); p.key('ret'); p.q.wait_for('Macro Def')
    p.type('ABC'); p.q.wait_for('ABC'); p.key('ctrl-f10'); p.q.wait_absent('Macro Def')
    p.capture('recorded'); p.exports.append(('TESTMAC.WPM','TESTMAC.WPM'))


def macro(p):
    record_macro(p)
    p.key('alt-f10'); p.q.wait_for('Macro:'); p.type('C:\\OUT\\TESTMAC'); p.key('ret')
    p.q.wait_for('ABCABC'); s=p.capture('executed')
    p.check('Recorded macro inserts ABC again', s.splitlines()[0]=='ABCABC')
    save_as(p,'MACROOUT')


def macro_repeat(p):
    record_macro(p); p.key('shift-f3'); p.q.wait_for('Doc 2')
    p.key('esc'); p.type('3'); p.key('alt-f10'); p.q.wait_for('Macro:')
    p.type('C:\\OUT\\TESTMAC'); p.key('ret'); p.q.wait_for('ABCABCABC')
    s=p.capture('repeated')
    p.check('Repeat Value executes macro three times in blank Doc 2', s.splitlines()[0]=='ABCABCABC')
    save_as(p,'REPEAT')


def clear_doc1(p):
    p.key('f7'); p.q.wait_for('Save document?'); p.key('n')
    p.q.wait_for('Exit WP?'); p.key('n'); p.q.wait_absent('Exit WP?')


def merge_command(p, number):
    p.key('shift-f9'); p.q.wait_for('End Record'); p.key(str(number))


def merge(p):
    for name in ['Alice','Bob']:
        p.type(name); p.q.wait_for(name); p.key('f9'); merge_command(p,2)
    p.capture('secondary-records'); save_as(p,'SECOND'); clear_doc1(p)
    p.type('Hello '); merge_command(p,1); p.q.wait_for('Enter Field:')
    p.type('1'); p.key('ret'); p.q.wait_absent('Enter Field:'); p.key('ctrl-ret')
    p.key('alt-f3'); p.q.wait_for('{FIELD}'); p.capture('primary-codes'); p.key('alt-f3')
    save_as(p,'PRIMARY'); clear_doc1(p)
    p.key('ctrl-f9'); p.q.wait_for('Merge'); p.key('1'); p.q.wait_for('Primary file:')
    p.type('C:\\OUT\\PRIMARY'); p.key('ret'); p.q.wait_for('Secondary file:')
    p.type('C:\\OUT\\SECOND'); p.key('ret'); p.q.wait_for('Hello Alice'); p.q.wait_for('Hello Bob')
    s=p.capture('merged')
    p.check('Both records substituted in order', s.index('Hello Alice') < s.index('Hello Bob'))
    p.check('No unresolved field text in visible output', '{FIELD}' not in s)
    save_as(p,'MERGED')
    p.contains.extend([('MERGED.WP5',b'Hello Alice'),('MERGED.WP5',b'Hello Bob')])


PROBES={'CMD51-050':center_delete,'CMD51-051':center_backspace,'CMD51-067':overwrite,
        'CMD51-131':macro,'CMD51-132':macro_repeat,'CMD51-134':merge,
        'CMD51-200':paired,'CMD51-201':lambda p:paired(p,True)}


def clean_exit(p):
    # A vanished save prompt precedes disk completion on some runs. Exit through
    # WP before stopping QEMU, so every export is closed by the application.
    for _ in range(2):
        p.key('f7'); p.q.wait_for('Save document?'); p.key('n')
        state=p.q.wait_until(lambda s: 'Exit doc 2?' in s or 'Exit WP?' in s, 'document/app exit confirmation')
        p.key('y')
        if 'Exit WP?' in state:
            p.q.wait_for('C:\\WP51>'); p.capture('clean-exit')
            return
        p.q.wait_for('Doc 1')
    raise RuntimeError('Could not exit the original application cleanly')
