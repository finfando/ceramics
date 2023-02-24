import os

from sqlalchemy import create_engine

from ceramics.orm import mapper_registry


def get_postgres_uri():
    host = os.environ.get("DB_HOST", "localhost")
    port = os.environ.get("DB_PORT", "5432")
    user = os.environ.get("DB_USER", "postgres")
    password = os.environ.get("DB_PASSWORD", "postgres")
    db_name = os.environ.get("DB_NAME", "postgres")
    return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"


def get_api_url():
    host = os.environ.get("API_HOST", "localhost")
    port = 5000 if host == "localhost" else 80
    return f"http://{host}:{port}"


def recreate_schema():
    engine = create_engine(get_postgres_uri())
    mapper_registry.metadata.drop_all(engine)
    mapper_registry.metadata.create_all(engine)
