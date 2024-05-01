# Troubleshooting

## Pipeline hangs

If a job never completes, first check the step timeout in your pipeline YAML (`timeout_seconds` per step or global default). Inspect worker logs for a stuck subprocess or a blocked network call. Increase logging temporarily with `PIPELINE_LOG_LEVEL=debug` and confirm the queue consumer’s visibility timeout exceeds your longest step.

## Storage errors

Upload and download failures usually mean missing or invalid credentials. Verify the worker role or access keys can reach the configured bucket and prefix. Test connectivity with the same endpoint and region the app uses. For S3-compatible backends, confirm path-style vs virtual-hosted style matches your deployment.

## Authentication failures

API and worker requests return `401` when the bearer token is missing, wrong, or expired. Rotate `PIPELINE_AUTH_TOKEN` if tokens are short-lived, and ensure clocks are synchronized (NTP) so JWT `exp` checks do not fail skewed hosts.

## Worker not starting

If the process exits immediately or never polls the queue, check `PIPELINE_QUEUE_URL` for typos and that the URL is reachable from the worker network. Confirm IAM or queue policy allows `ReceiveMessage` and `DeleteMessage`. For Redis-backed dev queues, verify the host/port and TLS settings match `docker-compose` overrides.
