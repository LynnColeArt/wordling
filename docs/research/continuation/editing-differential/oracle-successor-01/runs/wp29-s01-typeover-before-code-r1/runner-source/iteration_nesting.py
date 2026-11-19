"""Original macro iteration and page-control scope across nested primary files."""
from advanced import macro_start, macro_command, merge_named, merge_command, field, perform_merge, secondary
from extended import save_as, clear_doc1
from history_loops import emit, finish, output


def foreach(p):
    macro_start(p,'EACHLOOP')
    emit(p,[('FOR EACH','N~15~10~15~5~~'),('VARIABLE','N~/'),('END FOR','DONE')])
    finish(p,'EACHLOOP','DONE',True);output(p,'15/10/15/5/DONE')


def condition(p,var,value):
    emit(p,[('IF',''),('VARIABLE',var+'~='+str(value)+'~')])


def next_iteration(p):
    macro_start(p,'NEXTLOOP');emit(p,[('FOR','N~1~3~1~')]);condition(p,'N',2)
    emit(p,[('NEXT',''),('END IF',''),('VARIABLE','N~X'),('END FOR','DONE')])
    finish(p,'NEXTLOOP','DONE',True);output(p,'1X3XDONE')


def break_iteration(p):
    macro_start(p,'BREAKLP');emit(p,[('FOR','N~1~5~1~')]);condition(p,'N',3)
    emit(p,[('BREAK',''),('END IF',''),('VARIABLE','N~'),('END FOR','DONE')])
    finish(p,'BREAKLP','DONE',True);output(p,'12DONE')


def nested_break(p):
    macro_start(p,'NESTBRK');emit(p,[('FOR','I~1~2~1~'),('FOR','J~1~3~1~')])
    condition(p,'J',2)
    emit(p,[('BREAK',''),('END IF',''),('VARIABLE','I~'),('VARIABLE','J~'),
            ('END FOR','R'),('END FOR','DONE')])
    finish(p,'NESTBRK','DONE',True);output(p,'11R21RDONE')


def mixed_loops(p):
    macro_start(p,'MIXLOOP')
    emit(p,[('FOR','I~1~2~1~'),('ASSIGN','J~0~'),('WHILE',''),('VARIABLE','J~<2~'),
            ('VARIABLE','I~'),('VARIABLE','J~/'),('ASSIGN','J~'),('VARIABLE','J~+1~'),
            ('END WHILE',''),('END FOR','DONE')])
    finish(p,'MIXLOOP','DONE',True);output(p,'10/11/20/21/DONE')


def page_control(p,on):
    if on:merge_named(p,'PAGE ON')
    else:merge_command(p,4)


def nested_pages(p,child_on=True,restore=False):
    secondary(p)
    page_control(p,child_on);p.type('C');field(p,1);p.key('ret')
    p.key('alt-f3');p.q.wait_for('Reveal Codes to restore');p.capture('child-codes');p.key('alt-f3')
    save_as(p,'CHILD');clear_doc1(p)
    page_control(p,not child_on);p.type('P');field(p,1);p.key('ret')
    merge_named(p,'NEST PRIMARY');p.q.wait_for('Enter Filename:')
    p.type('C:\\OUT\\CHILD');p.key('ret');p.q.wait_absent('Enter Filename:')
    if restore:page_control(p,True)
    p.type('R');p.key('ret');perform_merge(p)
    for text in ['PAlice','CAlice','PBob','CBob']:p.q.wait_for(text)
    pages=2 if child_on or restore else 1
    p.q.wait_until(lambda s:'Doc 1 Pg '+str(pages)+' ' in s and 'Repositioning' not in s,
                   'nested merge completed on page '+str(pages))
    s=p.capture('nested-merge')
    markers=['PAlice','CAlice','PBob','CBob']
    p.check('Nested primary uses the current record and returns in order',
            all(s.index(a)<s.index(b) for a,b in zip(markers,markers[1:])))
    p.check('Parent resumes after each nested call',s.splitlines().count('R')==2)
    p.check('Page-control scope produces page '+str(pages),'Doc 1 Pg '+str(pages)+' ' in s)
    p.key('alt-f3');p.q.wait_for('Reveal Codes to restore');p.capture('merged-codes')
    save_as(p,'MERGED');p.page_expectations.append(('MERGED.WP5',pages-1))
    p.contains.extend(('MERGED.WP5',x.encode('ascii')) for x in markers)


PROBES={'CMD51-218':foreach,'CMD51-219':next_iteration,'CMD51-220':break_iteration,
        'CMD51-221':nested_break,'CMD51-222':mixed_loops,'CMD51-223':nested_pages,
        'CMD51-224':lambda p:nested_pages(p,False),
        'CMD51-225':lambda p:nested_pages(p,False,True)}
