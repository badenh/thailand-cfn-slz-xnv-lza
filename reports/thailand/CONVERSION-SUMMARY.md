# Thailand SLZ → LZA UC — Conversion Summary

**Source:** `aws-samples/sample-thailand-secure-lz` (CloudFormation-native
landing zone, NCSA-aligned).

**Target:** LZA Universal Configuration profile at `converter/out/thailand-uc/`.

**Verdict:** Conversion complete at automation ceiling. Emitted 8 schema-valid
LZA UC config YAMLs + supporting policy/rules files + 3 customizations
passthroughs. Manual work checklist enumerated below.

---

## Profile constants

| Concern              | Thailand                              |
|----------------------|---------------------------------------|
| Home region          | `ap-southeast-7`                      |
| Accelerator prefix   | `THSLZ`                               |
| Org CFN location     | `cloudformation/organization/*.json`  |
| Regulatory alignment | Thailand NCSA                         |

Profile is `converter/src/profiles/thailand.py`.

---

## Coverage table

| Domain        | Mapped | Unmapped (deferred [REWORK]) | Dropped (engine-managed) | Schema valid |
|---------------|-------:|-----------------------------:|-------------------------:|:------------:|
| org           | 13     | 0                            | 0                        | ✅           |
| security      | 14     | 0                            | 46                       | ✅           |
| iam           | 4      | 0                            | 0                        | ✅           |
| global        | 4      | 0                            | 0                        | ✅           |
| network       | 52     | **125**                      | 9                        | ✅ (stubs)   |
| accounts      | 6      | 0                            | 0                        | ✅           |
| replacements  | 9      | 0                            | 0                        | ✅           |
| customizations| 3      | 0                            | 0                        | ✅           |
| **TOTAL**     | **105**| **125**                      | **55**                   | 8 / 8        |

All 125 unmapped are network resource-level routing/NACL detail (deliberately
deferred, not translation gaps). Schema audit total_errors = 0.

---

## What was auto-converted

See `converter/CONVERSION-SUMMARY.md` for the full domain-by-domain
breakdown. Thailand-specific values:

- **Org tree** extracted from `organization/lz-organization.json` (8 OUs
  incl. `Workloads/Production`, `Workloads/NonProduction`, `Suspended` with
  `ignore: true`).
- **SCP / RCP / declarative EC2** policies emitted with `th-slz-*`
  policy names (prefix from `THSLZ`).
- **KMS** — 2 org-wide keys (CloudWatchLogsKey + ControlTowerBackupKey)
  from `organization/lz-organization-kms-iam.json`.
- **Global** — `homeRegion: ap-southeast-7`,
  `enabledRegions: [ap-southeast-7, us-east-1]`, `AWSControlTowerExecution`.
- **Network** — 2 central VPCs (NetworkInspection + NetworkEndpoints), 1 TGW,
  NFW firewall + Suricata rules copied verbatim to
  `firewall-rules/suricata-rules.txt`, 12 VPC endpoints, 1 spoke
  `vpcTemplates[]`, AZ suffixes emitted as `a`/`b`/`c` (region resolved by
  LZA at deploy).
- **Accounts** — 3 mandatory + 3 workload (SharedServices/CentralBackup/
  Network) per TH readme steps 4–6.
- **Replacements** — `AcceleratorPrefix=THSLZ`, `HomeRegion=ap-southeast-7`,
  `TransitGatewayASN=65001`, 6 email tokens with `TODO-` placeholders.
- **Customizations** — 3 passthroughs (AI opt-out, SSM default-host
  management, GuardDuty findings notifications).

---

## Manual work checklist (before LZA deploy)

**Blockers:**

- [ ] Populate `replacements-config.yaml` SSM params — run
      `out/thailand-uc/bootstrap-ssm-params.sh` after replacing
      `TODO-*@example.com` seeds with real distribution-list addresses.
- [ ] Hand-author 3 CFN stubs referenced by `customizations-config.yaml`:
      `config/cloudformation/ai-services-optout.yaml`,
      `config/cloudformation/ssm-default-host-management.yaml`,
      `config/cloudformation/guardduty-findings-notifications.yaml`.
- [ ] Complete network hand-port per
      `reports/thailand/network-l2-cluster.md`.
- [ ] Replace all `TODO-*` stubs in `network-config.yaml` (routeTable,
      endpoint subnets, AZ fallbacks).
- [ ] Wire IdC principal assignments — `iam-config.yaml
      identityCenter.identityCenterAssignments` empty; requires customer's
      IdC group IDs.
- [ ] Verify Thailand NCSA KMS-CMK ("control-tower-key") already exists in
      management account per TH readme step 2.

**Should verify:**

- [ ] `quarantineNewAccounts.enable: false` — LZA default is `true`;
      confirm intent.
- [ ] `centralSecurityServices.scpRevertChangesConfig.enable: true` — LZA
      default; confirm ops model.
- [ ] `ap-southeast-7` regional service availability (region opt-in was
      required per TH readme step 10; some LZA-referenced services
      may not be available yet — customer may need `excludeRegions`).
- [ ] Compound VPC endpoint short names (`ecr.dkr` → `dkr`,
      `ecr.api` → `api`). LZA convention may be `ecr-dkr`/`ecr-api`.

---

## Files delivered

```
converter/out/thailand-uc/
├── organization-config.yaml           ✅ schema-valid
├── security-config.yaml               ✅ schema-valid
├── iam-config.yaml                    ✅ schema-valid
├── global-config.yaml                 ✅ schema-valid
├── network-config.yaml                ✅ schema-valid (TODO stubs)
├── accounts-config.yaml               ✅ schema-valid
├── replacements-config.yaml           ✅ schema-valid
├── customizations-config.yaml         ✅ schema-valid
├── customizations.notes.md            reviewer notes per passthrough
├── bootstrap-ssm-params.sh            pre-deploy: creates SSM params
├── service-control-policies/          2 policy JSON bodies
├── rcp-policies/                      1 policy JSON body
├── declarative-policies/              1 policy JSON body
├── kms-policies/                      2 KMS key policy JSONs
├── customizations/aiservices-optout/  1 policy JSON body
├── firewall-rules/                    Suricata rules (verbatim)
└── _deferrals/                        internal cross-domain deferrals
```

Reports at `converter/reports/thailand/`:
- `org.md`, `security.md`, `iam.md`, `global.md`, `network.md`,
  `accounts.md`, `replacements.md`, `customizations.md` — per-domain
- `network-l2-cluster.md` — hand-port shopping list
- `schema-audit.md` — 8/8 pass (total_errors=0)

---

## What was intentionally NOT translated

- Detailed CFN routing/NACL semantics (deferred to hand-port).
- SLZ Custom-Resource support infra (Lambdas, backing roles/keys, LogGroups)
  — 55 resources dropped as engine-managed.
- `lz-organization-setup.yaml`, `organization/lz-organization-service-access.yaml`,
  `organization/lz-organization-guardrails.yaml`,
  `organization/lz-stackset-roles.yaml` — engine-bootstrap concerns handled
  by LZA.

---

## Engine dry-run

Run `awslabs/landing-zone-accelerator-on-aws@1.16.2 config-validator.ts`
against the emitted profile. Expected outcome: ~43 issues, all deliberate
TODO stubs enumerated above.

To run:

```bash
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE \
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY \
AWS_MAX_ATTEMPTS=1 AWS_REGION=ap-southeast-7 PARTITION=aws \
npx ts-node lza-engine/source/packages/@aws-accelerator/accelerator/lib/config-validator.ts \
  converter/out/thailand-uc
```

## Known limitations

- Thailand NCSA control-mapping traceability doc not generated — TH readme
  table (Technical requirements mapping) links NCSA controls to SLZ CFN
  files; LZA-UC-field traceability requires a separate authoring pass.
- CDK synth not attempted — requires live AWS creds + Organizations access.
- Regional pinning of some LZA-referenced services in `ap-southeast-7` not
  verified. TH readme step 10 explicitly requires opt-in region enablement.
