# Security

## Authentication

All HTTP APIs and worker registration use bearer tokens (`Authorization: Bearer <token>`). Tokens are issued by the control plane and should be treated as secrets—never commit them to source control or log them in full.

## Permissions

The permission model maps tokens to roles (`viewer`, `operator`, `admin`). Viewers can read job status; operators may enqueue and cancel jobs; admins manage plugins, secrets metadata, and retention policies. Fine-grained resource ACLs apply per project when multi-tenancy is enabled.

## Reporting vulnerabilities

Please report security issues privately to **security@example.com** with steps to reproduce and affected versions. Do not open public issues for undisclosed vulnerabilities. We aim to acknowledge within five business days.

## Best practices

Store long-lived credentials in a secret manager and inject them at runtime. Run workers with least privilege—only storage, queue, and KMS permissions required for the job. Keep dependencies patched, enable audit logging for API mutations, and use separate tokens per environment (staging vs production).
