import json
import os
import boto3

# Resolve paths safely (independent of where script is run)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DATA_DIR = os.path.join(BASE_DIR, "..", "data")

# IAM client (read-only credentials)
iam = boto3.client("iam")


def ensure_directories():

    paths = [
        BASE_DATA_DIR,
        os.path.join(BASE_DATA_DIR, "policies"),
        os.path.join(BASE_DATA_DIR, "policies", "managed"),
        os.path.join(BASE_DATA_DIR, "policies", "inline"),
    ]

    for path in paths:
        os.makedirs(path, exist_ok=True)

def json_serial(obj):

    if hasattr(obj, "isoformat"):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")


def collect_users():

    paginator = iam.get_paginator("list_users")
    users = []

    for page in paginator.paginate():
        users.extend(page.get("Users", []))

    output_path = os.path.join(BASE_DATA_DIR, "users.json")
    with open(output_path, "w") as f:
        json.dump(users, f, indent=2, default=json_serial)

    print(f"[+] Collected {len(users)} IAM users")

def collect_roles():

    paginator = iam.get_paginator("list_roles")
    roles = []

    for page in paginator.paginate():
        roles.extend(page.get("Roles", []))

    output_path = os.path.join(BASE_DATA_DIR, "roles.json")
    with open(output_path, "w") as f:
        json.dump(roles, f, indent=2, default=json_serial)

    print(f"[+] Collected {len(roles)} IAM roles")

def collect_trust_policies():

    paginator = iam.get_paginator("list_roles")
    trust_policies = []

    for page in paginator.paginate():
        for role in page.get("Roles", []):
            trust_policies.append({
                "RoleName": role.get("RoleName"),
                "Arn": role.get("Arn"),
                "AssumeRolePolicyDocument": role.get("AssumeRolePolicyDocument")
            })

    output_path = os.path.join(BASE_DATA_DIR, "trust-policies.json")
    with open(output_path, "w") as f:
        json.dump(trust_policies, f, indent=2, default=json_serial)

    print(f"[+] Collected trust policies for {len(trust_policies)} roles")

def collect_managed_policies():

    paginator = iam.get_paginator("list_policies")

    for page in paginator.paginate(Scope="All"):
        for policy in page.get("Policies", []):
            policy_arn = policy["Arn"]
            policy_name = policy["PolicyName"]
            default_version_id = policy["DefaultVersionId"]

            version = iam.get_policy_version(
                PolicyArn=policy_arn,
                VersionId=default_version_id
            )

            policy_document = {
                "PolicyName": policy_name,
                "Arn": policy_arn,
                "DefaultVersionId": default_version_id,
                "Document": version["PolicyVersion"]["Document"]
            }

            filename = f"{policy_name}.json"
            output_path = os.path.join(
                BASE_DATA_DIR, "policies", "managed", filename
            )

            with open(output_path, "w") as f:
                json.dump(policy_document, f, indent=2, default=json_serial)

    print("[+] Collected managed IAM policies")

def collect_inline_policies():

    # Inline policies for users
    user_paginator = iam.get_paginator("list_users")
    for page in user_paginator.paginate():
        for user in page.get("Users", []):
            user_name = user["UserName"]

            policy_names = iam.list_user_policies(
                UserName=user_name
            ).get("PolicyNames", [])

            for policy_name in policy_names:
                policy = iam.get_user_policy(
                    UserName=user_name,
                    PolicyName=policy_name
                )

                policy_document = {
                    "AttachedTo": "User",
                    "UserName": user_name,
                    "PolicyName": policy_name,
                    "Document": policy["PolicyDocument"]
                }

                filename = f"user_{user_name}_{policy_name}.json"
                output_path = os.path.join(
                    BASE_DATA_DIR, "policies", "inline", filename
                )

                with open(output_path, "w") as f:
                    json.dump(policy_document, f, indent=2, default=json_serial)

    # Inline policies for roles
    role_paginator = iam.get_paginator("list_roles")
    for page in role_paginator.paginate():
        for role in page.get("Roles", []):
            role_name = role["RoleName"]

            policy_names = iam.list_role_policies(
                RoleName=role_name
            ).get("PolicyNames", [])

            for policy_name in policy_names:
                policy = iam.get_role_policy(
                    RoleName=role_name,
                    PolicyName=policy_name
                )

                policy_document = {
                    "AttachedTo": "Role",
                    "RoleName": role_name,
                    "PolicyName": policy_name,
                    "Document": policy["PolicyDocument"]
                }

                filename = f"role_{role_name}_{policy_name}.json"
                output_path = os.path.join(
                    BASE_DATA_DIR, "policies", "inline", filename
                )

                with open(output_path, "w") as f:
                    json.dump(policy_document, f, indent=2, default=json_serial)

    print("[+] Collected inline IAM policies (users and roles)")


if __name__ == "__main__":
    ensure_directories()
    collect_users()
    collect_roles()
    collect_trust_policies()
    collect_managed_policies()
    collect_inline_policies()
