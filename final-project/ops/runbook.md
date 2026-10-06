# Local Operations Runbook

Run commands from the repository root and keep all verification data synthetic.

## Check service health

```bash
docker compose -f final-project/docker-compose.yml ps
curl --silent --show-error --output /dev/null --write-out '%{http_code}\n' http://127.0.0.1:8000/tasks
```

## Diagnose task API or database errors

```bash
docker compose -f final-project/docker-compose.yml logs --no-color --tail=100 backend postgres
```

Check whether PostgreSQL is healthy before interpreting backend connection errors. Avoid copying raw environment values, database URLs, credentials, or task bodies into reports.

## Recover local services

```bash
docker compose -f final-project/docker-compose.yml up -d --wait postgres
docker compose -f final-project/docker-compose.yml ps
curl --silent --show-error --output /dev/null --write-out '%{http_code}\n' http://127.0.0.1:8000/tasks
```

To stop the local stack while retaining data, run `docker compose -f final-project/docker-compose.yml stop`. Never use `docker compose down -v` for routine diagnosis; it deletes the database volume.

See `diagnostics/database-outage.md` for the verified local outage/recovery exercise.