# WP104 original fixed-resource/ROM recheck

Verdict: **APPROVE the bounded static ORIGINAL preparation/foreground composition and fixed VGA-ROM binding as an explicit WP104 source-contract clarification, with the correction below: pin the already-public exact sizes now.** No generic P API or additional prerequisite package is identified for these five roles. This is architecture/source guidance, not a grant, real original fit test, source approval of an unseen implementation, or permission to probe/run original assets.

## Public facts resolve all sizes

`docs/research/continuation/code-pair-history/final-preflight.json`, `/baseline_identities/0..4`, records every expected size/hash/path below. Receipt SHA256 `065ed1c9c192755ca2a5d5009ae13ab9e5f344946a05560f3a322369b38c29b9`. The same set appears in `preparation/sealed-plan.json` SHA256 `f601796cfb9ad2b4beb388adc9ba81cb5bc75f8d6f16920e41d5d424dd10da39` and committed prelaunch receipts. All hashes match current public environment.json. These are existing metadata facts, not fresh stat/read of their targets. Adversarial coerced/mutation registry copies are not used as authority.

| Role | Existing expected size | Hash from public matching receipt/profile |
|---|---:|---|
| boot | 1,474,560 | e7b599780eef4f0a068a47185aca00f30b37971a85c54084c881729e544ed4ca |
| disk | 67,108,864 | ba1a6a5f475c0f6487697be10654566d164bb8c4d091ed8709d48260e9dc72e1 |
| QEMU | 26,359,752 | 28fa14f1c45fca7422e3ec5737768b33b705de2f31014a76e658d4263464a6a5 |
| BIOS | 262,144 | 1a9ea4f17bcfb27bda5728e2c21d9fa074cf7947b9b4910bb28213a735c96735 |
| VGA BIOS | 39,424 | 4eecd8e752efc02c6c0fe87eb92bf66934cb9ea67b0e1bc41e86f8430c8bf8a0 |

Required correction: do not describe these four expected sizes as undiscovered or postpone their definition to a caller-filled generic future object. Source-owned OriginalResourcePlan can pin the fixed five role/path/hash/size expectations now, with exact type/bounds and no extra/duplicate/substituted roles. A later accepted ORIGINAL candidate/row must bind that exact plan and actual declared operations/aggregate fit. Missing/changed facts refuse before private/store/guard effects; a new real resource version requires explicit profile/source review. Historical expected metadata is not proof of present inode/bytes/tool fitness: actual current capture remains UNKNOWN/unrun until a later genuine authorized release. Search evidence is retained separately in wp104-public-resource-size-search.json; no private asset was inspected.

## Approved P can express it without new authority

Actual `Session._spec` accepts ResourceArgument only over registered SourceLease/WorkingLease and passes the retained reference. Worker command_spec resolves/validates the actual lease and constructs prefix+source-owned path+suffix; callers cannot replace it with observed path/size/hash facts (`lifetime.py:540–551,1176–1205`). QEMU is a real captured SourceLease→ExecutableLease; four declared boot/disk/BIOS/VGA sources can be prepared as four WorkingLeases, with returned mutation successor where applicable. `prepare` enforces the existing resource/copy ceilings (`artifacts.py:453–497`); do not create a fifth working resource or parallel Session to accommodate firmware.

The fixed argument pair can be constructed as:

```text
'-global', ResourceArgument('VGA.romfile=', prepared_vga_lease, '')
```

alongside fixed `-vga std`; BIOS remains a retained lease argument to `-bios`, and boot/disk use fixed `file=` prefix/drive suffix. No generic `-global` selector/property/path callback, raw public path authority or legacy guest.arguments call is admitted. The new sealed code derives the reviewed finite constants from guest.py ancestry; it must not import the old eager/global launcher. Omit daemonize/pidfile, keep one foreground, fixed source-owned endpoint and original offline limits.

Four prepared base files total68,884,992 bytes; five captured base sources total95,244,744 bytes. Each expected file fits64MiB, the four base copies fit128MiB and captured base set fits256MiB. These sums are **not** a complete 4GiB IO/time/RSS/FD/command/source/transfer/response proof: repeated source verification, preparation/helper sources, full capture/copy/readback, derivation/output and cleanup must still fit the original immutable all-phase budget. Unknown actual fit cannot be zeroed or converted into a cap increase. Additional sources are counted normally under existing32-source ceiling; no extra working-file exemption is inferred.

## QEMU8.2.2 primary source verification

Upstream tagged8.2.2 supports `-global driver.property=value` for machine-created devices and defines `-vga std` as standard VGA with Bochs VBE extensions. [QEMU8.2.2 option source](https://github.com/qemu/qemu/blob/v8.2.2/qemu-options.hx#L531-L552), [VGA option](https://github.com/qemu/qemu/blob/v8.2.2/qemu-options.hx#L2158-L2174).

For PCI VGA, `pci_vga_init` maps VGA_STD to actual device type `VGA`; that type inherits the PCI `romfile` string property and defaults to `vgabios-stdvga.bin`. [PCI device selection/property](https://github.com/qemu/qemu/blob/v8.2.2/hw/pci/pci.c#L1801-L1811), [VGA type/default](https://github.com/qemu/qemu/blob/v8.2.2/hw/display/vga-pci.c#L354-L383). The selected pc-i440fx profile uses the PCI path; this is not a universal claim about ISA/non-PC VGA. PC VGA initialization chooses the PCI route when its PCI bus is present. [PC initialization](https://github.com/qemu/qemu/blob/v8.2.2/hw/i386/pc.c#L1035-L1048).

PCI realization uses its class default only when no instance romfile is supplied. The ROM loader resolves/loads the chosen file and fails if absent/empty. Hence the fixed prepared path prevents this default VGA ROM lookup from silently reopening the unretained installed default. Explicit-ROM handling also differs from default-ROM handling in the conditional PCI-ID patch path; record it as an exact reviewed argv binding rather than asserting bit-identical historical execution. [PCI ROM loading](https://github.com/qemu/qemu/blob/v8.2.2/hw/pci/pci.c#L2024-L2035), [loader/default handling](https://github.com/qemu/qemu/blob/v8.2.2/hw/pci/pci.c#L2177-L2265). This is tagged-source reasoning, not an observed run of Ubuntu's patched packaged binary; its actual version/hash and authorized later fitness remain required.

## Scope disposition

WP104 already owns original.py/original_release.py/issuance/bootstrap, fixed QEMU preparation/foreground composition and explicit firmware/resource closure. Pinning existing expected sizes and this exact `VGA.romfile` retained argument implements that contract without changing generic P/account/ownership or adding another device, authority or lifecycle. Record this review/reference and precise argv/data-plan change in WP104's source design/manifest before freeze; do not hide it as an arbitrary option allowlist. It needs a bounded reviewed clarification, not a new WP106/API predecessor. Separate wider runtime option/profile changes would require fresh review.

WP104 must still deliver actual ORIGINAL code composition, not a permanently hardcoded refusal stub presented as that delivery. Its current CONTROL-only roster and stage guard must keep ORIGINAL unreleasable until WP105 route, WP101 exact recipe/plan/source review and a later genuine ROOT ORIGINAL decision. Real original current fitness, readiness, native semantics and full budget remain UNKNOWN. Static harmless/schema tests can verify role completeness, exact size/caps and lease-shaped argv/refusal before effects; they cannot masquerade as actual P capture of private originals. Independent final source/CONTROL review remains separate.

Read-only committed metadata/source and public upstream source investigation only. No private asset stat/read, shared-guard probe, tool/image invocation, original/QEMU process, Mac job, Git/index/runtime/source mutation, grant or leaf occurred.
