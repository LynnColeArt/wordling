"""Frozen original-operation traces, not a native API producer or writer."""
from frames import normal
CLASSES=['empty-insert-and-reload','ascii-boundaries-and-reload','typeover-replace-extend-and-reload','same-byte-noop-and-reload']
EXPECTED=[('ABCD','ABCDQ'),('XABYCDZ','XABRYCDZ'),('AXYDQ','RXYDQ'),('ABCD','ABCD')]
def operation_plan(index):
 # Explicit semantic trace used to check UI expectations; never emitted native.
 before=[('text','ABCD')]
 if index==1:before += [('home',None),('text','X'),('right',2),('text','Y'),('right',2),('text','Z')]
 if index==2:before += [('home',None),('right',1),('mode',True),('text','XY'),('end',None),('text','Q')]
 if index==3:before += [('home',None),('mode',True),('text','AB')]
 after=[('end',None),('text','Q')]if index==0 else[('right',3),('text','R')]if index==1 else[('mode',True),('text','R')]if index==2 else[('mode',True),('text','A')]
 return {'id':CLASSES[index],'before_Save_S0':before,'after_clear_Retrieve_S0':after,'S0_body':EXPECTED[index][0],'S1_FIN_body':EXPECTED[index][1],'initial_source':'EXACT_H1_C46FIN_e72402_notPRE01','mode_after_clear':'only two exact source-qualified normal frame variants may be observed, then explicit original Insert toggles to requested mode','sufficiency':'operation trace and Save/reload observations, NOT native permission or independent sufficiency by itself'}
def leaves(private):
 return [{'id':f'wp51-{case}-r{repeat}','case':case,'class_index':index,'repetition':repeat,'private_work':str(private/'runs'/f'wp51-h1-c{index+1}-r{repeat}')}for index,case in enumerate(CLASSES)for repeat in [1,2]]
