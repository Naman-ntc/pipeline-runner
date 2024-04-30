# HTTP API reference

Base URL: `https://<host>:<port>`. All responses are JSON unless noted.

## GET /api/status

Returns whether the pipeline-runner service is up and which version it reports.

**Request**

```http
GET /api/status HTTP/1.1
Host: localhost:8080
Accept: application/json
```

**Response** `200 OK`

```json
{
  "ok": true,
  "service": "pipeline-runner",
  "version": "1.2.3"
}
```

Use this endpoint for load balancer health checks and deployment verification.
