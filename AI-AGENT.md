# AI agent guide — using this converter as a base

Read this if you (Claude / other LLM agent) have been asked to convert
another CloudFormation-native Landing Zone to LZA UC, or extend this
converter. Assumes you've read `README.md` and `REUSABILITY.md`.

## Mental model

**Engine + profile split, dispatch-table driven.** `src/common.py` +
`src/mappers/*.py` + `src/profile.py` are `[GEN]` — reusable across LZ
variants. `src/profiles/<name>.py` is `[TH]` — everything else lives
there. Adding a source LZ = new profile file, no engine changes for
common cases.

## Pipeline order (do NOT rearrange lightly)

```
L1 extraction (deterministic, per-domain mapper)
   ↓
schema audit (jsonschema vs cached LZA schemas)
   ↓
L2 pass (reasoning-driven — you fill gaps L1 left)
   ↓
engine dry-run (LZA config-validator.ts — real gate)
   ↓
reviewer hand-port (TODO stubs, real emails, CFN stub authoring)
```

Each layer catches what the previous missed. **Never skip layers.** The
schema audit catches shape errors; the engine catches cross-references
+ AWS-native format constraints (emails, AZ naming) the schema doesn't
express.

## Boundary rules — [GEN] vs [TH]

Before adding a constant / function / helper, decide which side of the
boundary it lives on.

| Kind of decision                                    | Bucket | Where          |
|-----------------------------------------------------|--------|----------------|
| CFN intrinsic resolver (`Ref`, `Fn::Join`, …)       | GEN    | `common.py`    |
| Dispatch by CFN Type (`Custom::*`, `AWS::EC2::VPC`) | GEN    | `mappers/*.py` |
| LZA schema field name / shape                       | GEN    | `mappers/*.py` |
| Source-LZ file names + roles                        | TH     | `profiles/*.py`|
| Accelerator prefix, home region, ASN default        | TH     | `profiles/*.py`|
| Account naming convention                           | TH     | `profiles/*.py`|
| Default OU targets for policies                     | TH     | `profiles/*.py`|
| Regional pinning / partition                        | TH     | `profiles/*.py`|

If you're about to hard-code a source-LZ string in a mapper, stop —
push it up to the profile.

## Working with the schema audit

**Always** validate against LZA source schema before extending a mapper.
Use `gh api` (no clone needed):

```bash
gh api repos/awslabs/landing-zone-accelerator-on-aws/contents/source/packages/@aws-accelerator/config/lib/<name>-config.ts \
  | python3 -c "import json,sys,base64; print(base64.b64decode(json.load(sys.stdin)['content']).decode())"
```

Or for JSON schema:

```bash
gh api repos/awslabs/landing-zone-accelerator-on-aws/contents/source/packages/@aws-accelerator/config/lib/schemas/<name>-config.json
```

Do this **before** emitting new fields. Invented fields (like the
initial `guardduty.malwareProtection`) waste time; schema-grep catches
them in seconds.

## L1 → L2 handoff protocol

- L1 emits deterministic output + `unmapped/<domain>.json` with reason +
  hint per gap.
- L2 reads `unmapped/*.json`, applies reasoning-driven fixes. Sources
  for L2 decisions:
  - The source LZ's readme (deploy steps often name real targets)
  - Nested-stack CFN files (parent → child parameter wiring reveals intent)
  - Source repo commits, related samples
- L2 output paths:
  - Fixes that generalize → update mapper's profile constants or dispatch
  - Reviewer-only choices → `reports/<profile>/*-l2-cluster.md`
  - Real blockers → `customizations-config.yaml` passthrough entry

## Handling "no first-class LZA UC field" cases

1. Verify via LZA source schema (`gh api` grep — must confirm, not guess).
2. If genuinely absent: use `mappers/customizations.py` aggregator queue.
   Call `register_file_passthrough(...)` or `register_<specific>(...)`.
   Persist policy body / template body under
   `out/<profile>-uc/customizations/<subdir>/`.
3. Emit reviewer note describing what CFN stub they must author.

Do NOT invent fake fields. Do NOT hand-edit generated YAML — fix the
mapper.

## Common failure modes (observed patterns)

- **CFN YAML short-tag load failure** → use `common._yaml_load_cfn`
  (extends SafeLoader with `!Ref/!GetAtt/!Sub/!ImportValue/…`).
- **Values wrapped in intrinsics** (`Ref`, `Fn::FindInMap`, `Fn::Sub`,
  `Fn::Join`) → use `common.resolve_ref` which handles all four; extend
  it if you find a new intrinsic pattern.
- **`Fn::Sub` with pseudo-params** like `${AWS::Region}` → resolver
  returns unchanged; use domain-specific extractor (see
  `mappers/network._short_service` for the pattern).
- **Custom resources backed by Lambdas** — the Lambda / IAM / LogGroup /
  KMS aren't domain; only the `Custom::*` resource's Properties are.
  Add backing types to `BACKING_TYPES` set, dispatch `Custom::*` to
  a handler.
- **Multiple LZA schema versions for same field** (e.g. replacements V1
  vs V2) — check anyOf branches in the JSON schema; pick the shape
  that supports what you're expressing.
- **Empty required list** — many LZA fields require empty `[]` not
  missing key. Schema audit surfaces these fast.

## When to build engine features vs profile-level workarounds

Extend the engine (`[GEN]`) if:
- New CFN Type appears in ≥2 LZ variants (add handler)
- New CFN intrinsic pattern appears (extend resolver)
- New "no UC field" case appears (add registrar in customizations)
- New LZA schema field type appears (extend mapper builder)

Keep it in the profile (`[TH]`) if:
- Naming convention (subnet suffix scheme, account name style)
- Region/partition choice
- Deployment-target OU defaults
- Which source files play which role

If in doubt, ask: "would a second source LZ benefit from this being
generic?" If yes, `[GEN]`. If it's a customer/source choice, `[TH]`.

## Testing your changes

```bash
# Fast loop — 3 commands
rm -rf converter/out/<profile>-uc                             # clean
python3 -m converter.src.run --profile <name>                 # regenerate
python3 -m converter.src.schema_audit                         # validate
```

Engine dry-run only when schema audit is 0 errors:

```bash
cd lza-engine/source/packages/@aws-accelerator/accelerator
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE \
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY \
AWS_MAX_ATTEMPTS=1 AWS_REGION=<home-region> PARTITION=aws \
npx ts-node lib/config-validator.ts /path/to/converter/out/<profile>-uc
```

Iterate 3-5 times normal. Each iteration cluster errors by type + fix
in bulk.

## What to write in NOTES.md when you land a change

- **[GEN]** if the change is engine-level and benefits future profiles.
- **[TH]** if it's profile-only.
- **[REWORK]** if you deferred something.
- **[RISK]** if you emitted a stub that could ship broken.
- Cite file paths + line numbers. Note counters (mapped/unmapped/dropped
  deltas). Note what upstream source data you used to make the decision.

Future-you (or the next agent) reads NOTES.md to understand why the
converter is shaped the way it is. Terse is fine; missing is not.

## What to hand back to the human

Every conversion run should produce:
1. Updated `converter/out/<profile>-uc/` — the 8 config YAMLs
2. Updated `converter/reports/<profile>/` — coverage + schema + engine
   dry-run + l2-cluster
3. Updated (or new) `converter/CONVERSION-SUMMARY.md` — reviewer-facing
   single doc
4. Updated `NOTES.md` — running log entry with date, counters, decisions
5. `TODO stubs` explicitly enumerated in the summary — never leave a
   silent stub

## Anti-patterns (do not do)

- ❌ Hand-edit generated YAML to fix a validator error. Fix the mapper.
- ❌ Invent a schema field without grep-verifying it exists. Wastes iterations.
- ❌ Skip schema audit + jump to engine dry-run. Schema audit is cheaper.
- ❌ Skip engine dry-run because schema audit passed. Engine catches more.
- ❌ Attempt mechanical translation of network routing detail without
   hand-review. LZA models routing at higher abstraction — cluster and
   defer instead.
- ❌ Add profile-specific strings to `[GEN]` files. Push to profile.
- ❌ Silently drop a source resource. Always emit a mapped/unmapped/dropped
   entry with reason.
- ❌ Trust `{{ tokens }}` will resolve without SSM/inline value backing.
   LZA V2 replacements need explicit `type` + either `value` (String/Number)
   or `path` (SSM).

## Convergence signal

Engine dry-run "remaining issues" count monotonically decreases across
iterations. When the count matches the enumerated TODO stubs in
`CONVERSION-SUMMARY.md` §Manual work checklist exactly (no unaccounted
diff), you're done — hand back to reviewer.

Example (Thailand): remaining issues count converges to the enumerated
TODO stubs in the summary.
