# SLZ → LZA UC converter

Convert CloudFormation-native Landing Zone samples (like
`aws-samples/sample-thailand-secure-lz`) into a Landing Zone Accelerator
Universal Configuration (LZA UC) profile.

## Upstream repos (clone as siblings before running)

This repo only contains the converter. The source LZ templates, the LZA
engine, and the LZA UC schemas live in upstream AWS repos. Clone them as
siblings of `converter/` before running anything:

```bash
git clone https://github.com/aws-samples/sample-thailand-secure-lz.git
git clone https://github.com/awslabs/landing-zone-accelerator-on-aws.git lza-engine
git clone https://github.com/aws/lza-universal-configuration.git
```

Expected layout after cloning:

```
<workspace>/
├── converter/                          this repo
├── sample-thailand-secure-lz/          source LZ (Thailand)
├── lza-engine/                         LZA engine (for dry-run validator)
└── lza-universal-configuration/        LZA UC schemas + docs
```

- **What it does:** reads a source LZ's CFN templates, emits 8 schema-valid
  LZA UC config YAMLs + supporting policy/rule files + customizations
  passthroughs for anything without a first-class LZA UC field.
- **What it doesn't do:** mechanically translate CFN-level route/NACL/TGW
  wiring — those are marked as `TODO-*` stubs for hand-port.
- **Ceiling:** ~80% auto. Remaining 20% is deliberate hand-port + reviewer
  choices (real emails, IdC assignments, network routing detail).

## Reference conversion

Thailand profile results:

| Output                          | Thailand                                     |
|---------------------------------|----------------------------------------------|
| UC config profile               | `converter/out/thailand-uc/`                 |
| Per-domain coverage reports     | `converter/reports/thailand/`                |
| Network hand-port shopping list | `converter/reports/thailand/network-l2-cluster.md` |
| Engine dry-run report           | `converter/reports/thailand/engine-dry-run.md`     |
| Schema audit                    | `converter/reports/thailand/schema-audit.md`       |

Reviewer-facing summary: `converter/CONVERSION-SUMMARY.md`.

Read `CONVERSION-SUMMARY.md` first if you're a reviewer picking this up
cold.

---

## Quickstart

```bash
# Prereqs: python3, pyyaml, jsonschema, gh CLI, node/yarn (for engine dry-run)

# Rerun a conversion from scratch (pick profile via env var)
CONVERTER_PROFILE=thailand python3 -m converter.src.run           # writes 8 YAML configs
CONVERTER_PROFILE=thailand python3 -m converter.src.l2_reports    # emits network hand-port list
CONVERTER_PROFILE=thailand python3 -m converter.src.schema_audit  # validates vs LZA JSON schemas
```

Output lands under `converter/out/<profile>-uc/`.

## Optional: engine dry-run (real LZA validator)

```bash
# lza-engine should already be cloned as a sibling (see Upstream repos above)
cd ../lza-engine/source
yarn install
(cd packages/@aws-lza && yarn build)
(cd packages/@aws-accelerator/config && yarn build)
(cd packages/@aws-accelerator/accelerator && yarn build)

# Run validator with dummy creds (fail-fast on any SSM call)
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE \
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY \
AWS_MAX_ATTEMPTS=1 AWS_REGION=<home-region> PARTITION=aws \
npx ts-node packages/@aws-accelerator/accelerator/lib/config-validator.ts \
  /path/to/converter/out/<profile>-uc
```

Interpret validator output against `CONVERSION-SUMMARY.md` §Manual work
checklist — every remaining engine complaint should match a documented
TODO stub.

## Convert a different source LZ

See `REUSABILITY.md` — engine is source-agnostic; new source = new profile
file under `src/profiles/`. Copy `_template.py`, fill constants, run.

## What you'll need to do by hand after the converter finishes

Full list: `CONVERSION-SUMMARY.md` §Manual work checklist. Highlights:

- Replace `TODO-*@example.com` placeholders with real distribution lists
- Hand-author 3 CFN stubs referenced by `customizations-config.yaml`
- Hand-port network detail per `network-l2-cluster.md` (routing, NACLs,
  TGW attachments — LZA models these at higher abstraction than CFN)
- Replace `TODO-rt` / `TODO-endpoint-subnet-a` stubs in `network-config.yaml`
- Wire IdC principal assignments (customer's IdC group IDs required)
- Verify regional service availability for your home region

## Directory layout

```
converter/
├── README.md                      you are here
├── CONVERSION-SUMMARY.md          reviewer-facing per-conversion summary
├── REUSABILITY.md                 how to add a new source-LZ profile
├── NOTES.md                       dev running log (phasing/rework/decisions)
├── AI-AGENT.md                    guide for AI systems doing similar work
├── src/
│   ├── run.py                     pipeline entrypoint
│   ├── schema_audit.py            validate emitted YAMLs vs LZA schemas
│   ├── l2_reports.py              cluster + summarize unmapped items
│   ├── common.py                  generic helpers (CFN loader, intrinsics)
│   ├── profile.py                 profile loader (env / --profile CLI)
│   ├── mappers/                   per-domain CFN → UC mapping
│   └── profiles/
│       ├── thailand.py            Thailand SLZ profile
│       └── _template.py           starting point for new profiles
├── out/<profile>-uc/              generated UC config profile
├── reports/<profile>/             coverage + audit reports
└── unmapped/<profile>/            machine-readable unmapped items (for L2)
```

## Troubleshooting

- **"unknown domain"** — check `run.py DOMAINS` dict; typo in CLI arg.
- **Empty output, no errors** — check `CONVERTER_PROFILE` env var; likely
  a typo silently loaded wrong profile.
- **Schema audit 51 errors** — did you rebuild after editing a mapper?
  Run `rm -rf out/<profile>-uc/` then `python -m converter.src.run`.
- **Engine validator hangs 2+ min** — you have real AWS creds active
  and it's trying real SSM API calls with retries. Use dummy creds +
  `AWS_MAX_ATTEMPTS=1` per Quickstart above.
- **"Additional properties are not allowed"** — schema drift. LZA JSON
  schemas at `converter/.schemas/` are cached; delete + rerun
  `schema_audit.py` to refetch from the LZA repo.
