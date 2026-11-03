"""Closed errors for the one-leaf TEST authority foundation (Apache-2.0)."""

class Refusal(RuntimeError):
    def __init__(self, code, *, partial=False):
        self.code = code
        self.partial = partial
        super().__init__(code)


class Opaque:
    """Trusted same-interpreter capabilities are never persistent value objects."""
    def __copy__(self):
        raise Refusal('CapabilityNotCopyable')

    def __deepcopy__(self, memo):
        raise Refusal('CapabilityNotCopyable')

    def __reduce_ex__(self, protocol):
        raise Refusal('CapabilityNotSerializable')
