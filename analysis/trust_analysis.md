# Trust Relationship Analysis

This document analyzes IAM role trust policies to understand
which identities are allowed to assume which roles.

This analysis focuses on trust breadth and restriction, not abuse.

## Trust Relationship Overview

This section documents which principals are allowed to assume IAM roles
based on role trust policies. The goal is to understand trust boundaries,
not to assess abuse or exploitation.

### Amazon_EventBridge_Invoke_Sns_1545616246

- Principal type: AWS service
- Trusted principal: events.amazonaws.com
- Trust scope: Account-restricted
- Conditions present:
  - aws:SourceAccount
  - aws:SourceArn (specific EventBridge rule)

This role is assumable only by Amazon EventBridge within the same AWS account
and is further restricted to a specific EventBridge rule.

### AWSServiceRoleForResourceExplorer

- Principal type: AWS service
- Trusted principal: resource-explorer-2.amazonaws.com
- Trust scope: Service-linked
- Conditions present: None

This is an AWS service-linked role used by AWS Resource Explorer.
The trust relationship allows assumption only by the associated AWS service.

### AWSServiceRoleForSupport

- Principal type: AWS service
- Trusted principal: support.amazonaws.com
- Trust scope: Service-linked
- Conditions present: None

This role is used by AWS Support to perform account-level support
and administrative functions on behalf of the customer.

### AWSServiceRoleForTrustedAdvisor

- Principal type: AWS service
- Trusted principal: trustedadvisor.amazonaws.com
- Trust scope: Service-linked
- Conditions present: None

This role enables AWS Trusted Advisor to access resources
for cost, performance, and security recommendations.

### VPCFlowLogs-Cloudwatch-1768680094945

- Principal type: AWS service
- Trusted principal: vpc-flow-logs.amazonaws.com
- Trust scope: Account-restricted
- Conditions present:
  - aws:SourceAccount
  - aws:SourceArn (VPC flow log resource)

This role is assumable only by the VPC Flow Logs service
for flow log resources within the same AWS account.

## Trust Relationship Summary

All observed IAM roles are trusted exclusively by AWS service principals.
No roles are trusted by IAM users, external accounts, or wildcard principals.

Trust policies are either service-linked or explicitly restricted
to AWS services operating within the same account.
