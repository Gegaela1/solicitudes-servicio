import os
import secrets
import tempfile
from pathlib import Path

os.environ["SECRET_KEY"] = secrets.token_urlsafe(48)
TEST_DIR = Path(tempfile.mkdtemp(prefix="pf01-", dir="work/tmp"))
os.environ["DATABASE_URL"] = "sqlite:///" + (TEST_DIR / "test.db").as_posix()

import pytest
from fastapi.testclient import TestClient

from app.db.session import Base, SessionLocal, engine
from app.main import app
from app.models.entities import Rol, Servicio


@pytest.fixture(autouse=True)
def database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    with SessionLocal.begin() as db:
        db.add_all([Rol(nombre=n) for n in ["solicitante", "atencion", "coordinacion"]])
    with SessionLocal.begin() as db:
        db.add(Servicio(nombre="Peticiones generales"))
    yield


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client
