"""FastAPI application — recipe service (reference implementation).

Discipline gates the autograder enforces:
- Neo4j driver, Weaviate client, spaCy pipeline, and the flan-t5-base
  generator are constructed exactly once per process inside `lifespan`.
- `CORSMiddleware` registered with `allow_origins=[WEB_ORIGIN]`.
- `/extract`, `/kg/query`, `/rag/answer` use Pydantic shapes from `models.py`.
- `/kg/query` converts `UnsupportedQueryError` to 422 with structured detail.
- `/readyz` probes Neo4j (`RETURN 1`) AND Weaviate (`client.is_ready()`)
  within 2 seconds; failure → 503.
- `/healthz` does NOT touch Neo4j or Weaviate.
"""
import sys
import traceback
from contextlib import asynccontextmanager

import spacy
import weaviate
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from neo4j import GraphDatabase
from pydantic import ValidationError
from sentence_transformers import SentenceTransformer

from .deps import get_embedder, get_generator, get_nlp, get_session, get_weaviate
from .kg import wrap_kg_query
from .m8_rag import load_generator
from .models import (
    ExtractRequest,
    ExtractResponse,
    HealthResponse,
    KGRequest,
    KGResponse,
    RAGRequest,
    RAGResponse,
    UnsupportedQueryDetail,
)
from .nlp import extract_entities
from .rag import compose_rag
from .settings import Settings
from .w9b_mapper.errors import UnsupportedQueryError
from .w9b_mapper.shapes import SUPPORTED_PATTERNS


settings_cache: Settings | None = None


def load_settings() -> Settings:
    global settings_cache
    if settings_cache is None:
        try:
            settings_cache = Settings()
        except ValidationError as exc:
            raise EnvironmentError(
                "Missing or invalid environment configuration for API startup: "
                + "; ".join(err["msg"] for err in exc.errors())
            ) from exc
    return settings_cache


def _startup_step(label: str, fn):
    """Temporary CI diagnostic — remove after root cause found."""
    print(f"[startup] BEFORE {label}", flush=True)
    try:
        result = fn()
        print(f"[startup] AFTER {label}", flush=True)
        return result
    except Exception:
        print(f"[startup] FAILED {label}", file=sys.stderr, flush=True)
        traceback.print_exc(file=sys.stderr)
        raise


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("[startup] lifespan entered", flush=True)

    settings = _startup_step("load_settings()", load_settings)

    app.state.neo4j_driver = _startup_step(
        "Neo4j init",
        lambda: GraphDatabase.driver(
            settings.neo4j_uri,
            auth=(settings.neo4j_user, settings.neo4j_password),
        ),
    )
    app.state.weaviate_client = _startup_step(
        "Weaviate init",
        lambda: weaviate.Client(settings.weaviate_url),
    )
    app.state.nlp = _startup_step(
        "spacy.load()",
        lambda: spacy.load("en_core_web_sm"),
    )
    app.state.generator = _startup_step("load_generator()", load_generator)
    # Same sentence-transformers model the seed used at ingest. The
    # Weaviate class is `vectorizer=none`, so /rag/answer encodes the
    # query externally and queries via `with_near_vector`.
    app.state.embedder = _startup_step(
        "SentenceTransformer()",
        lambda: SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2"),
    )
    app.state.settings = settings

    print("[startup] lifespan startup complete — yielding", flush=True)
    yield
    app.state.neo4j_driver.close()


app = FastAPI(title="M10 Recipe Service", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[load_settings().web_origin],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/extract", response_model=ExtractResponse)
def extract(req: ExtractRequest, nlp=Depends(get_nlp)) -> ExtractResponse:
    return ExtractResponse(entities=extract_entities(req.text, nlp))


@app.post("/kg/query", response_model=KGResponse)
def kg_query(req: KGRequest, session=Depends(get_session)) -> KGResponse:
    try:
        cypher, params = wrap_kg_query(req.question)
    except UnsupportedQueryError:
        raise HTTPException(
            status_code=422,
            detail=UnsupportedQueryDetail(
                reason="unsupported_question",
                supported_patterns=list(SUPPORTED_PATTERNS),
            ).model_dump(),
        )
    rows = [r.data() for r in session.run(cypher, **params)]
    return KGResponse(cypher=cypher, rows=rows, count=len(rows))


@app.post("/rag/answer", response_model=RAGResponse)
def rag_answer(
    req: RAGRequest,
    weaviate_client=Depends(get_weaviate),
    generator=Depends(get_generator),
    embedder=Depends(get_embedder),
) -> RAGResponse:
    result = compose_rag(req.question, embedder, weaviate_client, generator, k=req.k)
    return RAGResponse(**result)


@app.get("/healthz", response_model=HealthResponse)
def healthz() -> HealthResponse:
    return HealthResponse(status="ok")


@app.get("/readyz")
def readyz(
    session=Depends(get_session),
    weaviate_client=Depends(get_weaviate),
):
    detail = {"neo4j": "unknown", "weaviate": "unknown"}
    try:
        session.run("RETURN 1").single()
        detail["neo4j"] = "ok"
    except Exception as exc:
        detail["neo4j"] = f"unavailable: {exc.__class__.__name__}"
    try:
        if weaviate_client.is_ready():
            detail["weaviate"] = "ok"
        else:
            detail["weaviate"] = "not ready"
    except Exception as exc:
        detail["weaviate"] = f"unavailable: {exc.__class__.__name__}"

    if detail["neo4j"] != "ok" or detail["weaviate"] != "ok":
        raise HTTPException(status_code=503, detail=detail)
    return detail


print("[startup] api.main module import complete", flush=True)
