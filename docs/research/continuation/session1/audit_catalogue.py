#!/usr/bin/env python3
"""Audit exact owned canonical changes and semantic case-to-state associations."""
import json
from pathlib import Path
import subprocess

ROOT=Path(__file__).resolve().parents[4]
HERE=Path(__file__).parent
OLD={'CMD51-019','CMD51-020','CMD51-049','CMD51-065','CMD51-067','CMD51-069','CMD51-070','CMD51-087'}
NEW={f'CMD51-{n}' for n in range(237,245)}


def baseline(path):
    return json.loads(subprocess.check_output(['git','show','7deeaf6:'+path],cwd=ROOT,text=True))


def check(cases,features,index):
    before=baseline('docs/research/command-scenarios.json');old={c['id']:c for c in before}
    current={c['id']:c for c in cases}
    assert [c['id'] for c in cases[:len(before)]]==[c['id'] for c in before]
    assert set(current)-set(old)==NEW
    assert all(current[cid]==old[cid] for cid in old if cid not in OLD),'Unrelated canonical row changed'
    previous=baseline('docs/research/feature-inventory.json')
    assert len(features)==len(previous)==91
    for a,b in zip(features,previous):
        assert {k:v for k,v in a.items() if k!='command_scenario_ids'}=={k:v for k,v in b.items() if k!='command_scenario_ids'}
        assert a['command_scenario_ids']==[c['id'] for c in cases if a['id'] in c['feature_ids']]
    for cid in sorted(OLD|NEW):
        c=current[cid]
        assert c['oracle_status']=='partially-observed' and c['implementation_status']=='not-implemented'
        if cid in OLD:assert c['title']==old[cid]['title']
        for sub in c['session1_subcases']:
            branch=index['branches'][sub['branch']]
            assert cid in branch['case_ids']
            assert set(sub['run_manifests'])=={r['manifest'] for r in branch['runs']}
            assert sub['accepted_state_labels'] and set(sub['accepted_state_labels'])<=set(branch['states'])
            labels=sub['accepted_state_labels']
            if cid=='CMD51-019':assert all('-after' in label for label in labels),'After-initial case linked to wrong state'
            if cid=='CMD51-020':assert all('-before' in label for label in labels),'Before-initial case linked to wrong state'
            if cid=='CMD51-237':assert all(label.startswith('retrieve-f1-') for label in labels)
            if cid=='CMD51-238':assert all(label.startswith('retrieve-esc-') for label in labels)
            if cid=='CMD51-241':assert 'exit-save-escape-advance' in labels and 'exit-save-cancel' not in labels
            if cid=='CMD51-244':
                assert labels==['exit-dos-result'],'Quit case lacks exclusive post-wait DOS association'
                for fact in branch['states']['exit-dos-result']:
                    screen=(ROOT/fact['screen_path']).read_text()
                    assert 'C:\\WP51>' in screen,'Quit terminal state lacks DOS prompt'
                    assert fact['hardware_cursor']=={'row':0,'column':8},'Quit DOS cursor differs'
                    assert '/exit-dos-result/' in fact['screen_path'],'Quit terminal path is not post-wait capture'
            if cid=='CMD51-243':
                for fact in branch['states']['exit-choice-result']:assert fact['first_line']==''
    assert all(c['implementation_status']=='not-implemented' for c in cases)
    assert sum(c['oracle_status']=='partially-observed' for c in cases)==68
    assert sum(c['oracle_status']=='not-run' for c in cases)==176


if __name__=='__main__':
    cases=json.loads((ROOT/'docs/research/command-scenarios.json').read_text())
    features=json.loads((ROOT/'docs/research/feature-inventory.json').read_text())
    index=json.loads((HERE/'state-index.json').read_text())
    check(cases,features,index)
    print('WP13 owned canonical rows, exact back-links and semantic state associations valid:244/68/176')
