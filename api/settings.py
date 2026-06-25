"""Process-level settings — env-var-backed.

Centralizes URL, credential, and origin reads so paths through the code
do not pepper `os.environ[...]` calls.
"""
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Container for the env-var-backed configuration.

    Reads at construction time. Construct once in lifespan; do not
    re-construct per request.
    """

    neo4j_uri: str = Field("bolt://localhost:7687", env="NEO4J_URI")
    neo4j_user: str = Field("neo4j", env="NEO4J_USER")
    neo4j_password: str = Field(..., min_length=1, env="NEO4J_PASSWORD")
    weaviate_url: str = Field("http://localhost:8080", env="WEAVIATE_URL")
    web_origin: str = Field("http://localhost:3000", env="WEB_ORIGIN")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
