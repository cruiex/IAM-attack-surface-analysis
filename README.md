# IAM Attack Surface & Privilege Escalation Analysis (AWS)

## Overview
This project performs a structured, read-only security analysis of AWS IAM
to evaluate identity attack surface and privilege escalation risk arising
from IAM misconfigurations or excessive permissions.

The focus is on understanding how far a non-admin identity could
theoretically progress due to IAM design choices, without exploiting,
modifying, or interacting with AWS resources beyond read-only access.

---

## Scope

### Included
- IAM users
- IAM roles
- Managed and inline IAM policies
- IAM trust relationships
- Privilege escalation path modeling (conceptual)

### Explicitly Excluded
- Any form of attack or exploitation
- EC2, VPC, Lambda, CloudTrail, EventBridge
- SOC, detection, or alerting workflows
- Modification of AWS resources or policies

---

## Methodology

1. **Read-only data collection**
   - IAM configuration collected using a dedicated IAMReadOnlyAccess audit user
   - Single point-in-time snapshot

2. **Identity and permission inventory**
   - Enumeration of IAM users, roles, and policy attachment models
   - Separation of raw data from analysis artifacts

3. **Trust relationship analysis**
   - Examination of role trust policies
   - Classification of service-linked, service-restricted, and human-accessible roles

4. **Privilege escalation modeling**
   - Logical reachability analysis based on IAM permissions and trust
   - No simulation or execution of escalation techniques

5. **Risk classification and recommendations**
   - Findings categorized as LOW / MEDIUM / HIGH
   - Remediation guidance aligned with least-privilege principles

---

## Project Structure

iam-attack-surface-analysis/
├── data/ Raw IAM data excluded to avoid exposing account metadata
├── analysis/ # Written security analysis
├── reports/ # Findings, risk summary, recommendations
├── src/ # Data collection scripts
├── README.md
├── requirements.txt
└── .gitignore


---

## Key Outcomes

- Complete IAM identity inventory
- Verification of trust boundaries between users and roles
- Identification (or absence) of privilege escalation paths
- Risk-based IAM security findings
- Actionable security recommendations


