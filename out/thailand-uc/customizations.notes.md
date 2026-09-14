# Customizations passthrough — reviewer notes

## THSLZ-ai-services-optout

Wrap AWS::Organizations::Policy Type=AISERVICES_OPT_OUT_POLICY with Content loaded from customizations/aiservices-optout/th-slz-ai-optout.json, TargetIds set to Root OU id, Name=THSLZ-th-slz-ai-optout.

## THSLZ-ssm-default-host-management

Hand-author CFN template with a custom resource that calls ssm:UpdateServiceSetting with SettingId '/ssm/managed-instance/default-ec2-instance-management-role' value 'AWSSystemsManagerDefaultEC2InstanceManagementRole'. Replaces SLZ Custom::SSMDefaultHostManagement from lz-account-baseline.yaml.

## THSLZ-guardduty-findings-notifications

Copy source SLZ template `lz-audit-guardduty-notifications.yaml` into config/cloudformation/guardduty-findings-notifications.yaml. GuardDuty findings → EventBridge → SNS → email subscriptions. No first-class LZA UC field. Passthrough entire template.
