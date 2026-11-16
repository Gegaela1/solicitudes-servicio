from app.api.workflow import router as workflow_router
from app.api.history import router as history_router
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.orm.exc import StaleDataError
from app.api.users import router as users_router
from app.api.cases import router as cases_router
from app.core.config import load_settings
from app.api.auth import router as auth_router

load_settings()
FRONTEND = Path(__file__).resolve().parent / "frontend"
app = FastAPI(title="Solicitudes de servicio", version="1.0.0")
app.mount("/static", StaticFiles(directory=FRONTEND), name="static")
app.include_router(auth_router)


@app.get("/api/v1/salud", tags=["Sistema"])
def health():
    return {"estado": "disponible"}


@app.get("/", include_in_schema=False)
def home():
    return FileResponse(FRONTEND / "index.html")


@app.exception_handler(RequestValidationError)
async def validation_error(request: Request, exc: RequestValidationError):
    # No devolver input/context: pueden contener contraseñas y otros secretos.
    return JSONResponse(
        status_code=422,
        content={
            "detail": [
                {"loc": list(e["loc"]), "msg": e["msg"], "type": e["type"]} for e in exc.errors()
            ]
        },
    )


@app.exception_handler(IntegrityError)
async def integrity_error(request: Request, exc: IntegrityError):
    return JSONResponse(
        status_code=409, content={"detail": "Conflicto de unicidad o integridad. Revisa los datos."}
    )


@app.exception_handler(StaleDataError)
async def stale_error(request: Request, exc: StaleDataError):
    return JSONResponse(
        status_code=409, content={"detail": "El caso cambió. Recarga antes de continuar."}
    )


@app.exception_handler(OperationalError)
async def operational_error(request: Request, exc: OperationalError):
    return JSONResponse(
        status_code=409,
        content={"detail": "Operación temporalmente no disponible. Recarga e intenta nuevamente."},
    )


app.include_router(users_router)

app.include_router(cases_router)

app.include_router(history_router)

app.include_router(workflow_router)
