# Security Recommendations

The following recommendations are based on the observed IAM configuration
and aim to further reduce identity attack surface and blast radius.

## Recommendation 1: Transition Administrative Access to Roles

Where feasible, replace long-lived administrative IAM users with
role-based access using temporary credentials.

This reduces credential exposure and improves access lifecycle control.

## Recommendation 2: Perform Periodic IAM Configuration Reviews

Regularly review IAM users, roles, policies, and trust relationships
to ensure permissions remain aligned with least-privilege principles.

## Recommendation 3: Maintain Strict Trust Policies for IAM Roles

Continue restricting IAM role trust policies to specific AWS services
and avoid granting role assumption to IAM users unless explicitly required.

