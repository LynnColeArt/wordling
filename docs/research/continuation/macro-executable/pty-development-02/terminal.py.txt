"""Bounded ASCII VT observation for the declared synthetic PTYs, not native data.

Raw wire is always retained. Queries/styles/keyboard modes do not become text;
unknown escape controls are recorded, never claimed as physical qualification.
"""
class Terminal:
    def __init__(self,columns=150,rows=30):
        assert 1<=columns<=4096 and 1<=rows<=4096
        self.columns,self.height=columns,rows
        self.cells=[[' ']*columns for _ in range(rows)]
        self.x=self.y=0;self.top=0;self.bottom=rows-1;self.saved=(0,0)
        self.pending=bytearray();self.unknown=[];self.last=' '
    def up(self):
        self.cells.pop(self.top);self.cells.insert(self.bottom,[' ']*self.columns)
    def down(self):
        self.cells.pop(self.bottom);self.cells.insert(self.top,[' ']*self.columns)
    def line(self):
        if self.y==self.bottom:self.up()
        else:self.y=min(self.height-1,self.y+1)
    def put(self,c):
        if self.x>=self.columns:self.x=0;self.line()
        self.cells[self.y][self.x]=c;self.x+=1;self.last=c
    def csi(self,body,final):
        private=body[:1] in '?><!';plain=body.lstrip('?><!')
        try:params=[int(x.split(':')[0] or '0') for x in plain.split(';')] if plain else [0]
        except ValueError:params=[0]
        n=params[0] or 1
        if final in 'hl' and private:
            if params[0]==1049 and final=='h':self.cells=[[' ']*self.columns for _ in range(self.height)];self.x=self.y=0
            return
        if final in 'mqct' or (final=='p' and '$' in body) or (final=='u' and private):return
        if final in 'Hf':self.y=min(self.height-1,max(0,n-1));self.x=min(self.columns-1,max(0,(params[1] if len(params)>1 and params[1] else 1)-1))
        elif final=='G':self.x=min(self.columns-1,max(0,n-1))
        elif final=='d':self.y=min(self.height-1,max(0,n-1))
        elif final=='A':self.y=max(0,self.y-n)
        elif final in 'Be':self.y=min(self.height-1,self.y+n)
        elif final in 'Ca':self.x=min(self.columns-1,self.x+n)
        elif final=='D':self.x=max(0,self.x-n)
        elif final=='E':self.y=min(self.height-1,self.y+n);self.x=0
        elif final=='F':self.y=max(0,self.y-n);self.x=0
        elif final=='K':
            a=0 if params[0] in [1,2] else min(self.x,self.columns)
            b=self.columns if params[0] in [0,2] else min(self.columns,self.x+1)
            self.cells[self.y][a:b]=[' ']*(b-a)
        elif final=='J':
            if params[0] in [2,3]:self.cells=[[' ']*self.columns for _ in range(self.height)]
            elif params[0]==0:
                self.cells[self.y][min(self.x,self.columns):]=[' ']*max(0,self.columns-self.x)
                for y in range(self.y+1,self.height):self.cells[y]=[' ']*self.columns
            elif params[0]==1:
                for y in range(self.y):self.cells[y]=[' ']*self.columns
                end=min(self.columns,self.x+1);self.cells[self.y][:end]=[' ']*end
        elif final=='P':
            n=min(n,self.columns-min(self.x,self.columns));self.cells[self.y][self.x:]=self.cells[self.y][self.x+n:]+[' ']*n
        elif final=='@':
            n=min(n,self.columns-min(self.x,self.columns));self.cells[self.y][self.x:]=([' ']*n+self.cells[self.y][self.x:])[:self.columns-self.x]
        elif final=='X':
            n=min(n,self.columns-min(self.x,self.columns));self.cells[self.y][self.x:self.x+n]=[' ']*n
        elif final=='M':
            for _ in range(min(n,self.bottom-self.y+1)):
                self.cells.pop(self.y);self.cells.insert(self.bottom,[' ']*self.columns)
        elif final=='L':
            for _ in range(min(n,self.bottom-self.y+1)):
                self.cells.pop(self.bottom);self.cells.insert(self.y,[' ']*self.columns)
        elif final=='S':
            for _ in range(min(n,self.height)):self.up()
        elif final=='T':
            for _ in range(min(n,self.height)):self.down()
        elif final=='r':
            self.top=max(0,min(self.height-1,n-1));self.bottom=max(self.top,min(self.height-1,(params[1] if len(params)>1 and params[1] else self.height)-1));self.x=self.y=0
        elif final=='s':self.saved=(self.x,self.y)
        elif final=='u':self.x,self.y=self.saved
        elif final=='b':
            for _ in range(min(n,self.columns*self.height)):self.put(self.last)
        elif final=='n':return
        else:self.unknown.append('CSI'+body+final)
    def feed(self,raw):
        self.pending.extend(raw);p=0
        while p<len(self.pending):
            b=self.pending[p]
            if b==27:
                if p+1>=len(self.pending):break
                second=self.pending[p+1]
                if second==91:
                    end=p+2
                    while end<len(self.pending) and not 0x40<=self.pending[end]<=0x7e:end+=1
                    if end==len(self.pending):break
                    self.csi(bytes(self.pending[p+2:end]).decode('ascii'),chr(self.pending[end]));p=end+1;continue
                if second in [93,80,95,94]:
                    end=p+2
                    while end<len(self.pending) and self.pending[end]!=7 and self.pending[end:end+2]!=b'\x1b\\':end+=1
                    if end>=len(self.pending) or self.pending[end]==27 and end+1>=len(self.pending):break
                    p=end+(2 if self.pending[end]==27 else 1);continue
                if second in [40,41]:
                    if p+2>=len(self.pending):break
                    p+=3;continue
                if second==77:
                    if self.y==self.top:self.down()
                    else:self.y=max(0,self.y-1)
                elif second==68:self.line()
                elif second==69:self.x=0;self.line()
                elif second==55:self.saved=(self.x,self.y)
                elif second==56:self.x,self.y=self.saved
                elif second==61 or second==62:pass
                else:self.unknown.append('ESC'+chr(second))
                p+=2;continue
            if b==13:self.x=0
            elif b in [10,11,12]:self.line()
            elif b==8:self.x=max(0,self.x-1)
            elif b==9:self.x=min(self.columns-1,8*(self.x//8+1))
            elif 32<=b<=126:self.put(chr(b))
            elif b not in [0,7]:raise ValueError('nonASCII VT observation outside declared scope')
            p+=1
        del self.pending[:p]
        if len(self.pending)>65536:raise ValueError('VT escape acquisition bound')
    def rows(self):return [''.join(row) for row in self.cells]
    def text(self):return '\n'.join(self.rows())
