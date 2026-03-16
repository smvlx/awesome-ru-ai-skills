---
name: yandex-cloud
description: >
  Use when managing Yandex Cloud infrastructure via the yc CLI: creating buckets,
  uploading files, publishing static websites, checking billing, managing VMs,
  configuring networks, DNS, certificates, serverless functions, databases, or any
  Yandex Cloud resource. Triggers on mentions of Yandex Cloud, yc CLI, Object Storage
  buckets, S3 on Yandex, static website hosting on Yandex, or any Yandex Cloud
  service management. Always use this skill when the user mentions yandex cloud
  infrastructure, even if they don't say "yc" explicitly.
---

# Yandex Cloud CLI (`yc`)

## Overview

The `yc` CLI is the primary tool for managing all Yandex Cloud resources. This skill covers installation, authentication, and all major service groups. Object Storage also supports S3-compatible commands via `yc storage s3` and `yc storage s3api`.

## Preflight

Before any operation, check if `yc` is installed and authenticated:

```bash
# Check installation (default install path on macOS/Linux)
which yc || ls ~/yandex-cloud/bin/yc
yc version

# Check current config
yc config list
```

If `yc` is not found via `which` but exists at `~/yandex-cloud/bin/yc`, the PATH needs updating:
```bash
export PATH="$HOME/yandex-cloud/bin:$PATH"
```

If `yc` is not installed at all, guide the user through installation (see Installation section).
If `yc config list` shows no token/cloud/folder, guide through `yc init`.

## Installation

**macOS / Linux:**
```bash
curl -sSL https://storage.yandexcloud.net/yandexcloud-yc/install.sh | bash
```
Restart the terminal after installation. The script updates PATH automatically.

**Verify:**
```bash
yc version
```

## Authentication

### Interactive (recommended for personal use)
```bash
yc init
```
This walks through:
1. Get OAuth token from the URL it provides
2. Select cloud
3. Select default folder
4. Optionally set default availability zone

### Service Account (for automation)
```bash
# Create service account
yc iam service-account create --name my-sa

# Assign role
yc resource-manager folder add-access-binding <folder-id> \
  --role editor \
  --subject serviceAccount:<sa-id>

# Create authorized key
yc iam key create --service-account-name my-sa --output sa-key.json

# Create a profile using the key
yc config profile create my-sa-profile
yc config set service-account-key sa-key.json
```

### Federated login (SSO)
```bash
yc init --federation-id=<federation-id>
```

### Check current identity
```bash
yc config list
yc iam whoami
```

## Object Storage (Buckets & Files)

### Create a bucket
```bash
yc storage bucket create --name my-bucket
yc storage bucket create --name my-bucket --default-storage-class cold
```

### List / inspect buckets
```bash
yc storage bucket list
yc storage bucket get --name my-bucket
yc storage bucket stats --name my-bucket
```

### Upload files
```bash
# Single file
yc storage s3api put-object --bucket my-bucket --key path/to/file.html --body ./local-file.html

# Copy (supports local->s3, s3->local, s3->s3)
yc storage s3 cp ./local-file.txt s3://my-bucket/remote-file.txt
yc storage s3 cp --recursive ./my-site/ s3://my-bucket/

# Move
yc storage s3 mv ./file.txt s3://my-bucket/file.txt
```

### Download files
```bash
yc storage s3api get-object --bucket my-bucket --key file.txt ./downloaded.txt
yc storage s3 cp s3://my-bucket/file.txt ./local-file.txt
```

### Delete files
```bash
yc storage s3api delete-object --bucket my-bucket --key file.txt
yc storage s3 rm s3://my-bucket/file.txt
yc storage s3 rm --recursive s3://my-bucket/prefix/
```

### List objects
```bash
yc storage s3api list-objects --bucket my-bucket
yc storage s3api list-objects --bucket my-bucket --prefix "images/"
```

### Presigned URLs
```bash
yc storage s3 presign s3://my-bucket/file.txt
```

### ACLs
```bash
yc storage s3api get-object-acl --bucket my-bucket --key file.txt
yc storage s3api put-object-acl --bucket my-bucket --key file.txt --acl public-read
```

### Tagging
```bash
yc storage s3api put-object-tagging --bucket my-bucket --key file.txt \
  --tagging '{"TagSet": [{"Key": "env", "Value": "prod"}]}'
yc storage s3api get-object-tagging --bucket my-bucket --key file.txt
```

### Delete bucket
```bash
yc storage bucket delete --name my-bucket
```

## Static Website Hosting

### 1. Create bucket (name = your domain or any name)
```bash
yc storage bucket create --name my-website
```

### 2. Upload site files
```bash
yc storage s3 cp --recursive ./my-site/ s3://my-website/
```

### 3. Enable hosting
Create `hosting.json`:
```json
{
  "index": "index.html",
  "error": "error404.html"
}
```

```bash
yc storage bucket update --name my-website --website-settings-from-file hosting.json
```

### 4. Make bucket public
```bash
yc storage bucket update --name my-website \
  --public-read \
  --public-list
```

### 5. Verify
```bash
yc storage bucket get --full --name my-website
```

The site is available at: `http://my-website.website.yandexcloud.net`

For a custom domain, create a CNAME DNS record pointing to `my-website.website.yandexcloud.net`.

### HTTPS for custom domain
```bash
# Add certificate via Certificate Manager
yc certificate-manager certificate request --name my-cert \
  --domains example.com

# Attach to bucket
yc storage bucket set-https --name my-website \
  --certificate-id <certificate-id>
```

## Billing

There is **no `yc billing` command group**. Billing is managed via the Yandex Cloud console only.

- **View costs & usage**: `https://console.yandex.cloud/billing`
- **Billing API** (REST): `https://billing.api.cloud.yandex.net/billing/v1/billingAccounts`

You can set up a **serverless trigger** to react to billing budget thresholds:
```bash
yc serverless trigger create billing-budget \
  --name my-trigger \
  --billing-account-id <account-id> \
  --budget-id <budget-id> \
  --invoke-function-id <function-id>
```

## Compute (VMs)

```bash
# List VMs
yc compute instance list

# Create VM
yc compute instance create \
  --name my-vm \
  --zone ru-central1-a \
  --cores 2 --memory 4GB \
  --core-fraction 100 \
  --create-boot-disk image-folder-id=standard-images,image-family=ubuntu-2204-lts,size=20 \
  --network-interface subnet-name=default-ru-central1-a,nat-ip-version=ipv4 \
  --ssh-key ~/.ssh/id_rsa.pub

# Get VM info
yc compute instance get my-vm

# Start / stop / restart
yc compute instance start my-vm
yc compute instance stop my-vm
yc compute instance restart my-vm

# Delete VM
yc compute instance delete my-vm

# List available images
yc compute image list --folder-id standard-images

# Disks
yc compute disk list
yc compute disk create --name my-disk --size 50 --zone ru-central1-a
yc compute disk delete my-disk

# Snapshots
yc compute snapshot create --name my-snap --disk-name my-disk
yc compute snapshot list
```

## All Major Service Groups

For comprehensive reference on any service group below, run `yc <group> --help`.
See `references/service-groups.md` for the full command reference.

| Group | Description |
|-------|-------------|
| `compute` | VMs, disks, images, snapshots, instance groups |
| `storage` | Object Storage buckets, S3 operations |
| `vpc` | Networks, subnets, security groups, routing |
| `iam` | Users, service accounts, roles, keys, tokens |
| `resource-manager` | Clouds, folders |
| `certificate-manager` | TLS certificates |
| `dns` | DNS zones and records |
| `managed-postgresql` | Managed PostgreSQL clusters |
| `managed-mysql` | Managed MySQL clusters |
| `managed-clickhouse` | Managed ClickHouse clusters |
| `managed-mongodb` | Managed MongoDB clusters |
| `managed-redis` | Managed Redis clusters |
| `managed-kafka` | Managed Kafka clusters |
| `managed-kubernetes` | Kubernetes clusters and node groups |
| `serverless` | Functions, triggers, containers, API gateways |
| `container` | Container Registry |
| `ydb` | YDB databases |
| `kms` | Key Management Service |
| `logging` | Cloud Logging |
| `cdn` | CDN resources |
| `application-load-balancer` | L7 load balancers |
| `load-balancer` | Network load balancers |
| `organization-manager` | Organizations, federations |
| `dataproc` | Data Processing clusters |
| `datatransfer` | Data Transfer |
| `lockbox` | Secret management |
| `backup` | Cloud Backup |
| `audit-trails` | Audit Trails |
| `smartcaptcha` | SmartCaptcha |
| `baremetal` | Bare Metal servers |
| `managed-gitlab` | Managed GitLab |
| `quota-manager` | Quota management |

## Common Patterns

### Set default folder (avoids --folder-id everywhere)
```bash
yc config set folder-id <folder-id>
```

### Output as JSON (for scripting)
```bash
yc compute instance list --format json
yc storage bucket list --format json
```

### Switch profiles
```bash
yc config profile list
yc config profile activate <profile-name>
```

### Get IDs programmatically
```bash
INSTANCE_ID=$(yc compute instance get my-vm --format json | jq -r '.id')
```

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `yc: command not found` | Restart terminal or `source ~/.bashrc` / `source ~/.zshrc` |
| `unauthenticated` | Run `yc init` or check `yc config list` |
| `permission denied` | Check IAM roles: `yc resource-manager folder list-access-bindings <folder-id>` |
| `quota exceeded` | Check quotas in console or request increase |
| Wrong cloud/folder | `yc config set cloud-id <id>` / `yc config set folder-id <id>` |
