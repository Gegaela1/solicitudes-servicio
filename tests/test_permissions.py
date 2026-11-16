import pytest
from types import SimpleNamespace
from fastapi import HTTPException
from app.services.permissions import require_roles, can_view, responsible


def test_permissions():
    user = SimpleNamespace(id=1, roles=[SimpleNamespace(nombre="solicitante")])
    case = SimpleNamespace(solicitante_id=2, responsable_id=1)
    with pytest.raises(HTTPException) as e:
        can_view(user, case)
    assert e.value.status_code == 404
    with pytest.raises(HTTPException):
        responsible(user, case)
    user.roles.append(SimpleNamespace(nombre="coordinacion"))
    can_view(user, case)
    responsible(user, case)
    require_roles(user, "coordinacion")
