from pathlib import Path
from qualification import F5, F7, Run, SWITCH, native
import subprocess, sys, json, time
base=Path(sys.argv[2]).resolve()
binary=Path(sys.argv[1]).resolve()
workspace=base/'workspace'
workspace.mkdir(parents=True)
def run(name, cue, prefix=()):
 r=Run(Path.cwd(),binary,base/name)
 r.p.env['XDG_CACHE_HOME']=str(base/'cache')
 r.p.argv[r.p.argv.index('-root')+1]=str(workspace)
 r.p.proc=subprocess.Popen([*prefix, *r.p.argv],stdin=r.p.slave,stdout=r.p.slave,stderr=subprocess.PIPE,env=r.p.env)
 r.wait(cue)
 return r
def crash(r):
 r.p.proc.kill()
 r.p.proc.wait()
 r.p.close()
def normal(r):
 r.exit_application()
 r.finish(None,'normal exit')

def quit_all(r, screens, label):
    r.step(b"\x1b=", "focus menu")
    r.step("f", "open File", "Quit Wordling")
    r.step("q", "quit all documents")
    for screen in screens:
        r.wait(f"Save document {screen} before quitting?")
        r.step("n", "skip save")
    r.p.proc.wait(timeout=4)
    assert r.p.proc.returncode == 0
    r.finish(None, label)

r=run('first','Doc 1 Pg')
r.step('FIRST','edit one','FIRST')
r.step(SWITCH,'open second','Doc 2 Pg')
r.step('SECOND','edit two','SECOND')
r.until(lambda:any(len(json.loads(p.read_bytes())['Records'])==2 for p in (base/'cache').rglob('documents.json')), 'autosave both',timeout=8)
crash(r)
r=run('interrupted','Recover documents')
r.step(' ','uncheck second')
r.step(b'\r','review deletion','Permanently delete 1')
crash(r)
r=run('restore','Recover documents')
assert sum('[x]' in row for row in r.rows())==2
r.step(' ','uncheck second')
r.step(b'\r','review deletion','Permanently delete 1')
r.step('y','commit recovery','FIRST')
r.step(b'\x1b[21~','save recovered doc','Document to be saved:')
r.step('RESTORE.WP','name')
r.step(b'\r','publish')
r.until(lambda:(workspace/'RESTORE.WP').is_file(),'restored file')
assert native(workspace/'RESTORE.WP')[2]==b'FIRST'
normal(r)
r=run('clean','Doc 1 Pg')
assert 'Recover documents' not in '\n'.join(r.rows())
r.step('DISCARD','edit')
normal(r)
r=run('clean-again','Doc 1 Pg')
normal(r)

def new_document(run):
    run.step(b"\x1b=", "focus menu")
    run.step("f", "open File", "New Document")
    run.step("n", "create another document")

def check_tabs(run, count):
    row = run.rows()[1]
    assert sum(f"Doc {i}" in row for i in range(1, 7)) == count, row

def choose_three(run):
    run.step(" ", "uncheck newest document")
    run.step(b"\x1b[B", "move down")
    run.step(b"\x1b[B", "move down")
    run.step(" ", "uncheck middle document")
    run.step(b"\r", "review selection", "Permanently delete 2")

def fill(run, count):
    for i in range(1, count + 1):
        if i > 1:
            new_document(run)
        run.step(f"BUFFER{i}", "edit independent document", f"BUFFER{i}", 2)
    check_tabs(run, count)
    run.until(
        lambda: any(len(json.loads(p.read_bytes())["Records"]) == count
                    for p in (base / "cache").rglob("documents.json")),
        "autosave all open documents", timeout=8,
    )

r = run("five", "Doc 1 Pg")
fill(r, 5)
crash(r)
r = run("five-interrupted", "Recover documents")
choose_three(r)
crash(r)
restore_started = time.monotonic()
r = run("five-retry", "Recover documents")
assert sum("[x]" in row for row in r.rows()) == 5
choose_three(r)
r.step("y", "commit three selected documents", "BUFFER4", 2)
check_tabs(r, 3)
# Click each restored tab by its actual position in the visible row.
for tab, value in enumerate(("BUFFER4", "BUFFER2", "BUFFER1"), 1):
    x = r.rows()[1].index(f"Doc {tab}") + 1
    r.step(f"\x1b[<0;{x};2M".encode(), f"click tab {tab}", value, 2)
# Save the active third tab and kill Wordling before its first scheduled autosave.
r.step(b"\x1b[21~", "save third tab", "Document to be saved:")
r.step("SAVED.WP", "name saved document")
r.step(b"\r", "publish saved document")
saved = workspace / "SAVED.WP"
r.wait("Doc 3 SAVED.WP ", 1)
crash(r)
assert time.monotonic() - restore_started < 5, "crash missed the first autosave boundary"
assert native(saved)[2] == b"BUFFER1"

r = run("immediate-crash", "Recover documents")
assert sum("[x]" in row for row in r.rows()) == 2
r.step(b"\r", "restore the two unsaved documents before any further edits", "Doc 1 Pg")
check_tabs(r, 2)
original_tabs = {}
for tab in (1, 2):
    x = r.rows()[1].index(f"Doc {tab}") + 1
    r.step(f"\x1b[<0;{x};2M".encode(), f"inspect unsaved tab {tab}", f"Doc {tab} Pg")
    original_tabs[tab] = r.rows()[2].strip()
assert sorted(original_tabs.values()) == ["BUFFER2", "BUFFER4"]

for tab, value in original_tabs.items():
    x = r.rows()[1].index(f"Doc {tab}") + 1
    r.step(f"\x1b[<0;{x};2M".encode(), f"click unsaved tab {tab}", value, 2)
    r.step("UPDATED", "add edits after the first recovery", value + "UPDATED", 2)

def autosaved_bodies():
    import base64
    bodies = []
    for path in (base / "cache").rglob("documents.json"):
        for record in json.loads(path.read_bytes())["Records"]:
            raw = base64.b64decode(record["Native"])
            offset = int.from_bytes(raw[4:8], "little")
            bodies.append(raw[offset:])
    return sorted(bodies)

expected = [b"BUFFER2UPDATED", b"BUFFER4UPDATED"]
r.until(lambda: autosaved_bodies() == expected, "wait for next autosave of both edits", timeout=70)
crash(r)
r = run("two-unsaved", "Recover documents")
assert sum("[x]" in row for row in r.rows()) == 2
r.step(b"\r", "restore only the two unsaved documents", "Doc 1 Pg")
check_tabs(r, 2)
restored = []
for tab in (1, 2):
    x = r.rows()[1].index(f"Doc {tab}") + 1
    r.step(f"\x1b[<0;{x};2M".encode(), f"inspect restored tab {tab}", f"Doc {tab} Pg")
    restored.append(r.rows()[2].strip().encode())
assert sorted(restored) == expected, restored
assert native(saved)[2] == b"BUFFER1"
crash(r)
r = run("discard-two", "Recover documents")
r.step("d", "uncheck all")
r.step(b"\r", "review discard all", "Permanently delete 2")
r.step("y", "discard all", "Doc 1 Pg")
normal(r)

r = run("six", "Doc 1 Pg")
fill(r, 6)
new_document(r)
r.wait("six documents are already open")
check_tabs(r, 6)
crash(r)
r = run("six-restore", "Recover documents")
assert sum("[x]" in row for row in r.rows()) == 6
r.step(b"\r", "restore all six", "Doc 1 Pg")
check_tabs(r, 6)
for tab, value in enumerate(reversed(range(1, 7)), 1):
    x = r.rows()[1].index(f"Doc {tab}") + 1
    r.step(f"\x1b[<0;{x};2M".encode(), f"click restored tab {tab}", f"BUFFER{value}", 2)
quit_all(r, (6, 1, 2, 3, 4, 5), "six restored documents, clean quit")
r = run("after-six", "Doc 1 Pg")
normal(r)

# Stop the native replacement at syscall entry using strace fault injection.
# EINTR suppresses the exchange itself and SIGKILL prevents Wordling's rollback.
original = saved.read_bytes()
r = run("three-for-interrupted-save", "Doc 1 Pg")
fill(r, 3)
crash(r)

trace = base / "interrupted-save.strace"
r = run("crash-during-save", "Recover documents", (
    "strace", "-f", "-o", str(trace), "-e", "trace=renameat2",
    "-e", "inject=renameat2:error=EINTR:signal=SIGKILL:when=1",
))
assert sum("[x]" in row for row in r.rows()) == 3
r.step(b"\r", "restore the three documents", "BUFFER3", 2)
check_tabs(r, 3)
r.step(b"\x1b[21~", "save recovered document", "Document to be saved:")
r.step(saved.name, "name the existing native file")
r.step(b"\r", "request overwrite", f"Replace {saved.name}?")
r.step("y", "start native replacement")
assert r.p.proc.wait(timeout=5) == -9
r.p.close()

exchanges = [line for line in trace.read_text().splitlines() if "renameat2(" in line]
assert len(exchanges) == 1, exchanges
assert all(part in exchanges[0] for part in (
    '".wordling-candidate-', f'"{saved.name}"', "RENAME_EXCHANGE",
)), exchanges
assert "killed by SIGKILL" in trace.read_text()
assert saved.read_bytes() == original
assert any(native(candidate)[2] == b"BUFFER3"
           for candidate in workspace.glob(".wordling-candidate-*"))

r = run("after-interrupted-save", "Recover documents")
assert sum("[x]" in row for row in r.rows()) == 3
r.step(b"\r", "restore all three after the interrupted save", "Doc 1 Pg")
check_tabs(r, 3)
restored = []
for tab in (1, 2, 3):
    x = r.rows()[1].index(f"Doc {tab}") + 1
    r.step(f"\x1b[<0;{x};2M".encode(), f"inspect recovered tab {tab}", f"Doc {tab} Pg")
    restored.append(r.rows()[2].strip())
assert sorted(restored) == ["BUFFER1", "BUFFER2", "BUFFER3"], restored
assert saved.read_bytes() == original
quit_all(r, (3, 1, 2), "three restored after interrupted save, clean quit")

r = run("after-staging-crash", "Doc 1 Pg")
r.step(F5, "open List Files after the interrupted save", "Dir C:")
r.step(b"\r", "show the workspace listing", f"{saved.stem:<8}{saved.suffix}")
assert ".wordling-candidate-" not in "\n".join(r.rows())
r.step(F7, "close List Files", "Doc 1 Pg")
r.step("LATER", "write a fresh document")
r.step(b"\x1b[21~", "save a fresh replacement", "Document to be saved:")
r.step(saved.name, "name the existing native file")
r.step(b"\r", "request replacement after interrupted save", f"Replace {saved.name}?")
r.step("y", "confirm the later replacement")
r.until(lambda: native(saved)[2] == b"LATER", "new save supersedes the intact original")
normal(r)
