#!/usr/bin/env python3
"""Build a candidate and record its exact tracked production inputs."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess

PRODUCTION = ["cmd", "internal", "go.mod", "go.sum"]


def capture(repo, *args, env=None):
    return subprocess.check_output(args, cwd=repo, text=True, env=env)


def objects(data):
    decoder = json.JSONDecoder()
    while data := data.lstrip():
        item, end = decoder.raw_decode(data)
        yield item
        data = data[end:]


def hash_path(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("repo", type=Path)
    p.add_argument("out", type=Path)
    p.add_argument("--goos", choices=("linux", "darwin", "windows"))
    p.add_argument("--goarch", choices=("amd64", "arm64"))
    p.add_argument("--qa-save-faults", action="store_true", help="non-release binary with opt-in save fault hooks")
    args = p.parse_args()
    repo, out = args.repo.resolve(), args.out.resolve()
    env = dict(os.environ, CGO_ENABLED="0")
    if args.goos:
        env["GOOS"] = args.goos
    if args.goarch:
        env["GOARCH"] = args.goarch
    goos = capture(repo, "go", "env", "GOOS", env=env).strip()
    goarch = capture(repo, "go", "env", "GOARCH", env=env).strip()
    out.mkdir()
    head = capture(repo, "git", "rev-parse", "HEAD").strip()
    status = capture(repo, "git", "status", "--porcelain", "--", *PRODUCTION)
    if status:
        raise RuntimeError(f"production sources are dirty:\n{status}")
    tags = ["-tags=wordling_qa" if args.qa_save_faults else "-tags="]
    package_data = capture(repo, "go", "list", "-buildvcs=false", *tags, "-deps", "-json", "./cmd/wordling", env=env)
    local = {}
    for package in objects(package_data):
        directory = Path(package["Dir"])
        if not directory.is_relative_to(repo):
            continue
        for field in ("GoFiles", "CgoFiles", "CFiles", "HFiles", "SFiles", "EmbedFiles", "SysoFiles"):
            for relative in package.get(field, []):
                path = directory / relative
                local[str(path.relative_to(repo))] = hash_path(path)
    expected_seam = "internal/storage/qualification_" + ("fault" if args.qa_save_faults else "normal") + ".go"
    other_seam = "internal/storage/qualification_" + ("normal" if args.qa_save_faults else "fault") + ".go"
    assert expected_seam in local and other_seam not in local, "build selected wrong QA seam"
    for name in ("go.mod", "go.sum"):
        local[name] = hash_path(repo / name)
    path = out / ("wordling.exe" if goos == "windows" else "wordling")
    # Go may otherwise select the parent repository's HEAD for a nested Git
    # worktree. Bind the actual compiled source above and omit that stamp.
    build = ["go", "build", *tags, "-trimpath", "-buildvcs=false", "-o", str(path), "./cmd/wordling"]
    subprocess.run(build, cwd=repo, check=True, env=env)
    if capture(repo, "git", "rev-parse", "HEAD").strip() != head:
        raise RuntimeError("candidate checkout moved while building")
    for name, digest in local.items():
        if hash_path(repo / name) != digest:
            raise RuntimeError(f"build input changed during compilation: {name}")
    if capture(repo, "git", "status", "--porcelain", "--", *PRODUCTION):
        raise RuntimeError("production sources became dirty while building")
    record = {
        "schema": 1, "qa_save_faults": args.qa_save_faults, "target": {"goos": goos, "goarch": goarch},
        "source_commit": head, "production_tree": {
            name: capture(repo, "git", "rev-parse", f"{head}:{name}").strip()
            for name in PRODUCTION
        },
        "build_command": build, "go_version": capture(repo, "go", "version").strip(),
        "build_metadata": capture(repo, "go", "version", "-m", str(path)),
        "compiled_local_input_sha256": dict(sorted(local.items())),
        "binary_sha256": hash_path(path), "binary_path": str(path),
    }
    (out / "candidate.json").write_text(json.dumps(record, indent=2) + "\n")


if __name__ == "__main__":
    main()
