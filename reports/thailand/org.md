# Coverage report: org

- mapped: 13
- unmapped: 0
- dropped: 0

## Mapped

- organization/lz-organization.json::WorkloadOrganizationalUnit -> organizationalUnits[Workloads]
- organization/lz-organization.json::WorkloadProductionOrganizationalUnit -> organizationalUnits[Production]
- organization/lz-organization.json::WorkloadNonProductionOrganizationalUnit -> organizationalUnits[NonProduction]
- organization/lz-organization.json::InfrastructureOrganizationalUnit -> organizationalUnits[Infrastructure]
- organization/lz-organization.json::ForensicOrganizationalUnit -> organizationalUnits[Forensic]
- organization/lz-organization.json::SandboxOrganizationalUnit -> organizationalUnits[Sandbox]
- organization/lz-organization.json::SuspendedOrganizationalUnit -> organizationalUnits[Suspended]
- organization/lz-organization.json::SecurityOrganizationalUnit -> organizationalUnits[Security]
- organization/lz-organization-scp-guardrails.json::BaselineGuardrailPolicy -> serviceControlPolicies[th-slz-guardrail] targets=['Infrastructure', 'Security', 'Workloads', 'Sandbox', 'Forensic'] (L2-resolved)
- organization/lz-organization-scp-guardrails.json::DeclarativePolicy -> declarativePolicies[EnforceAccountEC2Baseline] targets=['Root'] (L2-resolved)
- organization/lz-organization-scp-approved-services.json::ApprovedServicesPolicy -> serviceControlPolicies[th-slz-approved-services] targets=['Infrastructure', 'Security', 'Workloads', 'Sandbox', 'Forensic'] (L2-resolved)
- organization/lz-organization-rcp-guardrails.json::BaselineResourceGuardrailPolicy -> resourceControlPolicies[th-slz-resource-guardrail] targets=['Infrastructure', 'Security', 'Workloads', 'Sandbox', 'Forensic'] (L2-resolved)
- organization/lz-organization-ai-optout.json::AIServiceOptOutPolicy -> customizations-config.yaml passthrough (Type=AISERVICES_OPT_OUT_POLICY)

## Unmapped (feed to L2)

_(none)_

## Dropped (intentional — engine handles)

_(none)_
