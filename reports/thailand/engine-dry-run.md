# Thailand LZA engine dry-run

Ran `awslabs/landing-zone-accelerator-on-aws` `config-validator.ts` against
`converter/out/thailand-uc/` with dummy AWS creds (fail-fast on SSM).

## Total issues: 43

All 43 issues are deliberate TODO stubs from the automation ceiling —
zero unexpected engine errors.

| Category                                     | Count | Source                                             |
|----------------------------------------------|------:|----------------------------------------------------|
| `Invalid email {{ *Email }}` (dupe per acct) | 12    | 6 workload accounts × 2 error lines each          |
| Missing customizations CFN template          | 3     | Reviewer authors 3 stubs                          |
| `route table "TODO-rt" does not exist`       | 27    | Deferred network hand-port                        |
| `interfaceEndpoints target subnet "TODO-endpoint-subnet-a" does not exist` | 1 | Deferred                              |

All remaining issues are enumerated TODO stubs in `CONVERSION-SUMMARY.md`.

## AWS creds warning

Expected. Validator hits SSM to resolve replacements at startup — with
dummy creds it emits:

```
UnrecognizedClientException: The security token included in the request is invalid.
in accounts-config.yaml config file
```

Not a config error. Ignored.

## Reproduce

```bash
cd lza-engine/source && \
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE \
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY \
AWS_MAX_ATTEMPTS=1 AWS_REGION=ap-southeast-7 PARTITION=aws \
npx ts-node packages/@aws-accelerator/accelerator/lib/config-validator.ts \
  /Users/badenh/claudetemp/th-convert-slz2lza/converter/out/thailand-uc
```
