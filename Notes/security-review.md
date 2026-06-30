# Security Review -- Terraform / Docker Compose / GCP Setup

**Date:** 2026-06-29
**Scope:** `terraform/`, `docker-compose.yaml`, `.gitignore`, credential handling
**Context:** Learning project (DataTalks.Club Zoomcamp Module 01)

---

## Findings

### 1. [HIGH] pgadmin-pgpass contains plaintext password and is not gitignored

**File:** `pgadmin-pgpass`
**Issue:** This file contains the Postgres password in plaintext (`pgdatabase:5432:*:root:root`) and is NOT matched by any rule in `.gitignore`. Running `git add .` or `git add -A` would stage and commit this file, pushing the password into git history permanently.

**Evidence:** `git check-ignore -v pgadmin-pgpass` returns no match.

**Recommendation:** Add these lines to `.gitignore`:

```
pgadmin-pgpass
pgadmin-servers.json
```

Even though the password here is `root` (a local dev password), building the habit of excluding credential files prevents future accidents when real credentials are involved.

---

### 2. [HIGH] .gitignore does not cover terraform.tfvars

**File:** `.gitignore`
**Issue:** The standard Terraform workflow stores sensitive variable values (like `project_id`) in `terraform.tfvars` or `*.auto.tfvars`. Neither pattern appears in `.gitignore`. If you create a `terraform/terraform.tfvars` with your GCP project ID or other config, it will be committed to git.

**Evidence:** `git check-ignore -v terraform/terraform.tfvars` returns no match.

**Recommendation:** Add to `.gitignore`:

```
terraform/*.tfvars
terraform/*.tfvars.json
```

---

### 3. [HIGH] .gitignore credential patterns have gaps

**File:** `.gitignore`
**Issue:** The current patterns are:

```
*.json.key
*-credentials.json
*-key.json
```

These miss common GCP service account key file names. Google Cloud by default names downloaded keys like `project-name-xxxxxxxxxxxx.json` (no `-key` or `-credentials` suffix). A downloaded service account key could be committed if its filename does not match these patterns.

**Recommendation:** Add a broader catch-all and/or a directory-based exclusion:

```
# GCP service account keys (broad catch)
*sa-key*.json
*service-account*.json
keys/
secrets/
```

Better yet, store GCP keys outside the repo entirely (e.g., `~/.config/gcloud/`) and reference them via the `GOOGLE_APPLICATION_CREDENTIALS` environment variable.

---

### 4. [MEDIUM] Docker Compose uses hardcoded default passwords

**File:** `docker-compose.yaml`
**Issue:** Postgres and pgAdmin passwords are hardcoded as `root`:

```yaml
POSTGRES_PASSWORD=root
PGADMIN_DEFAULT_PASSWORD=root
```

For a local learning environment this is acceptable, but it creates two risks:
- If the ports are exposed on a shared network (not just localhost), anyone can connect.
- It builds a bad habit that can carry into production setups.

**Recommendation:** Move passwords to a `.env` file (already gitignored) and reference them with variable substitution:

```yaml
environment:
  - POSTGRES_PASSWORD=${POSTGRES_PASSWORD:-root}
```

Then in `.env`:
```
POSTGRES_PASSWORD=root
PGADMIN_DEFAULT_PASSWORD=root
```

This keeps defaults for convenience but separates secrets from tracked config.

---

### 5. [MEDIUM] Docker Compose ports bound to all interfaces

**File:** `docker-compose.yaml`
**Issue:** Both services bind to `0.0.0.0` (all network interfaces):

```yaml
ports:
  - "5432:5432"   # Postgres
  - "8085:80"     # pgAdmin
```

On a machine connected to a network (e.g., campus Wi-Fi, coffee shop), anyone on the same network can reach your Postgres and pgAdmin instances with the `root`/`root` credentials.

**Recommendation:** Bind to localhost only:

```yaml
ports:
  - "127.0.0.1:5432:5432"
  - "127.0.0.1:8085:80"
```

---

### 6. [MEDIUM] GCS bucket has force_destroy = true

**File:** `terraform/main.tf` (line 19)
**Issue:** `force_destroy = true` means `terraform destroy` will delete the bucket and ALL objects inside it without confirmation. In a learning environment this is fine for easy cleanup, but be aware that this is a data-loss risk.

**Recommendation:** Acceptable for a learning project. When working with real data, remove `force_destroy` or add lifecycle policies. No action needed now, but be conscious of this when you move beyond the Zoomcamp.

---

### 7. [LOW] Terraform provider does not pin credentials source

**File:** `terraform/main.tf` (lines 11-14)
**Issue:** The provider block does not specify `credentials`. This means Terraform will use Application Default Credentials (ADC) from the environment, which is actually the correct and safe approach. No credentials are hardcoded.

**Status:** GOOD -- no issue. Noted for completeness.

---

### 8. [LOW] No Terraform backend configured (local state)

**File:** `terraform/main.tf`
**Issue:** No `backend` block is declared, so Terraform state is stored locally in `terraform.tfstate`. The `.gitignore` correctly excludes `terraform/*.tfstate` and `terraform/*.tfstate.backup`, so this is covered.

**Risk:** If the local state file is lost, Terraform loses track of the resources it created. For a learning project, you can just destroy and recreate. For real projects, use a remote backend (GCS bucket).

**Status:** Acceptable for learning. No action needed.

---

### 9. [LOW] BigQuery dataset has no access controls

**File:** `terraform/main.tf` (lines 31-34)
**Issue:** The `google_bigquery_dataset` resource uses default access controls (project-level). This is fine for a learning project since GCP IAM provides project-level isolation.

**Status:** Acceptable. No action needed.

---

## Summary

| # | Severity | Finding | Action Required |
|---|----------|---------|-----------------|
| 1 | HIGH | pgadmin-pgpass not gitignored | Add to .gitignore |
| 2 | HIGH | terraform.tfvars not gitignored | Add *.tfvars to .gitignore |
| 3 | HIGH | Credential .gitignore patterns have gaps | Broaden JSON key patterns |
| 4 | MEDIUM | Hardcoded passwords in docker-compose.yaml | Move to .env file |
| 5 | MEDIUM | Docker ports bound to 0.0.0.0 | Bind to 127.0.0.1 |
| 6 | MEDIUM | GCS bucket force_destroy = true | Acceptable for learning |
| 7 | LOW | Provider uses ADC (good) | No action |
| 8 | LOW | Local Terraform state (covered by .gitignore) | No action |
| 9 | LOW | BigQuery default access controls | No action |

---

## Recommended .gitignore additions

Add these lines to `.gitignore` to close the HIGH findings:

```gitignore
# Terraform variable files (may contain project IDs, secrets)
terraform/*.tfvars
terraform/*.tfvars.json

# pgAdmin config with embedded credentials
pgadmin-pgpass
pgadmin-servers.json

# Broader GCP key patterns
*service-account*.json
*sa-key*.json
keys/
secrets/
```

---

## Beginner Safety Checklist

1. **Never store GCP service account keys inside the repo.** Keep them in `~/.config/gcloud/` or another location outside the project tree. Set `GOOGLE_APPLICATION_CREDENTIALS` as an environment variable.

2. **Run `git status` before every commit.** Look for unexpected files, especially JSON files or anything with "key" or "credentials" in the name.

3. **Use `git add <specific-file>` instead of `git add .`** to avoid accidentally staging secrets.

4. **If you accidentally commit a secret:** rotating the credential is mandatory. Removing it from a later commit does NOT remove it from git history. Use `git filter-branch` or BFG Repo-Cleaner, and rotate the key in GCP Console immediately.

5. **Bind Docker ports to 127.0.0.1** when working on shared networks.

6. **Use `terraform plan` before `terraform apply`** and review what will be created, changed, or destroyed.
