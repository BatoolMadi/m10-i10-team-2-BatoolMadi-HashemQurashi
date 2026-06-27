# Team Roster — Module 10 Integration

This file is the team roster artifact for the Module 10 four-service Docker Compose Integration.

## Team Identity

- **Team name:** team-4
- **Team Slack channel:** #m10-team-4
- **Team-formation date:** 2026-06-24
- **Designated team submitter:** Hashem (Backend & Infra-Integration lead)

---

## Team Roster

| Role | Team Member identifier | Assigned by | Branch | Internal-PR reviewer | Primary files owned |
|---|---|---|---|---|---|
| Backend & Infra-Integration lead | Hashem | Instructional team | `main` | Batool | `api/*`, `docker-compose.yml`, `scripts/*`, `tests/integration/*` |
| Frontend lead | Batool | Instructional team | `frontend/nextjs-pages` | Hashem | `web/*`, `tests/frontend/playwright/*` |

---

## Per-Role File Checklist

### Backend & Infra-Integration lead

- [x] `api/main.py` — path operations, `lifespan`, CORS middleware
- [x] `api/models.py` — Pydantic shapes
- [x] `api/rag.py` — RAG composer with grounding contract
- [x] `api/deps.py` — `Depends()` functions
- [x] `api/Dockerfile` — single-stage Python
- [x] `docker-compose.yml` — four services, healthchecks, `depends_on` chain, named volumes
- [x] `seed_neo4j.sh`
- [x] `seed_weaviate.sh`
- [x] `.env.example`
- [x] `README.md` runbook
- [x] `tests/integration/test_stack_e2e.py`

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

All role branches merged to the team fork's `main` and `docker compose up -d` smoke passes locally for all team members.