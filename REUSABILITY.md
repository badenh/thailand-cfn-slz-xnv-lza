# Converter reusability guide

Engine + profile split. Adding a second source-LZ = new profile file, no
engine changes.

## Layout

```
converter/src/
├── common.py            [GEN] CFN loader, intrinsic resolver, reports helpers
├── profile.py           [GEN] profile loader (env/CLI → module)
├── run.py               [GEN] pipeline dispatcher
├── schema_audit.py      [GEN] validates emitted YAMLs against LZA schemas
├── l2_reports.py        [GEN] post-L1 clustering + reviewer summaries
├── profiles/
│   ├── thailand.py      [TH]  Thailand SLZ constants
│   ├── _template.py     [GEN] template for new profiles
│   └── <yours>.py       [PROFILE] new profile you add
└── mappers/
    ├── org.py           [GEN] AWS::Organizations::* handlers
    ├── security.py      [GEN] Custom::* + AccessAnalyzer + KMS handlers
    ├── iam.py           [GEN] AWS::SSO::PermissionSet handlers
    ├── globalcfg.py     [GEN] synthesized global-config
    ├── network.py       [GEN] VPC/TGW/NFW/endpoint handlers
    ├── accounts.py      [GEN] synthesized accounts + replacements
    └── customizations.py [GEN] passthrough queue aggregator
```

Everything under `[GEN]` is reusable across LZ variants. Only `profiles/*.py`
is per-LZ.

## Adding a new profile

1. Clone your source LZ repo alongside `sample-thailand-secure-lz/`:
   ```
   /path/to/workdir/
   ├── converter/
   ├── sample-thailand-secure-lz/
   └── <your-source-lz>/            ← new
   ```
2. Copy the template:
   ```
   cp converter/src/profiles/_template.py converter/src/profiles/<name>.py
   ```
3. Fill in every constant (paths, prefix, source file names, account list,
   deployment-target defaults).
4. Run:
   ```
   python -m converter.src.run --profile <name>
   python -m converter.src.l2_reports
   python -m converter.src.schema_audit
   ```
5. Fix errors iteratively — most errors trace back to a missing/misnamed
   source file in the profile, or a source-LZ pattern the mappers don't yet
   recognize. In the latter case, extend the mapper's dispatch table
   (`CUSTOM_HANDLERS`, `BACKING_TYPES`, `FILE_TO_CUSTOMIZATIONS`, etc.) —
   these are `[GEN]` and benefit all future profiles.

## Selecting profile at runtime

- CLI: `python -m converter.src.run --profile <name>`
- Env var: `CONVERTER_PROFILE=<name> python -m converter.src.run`
- Default: `thailand`

## When you should extend the engine, not just the profile

Sign that you're stretching the profile too far:
- Adding a new `Custom::*` type your source LZ uses → extend
  `mappers/security.py CUSTOM_HANDLERS`
- Adding a new whole-file customizations passthrough pattern → extend
  `mappers/security.py FILE_TO_CUSTOMIZATIONS` (or equivalent per-domain)
- Adding a new CFN intrinsic pattern the resolver doesn't handle →
  extend `common.resolve_ref`
- Adding a new SLZ→UC field mapping the mapper doesn't emit → extend
  the relevant mapper's builder

These are engine changes and stay `[GEN]`. Any new profile inherits them
automatically.

## What stays profile-specific forever

- Which CFN files exist in the source LZ and what role they play
- Account naming conventions
- Regional pinning + partition
- Accelerator prefix
- Default deployment-target OU lists when source LZ passes targets at runtime

If a decision is domain-shape (LZA schema field name) it's `[GEN]`. If it's
a source-LZ convention or customer choice, it's profile-specific.
