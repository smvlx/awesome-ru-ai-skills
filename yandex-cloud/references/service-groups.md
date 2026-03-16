# Yandex Cloud CLI — Service Group Reference

Use `yc <group> <subgroup> --help` for full options on any command.

## IAM (Identity & Access Management)

```bash
# Service accounts
yc iam service-account create --name <name>
yc iam service-account list
yc iam service-account get <name-or-id>
yc iam service-account delete <name-or-id>

# Keys
yc iam key create --service-account-name <name> --output key.json
yc iam access-key create --service-account-name <name>  # S3-compatible keys
yc iam api-key create --service-account-name <name>

# Tokens
yc iam create-token  # IAM token for current profile

# Roles
yc iam role list
yc resource-manager folder add-access-binding <folder-id> \
  --role <role> --subject serviceAccount:<sa-id>
yc resource-manager folder list-access-bindings <folder-id>
```

## VPC (Virtual Private Cloud)

```bash
# Networks
yc vpc network create --name my-net
yc vpc network list
yc vpc network delete my-net

# Subnets
yc vpc subnet create --name my-subnet \
  --network-name my-net \
  --zone ru-central1-a \
  --range 10.0.0.0/24
yc vpc subnet list
yc vpc subnet delete my-subnet

# Security groups
yc vpc security-group create --name my-sg --network-name my-net \
  --rule "direction=ingress,port=80,protocol=tcp,v4-cidrs=0.0.0.0/0" \
  --rule "direction=ingress,port=443,protocol=tcp,v4-cidrs=0.0.0.0/0" \
  --rule "direction=ingress,port=22,protocol=tcp,v4-cidrs=0.0.0.0/0"
yc vpc security-group list
yc vpc security-group delete my-sg

# Static IPs
yc vpc address create --name my-ip --external-ipv4 zone=ru-central1-a
yc vpc address list
yc vpc address delete my-ip
```

## DNS

```bash
# Zones
yc dns zone create --name my-zone --zone example.com. --public-visibility
yc dns zone list
yc dns zone delete my-zone

# Records
yc dns zone add-records --name my-zone \
  --record "www A 300 1.2.3.4"
yc dns zone add-records --name my-zone \
  --record "@ CNAME 300 my-bucket.website.yandexcloud.net."
yc dns zone list-records --name my-zone
yc dns zone delete-records --name my-zone \
  --record "www A 300 1.2.3.4"
```

## Certificate Manager

```bash
# Request Let's Encrypt certificate
yc certificate-manager certificate request --name my-cert \
  --domains example.com,www.example.com

# Import custom certificate
yc certificate-manager certificate create --name my-cert \
  --chain cert-chain.pem --key private-key.pem

# List / get
yc certificate-manager certificate list
yc certificate-manager certificate get my-cert

# Delete
yc certificate-manager certificate delete my-cert
```

## Managed PostgreSQL

```bash
# Create cluster
yc managed-postgresql cluster create \
  --name my-pg \
  --environment production \
  --network-name my-net \
  --host zone-id=ru-central1-a,subnet-name=my-subnet \
  --resource-preset s2.micro \
  --disk-size 20 \
  --disk-type network-ssd \
  --database name=mydb,owner=myuser \
  --user name=myuser,password=<password>

# List / get / delete
yc managed-postgresql cluster list
yc managed-postgresql cluster get my-pg
yc managed-postgresql cluster delete my-pg

# Databases & users
yc managed-postgresql database list --cluster-name my-pg
yc managed-postgresql user list --cluster-name my-pg

# Backups
yc managed-postgresql backup list --cluster-name my-pg
```

## Managed MySQL

```bash
yc managed-mysql cluster create \
  --name my-mysql \
  --environment production \
  --network-name my-net \
  --host zone-id=ru-central1-a,subnet-name=my-subnet \
  --resource-preset s2.micro \
  --disk-size 20 \
  --disk-type network-ssd \
  --database name=mydb \
  --user name=myuser,password=<password>

yc managed-mysql cluster list
yc managed-mysql cluster delete my-mysql
```

## Managed Kubernetes

```bash
# Create cluster
yc managed-kubernetes cluster create \
  --name my-k8s \
  --network-name my-net \
  --zone ru-central1-a \
  --subnet-name my-subnet \
  --public-ip \
  --service-account-name my-sa \
  --node-service-account-name my-sa

# Node groups
yc managed-kubernetes node-group create \
  --cluster-name my-k8s \
  --name my-nodes \
  --fixed-size 3 \
  --cores 2 --memory 4 \
  --disk-size 64

# Get kubeconfig
yc managed-kubernetes cluster get-credentials my-k8s --external

yc managed-kubernetes cluster list
yc managed-kubernetes cluster delete my-k8s
```

## Serverless

```bash
# Functions
yc serverless function create --name my-func
yc serverless function version create \
  --function-name my-func \
  --runtime nodejs18 \
  --entrypoint index.handler \
  --memory 128m \
  --execution-timeout 5s \
  --source-path ./function.zip
yc serverless function list
yc serverless function invoke my-func

# Triggers
yc serverless trigger create timer \
  --name my-timer \
  --cron-expression "0 * * * ? *" \
  --invoke-function-name my-func

yc serverless trigger create object-storage \
  --name my-trigger \
  --bucket-id my-bucket \
  --events create-object \
  --invoke-function-name my-func

# Containers
yc serverless container create --name my-container
yc serverless container revision deploy \
  --container-name my-container \
  --image cr.yandex/<registry-id>/my-image:latest \
  --cores 1 --memory 512m

# API Gateway
yc serverless api-gateway create --name my-gw \
  --spec api-spec.yaml
```

## Container Registry

```bash
# Registry
yc container registry create --name my-registry
yc container registry list

# Auth docker
yc container registry configure-docker

# Images
yc container image list --registry-name my-registry
yc container image delete <image-id>
```

## Lockbox (Secrets)

```bash
yc lockbox secret create --name my-secret \
  --payload '[{"key": "db_password", "text_value": "s3cret"}]'
yc lockbox secret list
yc lockbox payload get --name my-secret
yc lockbox secret delete my-secret
```

## CDN

```bash
yc cdn resource create --cname cdn.example.com \
  --origin-group-id <id>
yc cdn resource list
yc cdn origin-group create --name my-origins \
  --origin source=my-bucket.website.yandexcloud.net,enabled=true
```

## Load Balancers

```bash
# L7 (Application)
yc application-load-balancer load-balancer create --name my-alb \
  --network-name my-net
yc application-load-balancer load-balancer list

# Network (L4)
yc load-balancer network-load-balancer create --name my-nlb
yc load-balancer network-load-balancer list
```

## Resource Manager

```bash
# Clouds
yc resource-manager cloud list
yc resource-manager cloud get <cloud-id>

# Folders
yc resource-manager folder create --name my-folder
yc resource-manager folder list
yc resource-manager folder delete my-folder
```

## Config & Profiles

```bash
# Current config
yc config list

# Set defaults
yc config set cloud-id <cloud-id>
yc config set folder-id <folder-id>
yc config set compute-default-zone ru-central1-a

# Profiles
yc config profile create <name>
yc config profile activate <name>
yc config profile list
yc config profile delete <name>

# Get IAM token
yc iam create-token
```

## Availability Zones

| Zone | Location |
|------|----------|
| `ru-central1-a` | Vladimir |
| `ru-central1-b` | Ryazan |
| `ru-central1-d` | Kaluga |
