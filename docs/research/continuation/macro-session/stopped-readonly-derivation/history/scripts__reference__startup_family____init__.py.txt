"""Wordling generic reference startup family; no original-software authority."""
from .engine import Failure, Limits, Identity, Result, EndpointSpec, decode_json
from .artifacts import ArtifactSpec, CommandSpec
from . import engine, lifetime

API_VERSION = 1


class Attempt:
    """Compatibility composition adapter over the single supervision kernel."""

    def __init__(self, directory, limits=Limits()):
        self._kernel = engine.LegacyKernel(directory, limits, ArtifactSpec, CommandSpec)

    @property
    def limits(self):
        return self._kernel.limits

    @property
    def directory(self):
        return self._kernel.directory

    @property
    def fd(self):
        return self._kernel.fd

    @property
    def directory_identity(self):
        return self._kernel.directory_identity

    @property
    def journal(self):
        return self._kernel.journal

    def copy(self, source, name):
        return self._kernel.copy(source, name)

    def snapshot(self, sources):
        return self._kernel.snapshot(sources)

    def publish(self, name, value):
        return self._kernel.publish(name, value)

    def run(self, command, *, before_spawn=None, readiness=None, after_identity=None):
        return self._kernel.run(command, before_spawn=before_spawn, readiness=readiness,
                                after_identity=after_identity)

    def close(self):
        return self._kernel.close()

    def __enter__(self):
        self._kernel.__enter__()
        return self

    def __exit__(self, *args):
        return self._kernel.__exit__(*args)

from .artifacts import (SourceObservation, SourceRequest, StreamPolicy, SourceLease, WorkingLease,
                        ExecutableLease, MutationSpec, LaunchSpec, ResourceArgument, NewWorkspace)
from .lifetime import (SharedEnvelopePolicy, UsageObservation, ManagedPolicy, StartupFailure, Session, ProcessLease, CheckedChannel,
                       IdentityObservation, ReadyObservation, IOObservation, Snapshot,
                       MutationResult, ExitObservation, PartialOutcome, SessionOutcome, open_session)


def source_binding():
    root,dev,ino,closure=_source_binding
    return dict(root=root,device=dev,inode=ino,version=API_VERSION,sha256=dict(closure))
