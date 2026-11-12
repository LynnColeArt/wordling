"""Separate public consumer for actual source-bound HELLO refusal variants."""
import dataclasses
import importlib.util
import json
from pathlib import Path
import sys
import time
sp=importlib.util.spec_from_file_location('creation_public_consumer',sys.argv[1]);st=importlib.util.module_from_spec(sp);sp.loader.exec_module(st)
workspace=Path(sys.argv[2]);now=time.monotonic();session=None
try:
 session=st.open_session(st.NewWorkspace(str(workspace)),st.StreamPolicy(),st.ManagedPolicy(),
    envelope=st.SharedEnvelopePolicy(now,now+5,measurement_completion=sys.argv[3] if len(sys.argv)>3 else 'bounded-original-v1'))
 print(json.dumps(dict(accepted=True)))
except st.StartupFailure as error:
 print(json.dumps(dict(accepted=False,error=error.code,partial=dataclasses.asdict(error.observation),
     creation=dict(getattr(error,'creation',())),workspace_exists=workspace.exists(),
     journal=(workspace/'session.jsonl').read_text() if (workspace/'session.jsonl').exists() else None)))
finally:
 if session:session.close()
