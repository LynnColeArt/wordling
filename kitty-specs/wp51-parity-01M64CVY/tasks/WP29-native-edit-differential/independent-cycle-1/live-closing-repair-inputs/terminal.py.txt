"""Strict bounded diagnostic VT cell decoder, NOT a document/editor model.

Only controls emitted by the pinned Bubble Tea capture profile are supported.
Unknown/incomplete output is evidence failure, never stripped into a passing view.
"""
import re

class TerminalFailure(ValueError):pass

class Screen:
    def __init__(self,width=140,height=32):
        if not (1<=width<=512 and 1<=height<=128):raise TerminalFailure('VT dimensions')
        self.width,self.height=width,height;self.rows=[[' ']*width for _ in range(height)];self.x=self.y=0;self.saved=(0,0);self.pending=b'';self.controls=[]
    def blank(self):return [' ']*self.width
    def feed(self,data):
        b=self.pending+data;at=0
        while at<len(b):
            c=b[at]
            if c==27:
                if at+1==len(b):break
                if b[at+1]==ord('['):
                    m=re.match(rb'\x1b\[([0-?]*)([ -/]*)([@-~])',b[at:])
                    if not m:
                        if len(b)-at>128:raise TerminalFailure('Oversized/incomplete CSI')
                        break
                    self.csi(*(x.decode('ascii')for x in m.groups()));self.controls.append(m.group().hex());at+=len(m.group());continue
                if b[at+1]==ord('M'):
                    if self.y==0:self.rows.insert(0,self.blank());self.rows.pop()
                    else:self.y-=1
                    self.controls.append('1b4d');at+=2;continue
                raise TerminalFailure('Unknown ESC '+b[at:at+8].hex())
            if c==13:self.x=0
            elif c==10:
                self.y+=1
                if self.y==self.height:self.rows.pop(0);self.rows.append(self.blank());self.y-=1
            elif c==8:self.x=max(0,self.x-1)
            elif c==9:self.x=min(self.width-1,(self.x//8+1)*8)
            elif 32<=c<=126:
                if self.x==self.width:self.x=0;self.y+=1
                if self.y==self.height:self.rows.pop(0);self.rows.append(self.blank());self.y-=1
                self.rows[self.y][self.x]=chr(c);self.x+=1
            else:raise TerminalFailure('Unqualified nonASCII/control output '+hex(c))
            at+=1
        self.pending=b[at:]
    def csi(self,params,inter,final):
        if params.startswith(('?','>','<')):
            allowed=(final in ['h','l']and params in ['?1049','?2004','?2026','?25'])or(final=='u'and inter==''and params in ['?','>31','<1'])or(final=='m'and params in ['>4','>4;2'])or(final=='p'and inter=='$'and params in ['?2026','?2027'])or(final=='W'and params=='?5')
            if not allowed:raise TerminalFailure('Unknown private CSI '+params+inter+final)
            if params=='?1049'and final=='h':self.rows=[self.blank()for _ in range(self.height)];self.x=self.y=0
            return
        if inter:
            if inter==' 'and final=='q':return # cursor shape only
            raise TerminalFailure('Unknown intermediate CSI '+params+inter+final)
        try:v=[int(x)if x else 0 for x in params.split(';')]
        except ValueError as e:raise TerminalFailure('CSI parameter')from e
        n=v[0]or 1
        if final in ['H','f']:self.y=max(0,min(self.height-1,(v[0]or 1)-1));self.x=max(0,min(self.width-1,((v[1]if len(v)>1 else 1)or 1)-1))
        elif final=='G':self.x=min(self.width-1,n-1)
        elif final=='d':self.y=min(self.height-1,n-1)
        elif final=='A':self.y=max(0,self.y-n)
        elif final=='B':self.y=min(self.height-1,self.y+n)
        elif final=='C':self.x=min(self.width-1,self.x+n)
        elif final=='D':self.x=max(0,self.x-n)
        elif final=='J':
            if v[0]==2:self.rows=[self.blank()for _ in range(self.height)]
            elif v[0]==0:
                self.rows[self.y][self.x:]=[' ']*(self.width-self.x)
                for row in range(self.y+1,self.height):self.rows[row]=self.blank()
            elif v[0]==1:
                for row in range(self.y):self.rows[row]=self.blank()
                self.rows[self.y][:self.x+1]=[' ']*(self.x+1)
            else:raise TerminalFailure('Erase display mode')
        elif final=='K':
            if v[0]==0:self.rows[self.y][self.x:]=[' ']*(self.width-self.x)
            elif v[0]==1:self.rows[self.y][:self.x+1]=[' ']*(self.x+1)
            elif v[0]==2:self.rows[self.y]=self.blank()
            else:raise TerminalFailure('Erase line mode')
        elif final=='P':self.rows[self.y][self.x:]=self.rows[self.y][self.x+n:]+[' ']*min(n,self.width-self.x)
        elif final=='@':self.rows[self.y][self.x:]=([' ']*min(n,self.width-self.x)+self.rows[self.y][self.x:])[:self.width-self.x]
        elif final=='L':self.rows[self.y:]=([self.blank()for _ in range(min(n,self.height-self.y))]+self.rows[self.y:])[:self.height-self.y]
        elif final=='M':self.rows[self.y:]=self.rows[min(self.height,self.y+n):]+[self.blank()for _ in range(min(n,self.height-self.y))]
        elif final=='m':return # rendition cannot affect the decoded cells
        elif final=='s':self.saved=(self.x,self.y)
        elif final=='u':self.x,self.y=self.saved
        else:raise TerminalFailure('Unknown CSI '+params+final)
    def snapshot(self):
        if self.pending:raise TerminalFailure('Incomplete emitted terminal control')
        return {'rows':[''.join(r)for r in self.rows],'terminal_cursor':{'row':self.y,'column':self.x},'width':self.width,'height':self.height}
    def state(self):
        snap=self.snapshot();rows=snap['rows'];status=[]
        for row in rows:
            m=re.fullmatch(r'(Editing|RetrieveName|SaveName|ReplaceQuestion|ExitSaveQuestion|ExitQuestion|Waiting|Exited|DeleteQuestion|HistoryPreview) \| (.*?) \| gap (\d+) \| (NotSaved|SameFileNoOp|NewNamePublished|SaveFailed|SaveUncertain)\s*',row)
            if m:status.append({'mode':m[1],'name':m[2],'gap':int(m[3]),'save':m[4]})
        if len(status)!=1:raise TerminalFailure('No unique current reducer status row')
        fields=[]
        for row in rows:
            m=re.fullmatch(r'(Typeover )?Dirty=(true|false) Block=(true|false) revision=(\d+) history=(unknown|\d+) qualified=(true|false)\s*',row)
            if m:fields.append({'typeover':bool(m[1]),'dirty':m[2]=='true','block':m[3]=='true','revision':int(m[4]),'history_count':None if m[5]=='unknown'else int(m[5]),'history_qualified':m[6]=='true'})
        if len(fields)!=1:raise TerminalFailure('No unique current reducer detail row')
        return status[0]|fields[0]|{'terminal_cursor':snap['terminal_cursor']}
