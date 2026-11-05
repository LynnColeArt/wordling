"""Original FOR EACH values, nested NEXT, file BREAK and secondary-page probes."""
from advanced import macro_start, merge_named, merge_command, field, perform_merge, secondary
from extended import save_as, clear_doc1
from history_loops import emit, finish, output
from iteration_nesting import condition, page_control


def each_strings(p):
    macro_start(p,'STRLIST')
    emit(p,[('FOR EACH','V~"red"~"blue sky"~"red"~~'),('VARIABLE','V~/'),('END FOR','RAW:'),
            ('FOR EACH','V~red~blue sky~red~~'),('VARIABLE','V~/'),('END FOR','DONE')])
    finish(p,'STRLIST','DONE',True);output(p,'"red"/"blue sky"/"red"/RAW:red/blue sky/red/DONE')


def each_expressions(p):
    macro_start(p,'EXPRLIST')
    emit(p,[('ASSIGN','B~4~'),('FOR EACH','V~1+2~'),('VARIABLE','B~+4~'),
            ('VARIABLE','B~+1~~'),('VARIABLE','V~/'),('END FOR','DONE')])
    finish(p,'EXPRLIST','DONE',True);output(p,'3/8/5/DONE')


def nested_next(p):
    macro_start(p,'NESTNEXT');emit(p,[('FOR','I~1~2~1~'),('FOR','J~1~3~1~')])
    condition(p,'J',2)
    emit(p,[('NEXT',''),('END IF',''),('VARIABLE','I~'),('VARIABLE','J~/'),
            ('END FOR','R'),('END FOR','DONE')])
    finish(p,'NESTNEXT','DONE',True);output(p,'11/13/R21/23/RDONE')


def macro_break(p,nested=False):
    if nested:
        macro_start(p,'CHILD');emit(p,[(None,'C'),('BREAK','CHILDBAD')])
        finish(p,'CHILD','CHILDBAD')
        macro_start(p,'PARENT');emit(p,[(None,'P'),('NEST','C:\\OUT\\CHILD~RDONE')])
        finish(p,'PARENT','RDONE',True);output(p,'PCCHILDBADRDONE')
    else:
        macro_start(p,'TOPBREAK');emit(p,[(None,'A'),('BREAK','BDONE')])
        finish(p,'TOPBREAK','DONE',True);output(p,'ABDONE')


def record(p,name):
    p.type(name);p.key('f9');merge_command(p,2)


def codes_save(p,name,label):
    p.key('alt-f3');p.q.wait_for('Reveal Codes to restore');p.capture(label);p.key('alt-f3')
    save_as(p,name);clear_doc1(p)


def merge_break(p,in_secondary=False):
    if in_secondary:
        record(p,'Alice');merge_named(p,'BREAK');record(p,'Bob')
        codes_save(p,'SECOND','secondary-break-codes')
        p.type('Hello ');field(p,1);p.key('ret')
    else:
        secondary(p);p.type('P');field(p,1);p.key('ret');merge_named(p,'BREAK');p.type('BAD')
    perform_merge(p)
    if in_secondary:
        p.q.wait_for('Hello Alice');s=p.capture('secondary-break-result')
        p.check('Secondary BREAK stops before Bob','Hello Alice' in s and 'Bob' not in s)
        p.check('Secondary BREAK leaves a partial second copy on page 2','Doc 1 Pg 2 ' in s and 'Hello\n' in s)
    else:
        p.q.wait_for('PAlice');p.q.wait_for('PBob')
        p.q.wait_for('Doc 1 Pg 2 ');s=p.capture('primary-break-result')
        p.check('Primary BREAK continues with next record',s.index('PAlice')<s.index('PBob'))
        p.check('Primary BREAK skips remainder','BAD' not in s)
    p.key('alt-f3');p.q.wait_for('Reveal Codes to restore');p.capture('merged-codes')
    save_as(p,'MERGED')
    p.page_expectations.append(('MERGED.WP5',1))


def nest_secondary_command(p):
    merge_named(p,'NEST SECONDARY');p.q.wait_for('Enter Filename:')
    p.type('C:\\OUT\\CHILD');p.key('ret');p.q.wait_absent('Enter Filename:')


def secondary_pages(p,child_on=True,restore=False):
    page_control(p,child_on);record(p,'Carol');record(p,'Dave')
    codes_save(p,'CHILD','child-secondary-codes')
    page_control(p,not child_on);record(p,'Alice')
    nest_secondary_command(p);record(p,'IGNORED')
    if restore:page_control(p,True)
    record(p,'Bob');record(p,'Eve');codes_save(p,'SECOND','parent-secondary-codes')
    p.type('Hello ');field(p,1);p.key('ret');perform_merge(p)
    names=['Alice','Carol','Dave','Bob','Eve']
    for name in names:p.q.wait_for('Hello '+name)
    s=p.capture('nested-secondary-result')
    p.check('Child records replace the nest record and parent resumes after it',
            all(s.index('Hello '+a)<s.index('Hello '+b) for a,b in zip(names,names[1:])))
    p.check('Suffix of NEST SECONDARY record is ignored','IGNORED' not in s)
    count=3 if child_on else (2 if restore else 1)
    p.check('Secondary page-control scope ends on page '+str(count+1),'Doc 1 Pg '+str(count+1)+' ' in s)
    p.key('alt-f3');p.q.wait_for('Reveal Codes to restore');p.capture('merged-codes')
    save_as(p,'MERGED');p.page_expectations.append(('MERGED.WP5',count))


def primary_child_break(p):
    secondary(p);p.type('C');field(p,1);p.key('ret');merge_named(p,'BREAK');p.type('CHILDBAD')
    codes_save(p,'CHILD','child-primary-break-codes')
    p.type('P');field(p,1);p.key('ret')
    merge_named(p,'NEST PRIMARY');p.q.wait_for('Enter Filename:')
    p.type('C:\\OUT\\CHILD');p.key('ret');p.q.wait_absent('Enter Filename:')
    p.type('R');p.key('ret');perform_merge(p)
    for text in ['PAlice','CAlice','PBob','CBob']:p.q.wait_for(text)
    p.q.wait_for('Doc 1 Pg 2 ');s=p.capture('nested-primary-break')
    p.check('Nested primary BREAK returns to parent and skips child remainder',
            s.splitlines().count('R')==2 and 'CHILDBAD' not in s)
    p.key('alt-f3');p.q.wait_for('Reveal Codes to restore');p.capture('merged-codes')
    save_as(p,'MERGED');p.page_expectations.append(('MERGED.WP5',1))


PROBES={'CMD51-226':each_strings,'CMD51-227':each_expressions,'CMD51-228':nested_next,
        'CMD51-229':macro_break,'CMD51-230':lambda p:macro_break(p,True),
        'CMD51-231':merge_break,'CMD51-232':lambda p:merge_break(p,True),
        'CMD51-233':secondary_pages,'CMD51-234':lambda p:secondary_pages(p,False),
        'CMD51-235':lambda p:secondary_pages(p,False,True),'CMD51-236':primary_child_break}
