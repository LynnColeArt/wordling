"""Actual public peer/issued-receipt integration against private harmless Unix fixtures."""
from pathlib import Path
import copy,importlib,json,os,sys,tempfile,threading,time
from enter_sources import B,HERE,ROOT,interfaces
from enter_safety import guard

def challenge(foreign=False):
 mods=interfaces();qmod=importlib.import_module('qmp');g=guard();threads=[];processes=[]
 with tempfile.TemporaryDirectory(prefix='wordling-wp57-peer-proof-')as d:
  work=Path(d);runtime=work/'runtime';runtime.mkdir();socket=runtime/'qmp.sock';wire=work/'server-wire';wire.write_bytes(b'');facade=type('Paths',(),dict(RUNTIME=runtime,SOCKET=socket))
  def start(script,pidfile,kind):
   args=[sys.executable,'-B',str(HERE/script),str(pidfile),str(work/'boot.img'),str(work/'harddisk.img'),'unix:'+str(socket)+',',str(wire)if script=='fixture_qmp.py'else kind];row=dict(argv=args,cleanup=[])
   def worker():
    try:out,err=B.process(args,ROOT,timeout=2,receipts=row['cleanup']);row.update(exit=0,stdout=out.hex(),stderr=err.hex())
    except BaseException as e:row.update(error=getattr(e,'code',type(e).__name__))
   t=threading.Thread(target=worker);t.start();threads.append(t);processes.append(row);deadline=time.monotonic()+1
   while not pidfile.exists():B.require(time.monotonic()<deadline and t.is_alive(),'FixtureStartup','bounded actual private actor');time.sleep(.005)
   return args
  serverargs=start('fixture_qmp.py',runtime/'qemu.pid','server')
  if foreign:
   # Separate positively owned fixture process names this endpoint in argv but does not serve it.
   serverpid=(runtime/'qemu.pid').read_text();(runtime/'qemu.pid').unlink();ownerargs=start('fixture_child.py',runtime/'qemu.pid','owner');owned=g.owned_identity(facade,work,ownerargs)
  else:owned=g.owned_identity(facade,work,serverargs)
  error=None;receipt=None;row=None
  try:
   if foreign:
    try:
     with mods['peer'].connect(facade,qmod.QMP,owned,g.same_identity):raise AssertionError('foreign peer accepted')
    except ValueError as e:error=getattr(e,'code',type(e).__name__)
    B.require(error=='QMPEndpointPeerMismatch','FixtureRefusal','foreign PID before capabilities');B.require(wire.read_bytes()==b'','ForeignCommands','zero sent commands');B.require(Path('/proc',serverpid).exists()and Path('/proc',str(owned['pid'])).exists(),'ForeignUntouched','no signal from rejected connection')
   else:
    receipt=mods['stopping'].normal_quit(facade,qmod.QMP,owned,g.same_identity,g.stopped,work/'actual-quit-wire');row=dict(normal_DOS=True,guest_stopped=True,stop_method=mods['stopping'].NORMAL,quit_exchange=receipt.snapshot(),stop_proof=receipt.snapshot()['owned_stopped']);B.require(mods['stopping'].validate(receipt,row,owned),'IssuedReceipt','actual opaque same-process receipt');bad=copy.deepcopy(row);bad['quit_exchange']['sha256']='0'*64
    try:mods['stopping'].validate(receipt,bad,owned);raise AssertionError('rehashed/retargeted receipt accepted')
    except ValueError:pass
    try:mods['stopping'].validate(receipt.snapshot(),row,owned);raise AssertionError('JSON minted receipt accepted')
    except ValueError:pass
  finally:
   for t in threads:t.join(timeout=3);B.require(not t.is_alive(),'FixturePending','all private workers settled')
  return dict(fixture_only=True,actual_original_launched=0,original_qualification=False,foreign_peer=foreign,error=error,wire=wire.read_text(),processes=processes,issued_receipt=None if receipt is None else receipt.snapshot(),TEST_normal_DOS_flag_is_not_original_proof=True)
