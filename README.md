# Solicitudes de servicio — PF-01

Aplicaciones y Servicios Web. Trabajo individual. Entrega prevista: 18-11-2026 antes de las 18:00, Colombia. Nombre de la estudiante y URL del repositorio: pendientes de completar.

## Estado

Incremento 0: página inicial, conexión JavaScript con API y documentación OpenAPI. Sin registro de solicitudes, persistencia ni autenticación. CA-01 a CA-06 pendientes. No es todavía una solución completa.

## Ejecutar en PowerShell

```powershell
Set-Location 'C:\Users\Usuario\Documents\solicitudes-servicio'
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Abrir http://127.0.0.1:8000 y http://127.0.0.1:8000/docs . Detener con Ctrl+C. No hace falta activar el entorno si se usa su intérprete explícitamente.

Para una instalación nueva con Python 3.14.2:

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip check
```

Las versiones fijadas corresponden al entorno existente; la reinstalación limpia sigue pendiente de comprobar.

## Endpoint implementado

| Método | Ruta | Respuesta | Relación |
|---|---|---|---|
| GET | /api/v1/salud | 200, {"estado":"disponible"} | Base técnica RNF-03/05/06 |

`app/main.py` define la aplicación y entrega el HTML. `app/frontend/js/inicio.js` consulta la API con fetch y comprueba HTTP y JSON. CSS presenta la página. Ambos usan el mismo origen. No hay acceso a BD.

## Documentación

- [Requisitos](docs/requisitos.md)
- [Decisiones y diseño provisional](docs/decisiones.md)
- [Pruebas](docs/pruebas.md)
- [Trazabilidad](docs/trazabilidad.md)

## Control de versiones y siguiente unidad

Se encontró Git inicializado sin commits ni remoto. Rama creada y verificada: chore/base-aplicacion (preparación transversal, excepción pendiente de validar frente a rama por RF). No hay PR real que citar. Antes de confirmar: revisar git diff y archivos preparados; excluir .venv, .env y bases locales.

Commit propuesto: `chore: agregar base FastAPI e interfaz con comprobación de salud`.
PR propuesto hacia main: base ejecutable y verificación I0; los resultados deben coincidir con docs/pruebas.md. El primer PR requiere una rama main con commit base; no simular historial previo.

Siguiente incremento: configurar entorno y persistencia inicial con SQLAlchemy/SQLite/Alembic; verificar compatibilidad oficial con Python 3.14 antes de instalar. Después: cuentas, Argon2 y JWT, antes de exponer solicitudes protegidas.
