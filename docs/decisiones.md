# Decisiones y pendientes

Las decisiones siguientes son propuestas autorizadas por la estudiante, no aprobación textual del cliente.

6. DECISIONES PROVISIONALES AUTORIZADAS POR MÍ

Distingue estas decisiones de respuestas textuales del cliente:

- Coordinación también cumple funciones administrativas; no hay cuarto rol.
- Podemos inferir estados coherentes.
- Coordinación puede corregir administrativamente dejando trazabilidad.
- Se conservan las acciones del responsable y los permisos previos del solicitante.
- El autorregistro solo concede rol solicitante.
- Correo normalizado único como identificador de acceso.
- Documento almacenado como texto; unicidad no confirmada.
- Corrección y cancelación del solicitante solo en estado registrada.
- Iniciar revisión marca el bloqueo de esas acciones.
- Personal ve todos los casos, pero gestiona los asignados; puede revisar casos nuevos.
- Coordinación puede supervisar y gestionar; para finalizar debe figurar como responsable.
- Requerimientos adicionales por texto; no implementar adjuntos.
- Un requerimiento pendiente por solicitud.
- Historial sin eliminación ni sobrescritura; correcciones mediante nuevos registros.
- Notas internas no visibles al solicitante.
- Notificaciones internas, sin correo real.
- Duplicados identificados manualmente por coordinación y vinculados al caso original.
- Reapertura decidida por coordinación, con motivo y mismo radicado.
- Prioridades propuestas: baja, normal, alta.
- Plazos configurables por servicio.
- Sin plazo acordado, dejarlo sin definir.
- Horas calendario y sin descontar esperas como política provisional de demostración.
- No presentar esos plazos como compromisos reales del cliente.

Pendientes:
- Plazos y prioridades reales por servicio.
- Días hábiles o calendario y pausas.
- Si alguna documentación adicional futura requerirá archivos.
- Alcance definitivo aprobado.
- Despliegue exigido.
- Si preguntas están incluidas en los 20 minutos.
- Exigencia explícita de scopes JWT: no confirmada.

No detengas tareas independientes por estos pendientes. Registra las suposiciones y su impacto.

10. STACK ACORDADO COMO BASE

- Python.
- FastAPI.
- Pydantic 2.
- SQLAlchemy.
- SQLite.
- Alembic.
- PyJWT.
- Hash con Argon2 mediante una biblioteca mantenida, propuesta pwdlib.
- HTML, CSS y JavaScript con fetch.
- FastAPI sirve frontend y API desde el mismo origen.
- Ruff propuesto para formato y análisis.
- Pruebas manuales oficiales y automatizadas selectivas.
- OpenAPI y documentación interactiva.

Verifica documentación oficial vigente y compatibilidad antes de añadir dependencias, especialmente con Python 3.14.2.
Fija las versiones efectivamente instaladas y comprobadas.
No confíes únicamente en que pip resuelva: comprueba importación, arranque y comportamiento.

Arquitectura:
Navegador → rutas FastAPI y esquemas → servicios de negocio → SQLAlchemy → SQLite.

Evita microservicios, repositorios genéricos innecesarios y abstracciones sin utilidad.

11. ESTADOS PROPUESTOS

- registrada
- en_revision
- pendiente_informacion
- aceptada
- asignada
- en_atencion
- finalizada
- rechazada
- cancelada
- cerrada_duplicidad

Transiciones:
- Crear → registrada.
- registrada → en_revision: atención o coordinación.
- registrada → cancelada: propietario.
- en_revision → aceptada.
- en_revision → rechazada, con motivo.
- aceptada → asignada: coordinación.
- asignada → en_atencion: responsable.
- en_revision o en_atencion → pendiente_informacion.
- Respuesta del propietario → etapa anterior guardada.
- en_atencion → finalizada: responsable, respuesta y resultado.
- finalizada → en_revision: coordinación aprueba reapertura.
- Estado activo → cerrada_duplicidad: coordinación, motivo y caso original.

Reglas:
- Reasignación conserva estado y deja historial.
- Petición de reapertura no cambia estado por sí sola.
- Reapertura rechazada conserva finalizada.
- Reapertura aprobada conserva radicado e historial.
- Información aún insuficiente permite nuevo requerimiento.
- Cerrar duplicado cierra también requerimientos pendientes con motivo.
- Transiciones inválidas rechazadas por servidor.

12. MODELO DE DATOS PROVISIONAL

Revisa coherencia antes de convertirlo en migraciones.

usuarios:
- id PK.
- nombre.
- documento.
- correo único normalizado.
- hash_contrasena.
- activo.
- creado_en.

roles:
- id PK.
- nombre único.
- Valores: solicitante, atencion, coordinacion.

usuarios_roles:
- usuario_id FK.
- rol_id FK.
- PK compuesta para impedir duplicación.

servicios:
- id PK.
- nombre único.
- activo.
- prioridad_predeterminada opcional.
- plazo_objetivo_horas opcional y positivo.

solicitudes:
- id PK.
- radicado único inmutable.
- solicitante_id FK.
- servicio_id FK.
- responsable_id FK opcional.
- nombre_solicitante.
- documento_solicitante.
- correo_solicitante.
- asunto.
- descripcion.
- estado.
- prioridad opcional.
- plazo_objetivo_horas opcional.
- respuesta_final opcional hasta finalizar.
- resultado_final opcional hasta finalizar.
- creada_en.
- actualizada_en.
- revision_iniciada_en.
- atencion_iniciada_en.
- finalizada_en.
- solicitud_original_id FK autorreferenciada opcional.
- mecanismo de control de concurrencia por definir.

intervenciones:
- id PK.
- solicitud_id FK.
- autor_id FK.
- tipo.
- detalle.
- interna.
- estado_anterior.
- estado_nuevo.
- datos_cambio sin secretos.
- rectifica_id FK opcional.
- creada_en.

requerimientos_informacion:
- id PK.
- solicitud_id FK.
- solicitado_por_id FK.
- pregunta.
- etapa_retorno.
- respuesta opcional.
- respondido_por_id FK opcional.
- creado_en.
- respondido_en.
- cerrado_en.
- motivo_cierre.

peticiones_reapertura:
- id PK.
- solicitud_id FK.
- solicitante_id FK.
- motivo.
- estado: pendiente, aprobada o rechazada.
- resuelto_por_id FK opcional.
- motivo_decision.
- creado_en.
- resuelto_en.

notificaciones:
- id PK.
- destinatario_id FK.
- solicitud_id FK.
- mensaje.
- creada_en.
- leida_en opcional.

Consideraciones:
- Habilitar claves foráneas de SQLite.
- Datos de solicitante en solicitud conservan lo presentado originalmente.
- Perfil actualizado no cambia solicitudes históricas.
- Roles del responsable se comprueban en servidor.
- Finalización y su historial se escriben en una transacción.
- Reapertura conserva finalizaciones anteriores en historial.
- Cambios de configuración no alteran solicitudes anteriores silenciosamente.
- Usar UTC internamente y mostrar hora de Colombia.
- No usar el radicado como credencial de acceso.
- No añadir eliminación física de casos o historial.

Genera y mantén:
- Diagrama ER.
- Modelo relacional.
- Diccionario de datos.
- Diagrama de clases de dominio.
Los diagramas deben coincidir con la implementación real y distinguir el diseño pendiente.

13. API PROPUESTA

Prefijo /api/v1.

POST /auth/registro
POST /auth/token
GET /usuarios/me
POST /usuarios
PUT /usuarios/{id}/roles
GET /servicios
PATCH /servicios/{id}/configuracion
POST /solicitudes
GET /solicitudes
GET /solicitudes/{id}
PATCH /solicitudes/{id}
GET /solicitudes/{id}/historial
POST /solicitudes/{id}/revision
POST /solicitudes/{id}/aceptacion
POST /solicitudes/{id}/rechazo
PUT /solicitudes/{id}/responsable
POST /solicitudes/{id}/inicio-atencion
POST /solicitudes/{id}/intervenciones
POST /solicitudes/{id}/requerimientos
POST /requerimientos/{id}/respuesta
POST /solicitudes/{id}/finalizacion
POST /solicitudes/{id}/cancelacion
POST /solicitudes/{id}/reaperturas
POST /reaperturas/{id}/decision
POST /solicitudes/{id}/duplicidad
GET /reportes/solicitudes
GET /notificaciones
PATCH /notificaciones/{id}/lectura

Comprobación técnica:
GET /api/v1/salud

Rutas propuestas, todavía no implementadas ni obligadas literalmente por la guía.
Puedes refinarlas justificadamente, conservando trazabilidad.

Define entrada, salida, permisos, validaciones y errores antes de cada unidad.
No expongas modelos ORM directamente ni permitas asignación arbitraria de campos.
Listados paginados y filtros validados.
Consulta por radicado dentro de permisos del usuario.

HTTP propuesto:
- 201 creación.
- 200 consulta y actualización con respuesta.
- 401 autenticación ausente o inválida.
- 403 operación prohibida.
- 404 inexistente o caso ajeno que no deba revelarse.
- 409 conflicto de estado, duplicación o concurrencia.
- 422 datos inválidos.

14. SEGURIDAD PROPUESTA

- JWT de acceso, duración inicial propuesta 30 minutos.
- Validar firma, algoritmo y expiración.
- sub identifica cuenta.
- Consultar cuenta activa y permisos vigentes en operaciones protegidas.
- No incluir secretos ni datos personales innecesarios en JWT.
- Contraseñas solo mediante hash.
- Primera coordinación creada con comando local, sin contraseña fija.
- Clave de firma en .env.
- Sin refresh tokens inicialmente.
- Frontend conserva token solo en memoria.
- Recargar exige nuevo acceso.
- Cierre de sesión elimina token del frontend, pero no revoca una copia previamente emitida; documentar limitación.
- Autorregistro nunca acepta roles privilegiados.
- Ocultar botones no sustituye autorización.
- Datos de demostración ficticios.

Variables previstas:
DATABASE_URL
SECRET_KEY
ACCESS_TOKEN_EXPIRE_MINUTES
APP_ENV

No publiques secretos ni los incluyas en capturas.

## Incremento 0 implementado
FastAPI sirve index.html con FileResponse y CSS/JS con StaticFiles. Se usan rutas relativas al archivo Python para evitar depender del directorio del proceso. El navegador usa fetch con ruta del mismo origen, tiempo límite de 8 segundos y mensaje de error. No se necesitan CORS ni dependencias nuevas.

Los modelos, estados, JWT, rutas de negocio y migraciones anteriores siguen siendo diseño pendiente. El catálogo limita la elección de servicio; aun así la evaluación puede rechazar una petición cuyo contenido no corresponda al servicio seleccionado. No se añade captura libre de servicios.

Concurrencia y consistencia de reapertura requieren resolver el diseño antes de migraciones.

Documentación oficial consultada el 16-11-2026: https://fastapi.tiangolo.com/tutorial/static-files/ y https://fastapi.tiangolo.com/advanced/custom-response/#fileresponse .

PowerPoint: se extrajo el texto de 12 diapositivas y las relaciones de diapositivas. No se encontraron partes notesSlides ni enlaces externos en esas relaciones. No se inspeccionó visualmente ni se auditó cada elemento del paquete. El PR #4 de la diapositiva 10 es un ejemplo, no evidencia del proyecto.
