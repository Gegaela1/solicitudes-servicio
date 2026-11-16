from app.services import operations_cases as operations
from app.schemas.cases import ServiceConfig
from app.schemas.cases import Correction
from typing import Annotated
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.api.deps import current_user
from app.db.session import get_db
from app.schemas.cases import CaseCreate, Filters

router = APIRouter(prefix="/api/v1", tags=["Solicitudes"])


@router.get("/servicios")
def services(user=Depends(current_user), db: Session = Depends(get_db)):
    return operations.services(user=user, db=db)


@router.post("/solicitudes", status_code=201)
def create(data: CaseCreate, user=Depends(current_user), db: Session = Depends(get_db)):
    return operations.create(data=data, user=user, db=db)


@router.get("/solicitudes")
def listing(
    filters: Annotated[Filters, Query()], user=Depends(current_user), db: Session = Depends(get_db)
):
    return operations.listing(filters=filters, user=user, db=db)


@router.get("/solicitudes/{sid}")
def detail(sid: int, user=Depends(current_user), db: Session = Depends(get_db)):
    return operations.detail(sid=sid, user=user, db=db)


@router.get("/solicitudes/{sid}/resultado")
def result(sid: int, user=Depends(current_user), db: Session = Depends(get_db)):
    return operations.result(sid=sid, user=user, db=db)


@router.patch("/solicitudes/{sid}")
def correct(sid: int, data: Correction, user=Depends(current_user), db: Session = Depends(get_db)):
    return operations.correct(sid=sid, data=data, user=user, db=db)


@router.patch("/servicios/{sid}/configuracion")
def configure_service(
    sid: int, data: ServiceConfig, user=Depends(current_user), db: Session = Depends(get_db)
):
    return operations.configure_service(sid=sid, data=data, user=user, db=db)
