# Pruebas del incremento 0

Fecha: 16-11-2026 (Colombia). Versión de aplicación: 0.0.1, sin commit. Entorno: Windows, Python 3.14.2 y versiones fijadas en requirements.txt. Estas verificaciones no sustituyen PF-01 a PF-12.

## Preparación

En PowerShell, desde la raíz:

```powershell
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Mantener esa consola abierta. En otra consola:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/api/v1/salud
(Invoke-WebRequest http://127.0.0.1:8000/).StatusCode
(Invoke-WebRequest http://127.0.0.1:8000/docs).StatusCode
curl.exe -i http://127.0.0.1:8000/no-existe
```

## Resultados observados

| ID | Relación | Entrada / pasos | Esperado | Observado | Estado |
|---|---|---|---|---|---|
| I0-01 | RNF-05 | pip check con .venv | Sin incompatibilidades | No broken requirements found | Aprobada |
| I0-02 | RNF-05 | Importar app.main y generar app.openapi() | Importación y contrato disponibles | Correctos | Aprobada |
| I0-03 | RNF-03 | Arrancar Uvicorn | Startup complete | Servidor iniciado | Aprobada |
| I0-04 | RNF-03 | GET /api/v1/salud sin cuerpo | 200 y {"estado":"disponible"} | Coincide exactamente | Aprobada |
| I0-05 | RNF-05 | GET / y CSS/JS | 200 | 200 en los tres recursos | Aprobada |
| I0-06 | RNF-05 | GET /docs y /openapi.json | 200 y contrato con salud | Coincide | Aprobada |
| I0-07 | RNF-03 | GET /no-existe | 404 controlado | 404 | Aprobada |
| I0-08 | RNF-05 | Abrir / en navegador; pulsar Comprobar conexión | Mensaje de éxito | Conexión correcta. El sistema está disponible. | Aprobada |
| I0-09 | RNF-03 | Con página cargada, detener servidor y pulsar Comprobar conexión | Mensaje de error y botón habilitado | Mensaje de error visible; al reiniciar y pulsar, vuelve el éxito | Aprobada |

Evidencia HTTP: [incremento-0-http.json](../evidencias/incremento-0-http.json), peticiones reales con urllib y aserciones de código, JSON y presencia de ruta OpenAPI. Evidencia de navegador: observación del árbol accesible en el navegador integrado, incluida la respuesta después de pulsar el botón. No hay captura guardada. /docs devuelve HTML, pero la carga de sus recursos Swagger externos no se ha comprobado visualmente.

Al principio el entorno de ejecución bloqueó sockets con WinError 10013. Tras conceder acceso de red se repitieron las peticiones y pasaron. Esto fue una restricción del entorno del agente; no se cambió la configuración de Windows.

Reproducción de I0-09 (ejecutada): cargar la página, detener Uvicorn con Ctrl+C sin cerrar la pestaña, pulsar el botón y comprobar el mensaje de error. Volver a arrancar Uvicorn y pulsar nuevamente para recuperar el mensaje de éxito. Se observó el error y la recuperación en el navegador integrado.

## Git

Se verificó rama chore/base-aplicacion, repositorio sin commits ni remoto. La primera creación de rama falló por permisos; después de conceder acceso a .git se creó correctamente. No hay commit ni PR creado. git diff no muestra contenido de archivos sin seguimiento: revisar esos archivos explícitamente antes de preparar un commit.

## Pendiente

No se ha verificado instalación limpia ni persistencia, JWT, permisos, reglas o integración con BD. Todos los escenarios PF siguen pendientes. Para cada escenario futuro se documentarán RF, criterio AC, precondiciones, datos, pasos, esperado, observado, HTTP, evidencia y estado.
