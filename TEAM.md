# Team Roster — Module 10 Integration

This file is the team roster artifact for the Module 10 four-service Docker Compose Integration.

## Team Identity

- **Team name:** team-4
- **Team Slack channel:** #m10-team-4
- **Team-formation date:** 2026-06-24
- **Designated team submitter:** Hashem
---

## Team Roster

| Role | Team Member identifier | Branch |
|---|---|---|
| Backend Lead | Hashem | `backend/api-endpoints` |
| Frontend Lead | Batool | `frontend/nextjs-pages` |
| Infra-Integration | Shared (Batool + Hashem) | `infra/docker-compose` |
---

## Per-Role File Checklist

### Backend lead

* [x] `api/main.py`
* [x] `api/models.py`
* [x] `api/rag.py`
* [x] `api/deps.py`
* [x] `api/Dockerfile`

### Infra-Integration (Shared: Batool + Hashem)

* [x] `docker-compose.yml`
* [x] `scripts/seed_neo4j.sh`
* [x] `scripts/seed_weaviate.sh`
* [x] `scripts/healthcheck_stack.sh`
* [x] `.env.example`
* [x] `README.md`
* [x] `tests/integration/test_stack_e2e.py`


### Frontend lead

- [x] `web/pages/extract.tsx`
- [x] `web/pages/kg.tsx`
- [x] `web/pages/rag.tsx`
- [x] `web/lib/types.ts` — three TypeScript interfaces mirroring Pydantic
- [x] `web/Dockerfile` — multi-stage Node
- [x] `tests/frontend/playwright/*.spec.ts` — one per page

---

## Escalation Checklist

1. **Inline comment on the internal PR.**
2. **Team Slack channel with TA tagged.**
3. **Support Instructor.**
4. **Lead Instructor.**

*Escalation path taken:* None required; roles were successfully coordinated.

---

## Contract-Change Protocol

- **Backend lead** announces any Pydantic shape change on the team Slack channel **before** the change lands.
- **Frontend lead** requests new backend fields via an internal-PR comment on the Backend lead's branch.
- **Infra-Integration lead** announces any `.env` or DNS-affecting change before the change lands.

---

## Submission

All assigned role branches (`backend/api-endpoints`, `frontend/nextjs-pages`, `infra/docker-compose`) have been completed and merged into the team fork's main branch. All team members verified `docker compose up -d` and end-to-end stack health successfully.