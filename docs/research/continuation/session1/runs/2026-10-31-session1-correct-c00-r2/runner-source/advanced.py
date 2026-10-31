"""Original-app probes for paired-code blocks, restoration, automation and pages."""
import time
from extended import save_as, top, position, clear_doc1, merge_command


def bold_fixture(p):
    p.type('A');p.key('f6');p.type('BC');p.key('f6');p.type('D')
    p.q.wait_for('ABCD');p.key('alt-f3');p.q.wait_for('A[BOLD]BC[bold]D')
    save_as(p,'ORIGIN');top(p)


def select_block(p, rights, end_position):
    p.key('alt-f4');p.q.wait_for('Block')
    p.key(','.join(['right']*rights));position(p,end_position)
    p.capture('selected-block');p.key('backspace');p.q.wait_for('Delete Block?')
    p.capture('delete-confirmation');p.key('y');p.q.wait_absent('Delete Block?')


def block_half(p, closing=False):
    bold_fixture(p);p.key(','.join(['right']*(4 if closing else 1)))
    position(p,'1.3' if closing else '1.1')
    select_block(p,1,'1.3' if closing else '1.1')
    p.q.wait_for('A[BOLD]BC[bold]D');s=p.capture('pair-repaired')
    p.check('Deleting only one blocked boundary retains text and paired bold span',
            s.splitlines()[0]=='ABCD' and 'A[BOLD]BC[bold]D' in s and '[Block]' not in s)
    save_as(p,'REPAIRED');p.same_body.append(('ORIGIN.WP5','REPAIRED.WP5'))


def undelete_block(p):
    bold_fixture(p);p.key('right');position(p,'1.1');select_block(p,4,'1.3')
    p.q.wait_until(lambda s:s.splitlines()[0]=='AD','attributed span removed')
    s=p.capture('deleted');p.check('Both codes and BC removed by block deletion','[BOLD]' not in s and '[bold]' not in s)
    save_as(p,'DELETED');p.key('f1');p.q.wait_for('Undelete:');p.capture('restore-preview')
    p.key('1');p.q.wait_absent('Undelete:');p.q.wait_for('A[BOLD]BC[bold]D')
    s=p.capture('restored');p.check('Block Undelete restores text and both bold codes','A[BOLD]BC[bold]D' in s)
    save_as(p,'RESTORED');p.same_body.append(('ORIGIN.WP5','RESTORED.WP5'))


def undelete_char(p):
    bold_fixture(p);p.key('right');position(p,'1.1')
    p.key('delete');p.q.wait_absent('[BOLD]');p.key('delete,delete')
    p.q.wait_until(lambda s:s.splitlines()[0]=='AD','BC removed by character deletion')
    p.capture('deleted');save_as(p,'DELETED');p.key('f1');p.q.wait_for('Undelete:')
    p.capture('restore-preview');p.key('1');p.q.wait_absent('Undelete:');p.q.wait_for('ABCD')
    s=p.capture('restored-without-attributes')
    p.check('Character Undelete restores BC without the deleted paired bold codes',
            s.splitlines()[0]=='ABCD' and '[BOLD]' not in s and '[bold]' not in s)
    save_as(p,'RESTORED')


def macro_start(p,name):
    p.key('home,ctrl-f10');p.q.wait_for('Define macro:');p.type('C:\\OUT\\'+name)
    p.key('ret');p.q.wait_for('Description:');p.type('Wordling reference');p.key('ret')
    p.q.wait_for('Ctrl-PgUp for macro commands');p.key('end');time.sleep(.35)


def macro_command(p,name):
    p.key('ctrl-pgup');p.q.wait_for('Name Search; Arrows; Enter to Select')
    p.type(name);p.q.wait_for('{'+name+'}');p.key('ret')
    p.q.wait_absent('Name Search; Arrows; Enter to Select')


def macro_key(p,key):
    p.key('ctrl-v');p.q.wait_for('Press Command Key:');p.key(key);p.q.wait_absent('Press Command Key:')


def macro_finish(p,name):
    tail='TAIL' if name=='FLOW' else ('SHOULDNOT' if name=='FAILSRCH' else 'HANDLED')
    p.q.wait_for(tail)
    p.key('home,home,home,up');p.q.wait_for('{DISPLAY OFF}');p.capture('macro-source-head')
    p.key('end');p.q.wait_for(tail);p.capture('macro-source-tail')
    p.key('f7');p.q.wait_for('Doc 1')
    p.exports.append((name+'.WPM',name+'.WPM'))
    p.key('alt-f10');p.q.wait_for('Macro:');p.type('C:\\OUT\\'+name);p.key('ret')


def macro_flow(p):
    macro_start(p,'FLOW')
    for command,text in [('IF','1~TRUE'),('ELSE','BAD'),('END IF',''),
                         ('IF','0~BAD'),('ELSE','FALSE'),('END IF',''),
                         ('GO','DONE~SKIP'),('LABEL','DONE~TAIL')]:
        macro_command(p,command);p.type(text)
    macro_finish(p,'FLOW');p.q.wait_for('TRUEFALSETAIL');s=p.capture('branches-and-jump')
    p.check('True and false IF branches and GO/LABEL skip unwanted text',s.splitlines()[0]=='TRUEFALSETAIL')
    save_as(p,'FLOWOUT');p.contains.append(('FLOWOUT.WP5',b'TRUEFALSETAIL'))


def macro_search(p,handled=False):
    name='HANDLER' if handled else 'FAILSRCH';macro_start(p,name)
    if handled:
        macro_command(p,'ON NOT FOUND');macro_command(p,'GO');p.type('MISS~~')
    p.type('BEFORE');macro_key(p,'f2');p.type('ABSENT');macro_key(p,'f2');p.type('SHOULDNOT')
    if handled:
        macro_command(p,'QUIT');macro_command(p,'LABEL');p.type('MISS~HANDLED')
    macro_finish(p,name)
    if handled:
        p.q.wait_for('BEFOREHANDLED');s=p.capture('handled-not-found')
        p.check('ON NOT FOUND redirects to handler and skips sentinel',s.splitlines()[0]=='BEFOREHANDLED')
    else:
        p.q.wait_until(lambda s:s.splitlines()[0]=='BEFORE' and 'Doc 1' in s,
                       'default failed-search return to document')
        time.sleep(.35)
        s=p.capture('default-search-stopped')
        p.check('Default failed search stops before sentinel',s.splitlines()[0]=='BEFORE' and 'SHOULDNOT' not in s)
        p.type('READY');p.q.wait_for('BEFOREREADY');s=p.capture('interactive-recovery')
        p.check('Editing resumes after failed macro; sentinel remains absent',s.splitlines()[0]=='BEFOREREADY')
    save_as(p,'ERROROUT')


def macro_error(p):
    macro_start(p,'ONERROR');macro_command(p,'ON ERROR');macro_command(p,'GO');p.type('ERR~~')
    macro_command(p,'NEST');p.type('C:\\OUT\\MISSING~SHOULDNOT')
    macro_command(p,'QUIT');macro_command(p,'LABEL');p.type('ERR~HANDLED')
    macro_finish(p,'ONERROR');p.q.wait_for('HANDLED');s=p.capture('handled-missing-file')
    p.check('ON ERROR handles missing nested macro and bypasses sentinel',s.splitlines()[0]=='HANDLED')
    save_as(p,'ERROROUT')


def secondary(p,conditional=False):
    for name,value in [('Alice','YES'),('Bob','')]:
        p.type(name);p.q.wait_for(name);p.key('f9')
        if conditional:
            p.type(value);p.key('f9')
        merge_command(p,2)
    p.capture('secondary-records');save_as(p,'SECOND');clear_doc1(p)


def field(p,number):
    merge_command(p,1);p.q.wait_for('Enter Field:');p.type(str(number));p.key('ret');p.q.wait_absent('Enter Field:')


def merge_named(p,name):
    merge_command(p,6);p.q.wait_for('Name Search')
    p.type(name);p.q.wait_for('{'+name+'}');p.key('ret');p.q.wait_absent('Name Search')


def perform_merge(p):
    p.key('alt-f3');p.q.wait_for('Reveal Codes to restore');p.q.wait_for('{FIELD}');p.capture('primary-codes');p.key('alt-f3')
    save_as(p,'PRIMARY');clear_doc1(p)
    p.key('ctrl-f9');p.q.wait_for('Merge');p.key('1');p.q.wait_for('Primary file:')
    p.type('C:\\OUT\\PRIMARY');p.key('ret');p.q.wait_for('Secondary file:')
    p.type('C:\\OUT\\SECOND');p.key('ret')


def merge_pages(p,page_off=False):
    secondary(p)
    if page_off:merge_command(p,4)
    p.type('Hello ');field(p,1);p.key('ret')
    perform_merge(p);p.q.wait_for('Hello Alice');p.q.wait_for('Hello Bob')
    pages=1 if page_off else 2
    p.q.wait_until(lambda s:'Doc 1 Pg '+str(pages)+' ' in s and 'Repositioning' not in s,
                   'merge completed on page '+str(pages))
    s=p.capture('merged-last-page')
    p.check('Original merge ends on expected page '+str(pages),'Pg '+str(pages)+' ' in s)
    p.check('Both native records substituted in order',s.index('Hello Alice')<s.index('Hello Bob'))
    p.key('alt-f3');p.q.wait_for('Reveal Codes to restore');p.capture('merged-codes')
    save_as(p,'MERGED');p.page_expectations.append(('MERGED.WP5',0 if page_off else 1))
    p.contains.extend([('MERGED.WP5',b'Hello Alice'),('MERGED.WP5',b'Hello Bob')])


def merge_conditional(p):
    secondary(p,True);merge_named(p,'IF BLANK');p.q.wait_for('Enter Field:')
    p.type('2');p.key('ret');p.q.wait_absent('Enter Field:');p.type('EMPTY')
    merge_named(p,'ELSE');p.type('FILLED');merge_named(p,'END IF');p.type(' ');field(p,1)
    perform_merge(p);p.q.wait_for('FILLED Alice');p.q.wait_for('EMPTY Bob')
    s=p.capture('conditional-records')
    p.check('IF BLANK/ELSE selects both branches from original secondary fields',
            s.index('FILLED Alice')<s.index('EMPTY Bob') and 'EMPTY Alice' not in s and 'FILLED Bob' not in s)
    save_as(p,'MERGED');p.page_expectations.append(('MERGED.WP5',1))
    p.contains.extend([('MERGED.WP5',b'FILLED Alice'),('MERGED.WP5',b'EMPTY Bob')])


PROBES={'CMD51-202':block_half,'CMD51-203':lambda p:block_half(p,True),
        'CMD51-204':undelete_block,'CMD51-045':undelete_char,'CMD51-205':macro_flow,
        'CMD51-178':macro_search,'CMD51-206':lambda p:macro_search(p,True),
        'CMD51-210':macro_error,'CMD51-207':merge_pages,
        'CMD51-208':lambda p:merge_pages(p,True),'CMD51-209':merge_conditional}
