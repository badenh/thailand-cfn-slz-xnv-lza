# Coverage report: security

- mapped: 14
- unmapped: 0
- dropped: 46

## Mapped

- lz-account-baseline.yaml::SSMDefaultHostManagement -> Custom::SSMDefaultHostManagement -> (ack)
- lz-account-baseline.yaml::SSMSessionPreferences -> Custom::SSMSessionPreferences -> (ack)
- lz-account-baseline.yaml::EC2DataProtectionSecurity -> Custom::EC2DataProtectionSecurity -> centralSecurityServices.ebsDefaultVolumeEncryption
- lz-account-baseline.yaml::CustomPasswordPolicy -> Custom::SetPasswordPolicy -> iamPasswordPolicy
- lz-account-baseline.yaml::S3PublicAccessBlock -> Custom::S3PublicAccessBlock -> centralSecurityServices.s3PublicAccessBlock
- lz-audit-guardduty.yaml::GuardDutyConfiguration -> Custom::GuardDutyConfiguration -> centralSecurityServices.guardduty
- lz-audit-guardduty-notifications.yaml::<file> -> customizations-config.yaml passthrough (guardduty-findings-notifications)
- lz-delegate-security-services.yaml::SecurityServicesAdminDelegation -> Custom::SecurityServicesAdminDelegation -> (ack)
- lz-delegate-firewall-manager-ipam.yaml::AdminDelegation -> Custom::AdminDelegation -> (ack)
- lz-audit-access-analyzer.json::OrganizationAccessAnalyzer -> AWS::AccessAnalyzer::Analyzer -> accessAnalyzer
- organization/lz-organization-kms-iam.json::CloudWatchLogsKey -> keyManagementService.keySets[cloudwatch-logs-key]
- organization/lz-organization-kms-iam.json::CloudWatchLogsKeyAlias -> attached to KeyConfig (implicit)
- organization/lz-organization-kms-iam.json::ControlTowerBackupKey -> keyManagementService.keySets[control-tower-backup-key]
- organization/lz-organization-kms-iam.json::ControlTowerBackupKeyAlias -> attached to KeyConfig (implicit)

## Unmapped (feed to L2)

_(none)_

## Dropped (intentional — engine handles)

- **lz-account-baseline.yaml::EbsDefaultEncryptionKey** — engine-managed backing infra (AWS::KMS::Key)
- **lz-account-baseline.yaml::EbsDefaultEncryptionKeyAlias** — engine-managed backing infra (AWS::KMS::Alias)
- **lz-account-baseline.yaml::CloudWatchEncryptionKey** — engine-managed backing infra (AWS::KMS::Key)
- **lz-account-baseline.yaml::CloudWatchEncryptionKeyAlias** — engine-managed backing infra (AWS::KMS::Alias)
- **lz-account-baseline.yaml::AWSSystemsManagerDefaultEC2InstanceManagementRole** — engine-managed backing infra (AWS::IAM::Role)
- **lz-account-baseline.yaml::EC2LambdaExecutionRole** — engine-managed backing infra (AWS::IAM::Role)
- **lz-account-baseline.yaml::SSMDefaultHostManagementLambdaLogGroup** — engine-managed backing infra (AWS::Logs::LogGroup)
- **lz-account-baseline.yaml::SSMDefaultHostManagementLambda** — engine-managed backing infra (AWS::Lambda::Function)
- **lz-account-baseline.yaml::SSMSessionPreferencesLambdaLogGroup** — engine-managed backing infra (AWS::Logs::LogGroup)
- **lz-account-baseline.yaml::SSMSessionPreferencesLambda** — engine-managed backing infra (AWS::Lambda::Function)
- **lz-account-baseline.yaml::EC2DataProtectionSecurityUpdateLambda** — engine-managed backing infra (AWS::Lambda::Function)
- **lz-account-baseline.yaml::EC2DataProtectionSecurityUpdateLambdaLogGroup** — engine-managed backing infra (AWS::Logs::LogGroup)
- **lz-account-baseline.yaml::SetPasswordPolicyLambdaLogGroup** — engine-managed backing infra (AWS::Logs::LogGroup)
- **lz-account-baseline.yaml::SetPasswordPolicyLambda** — engine-managed backing infra (AWS::Lambda::Function)
- **lz-account-baseline.yaml::S3LambdaExecutionRole** — engine-managed backing infra (AWS::IAM::Role)
- **lz-account-baseline.yaml::S3PublicAccessBlockLambda** — engine-managed backing infra (AWS::Lambda::Function)
- **lz-account-baseline.yaml::S3PublicAccessBlockLambdaLogGroup** — engine-managed backing infra (AWS::Logs::LogGroup)
- **lz-account-baseline.yaml::SessionManagerLogGroup** — engine-managed backing infra (AWS::Logs::LogGroup)
- **lz-account-baseline.yaml::SSMLambdaExecutionRole** — engine-managed backing infra (AWS::IAM::Role)
- **lz-audit-guardduty.yaml::GuardDutyCloudWatchEncryptionKey** — engine-managed backing infra (AWS::KMS::Key)
- **lz-audit-guardduty.yaml::GuardDutyCloudWatchEncryptionKeyAlias** — engine-managed backing infra (AWS::KMS::Alias)
- **lz-audit-guardduty.yaml::LambdaExecutionRole** — engine-managed backing infra (AWS::IAM::Role)
- **lz-audit-guardduty.yaml::GuardDutyConfigurationLambda** — engine-managed backing infra (AWS::Lambda::Function)
- **lz-audit-guardduty.yaml::GuardDutyConfigurationLambdaLogGroup** — engine-managed backing infra (AWS::Logs::LogGroup)
- **lz-audit-guardduty-notifications.yaml::EventBridgeRole** — included in whole-file customizations passthrough
- **lz-audit-guardduty-notifications.yaml::SNSTopic** — included in whole-file customizations passthrough
- **lz-audit-guardduty-notifications.yaml::SNSTopicPolicy** — included in whole-file customizations passthrough
- **lz-audit-guardduty-notifications.yaml::SNSTopicEncryptionKey** — included in whole-file customizations passthrough
- **lz-audit-guardduty-notifications.yaml::SNSTopicEncryptionKeyAlias** — included in whole-file customizations passthrough
- **lz-audit-guardduty-notifications.yaml::EventBridgeRule** — included in whole-file customizations passthrough
- **lz-audit-guardduty-notifications.yaml::SNSSubscriptionFunction** — included in whole-file customizations passthrough
- **lz-audit-guardduty-notifications.yaml::CloudWatchEncryptionKey** — included in whole-file customizations passthrough
- **lz-audit-guardduty-notifications.yaml::CloudWatchEncryptionKeyAlias** — included in whole-file customizations passthrough
- **lz-audit-guardduty-notifications.yaml::SNSSubscriptionFunctionRole** — included in whole-file customizations passthrough
- **lz-audit-guardduty-notifications.yaml::SNSSubscriptionFunctionLogGroup** — included in whole-file customizations passthrough
- **lz-audit-guardduty-notifications.yaml::SNSSubscriptions** — included in whole-file customizations passthrough
- **lz-delegate-security-services.yaml::LambdaExecutionRole** — engine-managed backing infra (AWS::IAM::Role)
- **lz-delegate-security-services.yaml::SecurityServicesAdminDelegationLambda** — engine-managed backing infra (AWS::Lambda::Function)
- **lz-delegate-security-services.yaml::SecurityServicesAdminDelegationLambdaLogGroup** — engine-managed backing infra (AWS::Logs::LogGroup)
- **lz-delegate-security-services.yaml::SecurityServicesAdminCloudWatchEncryptionKey** — engine-managed backing infra (AWS::KMS::Key)
- **lz-delegate-security-services.yaml::SecurityServicesAdminEncryptionKeyAlias** — engine-managed backing infra (AWS::KMS::Alias)
- **lz-delegate-firewall-manager-ipam.yaml::LambdaExecutionRole** — engine-managed backing infra (AWS::IAM::Role)
- **lz-delegate-firewall-manager-ipam.yaml::AdminDelegationLambda** — engine-managed backing infra (AWS::Lambda::Function)
- **lz-delegate-firewall-manager-ipam.yaml::LogGroupKey** — engine-managed backing infra (AWS::KMS::Key)
- **lz-delegate-firewall-manager-ipam.yaml::AdminDelegationLambdaLogGroup** — engine-managed backing infra (AWS::Logs::LogGroup)
- **organization/lz-organization-kms-iam.json::EC2SSMServiceRole** — IAM role for KMS key access — engine-managed under LZA
