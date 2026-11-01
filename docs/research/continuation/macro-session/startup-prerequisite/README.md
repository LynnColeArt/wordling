# WP61 startup-family evidence

Read [the component contract](CONTRACT.md) and [verification report](REPORT.md).
This is an offline generic TEST capability, not original-session permission.

Reproduce from this lane:

    python -B -m unittest discover -s tests/reference/startup-prerequisite -v
    python -B -m unittest discover -s tests/reference/startup-seam -p test_transport.py -v
    python -B scripts/reference/startup_transport.py managed-fixture streaming64m
    python -B tests/reference/startup-prerequisite/probe_large.py
    python -B tests/reference/startup-prerequisite/mutate.py /tmp/a-new-mutant-output
    python -B scripts/review_checks.py --junitxml=/tmp/startup-family-configured.xml

Old mutation/capture runners write historical WP58 paths: do not regenerate this
evidence with them. The new runner uses its explicit fresh output directory and
disposable source copies through real public entrypoints.
