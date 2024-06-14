# Run request API

## Create a run

`POST /api/runs` with a JSON body:

| Field | Description |
| --- | --- |
| `pipeline_name` | Name of the pipeline to execute |
| `trigger` | What started the run (e.g. `manual`, `webhook`) |
| `parameters` | Key/value map passed into the pipeline |

## Get a run

`GET /api/runs/:id` returns the run identified by `:id` (status, logs pointer, timing).

## Related configuration

| Setting | Role |
| --- | --- |
| `max_concurrent_runs` | Cap parallel runs |
| `run_timeout_seconds` | Kill runs that exceed this duration |
| `cleanup_interval_seconds` | How often finished runs are pruned |

## Example

```bash
curl -sS -X POST http://localhost:8000/api/runs \
  -H 'Content-Type: application/json' \
  -d '{"pipeline_name":"deploy","trigger":"manual","parameters":{"env":"staging"}}'
```
