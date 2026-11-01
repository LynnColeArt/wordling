#!/usr/bin/env python3
"""Compile-valid removed report guard, killed by its public boundary assertion."""
import ast
import hashlib
import json
from pathlib import Path
import py_compile
import shutil
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parents[4]
OWNED=ROOT/'docs/research/continuation/explicit-secondary-data'
SOURCE=ROOT/'scripts/reference/explicit_secondary_data.py'
before=hashlib.sha256(SOURCE.read_bytes()).hexdigest()
with tempfile.TemporaryDirectory(prefix='wordling-wp67-report-mutant-') as directory:
    target=Path(directory)
    files=['scripts/reference/explicit_secondary_data.py',str((OWNED/'test_workflow.py').relative_to(ROOT)),str((OWNED/'qualification-source-final.json').relative_to(ROOT)),'docs/research/reference-runs/2026-10-29-advanced-03/CMD51-209/SECOND.WP5']
    for name in files:
        path=target/name;path.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/name,path)
    tree=ast.parse(SOURCE.read_text())
    for node in tree.body:
        if isinstance(node,ast.FunctionDef) and node.name=='report_destination':node.body=[ast.Return(value=ast.Constant(None))]
    mutated=target/'scripts/reference/explicit_secondary_data.py';mutated.write_text(ast.unparse(tree)+'\n')
    py_compile.compile(str(mutated),doraise=True)
    argv=[sys.executable,'-m','unittest','discover','-s',str(OWNED.relative_to(ROOT)),'-p','test_workflow.py','-k','test_report_cannot_replace_native_or_unrelated_file','-v']
    result=subprocess.run(argv,cwd=target,capture_output=True,text=True,timeout=30)
    killed=result.returncode!=0 and 'AssertionError: Refusal not raised' in result.stderr and 'FAIL: test_report_cannot_replace_native_or_unrelated_file' in result.stderr
    record={'name':'removed-report-destination-guard','compile_valid':True,'runtime_killed':killed,'argv':argv,'cwd':str(target),'status':result.returncode,'stdout':result.stdout,'stderr':result.stderr,'kill_assertion':'public report_destination must reject a protected actual prior-report path; no source hash refusal counts','mutant_sha256':hashlib.sha256(mutated.read_bytes()).hexdigest(),'actual_source_before':before,'actual_source_after':hashlib.sha256(SOURCE.read_bytes()).hexdigest()}
    (OWNED/'report-guard-mutant.json').write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps({'compile_valid':True,'runtime_killed':killed}))
    assert before==record['actual_source_after']
    raise SystemExit(0 if killed else 1)
