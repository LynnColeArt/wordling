"""Exercise save staging and replacement failures through the editor."""
from pathlib import Path
import sys

from physical_cases import choose_backup
from qualification import ENTER, F1, F10, Run, native


def exercise(run, syscall, backup_enabled):
    target = "ORIGINAL.WP"
    fixture = run.repo / "internal/document/testdata/fast_save_yes/SECOND.WP"
    run.seed(fixture, target)
    original_path = run.p.work / target
    original = original_path.read_bytes()
    backup = run.p.work / "ORIGINAL.BK!"
    backup.write_bytes((fixture.parent / "FIRST.WP").read_bytes())
    prior_backup = backup.read_bytes()
    trace = run.folder / "save-failure.strace"
    if syscall == "write-limit":
        run.p.argv[:0] = [
            sys.executable, "-c",
            "import os,resource,signal,sys; "
            "signal.signal(signal.SIGXFSZ,signal.SIG_IGN); "
            "resource.setrlimit(resource.RLIMIT_FSIZE,(128,128)); "
            "os.execv(sys.argv[1],sys.argv[1:])",
        ]
    elif syscall:
        run.p.argv[:0] = [
            "strace", "--kill-on-exit", "-f", "-o", str(trace),
            "-e", f"trace={syscall}", "-e", f"inject={syscall}:error=EIO:when=1",
        ]
    run.launch()
    choose_backup(run, backup_enabled)
    run.step("REPLACEMENT", "type replacement")
    run.step(F10, "native Save", "Document to be saved:")
    run.step(target, "name original")
    run.step(ENTER, "observe original target", f"Replace {target}?")
    if not syscall:
        run.p.work.chmod(0o500)
    try:
        run.step("y", "confirm replacement")
        run.wait("PublicationFailed" if syscall == "renameat2" else "CandidateFailed")
    finally:
        if not syscall:
            run.p.work.chmod(0o700)
    if syscall in ("fsync", "renameat2"):
        assert "(INJECTED)" in trace.read_text()
    assert original_path.read_bytes() == original
    assert backup.read_bytes() == prior_backup
    assert any("REPLACEMENT" in line for line in run.rows())
    assert not list(run.p.work.glob(".wordling-candidate-*"))
    run.step(F1, "cancel failed target prompt")
    if syscall not in ("fsync", "write-limit"):
        run.save("RETRY.WP", body_fragment=b"REPLACEMENT")
        assert native(run.p.work / "RETRY.WP")[2] == b"REPLACEMENT"
    run.exit_application()


if __name__ == "__main__":
    repo, binary, output = (Path(arg).resolve() for arg in sys.argv[1:])
    for label, syscall, backup_enabled in (
        ("create-denied", None, True),
        ("partial-write", "write-limit", True),
        ("stage-sync", "fsync", True),
        ("replace-backup-on", "renameat2", True),
        ("replace-backup-off", "renameat2", False),
    ):
        run = Run(repo, binary, output / label, classic_canvas=True)
        try:
            exercise(run, syscall, backup_enabled)
        except Exception as error:
            run.finish(repr(error), label)
            raise
        else:
            run.finish(None, label)
