"""Read-only raw state/command auditor. No field writer or guest execution."""
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT/'scripts/reference'))
import native_genesis as g
import qmp


def keys(trace):
    out=[]
    class Recorder:
        def key(self,key):out.append(key)
    for entry in trace:
        if 'key'in entry:out.extend(entry['key'].split(','))
        if 'type'in entry:qmp.QMP.type(Recorder(),entry['type'])
    return out


def sensitive(plan):
    events=[{'key':'f3'},{'key':'spc'},{'key':'alt-f3'},{'key':'alt-f3'}]
    if plan['initial_text']:events.append({'type':plan['initial_text']})
    if plan['id']=='empty-f10-cancel':return keys(events+[{'key':'f10'},{'key':'f1'}]),'empty-filename-after-F1'
    if plan['id']=='ascii-name-cancel':events +=[{'key':'f10'},{'type':'C:\\OUT\\G43DRAFT'},{'key':'f1'}]
    if plan['id']=='ascii-dirty-exit-return':events +=[{'key':'f7'},{'key':'f1'}]
    events +=[{'key':'f10'},{'type':'C:\\OUT\\'+plan['first_save_name']},{'key':'ret'}]
    return keys(events),'first-save-complete'


def trace_interval(trace,plan):
    expected,end=sensitive(plan);indices=[i for i,e in enumerate(trace)if e.get('capture')==end]
    g.need(len(indices)==1,'SensitiveCapture','Unique exact first-save/cancel completion required')
    g.need(keys(trace[:indices[0]+1])==expected,'HiddenSensitiveCommand','Unexpected Save/navigation/settings/type/cancel key in first interval')


def captured(directory,label):
    base=directory/label;raw=(base/'vram.bin').read_bytes()
    g.need(len(raw)==4000,'VGAExtent','Exact 80x25 original text capture required')
    actual='\n'.join(raw[i:i+160:2].replace(b'\0',b' ').decode('cp437').rstrip()for i in range(0,4000,160))+'\n'
    g.need((base/'screen.txt').read_text()==actual,'RehashedScreenChanged','Screen text must agree with actual VGA bytes')
    cursor=json.loads((base/'cursor.json').read_text());regs=cursor['crtc'];start=regs['12']*256+regs['13'];address=regs['14']*256+regs['15'];offset=(address-start)%32768
    g.need(cursor['row']==offset//80 and cursor['column']==offset%80 and 0<=cursor['row']<25,'CursorChanged','Reported filename/document cursor differs from raw CRTC values')
    return actual,cursor


def validate_name(s,name):
    g.need(s.splitlines()[-1]=='Document to be saved: C:\\OUT\\'+name,'WrongFilename','Actual complete short filename differs')


def wire_match(directory,trace):
    path=directory/'qmp-wire.jsonl';g.need(path.stat().st_size<=64*1024*1024,'WireBounds','Wire stream exceeds declared64MiB budget')
    commands=[]
    for line in path.read_text().splitlines():
        item=json.loads(line)
        if item['direction']=='tx-buffer':
            msg=json.loads(bytes.fromhex(item['raw_hex']));cmd=msg.get('arguments',{}).get('command-line','')
            if cmd.startswith('sendkey '):commands.append(cmd)
    g.need(commands==['sendkey '+key+' 80'for key in keys(trace)],'WireCommandChanged','Actual QMP keystrokes differ from complete declared trace')
    return len(commands)


def audit(directory,row,plan):
    trace=row['trace'];trace_interval(trace,plan)
    wire_match(directory,trace)
    screens={}
    for entry in trace:
        if 'capture'in entry:screens[entry['capture']]=captured(directory,entry['capture'])[0]
    g.need(g.state(screens['startup-normal'])=='main'and screens['startup-normal'].splitlines()[0]=='','NonemptyGenesis','Actual startup state not empty Doc1')
    g.need('Doc 1 Pg 1'in screens['startup-normal'].splitlines()[-1],'DocumentIdentity','Wrong active startup document')
    g.need('WP 5.1   03/09/92'in screens['release'],'ReleaseChanged','Wrong original release')
    if plan['initial_text']:
        g.need(screens['first-ascii-before-save'].splitlines()[0]==plan['initial_text'],'FirstTextChanged','Actual first typed body differs')
        if plan['id']=='ascii-name-cancel':
            validate_name(screens['cancel-filename-draft'],'G43DRAFT')
            g.need(screens['cancel-return'].splitlines()[0]==plan['initial_text']and g.state(screens['cancel-return'])=='main','CancelBranchChanged','Name cancel did not retain body/main')
        if plan['id']=='ascii-dirty-exit-return':
            g.need(g.state(screens['dirty-save-question-before-F1'])=='save'and g.state(screens['dirty-save-question-after-F1'])=='main','DirtyBranchChanged','F1 Save-question return differs')
    if plan['first_save_name']:
        validate_name(screens['first-save-typed-name'],plan['first_save_name'])
        g.need(g.state(screens['first-save-complete'])=='main'and 'C:\\OUT\\'+plan['first_save_name']in screens['first-save-complete'].splitlines()[-1],'NameCommitChanged','First saved displayed name differs')
    else:g.need(g.state(screens['empty-filename-before-F1'])=='filename'and g.state(screens['empty-filename-after-F1'])=='main','CancelBranchChanged','Empty filename F1 branch differs')
    for i,action in enumerate(row['exit_actions']):
        label='exit-state-'+str(i);st=g.state(screens[label]);key='f7'if st=='main'else'n'if st=='save'else'y'
        g.need(action=={'state':st,'key':key,'capture':label},'FakeExit','Exit key differs from captured prompt')
        at=next(j for j,e in enumerate(trace)if e.get('capture')==label)
        nextkeys=keys(trace[at+1:]);g.need(nextkeys and nextkeys[0]==key,'FakeExit','Next actual exit key must answer captured state')
    g.need(g.state(screens['clean-exit'])=='dos','FakeExit','No actual clear DOS completion')
    return {'first_interval':'exact declared commands','wire':'all actual keys match trace','raw_vga_cursor':'replayed','default_permission':False,
            'actual_states':{label:{'first_row':text.splitlines()[0],'footer':text.splitlines()[-1],'cursor':captured(directory,label)[1]}for label,text in screens.items()if label.startswith(('startup','first-','cancel-','dirty-','empty-','exit-','clean-'))}}
