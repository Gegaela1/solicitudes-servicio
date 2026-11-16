# Sistema de gestión de solicitudes de servicio

Proyecto Final 01 (PF-01), Aplicaciones y Servicios Web. Desarrollo individual: Gegaela1 (nombre académico completo pendiente de suministrar). Entrega prevista: 18-11-2026 antes de las 18:00, America/Bogota.

## Estado y evidencia

Implementados RF-01 a RF-19: interfaz HTML/CSS/JavaScript, API FastAPI, SQLite relacional, migración Alembic, JWT/Argon2, permisos, historial, atención, reapertura, duplicados, consolidado, plazos y avisos internos.

26 pruebas automatizadas aprobadas en entorno habitual y 26 en instalación separada; flujo HTTP real completado con datos ficticios. **Pendientes de entrega:** recorrido visual completo PF-12 (permiso de navegador denegado), revisión responsive/teclado/texto malicioso, publicación y PR en GitHub (sin autenticación disponible), aprobación académica final. No se declara el proyecto totalmente aceptado mientras esos puntos sigan pendientes.

No se ha confirmado la existencia privada del repositorio previsto. No hay URL remota ni PR real que citar. Cuenta pública suministrada: https://github.com/Gegaela1/ (perfil, no repositorio). El código y el historial real están en esta carpeta local.

## Problema, actores y alcance

Centraliza solicitudes dispersas para conservar recepción, evaluación, atención, respuesta y supervisión. Actores: solicitante, atención y coordinación; una cuenta puede acumular roles. Coordinación administra personal y permisos.

Servicios: certificados, actualización de información, documentos, consultas de trámites y peticiones generales. Son categorías administrativas; el sistema registra el resultado del trámite. Sin adjuntos, generación automática de certificados, correo real, pagos, WhatsApp ni integraciones externas. No hay despliegue cloud; el apunte “nerocu” sigue sin aclarar.

- [Requisitos, fuentes y criterios](docs/requisitos.md)
- [Respuestas del cliente aportadas](docs/entrevista.md)
- [Decisiones de implementación de la estudiante](docs/decisiones.md)
- [Alcance autorizado completo](docs/alcance_autorizado.txt)

No se inventó entrevista, aprobación del profesor ni revisión externa.

## Arquitectura y tecnologías

Navegador → API REST → esquemas y servicios → SQLAlchemy → SQLite. FastAPI sirve la página y la API en el mismo origen. No hay CORS abierto.

Python 3.14.2, FastAPI/Pydantic 2, SQLAlchemy, SQLite, Alembic, PyJWT y pwdlib/Argon2. Las versiones efectivamente instaladas y comprobadas están fijadas en requirements.txt, incluidas herramientas pytest/httpx/Ruff. Sin microservicios ni dependencias de frontend.

[Diseño, ER, modelo relacional, diccionario y clases](docs/diseno.md). Los esquemas compartidos se prepararon en rama transversal; cada RF tiene su rama y commit real. Las reglas están en app/services, las rutas HTTP en app/api, entradas explícitas en app/schemas y persistencia en app/models.

## Instalar desde una copia limpia

Requiere Python 3.14.2, PowerShell y Git. No hace falta cambiar configuración global de Git.

```powershell
Set-Location 'C:\Users\Usuario\Documents\solicitudes-servicio'
.\scripts\instalar.ps1
```

El script conserva un .venv existente, instala las versiones fijadas, comprueba pip, crea .env con clave aleatoria solo si no existe, aplica migraciones y prepara catálogo/roles. No borra BD ni crea contraseñas predeterminadas. En una copia extraída en otra ubicación, cambia Set-Location a esa carpeta.

Alternativa manual:

```powershell
New-Item -ItemType Directory -Force work/tmp | Out-Null
$env:TEMP=(Resolve-Path work/tmp).Path
$env:TMP=$env:TEMP
py -3.14 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe scripts/configurar.py
.\.venv\Scripts\python.exe -m alembic upgrade head
.\.venv\Scripts\python.exe -m scripts.preparar
```

En esta carpeta ya existe .venv verificado: no es necesario recrearlo. La instalación limpia se verificó aparte en .venv-clean y work/instalacion-limpia.db, sin tocar la BD de demostración.

## Configuración y acceso inicial seguro

.env.example contiene nombres de variables sin secreto. scripts/configurar.py genera SECRET_KEY aleatoria en .env. DATABASE_URL apunta a SQLite local; ACCESS_TOKEN_EXPIRE_MINUTES inicia en 30; APP_ENV identifica el entorno. Configuración inválida impide importar la aplicación con mensaje sin datos sensibles. Nunca publiques .env.

En una BD nueva:

```powershell
.\.venv\Scripts\python.exe -m scripts.crear_coordinador
```

Solicita nombre, documento, correo y contraseña sin eco; comprueba repetición y no permite argumentos de contraseña. No crea otra coordinación inicial si ya existe una activa. Luego coordinación crea el personal desde la interfaz. Solicitantes usan autorregistro.

Esta carpeta ya contiene cuentas **ficticias demo** creadas durante la verificación. Para utilizarlas, abre localmente `work/demo-acceso.json` en VS Code. Sus contraseñas fueron generadas aleatoriamente y el archivo está excluido de Git y de la entrega ZIP. No lo proyectes ni lo compartas. Para preparar demos en una instalación nueva:

```powershell
.\.venv\Scripts\python.exe -m scripts.datos_demo
```

El script no cambia contraseñas ni cuentas existentes. Si quieres separar una BD real de la demo, configura una URL SQLite nueva (sin borrar la anterior), migra, prepara roles y usa el comando interactivo de coordinación.

## Ejecutar

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8001
```

Abrir http://127.0.0.1:8001/ y http://127.0.0.1:8001/docs. Detener con Ctrl+C. --reload es opcional exclusivamente para desarrollo. Usa siempre el intérprete de .venv; no es obligatorio activar el entorno.

El JWT solo vive en memoria del navegador. Recargar exige nuevo acceso. Cambiar contraseña invalida tokens anteriores. Salir elimina la copia local, pero no revoca una copia emitida: limitación documentada. No hay refresh tokens ni recuperación por correo.

[Manual de recorridos por rol y errores](docs/manual_usuario.md).

## Servicios web

[API completa con rutas reales, esquemas, permisos y HTTP](docs/api.md) y [contrato OpenAPI](docs/openapi.json).

Grupos: auth/registro y auth/token; usuarios/me y cambio de contraseña; personal y roles; servicios/configuración; solicitudes con filtros, detalle y resultado; revisión, aceptación, rechazo, asignación, atención, finalización, cancelación; historial/rectificación; requerimientos/respuestas; reaperturas/decisiones; duplicidad; consolidado; notificaciones y lectura; salud.

GET /api/v1/salud → 200 y {"estado":"disponible"}. Las operaciones protegidas requieren Bearer JWT. Ejemplos reales sin credenciales: [flujo HTTP](evidencias/flujo-http-real.json). No se expone directamente el ORM.

## Pruebas

```powershell
.\.venv\Scripts\python.exe -m ruff check app scripts tests
.\.venv\Scripts\python.exe -m pytest -q --junitxml=evidencias/validacion-integral.xml
.\.venv\Scripts\python.exe -m alembic check
```

- [Matriz oficial y pruebas adicionales](docs/pruebas.md)
- [Resultado automatizado integral](evidencias/validacion-integral.xml)
- [Instalación limpia](evidencias/instalacion-limpia.xml)
- [Trazabilidad CA → RF → criterio → código → rama → PR pendiente → evidencia](docs/trazabilidad.md)

Las pruebas usan BD temporal propia. No borres la BD del usuario para probar. Para repetir el flujo HTTP real con servidor en 8001 y cuentas demo:

```powershell
.\.venv\Scripts\python.exe -m scripts.verificar_flujo_demo
```

Crea un nuevo caso ficticio, lo procesa con las cuentas de cada rol y guarda evidencia sin login/token/contraseña. No es una prueba de navegador y no sustituye PF-12.

## Git, GitHub y contribuciones

Todo el trabajo corresponde a la estudiante con asistencia técnica de Codex; no se atribuyen revisiones a otras personas. Hay 19 ramas feature/RF-XX y commits/merges locales reales por dependencias. La autorrevisión y evidencia se registraron antes de integrar. Sin autenticación GitHub utilizable, no se publicaron cambios ni se crearon PR.

```powershell
git log --all --graph --oneline
git branch --list 'feature/*'
git status --short
```

[Estado de GitHub y comandos concretos para publicar](docs/github.md). La falta de PR es una limitación académica explícita; no se deben abrir PR vacíos para aparentar cumplimiento. El evaluador requerirá acceso si el repositorio es privado.

## Sustentación y entrega

[Guion de 20 minutos, preguntas y respaldo](docs/sustentacion.md). Presentación editable con notas: docs/Sustentacion_PF01.pptx. El README es el informe principal; no se sustituyó por Word/PDF.

[Lista verificable de entrega](docs/entrega.md) y [avance y límites](docs/avances.md).

## Conclusiones y límites

La API y persistencia cumplen el flujo verificado de solicitudes y conservan permisos, estado e historial. Las pruebas cubren errores de entrada, JWT, propietario, responsables, reapertura, duplicidad, plazos, integridad y concurrencia. No se considera aceptación completa hasta ejecutar el recorrido visual y resolver GitHub/PR con el docente.

Dificultades observadas: restricción temporal durante pip/ensurepip resuelta con carpeta temporal local; aviso de deprecación de httpx en TestClient que no impide las pruebas; permiso de navegador denegado y autenticación GitHub no disponible. No se cambiaron protecciones de Windows.

Mejoras futuras sujetas a requisitos: políticas institucionales de plazos, recuperación de cuenta y recepción real de documentos si se autoriza. No se presentan como funciones ya implementadas.
