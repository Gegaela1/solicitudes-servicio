from app.services import operations_reports as operations
from typing import Annotated
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.api.deps import current_user
from app.db.session import get_db
from app.schemas.cases import Filters

router = APIRouter(prefix="/api/v1/reportes", tags=["Coordinación"])


@router.get("/solicitudes")
def report(
    filters: Annotated[Filters, Query()], user=Depends(current_user), db: Session = Depends(get_db)
):
    return operations.report(filters=filters, user=user, db=db)
