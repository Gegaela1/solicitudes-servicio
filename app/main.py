"""Punto de entrada del incremento 0: interfaz y comprobación de salud."""
from pathlib import Path
from typing import Literal

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

FRONTEND = Path(__file__).resolve().parent / "frontend"
app = FastAPI(title="Solicitudes de servicio", version="0.0.1")
app.mount("/static", StaticFiles(directory=FRONTEND), name="static")


class Salud(BaseModel):
    estado: Literal["disponible"]


@app.get("/api/v1/salud", response_model=Salud, tags=["Sistema"])
def consultar_salud() -> Salud:
    """Comprueba que la API responde; no verifica una base de datos."""
    return Salud(estado="disponible")


@app.get("/", response_class=FileResponse, include_in_schema=False)
def inicio() -> FileResponse:
    return FileResponse(FRONTEND / "index.html")
