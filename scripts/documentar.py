from pathlib import Path
import json
import re
from app.db.session import Base
from app.main import app

root = Path(".")
old = (root / "docs/requisitos.md").read_text(encoding="utf-8-sig")
criteria = {a: b.strip() for a, b in re.findall(r"(AC-RF-\d\d-01): (.+)", old)}
rf = {
    1: "Registrar solicitud y radicado",
    2: "Revisar, aceptar o rechazar",
    3: "Consultar solicitudes y estado",
    4: "Historial e intervenciones",
    5: "Finalización con respuesta y resultado",
    6: "Consultar resultado propio",
    7: "Consolidado y filtros",
    8: "JWT y cambio de contraseña",
    9: "Autorización",
    10: "Autorregistro",
    11: "Administración de cuentas y roles",
    12: "Asignación y reasignación",
    13: "Información adicional por texto",
    14: "Corrección de solicitud",
    15: "Cancelación antes de revisión",
    16: "Reapertura",
    17: "Duplicados",
    18: "Prioridades y plazos",
    19: "Notificaciones internas",
}
branches = {
    1: "registrar-solicitud",
    2: "evaluar-solicitud",
    3: "consultar-solicitudes",
    4: "historial-atencion",
    5: "finalizar-solicitud",
    6: "consultar-resultado",
    7: "consolidado",
    8: "autenticacion-jwt",
    9: "autorizacion",
    10: "autorregistro",
    11: "administrar-usuarios",
    12: "asignar-responsable",
    13: "informacion-adicional",
    14: "corregir-solicitud",
    15: "cancelar-solicitud",
    16: "reapertura",
    17: "duplicados",
    18: "prioridades-plazos",
    19: "notificaciones",
}
s = """# Requisitos y alcance

## Problema y objetivo
La información de solicitudes llega de forma dispersa y dificulta consultar pendientes, acciones y resultados. El sistema centraliza recepción, evaluación, atención, respuesta y supervisión.

Actores y stakeholders: solicitante, personal de atención, coordinación, estudiante desarrolladora y docente evaluador. La estudiante trabaja individualmente.

## Fuentes y estado de aprobación
- Guía PF-01 versión 002 del 04-11-2026, suministrada como texto pegado. El archivo README original independiente no se recibió en este chat.
- PowerPoint suministrado: texto de 12 diapositivas y relaciones de diapositivas revisadas; sin inspección visual completa.
- Respuestas reales aportadas por la estudiante: docs/entrevista.md. Fecha, medio y evidencia original pendientes.
- Decisiones autorizadas por la estudiante: docs/alcance_autorizado.txt (solicitud nueva, prevalece frente a borradores). No equivale a aprobación del profesor.

## Condiciones de la guía
CA-01: registro persistido y recuperable. CA-02: evaluación/gestión autorizada registrada. CA-03: estado coherente. CA-04: historial asociado. CA-05: resultado accesible al solicitante. CA-06: consolidado de varias solicitudes.

Se exige interfaz, REST y BD real. JWT procede de confirmación del profesor comunicada por la estudiante, no de una frase atribuida a la guía. GitHub, ramas y PR son evidencia académica requerida; los PR están pendientes por autenticación. No se exige Docker, CI ni nube. El apunte “nerocu” requiere aclaración.

## Alcance de esta versión
Cinco categorías administrativas; no expide certificados automáticamente ni modifica sistemas institucionales. Intercambio de información exclusivamente por texto. Incluye múltiples roles, administración, asignación, revisión, historial, respuesta, reapertura manual, duplicidad manual, plazos y avisos internos.

Excluye adjuntos, correo real, WhatsApp, pagos, recuperación por correo, integraciones externas, eliminación física y detección automática de duplicados.

## RF y criterios verificables
"""
for n, name in rf.items():
    rid = f"RF-{n:02}"
    cid = "AC-" + rid + "-01"
    s += f"\n### {rid} — {name}\n{cid}: {criteria.get(cid, 'Consultar alcance autorizado y prueba asociada.')}\n"
s += """
## Requisitos no funcionales
RNF-01: validación real en servidor. RNF-02: relaciones y persistencia. RNF-03: HTTP coherente y errores controlados. RNF-04: secretos fuera de respuestas, registros y Git. RNF-05: instalación reproducible. RNF-06: pruebas documentadas. No se prometen métricas de rendimiento/disponibilidad.

## Reglas y restricciones
RN-01: intervención ligada al caso. RN-02: resultado y respuesta ligados al caso. RN-03: transiciones cerradas. RN-04: seis datos obligatorios. RN-05: radicado único generado con identidad BD, inmutable. RN-06: propietario solo consulta sus casos salvo permisos de personal. RN-07: roles acumulables. RN-08: rechazo con motivo por contenido fuera de competencia aunque exista categoría. RN-09: coordinación asigna. RN-10: responsable finaliza. RN-11: corrección/cancelación del solicitante solo en registrada. RN-12: duplicados conservan historia y propietario. RN-13: prioridad y plazo por servicio.

No se aceptan propietario, fechas, hashes, autorías, radicado o estado desde entradas genéricas. Las acciones incluyen versión optimista. Los límites de longitud, plazos calendario y decisiones de reapertura son acuerdos de implementación de la estudiante. No son políticas reales del cliente. Detalle completo en alcance_autorizado.txt y esquemas Pydantic.

## Prioridad y aceptación
Todos los RF-01 a RF-19 pertenecen al alcance autorizado; se implementaron por dependencias. La implementación y pruebas de API no sustituyen aprobación docente ni demostración visual. PF-12 y prueba visual de texto malicioso están pendientes por permiso de navegador denegado.
"""
(root / "docs/requisitos.md").write_text(s, encoding="utf-8")
# Entrevista ya consolidada desde respuestas aportadas; conservarla al regenerar.
(root / "docs/decisiones.md").write_text(
    """# Decisiones de implementación

La solicitud más reciente, conservada en alcance_autorizado.txt, cierra las decisiones autorizadas por la estudiante y sustituye las propuestas anteriores. No se presenta como aprobación del cliente.

- Un monolito FastAPI sirve frontend y API. SQLAlchemy/SQLite y Alembic conservan relaciones y evolución. Se comprobó compatibilidad en Python 3.14.2 con importaciones, Argon2, pruebas e instalación separada.
- Correo normalizado con trim y minúsculas; documento textual no único; copias de identidad presentada en cada caso, independientes del perfil.
- Catálogo de cinco servicios sin servicio libre. La revisión puede rechazar el contenido cuando excede competencia, aunque se haya elegido una categoría válida.
- Radicado SOL-añoUTC-ID con mínimo ocho dígitos, calculado después del flush de identidad y dentro de la misma transacción.
- JWT HS256 fijado en servidor, 30 minutos inicialmente; versión de autenticación invalida tokens tras cambio de contraseña, roles o activación. Logout solo elimina copia de memoria, no revoca JWT emitido. No refresh tokens.
- Una coordinación inicial mediante comando interactivo; script demo separado con contraseñas aleatorias locales. Sin clave funcional predeterminada. .env excluido.
- Ciclos de atención preservan finalizaciones anteriores y permiten promediar solo ciclos resueltos. Cada reapertura reinicia ciclo con el plazo copiado original; sin modificar el servicio ni radicado.
- Horas calendario sin pausar esperas. Servicios inicialmente normal/sin plazo. No hay edición individual de plazos. Cambiar de servicio mediante corrección no recalcula silenciosamente la copia de prioridad/plazo ya registrada.
- Notas y auditoría detallada internas, eventos públicos separados. Rectificaciones solo de notas, con vínculo y misma privacidad cuando la anterior era interna. Las acciones de negocio se corrigen con su operación específica, sin alterar registros pasados.
- Cancelación solicita motivo como evidencia del retiro (decisión técnica de trazabilidad). No permite reapertura en esta versión.
- Se usa control optimista del ORM y versión de entrada. Las invariantes de última coordinación, asignación y grafo de duplicidad reservan la escritura SQLite antes de comprobarlas.
- Ramas reales por RF, commits y merges locales tras pruebas. No se disponía de autenticación GitHub utilizable sin interacción; no se simulan PR remotos.

## Pendientes externos
Aprobación definitiva del alcance, prioridades/plazos reales, política hábil/calendario institucional, necesidad futura de documentos, significado de “nerocu” y si las preguntas integran los 20 minutos. Ninguno se presenta como confirmado.

## Documentación oficial consultada
FastAPI: https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
SQLAlchemy: https://docs.sqlalchemy.org/en/20/intro.html
Alembic: https://alembic.sqlalchemy.org/en/latest/
pytest: https://docs.pytest.org/en/stable/
Consulta: 16-11-2026. Las versiones instaladas se conservan en requirements.txt; no se infieren de los ejemplos web.
""",
    encoding="utf-8",
)
# Diagramas y diccionario desde el modelo real, sin inventar atributos.
s = (root / "docs/diseno.md").read_text(encoding="utf-8-sig").split("## Diagrama ER implementado")[
    0
].rstrip() + "\n"
s += "\n## Diagrama ER implementado\n```mermaid\nerDiagram\n"
for table in Base.metadata.sorted_tables:
    for fk in table.foreign_keys:
        s += f'    {fk.column.table.name} ||--o{{ {table.name} : "{fk.parent.name}"\n'
s += "```\n\n## Modelo relacional y diccionario\nUTC interno: columnas DateTime sin zona en SQLite; serialización con Z. No hay eliminación desde la API.\n"
for table in Base.metadata.sorted_tables:
    s += (
        "\n### "
        + table.name
        + "\n\n| Columna | Tipo SQL | Nulo | Clave / restricción |\n|---|---|---|---|\n"
    )
    for col in table.columns:
        flags = []
        if col.primary_key:
            flags.append("PK")
        if col.unique:
            flags.append("UNIQUE")
        flags.extend("FK " + str(fk.target_fullname) for fk in col.foreign_keys)
        s += (
            f"| {col.name} | {col.type} | {'Sí' if col.nullable else 'No'} | {', '.join(flags)} |\n"
        )
    for c in table.constraints:
        if hasattr(c, "sqltext"):
            s += "\nCHECK: `" + str(c.sqltext) + "`\n"
    for idx in table.indexes:
        s += "\nÍndice: `" + idx.name + "`" + (" único" if idx.unique else "") + "\n"
s += "\n## Clases de dominio implementadas\n```mermaid\nclassDiagram\n"
for mapper in Base.registry.mappers:
    s += "    class " + mapper.class_.__name__ + " {\n"
    for col in mapper.columns:
        s += "        " + col.name + "\n"
    s += "    }\n"
s += '    Usuario "*" -- "*" Rol\n    Usuario "1" -- "*" Solicitud : propietario\n    Servicio "1" -- "*" Solicitud\n    Solicitud "1" -- "*" Intervencion\n    Solicitud "1" -- "*" Ciclo\n    Solicitud "1" -- "*" Requerimiento\n    Solicitud "1" -- "*" Reapertura\n    Solicitud "1" -- "*" Notificacion\n```\n'
s += """
## Estados
```mermaid
stateDiagram-v2
[*] --> registrada
registrada --> en_revision
registrada --> cancelada
en_revision --> aceptada
en_revision --> rechazada
aceptada --> asignada
asignada --> en_atencion
en_revision --> pendiente_informacion
en_atencion --> pendiente_informacion
pendiente_informacion --> en_revision
pendiente_informacion --> en_atencion
en_atencion --> finalizada
finalizada --> en_revision: reapertura aprobada
```
Cualquier estado activo puede cerrarse por duplicidad. Reasignar conserva estado. Pedir reapertura no cambia estado. Motivos y versión son obligatorios en acciones administrativas.

## Componentes y permisos
api contiene adaptadores HTTP; schemas define entradas explícitas; services/operations_* ejecuta reglas y transacciones; models refleja tablas; db activa claves foráneas; core protege configuración/JWT/Argon2. El frontend usa textContent, token en memoria y navegación por roles. La autorización efectiva se comprueba en servidor.

Solicitante: casos propios, corrección/cancelación solo registrada, respuesta a requerimiento propio y petición de reapertura. Atención: consulta global y evaluación; gestión operativa solo como responsable. Coordinación: administración, asignación, supervisión, duplicados, reaperturas y consolidado; también requiere ser responsable para iniciar/finalizar atención. Múltiples roles acumulan permisos conservando propiedad y estado.

## Prototipos y estado visual
La interfaz real está en app/frontend. Vista de acceso/registro; navegación de solicitudes, nueva solicitud, personal, servicios, consolidado y notificaciones; detalle con formularios según estado/permisos. No se incluyen capturas inventadas: la inspección del frontend completo quedó bloqueada por permiso de navegador denegado. Probar responsive, teclado y texto malicioso con el manual antes de exposición.
"""
(root / "docs/diseno.md").write_text(s, encoding="utf-8")
openapi = app.openapi()
(root / "docs/openapi.json").write_text(
    json.dumps(openapi, ensure_ascii=False, indent=2), encoding="utf-8"
)
s = """# API implementada

Prefijo /api/v1. Entradas y respuestas JSON. Login usa JSON correo/contrasena (no formulario OAuth2). En rutas protegidas enviar Authorization: Bearer <JWT>; nunca guardar el JWT en documentación ni capturas. Contrato generado desde la aplicación: [openapi.json](openapi.json), disponible en /docs y /openapi.json.

Las rutas públicas son salud, registro y token. Cualquier otra ruta de negocio exige cuenta activa y JWT válido. Devuelven diccionarios explícitos, nunca objetos ORM ni hashes.

| Método | Ruta | Entrada | Operación |
|---|---|---|---|
"""
for path, methods in openapi["paths"].items():
    for method, op in methods.items():
        body = (
            op.get("requestBody", {})
            .get("content", {})
            .get("application/json", {})
            .get("schema", {})
        )
        entry = body.get("$ref", "").split("/")[-1] or (
            "Parámetros de ruta/consulta" if op.get("parameters") else "Sin cuerpo"
        )
        s += f"| {method.upper()} | {path} | {entry} | {op.get('summary', '')} |\n"
s += """
## Entradas exactas
"""
for name, schema in openapi.get("components", {}).get("schemas", {}).items():
    if name in ("HTTPValidationError", "ValidationError"):
        continue
    s += "\n### " + name + "\n\n"
    for field, definition in schema.get("properties", {}).items():
        s += (
            "- `"
            + field
            + "`"
            + (" obligatorio" if field in schema.get("required", []) else " opcional")
            + ": "
            + json.dumps(definition, ensure_ascii=False)
            + "\n"
        )
s += """
## Salidas y permisos
- Cuenta: id, nombre, documento, correo, activo y roles. Solo coordinación lista/crea personal o modifica roles/activación; cada persona consulta me y cambia su contraseña con la actual.
- Token: access_token y token_type. Credenciales incorrectas siempre 401 sin confirmar existencia de cuenta.
- Solicitud: identidad presentada, IDs, radicado, estado, prioridad/plazo, versión, fechas, vencimiento y duraciones. Listar/detalle según propiedad o rol de personal. El resultado se consulta en /resultado solo si finalizada.
- Historial: id, tipo, detalle, fecha, estados y rectificación. Personal puede recibir autor, visibilidad y auditoría; un solicitante sin roles de personal nunca recibe notas internas ni datos_cambio.
- Requerimientos y reaperturas: lista paginada asociada a caso visible. Solo propietario responde/pide; coordinación decide reapertura.
- Servicios: catálogo para cuentas autenticadas; configuración solo coordinación.
- Reporte: items/total/page/size y conteos por estado/servicio/prioridad, pendientes_activos, vencidas, promedio_resolucion_horas (null si no existen ciclos resueltos). Solo coordinación.
- Notificaciones: lista propia y lectura propia; otro destinatario obtiene 404.

## Códigos y validación
201 creación; 200 consulta/acción con cuerpo; 401 autenticación inválida; 403 permiso insuficiente; 404 inexistente o caso ajeno; 409 estado, versión, unicidad o integridad; 422 entrada inválida. Campos extra rechazados. Errores de validación excluyen input y contexto para no reflejar contraseñas.

Listados de casos: page=1, size=20, máximo 100, orden fecha/ID descendente. Filtros exactos: estado, responsable_id, servicio_id, prioridad, desde, hasta, radicado. Fechas en Colombia; hasta incluye todo el día mediante límite UTC exclusivo del día siguiente. Reportes usan el mismo selector. Otros listados aceptan page/size; historial/requerimientos/reaperturas por caso; personal ordenado por ID.

Todos los cambios de caso aceptan version actual. Si obtienes 409, recarga y vuelve a evaluar; no reintentes silenciosamente. PATCH genérico solo acepta los seis datos presentados y motivo administrativo cuando corresponde. No acepta estado, propietario, radicado, autorías o fechas.

## Ejemplo sin secretos
GET /api/v1/salud devuelve 200 y {"estado":"disponible"}. Para ejemplos de flujo real con datos ficticios, consultar evidencias/flujo-http-real.json. Se excluyen expresamente llamadas de login y credenciales.
"""
(root / "docs/api.md").write_text(s, encoding="utf-8")
# Trazabilidad verificable a ramas y evidencias, sin PR inventados.
s = "# Trazabilidad\n\n| CA | RF y criterio | Componente | Rama real | PR | Evidencia |\n|---|---|---|---|---|---|\n"
ca = {1: "CA-01", 2: "CA-02", 3: "CA-03", 4: "CA-04", 5: "CA-05", 6: "CA-05", 7: "CA-06"}
modules = {
    1: "cases",
    2: "workflow",
    3: "cases",
    4: "history",
    5: "workflow",
    6: "cases",
    7: "reports",
    8: "auth",
    9: "permissions",
    10: "auth",
    11: "users",
    12: "workflow",
    13: "questions",
    14: "cases",
    15: "workflow",
    16: "reopen",
    17: "workflow",
    18: "cases",
    19: "notifications",
}
for n in rf:
    rid = f"RF-{n:02}"
    file = (
        "app/services/permissions.py" if n == 9 else "app/services/operations_" + modules[n] + ".py"
    )
    s += f"| {ca.get(n, 'Transversal')} | {rid}, AC-{rid}-01 | {file}; frontend app.js | feature/{rid}-{branches[n]} | Pendiente (sin autenticación) | evidencias/{rid}.xml; pruebas finales en validacion-integral.xml |\n"
s += "\nLas evidencias por RF fueron ejecutadas antes de la separación final de capas y se conservan como historia. validacion-integral.xml y instalacion-limpia.xml comprueban el código final. PF-12 y revisión visual completa están bloqueadas por navegador; no se declaran aprobadas por tener pruebas HTTP.\n"
(root / "docs/trazabilidad.md").write_text(s, encoding="utf-8")
print(
    "Requisitos, entrevista, diseño, diccionario, API y trazabilidad actualizados desde fuentes y modelo real."
)
