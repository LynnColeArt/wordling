"""Bounded history, nested macro/loop and PAGE ON reference probes."""
from advanced import macro_start, macro_command, merge_named, merge_command, field, perform_merge, secondary
from extended import top, position, save_as, clear_doc1


def history_fixture(p, words):
    p.type(' '.join(words));p.q.wait_for(' '.join(words));top(p)
    for i,word in enumerate(words):
        p.key(','.join(['delete']*len(word)))
        expected=' '*i+' '.join(['']+words[i+1:]) if i<len(words)-1 else ''
        p.q.wait_until(lambda s:s.splitlines()[0]==expected,'deletion '+word)
        if i<len(words)-1:
            p.key('right');position(p,f'1.{i+1}')
    save_as(p,'BASE')


def preview(p, word, label):
    p.q.wait_until(lambda s:'Undelete:' in s and s.splitlines()[0].strip()==word,'history preview '+word)
    s=p.capture(label);p.check('Preview '+word,s.splitlines()[0].strip()==word)


def history(p,overflow=False):
    words=['ONE','TWO','THREE']+(['FOUR'] if overflow else [])
    history_fixture(p,words)
    p.key('f1');preview(p,words[-1],'latest')
    p.key('2');preview(p,words[-2],'previous')
    p.key('2');preview(p,words[-3],'oldest-retained')
    if overflow:
        p.key('2');s=p.capture('beyond-third')
        p.check('Fourth history request cannot display evicted ONE','ONE' not in s and s.splitlines()[0].strip() in words[-3:])
    p.key('f1');p.q.wait_absent('Undelete:');save_as(p,'BROWSED')
    p.same_body.append(('BASE.WP5','BROWSED.WP5'))
    p.key('f1');preview(p,words[-1],'reopened-latest')
    p.key('2');preview(p,words[-2],'reopened-previous')
    p.key('2');preview(p,words[-3],'restore-choice');p.key('1');p.q.wait_absent('Undelete:')
    expected=' '*(len(words)-1)+words[-3]
    p.q.wait_until(lambda s:s.splitlines()[0]==expected,'oldest retained deletion restored')
    s=p.capture('restored');p.check('Oldest retained text restored at current cursor',s.splitlines()[0]==expected)
    save_as(p,'HISTORY');p.contains.append(('HISTORY.WP5',expected.encode('ascii')))


def emit(p, parts):
    for command,text in parts:
        if command:macro_command(p,command)
        if text:p.type(text)


def finish(p,name,tail,execute=False):
    p.q.wait_for(tail);p.key('home,home,home,up');p.q.wait_for('{DISPLAY OFF}')
    p.capture(name.lower()+'-source-head');p.key('end');p.q.wait_for(tail)
    p.capture(name.lower()+'-source-tail');p.key('f7');p.q.wait_for('Doc 1')
    p.exports.append((name+'.WPM',name+'.WPM'))
    if execute:
        p.key('alt-f10');p.q.wait_for('Macro:');p.type('C:\\OUT\\'+name);p.key('ret')


def output(p,expected,name='RESULT'):
    p.q.wait_until(lambda s:s.splitlines()[0]==expected and 'Doc 1' in s,'macro output '+expected)
    s=p.capture('executed');p.check('Exact macro result '+expected,s.splitlines()[0]==expected)
    save_as(p,name);p.contains.append((name+'.WP5',expected.encode('ascii')))


def nested(p,local=True):
    macro_start(p,'CHILD')
    if local:
        emit(p,[('ON ERROR',''),('GO','CERR~~'),('NEST','C:\\OUT\\MISSING~CHILDBAD'),
                ('QUIT',''),('LABEL','CERR~CHILD'),('RETURN','')])
        finish(p,'CHILD','{RETURN}')
    else:
        emit(p,[(None,'C'),('NEST','C:\\OUT\\MISSING~CHILDBAD')])
        finish(p,'CHILD','CHILDBAD')
    macro_start(p,'PARENT')
    emit(p,[('ON ERROR',''),('GO','PERR~~'),(None,'P'),('NEST','C:\\OUT\\CHILD~')])
    if local:emit(p,[(None,'R'),('NEST','C:\\OUT\\MISSING~')])
    emit(p,[(None,'PARENTBAD'),('QUIT',''),('LABEL','PERR~PARENT')])
    finish(p,'PARENT','PARENT',True)
    output(p,'PCHILDRPARENT' if local else 'PCPARENT')


def for_loop(p):
    macro_start(p,'FORLOOP')
    emit(p,[('FOR','N~1~3~1~'),('VARIABLE','N~'),('END FOR','/'),
            ('FOR','N~3~1~-1~'),('VARIABLE','N~'),('END FOR','DONE')])
    finish(p,'FORLOOP','DONE',True);output(p,'123/321DONE')


def while_loop(p):
    macro_start(p,'WHILELP')
    emit(p,[('ASSIGN','N~0~'),('WHILE','0~BAD'),('END WHILE',''),
            ('WHILE',''),('VARIABLE','N~<3~'),('VARIABLE','N~'),
            ('ASSIGN','N~'),('VARIABLE','N~+1~'),('END WHILE','DONE')])
    finish(p,'WHILELP','DONE',True);output(p,'012DONE')


def page_on(p,conditional=False):
    if conditional:
        for name,value in [('Alice',''),('Bob',''),('Carol','YES'),('Dave','YES')]:
            p.type(name);p.key('f9');p.type(value);p.key('f9');merge_command(p,2)
        p.capture('secondary-records');save_as(p,'SECOND');clear_doc1(p)
        merge_named(p,'IF BLANK');p.q.wait_for('Enter Field:');p.type('2');p.key('ret');p.q.wait_absent('Enter Field:')
        merge_command(p,4);merge_named(p,'ELSE');merge_named(p,'PAGE ON');merge_named(p,'END IF')
    else:
        secondary(p);merge_command(p,4)
    p.type('Hello ');field(p,1);p.key('ret')
    if not conditional:merge_named(p,'PAGE ON')
    perform_merge(p)
    names=['Alice','Bob','Carol','Dave'] if conditional else ['Alice','Bob']
    for name in names:p.q.wait_for('Hello '+name)
    s=p.capture('resumed-pagination')
    p.check('All records merged in order',all(s.index('Hello '+a)<s.index('Hello '+b) for a,b in zip(names,names[1:])))
    if conditional:p.check('Initial PAGE OFF records remain adjacent','Hello Alice\nHello Bob' in s)
    p.check('PAGE ON restores page 2','Doc 1 Pg 2 ' in s)
    p.key('alt-f3');p.q.wait_for('Reveal Codes to restore');p.capture('merged-codes')
    save_as(p,'MERGED');p.page_expectations.append(('MERGED.WP5',1))
    p.contains.extend(('MERGED.WP5',('Hello '+name).encode('ascii')) for name in names)


PROBES={'CMD51-043':history,'CMD51-211':lambda p:history(p,True),
        'CMD51-212':nested,'CMD51-213':lambda p:nested(p,False),
        'CMD51-214':for_loop,'CMD51-215':while_loop,
        'CMD51-216':page_on,'CMD51-217':lambda p:page_on(p,True)}
