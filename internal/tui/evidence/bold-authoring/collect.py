"""WP76 current source and custody receipt."""
import gzip
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import time

ROOT = Path('/home/lynn/projects/wordling/.worktrees/wp51-parity-01M64CVY-lane-h')
TMP = Path('/tmp/wordling-wp76-run')
PROMPT = Path('/tmp/spec-kitty-prompts/addc41014af625fc/spec-kitty-implement-wp51-parity-01M64CVY-WP76.md')
PRIMARY = ROOT.parent.parent
MISSION = PRIMARY / 'kitty-specs/wp51-parity-01M64CVY'
REVISION = MISSION / 'tasks/next-bold-wp74-76-promotion/source-equivalence-revision'
EVIDENCE = ROOT / 'internal/tui/evidence/bold-authoring'
BASE_COMMIT = '5bd5105e9014a839ea95c5b2efd21548ccd8756b'
BASE_PATH = 'internal/tui/evidence/character-repeat/before.json.gz'
BASE_BLOB = '5fd810927242843b1d5c0f2430f56df8abc1428b'
BASE_HASH = 'f42869ecf5d5a0c2bdff1eeed7b536b055dd4e1f9868a4efca99bf26d740d6d3'
EXPANDED_HASH = '779b7b371a8152089387670e8d706f134e1b171b4fb606ce602cd34e225763a0'
ENV = dict(os.environ, GOTOOLCHAIN='local', GOPROXY='off', PYTHONDONTWRITEBYTECODE='1')
RECORDS = []


def digest(data):
    return hashlib.sha256(data).hexdigest()


def compact(data):
    return json.dumps(data, ensure_ascii=True, sort_keys=True, separators=(',', ':')).encode()


def write_gz(path, data):
    path.write_bytes(gzip.compress(compact(data), mtime=0))


def run(argv, representation=None, require=True):
    started = time.monotonic()
    result = subprocess.run(argv, cwd=ROOT, env=ENV, timeout=300, capture_output=True)
    receipt = dict(argv=argv, cwd=str(ROOT), exit=result.returncode, elapsed=time.monotonic()-started,
                   stdout_bytes=len(result.stdout), stdout_sha256=digest(result.stdout),
                   stderr_hex=result.stderr.hex())
    if representation is None or result.returncode:
        receipt['stdout_hex'] = result.stdout.hex()
    else:
        receipt['stdout_representation'] = representation
    RECORDS.append(receipt)
    if require and result.returncode:
        raise RuntimeError((argv, result.returncode, result.stderr.decode(errors='replace')))
    return result.stdout


def path_name(data):
    path = data.decode('utf-8')
    assert path.encode() == data and '\\' not in path and not path.startswith('/')
    assert not set(path.split('/')) & {'', '.', '..', '.git'}
    return path


def identity(st):
    return (st.st_dev, st.st_ino, st.st_mode, st.st_size, st.st_mtime_ns, st.st_ctime_ns)


def read_rows(index, untracked):
    parents = {}
    inodes = set()
    rows = {}
    owned = {}
    size = 0
    for path, stage in [(p, i) for p, i in index.items()] + [(p, None) for p in untracked]:
        file = ROOT / path
        for parent in file.parents:
            if parent in parents:
                break
            st = parent.lstat()
            assert stat.S_ISDIR(st.st_mode), parent
            parents[parent] = (st.st_dev, st.st_ino, st.st_mode)
            if parent == ROOT:
                break
        before = file.lstat()
        assert stat.S_ISREG(before.st_mode) and before.st_nlink == 1, path
        assert (before.st_dev, before.st_ino) not in inodes, path
        inodes.add((before.st_dev, before.st_ino))
        with os.fdopen(os.open(file, os.O_RDONLY | os.O_NOFOLLOW), 'rb') as opened:
            assert identity(os.fstat(opened.fileno())) == identity(before), path
            sha = hashlib.file_digest(opened, 'sha256').hexdigest()
            assert opened.tell() == before.st_size, path
            assert identity(os.fstat(opened.fileno())) == identity(before), path
        assert identity(file.lstat()) == identity(before), path
        size += before.st_size
        row = dict(path=path, mode=oct(before.st_mode), size=before.st_size, sha256=sha)
        if stage is None:
            owned[path] = row
        else:
            rows[path] = dict(row, git=stage)
    for path, value in parents.items():
        st = path.lstat()
        assert (st.st_dev, st.st_ino, st.st_mode) == value, path
    return rows, owned, size


def discover():
    head = run(['git', 'rev-parse', 'HEAD']).decode().strip()
    parents = run(['git', 'rev-list', '--parents', '-n1', 'HEAD']).decode().split()
    index_raw = run(['git', 'ls-files', '--stage', '-z'], 'delta reconstructed index')
    tree_raw = run(['git', 'ls-tree', '-r', '-z', 'HEAD'], 'same stage0 rows as index: mode SP blob SP oid TAB path NUL')
    status = run(['git', 'status', '--porcelain=v1', '-z', '--untracked-files=all'])
    others = run(['git', 'ls-files', '--others', '--exclude-standard', '-z'])
    index = {}
    for row in index_raw.split(b'\0')[:-1]:
        stage, path = row.split(b'\t', 1)
        mode, oid, slot = stage.decode().split()
        p = path_name(path)
        assert p not in index and mode in {'100644', '100755'} and slot == '0', p
        index[p] = stage.decode()
    reconstructed_tree = b''.join(
        f'{mode} blob {oid}\t{p}'.encode() + b'\0'
        for p, stage in index.items()
        for mode, oid, _ in [stage.split()]
    )
    # Git tree ordering can differ from flattened index ordering at directory boundaries.
    assert set(reconstructed_tree.split(b'\0')) == set(tree_raw.split(b'\0'))
    if reconstructed_tree != tree_raw:
        RECORDS[-3]['stdout_representation'] = 'recursive Git tree ordering of exact HEAD, all rows equal to index'
    untracked = [path_name(p) for p in others.split(b'\0')[:-1]]
    status_untracked = [path_name(p[3:]) for p in status.split(b'\0')[:-1] if p.startswith(b'?? ')]
    assert set(untracked) == set(status_untracked)
    assert all(p.startswith(b'?? ') for p in status.split(b'\0')[:-1]), status
    return head, parents, index_raw, tree_raw, status, index, untracked


def base_rows():
    assert run(['git', 'rev-parse', BASE_COMMIT+':'+BASE_PATH]).decode().strip() == BASE_BLOB
    packed = run(['git', 'cat-file', 'blob', BASE_BLOB], 'approved immutable dictionary by blob')
    assert len(packed) == 5167269 and digest(packed) == BASE_HASH
    raw = gzip.decompress(packed)
    assert len(raw) == 31683177 and digest(raw) == EXPANDED_HASH
    base = json.loads(raw)
    assert set(base) == {'head', 'status', 'files'}
    rows = {}
    for row in base['files']:
        assert set(row) == {'path', 'git', 'mode', 'size', 'sha256'}
        p = path_name(row['path'].encode())
        assert p not in rows and stat.S_ISREG(int(row['mode'], 8))
        rows[p] = row
    assert len(rows) == 109980
    return rows


def verify_source(rows):
    e = '5a53a893dd7a18335ec42fc363b4f2baaf6650c5'
    g = '011c3c600f8a465e73129b70c3593b334a3ac65a'
    for ancestor in (BASE_COMMIT, e, g):
        run(['git', 'merge-base', '--is-ancestor', ancestor, 'HEAD'])
    wanted = {'01M6CYVMQKVCA2Y5SY7WPYNRE9':('WP73','approved'),
              '01M6N9KRM414MQEEE09EHKKHRF':('WP74','approved'),
              '01M6NBS97FQ5BC02HHAC9WJQAQ':('WP75','approved'),
              '01M6NC0FFKQG8WAE5F8AMXCCYB':('WP76','in_progress')}
    events = [json.loads(l) for l in (MISSION/'status.events.jsonl').read_text().splitlines()]
    chosen={a['event_id']:a for a in events if a['event_id'] in wanted}
    assert {k:(a['wp_id'],a['to_lane']) for k,a in chosen.items()}==wanted
    assert chosen['01M6N9KRM414MQEEE09EHKKHRF']['evidence']['review']['reference']==e
    assert chosen['01M6NBS97FQ5BC02HHAC9WJQAQ']['evidence']['review']['reference']==g
    product=('internal','cmd','go.mod','go.sum')
    def tree(commit):
        raw=run(['git','ls-tree','-r','-z',commit,'--',*product],
                'exact immutable Git tree by command and commit')
        return {path_name(p):h.decode() for h,p in
                (r.split(b'\t',1) for r in raw.split(b'\0')[:-1])}
    inherited=tree(BASE_COMMIT)
    approved_e=tree(e)
    approved_g=tree(g)
    actual=tree('HEAD')
    e_source={'internal/document/'+p for p in ('README.md','history.go','bold_authoring.go','bold_authoring_test.go')}
    g_source={'internal/editor/'+p for p in ('README.md','session.go','new_binding.go','bold_authoring.go','bold_authoring_test.go')}
    differences={}
    for p in sorted(inherited.keys()|actual.keys()):
        if inherited.get(p)==actual.get(p):
            continue
        if p in e_source or p.startswith(('internal/document/evidence/bold-authoring/',
                                          'internal/document/evidence/reference_controller/')):
            expected=approved_e
        elif p in g_source or p.startswith('internal/editor/evidence/bold-authoring/'):
            expected=approved_g
        else:
            raise AssertionError(('unapproved H product drift',p))
        assert actual.get(p)==expected.get(p),(p,actual.get(p),expected.get(p))
        differences[p]={'before':inherited.get(p),'after':actual.get(p),
                        'approved':e if expected is approved_e else g}
    assert e_source|g_source <= differences.keys()
    base=base_rows()
    for p,record in actual.items():
        expected=base.get(p)
        if expected and expected['git']==rows[p]['git']:
            assert rows[p]['sha256']==expected['sha256'],p
        else:
            raw=run(['git','cat-file','blob',record.split()[2]],'exact approved Git blob')
            assert digest(raw)==rows[p]['sha256'],p
    for folder,ref,expected_sha in (
        ('internal/document/evidence/bold-authoring/',e,'1baf8f84cbdde73e24b64aa2a050cbf8a63392e9150374d0e6778d598ca25bbe'),
        ('internal/editor/evidence/bold-authoring/',g,'7b5cc32141eef040e88daee86cbc774468d48eb466a34b1add7d4e81248bbec6')):
        seal=run(['git','show',ref+':'+folder+'SEAL.json'])
        assert digest(seal)==expected_sha==rows[folder+'SEAL.json']['sha256']
        members=json.loads(seal)['files']
        assert {p for p in rows if p.startswith(folder)}=={folder+r['path'] for r in members}|{folder+'SEAL.json'}
        for r in members:
            assert rows[folder+r['path']]['sha256']==r['sha256'],r['path']
    roots=['docs/research/reference-runs','docs/research/continuation',
           'internal/editor/testdata','internal/macro/runtime/testdata','internal/macro/wpm/testdata',
           'kitty-specs/wp51-parity-01M64CVY/contracts/native-fixtures.json']
    fixture_counts={}
    for root in roots:
        old=run(['git','ls-tree','-z',BASE_COMMIT,'--',root])
        cur=run(['git','ls-tree','-z','HEAD','--',root])
        assert old and cur,root
        a={p:r for p,r in rows.items() if p==root or p.startswith(root+'/')}
        if old!=cur:
            # The approved G/E ancestry may add research or controller records.
            # Existing H fixture files are individually protected regardless.
            raw=run(['git','ls-tree','-r','-z',BASE_COMMIT,'--',root],
                    'exact immutable H73 Git subtree by command and commit')
            for record in raw.split(b'\0')[:-1]:
                head,path=record.split(b'\t',1)
                mode,kind,oid=head.decode().split()
                assert kind=='blob' and a[path_name(path)]['git']==f'{mode} {oid} 0',path
        fixture_counts[root]=len(a)
    for path in ['internal/tui/evidence/reveal-anchors/run_pty.py','internal/tui/evidence/wp52/run_pty.py',
                 'docs/research/continuation/macro-executable/pty_test.py',
                 'docs/research/continuation/macro-executable/terminal.py']:
        assert digest(run(['git','show',BASE_COMMIT+':'+path]))==rows[path]['sha256'],path
    assert not any(p in rows for p in ('go.work','vendor/modules.txt'))
    return dict(events=chosen,issued_prompt=dict(path=str(PROMPT),sha256=digest(PROMPT.read_bytes())),
                inherited_product_count=len(inherited),current_product_count=len(actual),
                product_differences=differences,fixture_counts=fixture_counts,approved_e=e,approved_g=g)


def census(phase, output):
    started = time.monotonic()
    first = discover()
    head, parents, index_raw, _, status, index, untracked = first
    if phase == 'before':
        assert not status
    else:
        assert all(p.startswith(str(EVIDENCE.relative_to(ROOT))+'/') for p in untracked)
    rows, owned, size = read_rows(index, untracked)
    assert discover() == first
    base = base_rows()
    removed = sorted(base.keys() - rows.keys(), key=str.encode)
    upserts = [rows[p] for p in sorted(rows, key=str.encode) if rows[p] != base.get(p)]
    removed_set = set(removed)
    rebuilt = {p: r for p, r in base.items() if p not in removed_set}
    rebuilt.update({r['path']: r for r in upserts})
    assert rebuilt == rows
    canonical = [rows[p] for p in sorted(rows, key=str.encode)]
    rebuilt_index = b''.join((r['git']+'\t'+r['path']).encode()+b'\0' for r in canonical)
    assert rebuilt_index == index_raw
    delta = dict(schema='wordling-custody-reference-delta/v1', phase=phase, head=head,
                 base=dict(commit=BASE_COMMIT, path=BASE_PATH, blob=BASE_BLOB,
                           compressed_sha256=BASE_HASH, expanded_sha256=EXPANDED_HASH),
                 status_porcelain_v1_z_hex=status.hex(), removed=removed, upserts=upserts,
                 rows=len(rows), canonical_rows_sha256=digest(compact(canonical)),
                 index_stdout_bytes=len(index_raw), index_stdout_sha256=digest(index_raw),
                 index_reconstruction='git TAB path NUL, UTF8 byte order',
                 census_seconds=time.monotonic()-started, working_bytes_read=size)
    write_gz(output/(phase+'-delta.json.gz'), delta)
    receipt = dict(head=head, parents=parents, checkout=str(ROOT),
                   git_common_dir=run(['git','rev-parse','--git-common-dir']).decode().strip(),
                   owned_untracked=list(owned.values()))
    if phase == 'before':
        receipt['source_equivalence'] = verify_source(rows)
    else:
        prior = json.loads(gzip.decompress((EVIDENCE/'before-delta.json.gz').read_bytes()))
        prior_removed = set(prior['removed'])
        original = {p:r for p,r in base.items() if p not in prior_removed}
        original.update({r['path']:r for r in prior['upserts']})
        changes = {p for p in original.keys()|rows.keys() if original.get(p)!=rows.get(p)}
        expected = {'internal/tui/'+p for p in ['README.md','model.go','bold_authoring.go','bold_authoring_test.go']}
        assert changes == expected, sorted(changes)
        receipt['tracked_changes'] = sorted(changes)
    receipt['commands'] = RECORDS
    write_gz(output/(phase+'-receipt.json.gz'), receipt)
    print(json.dumps(dict(phase=phase, files=len(rows), bytes_read=size, removals=len(removed),
                          upserts=len(upserts), owned_untracked=len(owned), seconds=time.monotonic()-started)))


if __name__ == '__main__':
    phase = sys.argv[1]
    destination = TMP if phase == 'before' else EVIDENCE
    try:
        census(phase, destination)
    except BaseException:
        write_gz(destination/(phase+'-failed-command-receipts.json.gz'), RECORDS)
        raise
