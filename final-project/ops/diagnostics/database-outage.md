# Local Database Outage and Recovery

## Exercise

Performed against the existing local Docker Compose stack on 2026-10-06. No production service or data was involved. The existing Compose database volume was retained.

Commands, from the repository root:

```bash
docker compose -f final-project/docker-compose.yml up -d --build
curl --silent --show-error --output /dev/null --write-out '%{http_code}\n' http://127.0.0.1:8000/tasks
docker compose -f final-project/docker-compose.yml stop postgres
curl --silent --show-error --output /dev/null --write-out '%{http_code}\n' http://127.0.0.1:8000/tasks
docker compose -f final-project/docker-compose.yml logs --no-color --tail=80 backend
docker compose -f final-project/docker-compose.yml up -d --wait postgres
curl --silent --show-error --output /dev/null --write-out '%{http_code}\n' http://127.0.0.1:8000/tasks
docker compose -f final-project/docker-compose.yml stop
docker compose -f final-project/docker-compose.yml ps
```

Only `postgres` was stopped during the outage. Logs were inspected through a filter that emitted only generic connection-error class/symptom strings; credentials, database URLs, task bodies, and raw stack traces are not included here.

## Evidence

- Before outage: PostgreSQL and backend were healthy; `GET /tasks` returned HTTP `200`.
- With PostgreSQL stopped: `GET /tasks` returned HTTP `500`; sanitized backend symptom: `OperationalError`.
- Recovery: `up -d --wait postgres` reported PostgreSQL healthy; backend health returned to healthy; `GET /tasks` returned HTTP `200`.
- Cleanup: `docker compose stop` stopped frontend, backend, and PostgreSQL. `docker compose ps` showed no running services.
- No `docker compose down -v` was run; no database volume was deleted.

## Diagnosis

The API depends on PostgreSQL for task reads. Removing PostgreSQL caused SQLAlchemy/driver connection acquisition to fail and the endpoint returned an internal server error. Restoring PostgreSQL health restored the endpoint without application or data changes. This exercise confirms recovery after a database outage; it does not demonstrate graceful 503 handling or transaction retry behavior.