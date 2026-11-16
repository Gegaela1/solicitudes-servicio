from sqlalchemy import text

from app.db.session import engine


def test_base(client):
    assert client.get("/api/v1/salud").json() == {"estado": "disponible"}
    assert client.get("/").status_code == 200
    assert client.get("/inexistente").status_code == 404
    with engine.connect() as db:
        assert db.scalar(text("PRAGMA foreign_keys")) == 1
