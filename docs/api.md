# API implementada

Prefijo /api/v1. Entradas y respuestas JSON. Login usa JSON correo/contrasena (no formulario OAuth2). En rutas protegidas enviar Authorization: Bearer <JWT>; nunca guardar el JWT en documentación ni capturas. Contrato generado desde la aplicación: [openapi.json](openapi.json), disponible en /docs y /openapi.json.

Las rutas públicas son salud, registro y token. Cualquier otra ruta de negocio exige cuenta activa y JWT válido. Devuelven diccionarios explícitos, nunca objetos ORM ni hashes.

| Método | Ruta | Entrada | Operación |
|---|---|---|---|
| POST | /api/v1/auth/token | Login | Login |
| GET | /api/v1/usuarios/me | Sin cuerpo | Me |
| POST | /api/v1/usuarios/me/contrasena | PasswordChange | Change Password |
| POST | /api/v1/auth/registro | Registration | Register |
| GET | /api/v1/salud | Sin cuerpo | Health |
| GET | /api/v1/usuarios | Parámetros de ruta/consulta | Users |
| POST | /api/v1/usuarios | StaffCreate | Create |
| PUT | /api/v1/usuarios/{uid}/roles | StaffUpdate | Update |
| GET | /api/v1/servicios | Sin cuerpo | Services |
| POST | /api/v1/solicitudes | CaseCreate | Create |
| GET | /api/v1/solicitudes | Parámetros de ruta/consulta | Listing |
| GET | /api/v1/solicitudes/{sid} | Parámetros de ruta/consulta | Detail |
| PATCH | /api/v1/solicitudes/{sid} | Correction | Correct |
| GET | /api/v1/solicitudes/{sid}/resultado | Parámetros de ruta/consulta | Result |
| PATCH | /api/v1/servicios/{sid}/configuracion | ServiceConfig | Configure Service |
| GET | /api/v1/solicitudes/{sid}/historial | Parámetros de ruta/consulta | History |
| POST | /api/v1/solicitudes/{sid}/intervenciones | Note | Note |
| POST | /api/v1/solicitudes/{sid}/revision | Action | Review |
| POST | /api/v1/solicitudes/{sid}/aceptacion | Action | Accept |
| POST | /api/v1/solicitudes/{sid}/rechazo | Motive | Reject |
| PUT | /api/v1/solicitudes/{sid}/responsable | Assign | Assign |
| POST | /api/v1/solicitudes/{sid}/inicio-atencion | Action | Start |
| POST | /api/v1/solicitudes/{sid}/finalizacion | Finalize | Finish |
| POST | /api/v1/solicitudes/{sid}/cancelacion | Motive | Cancel |
| POST | /api/v1/solicitudes/{sid}/duplicidad | Duplicate | Duplicate |
| GET | /api/v1/solicitudes/{sid}/requerimientos | Parámetros de ruta/consulta | Questions |
| POST | /api/v1/solicitudes/{sid}/requerimientos | Question | Ask |
| POST | /api/v1/requerimientos/{rid}/respuesta | Answer | Answer |
| GET | /api/v1/solicitudes/{sid}/reaperturas | Parámetros de ruta/consulta | Listing |
| POST | /api/v1/solicitudes/{sid}/reaperturas | Motive | Request Reopening |
| POST | /api/v1/reaperturas/{rid}/decision | ReopenDecision | Decide |
| GET | /api/v1/reportes/solicitudes | Parámetros de ruta/consulta | Report |
| GET | /api/v1/notificaciones | Parámetros de ruta/consulta | Listing |
| PATCH | /api/v1/notificaciones/{nid}/lectura | Parámetros de ruta/consulta | Read |

## Entradas exactas

### Action

- `version` obligatorio: {"type": "integer", "minimum": 1.0, "title": "Version"}

### Answer

- `version` obligatorio: {"type": "integer", "minimum": 1.0, "title": "Version"}
- `respuesta` obligatorio: {"type": "string", "maxLength": 5000, "minLength": 1, "title": "Respuesta"}

### Assign

- `version` obligatorio: {"type": "integer", "minimum": 1.0, "title": "Version"}
- `motivo` obligatorio: {"type": "string", "maxLength": 2000, "minLength": 10, "title": "Motivo"}
- `responsable_id` obligatorio: {"type": "integer", "exclusiveMinimum": 0.0, "title": "Responsable Id"}

### CaseCreate

- `nombre` obligatorio: {"type": "string", "maxLength": 120, "minLength": 2, "title": "Nombre"}
- `documento` obligatorio: {"type": "string", "maxLength": 30, "minLength": 3, "title": "Documento"}
- `correo` obligatorio: {"type": "string", "maxLength": 254, "format": "email", "title": "Correo"}
- `servicio_id` obligatorio: {"type": "integer", "exclusiveMinimum": 0.0, "title": "Servicio Id"}
- `asunto` obligatorio: {"type": "string", "maxLength": 150, "minLength": 5, "title": "Asunto"}
- `descripcion` obligatorio: {"type": "string", "maxLength": 5000, "minLength": 20, "title": "Descripcion"}

### Correction

- `nombre` obligatorio: {"type": "string", "maxLength": 120, "minLength": 2, "title": "Nombre"}
- `documento` obligatorio: {"type": "string", "maxLength": 30, "minLength": 3, "title": "Documento"}
- `correo` obligatorio: {"type": "string", "maxLength": 254, "format": "email", "title": "Correo"}
- `servicio_id` obligatorio: {"type": "integer", "exclusiveMinimum": 0.0, "title": "Servicio Id"}
- `asunto` obligatorio: {"type": "string", "maxLength": 150, "minLength": 5, "title": "Asunto"}
- `descripcion` obligatorio: {"type": "string", "maxLength": 5000, "minLength": 20, "title": "Descripcion"}
- `version` obligatorio: {"type": "integer", "minimum": 1.0, "title": "Version"}
- `motivo` opcional: {"anyOf": [{"type": "string", "maxLength": 2000, "minLength": 10}, {"type": "null"}], "title": "Motivo"}

### Duplicate

- `version` obligatorio: {"type": "integer", "minimum": 1.0, "title": "Version"}
- `motivo` obligatorio: {"type": "string", "maxLength": 2000, "minLength": 10, "title": "Motivo"}
- `original_id` obligatorio: {"type": "integer", "exclusiveMinimum": 0.0, "title": "Original Id"}

### Finalize

- `version` obligatorio: {"type": "integer", "minimum": 1.0, "title": "Version"}
- `respuesta` obligatorio: {"type": "string", "maxLength": 5000, "minLength": 10, "title": "Respuesta"}
- `resultado` obligatorio: {"type": "string", "maxLength": 2000, "minLength": 5, "title": "Resultado"}

### Login

- `correo` obligatorio: {"type": "string", "format": "email", "title": "Correo"}
- `contrasena` obligatorio: {"type": "string", "maxLength": 128, "minLength": 1, "title": "Contrasena"}

### Motive

- `version` obligatorio: {"type": "integer", "minimum": 1.0, "title": "Version"}
- `motivo` obligatorio: {"type": "string", "maxLength": 2000, "minLength": 10, "title": "Motivo"}

### Note

- `version` obligatorio: {"type": "integer", "minimum": 1.0, "title": "Version"}
- `detalle` obligatorio: {"type": "string", "maxLength": 5000, "minLength": 1, "title": "Detalle"}
- `interna` opcional: {"type": "boolean", "title": "Interna", "default": true}
- `rectifica_id` opcional: {"anyOf": [{"type": "integer", "exclusiveMinimum": 0.0}, {"type": "null"}], "title": "Rectifica Id"}

### PasswordChange

- `actual` obligatorio: {"type": "string", "maxLength": 128, "minLength": 1, "title": "Actual"}
- `nueva` obligatorio: {"type": "string", "maxLength": 128, "minLength": 12, "title": "Nueva"}

### Question

- `version` obligatorio: {"type": "integer", "minimum": 1.0, "title": "Version"}
- `pregunta` obligatorio: {"type": "string", "maxLength": 2000, "minLength": 10, "title": "Pregunta"}

### Registration

- `nombre` obligatorio: {"type": "string", "maxLength": 120, "minLength": 2, "title": "Nombre"}
- `documento` obligatorio: {"type": "string", "maxLength": 30, "minLength": 3, "title": "Documento"}
- `correo` obligatorio: {"type": "string", "maxLength": 254, "format": "email", "title": "Correo"}
- `contrasena` obligatorio: {"type": "string", "maxLength": 128, "minLength": 12, "title": "Contrasena"}

### ReopenDecision

- `version` obligatorio: {"type": "integer", "minimum": 1.0, "title": "Version"}
- `motivo` obligatorio: {"type": "string", "maxLength": 2000, "minLength": 10, "title": "Motivo"}
- `aprobar` obligatorio: {"type": "boolean", "title": "Aprobar"}

### ServiceConfig

- `prioridad` obligatorio: {"type": "string", "enum": ["baja", "normal", "alta"], "title": "Prioridad"}
- `plazo_horas` opcional: {"anyOf": [{"type": "integer", "maximum": 8760.0, "minimum": 1.0}, {"type": "null"}], "title": "Plazo Horas"}

### StaffCreate

- `nombre` obligatorio: {"type": "string", "maxLength": 120, "minLength": 2, "title": "Nombre"}
- `documento` obligatorio: {"type": "string", "maxLength": 30, "minLength": 3, "title": "Documento"}
- `correo` obligatorio: {"type": "string", "maxLength": 254, "format": "email", "title": "Correo"}
- `contrasena` obligatorio: {"type": "string", "maxLength": 128, "minLength": 12, "title": "Contrasena"}
- `roles` obligatorio: {"items": {"type": "string", "enum": ["solicitante", "atencion", "coordinacion"]}, "type": "array", "maxItems": 3, "minItems": 1, "title": "Roles"}

### StaffUpdate

- `roles` obligatorio: {"items": {"type": "string", "enum": ["solicitante", "atencion", "coordinacion"]}, "type": "array", "maxItems": 3, "minItems": 1, "title": "Roles"}
- `activo` obligatorio: {"type": "boolean", "title": "Activo"}

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
