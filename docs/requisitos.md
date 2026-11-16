# Requisitos y alcance

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

### RF-01 — Registrar solicitud y radicado
AC-RF-01-01: Seis datos válidos generan un radicado único de BD; datos inválidos o propietario inyectado no persisten.

### RF-02 — Revisar, aceptar o rechazar
AC-RF-02-01: Solo atención o coordinación revisan y evalúan; rechazo exige motivo; estado o versión incorrecta produce 409.

### RF-03 — Consultar solicitudes y estado
AC-RF-03-01: Listados y detalle respetan propiedad; casos ajenos o inexistentes devuelven 404 y filtros inválidos 422.

### RF-04 — Historial e intervenciones
AC-RF-04-01: Cada nota conserva autor y caso; el solicitante no recibe notas ni auditoría interna; una rectificación agrega registro sin sobrescribir.

### RF-05 — Finalización con respuesta y resultado
AC-RF-05-01: Solo responsable inicia y finaliza; respuesta y resultado válidos se guardan junto al historial en la misma transacción.

### RF-06 — Consultar resultado propio
AC-RF-06-01: Un solicitante recupera la respuesta y finalización de su caso; un usuario ajeno recibe 404.

### RF-07 — Consolidado y filtros
AC-RF-07-01: Coordinación combina filtros con fechas Colombia inclusivas; conteos listado y métricas coinciden; solo ciclos finalizados integran el promedio.

### RF-08 — JWT y cambio de contraseña
AC-RF-08-01: Credenciales válidas permiten acceso; JWT alterado o expirado falla; cambiar contraseña invalida el JWT previo.

### RF-09 — Autorización
AC-RF-09-01: Un caso ajeno se oculta con 404; múltiples roles acumulan permisos sin omitir la condición de responsable.

### RF-10 — Autorregistro
AC-RF-10-01: Correo normalizado único; autorregistro asigna exclusivamente solicitante y rechaza roles o hashes adicionales.

### RF-11 — Administración de cuentas y roles
AC-RF-11-01: Solo coordinación crea personal; se conservan coordinadores activos y responsables elegibles de casos activos.

### RF-12 — Asignación y reasignación
AC-RF-12-01: Solo coordinación asigna personal activo; reasignación conserva estado y registra antes/después; no se deshabilita personal con casos activos.

### RF-13 — Información adicional por texto
AC-RF-13-01: Un único requerimiento abierto suspende revisión o atención; solo propietario responde una vez y recupera la etapa anterior.

### RF-14 — Corrección de solicitud
AC-RF-14-01: Propietario corrige solo registrada; coordinación corrige casos activos con motivo y auditoría; campos inmutables no se aceptan.

### RF-15 — Cancelación antes de revisión
AC-RF-15-01: Solo el propietario cancela en registrada; la cancelación se conserva en historial y se bloquea tras iniciar revisión.

### RF-16 — Reapertura
AC-RF-16-01: Una petición pendiente no cambia estado; aprobar conserva finalización previa y crea ciclo nuevo sin responsable ni respuesta vigente.

### RF-17 — Duplicados
AC-RF-17-01: Solo casos activos se vinculan a un original distinto del mismo propietario; se impiden ciclos y se cierran requerimientos pendientes.

### RF-18 — Prioridades y plazos
AC-RF-18-01: Solo coordinación configura prioridad y plazo opcional 1–8760; los casos copian valores y calculan vencimiento por ciclo sin pausar esperas.

### RF-19 — Notificaciones internas
AC-RF-19-01: Acciones generan avisos internos atómicos; cada cuenta lista y marca únicamente sus notificaciones sin revelar contenido privado.

## Requisitos no funcionales
RNF-01: validación real en servidor. RNF-02: relaciones y persistencia. RNF-03: HTTP coherente y errores controlados. RNF-04: secretos fuera de respuestas, registros y Git. RNF-05: instalación reproducible. RNF-06: pruebas documentadas. No se prometen métricas de rendimiento/disponibilidad.

## Reglas y restricciones
RN-01: intervención ligada al caso. RN-02: resultado y respuesta ligados al caso. RN-03: transiciones cerradas. RN-04: seis datos obligatorios. RN-05: radicado único generado con identidad BD, inmutable. RN-06: propietario solo consulta sus casos salvo permisos de personal. RN-07: roles acumulables. RN-08: rechazo con motivo por contenido fuera de competencia aunque exista categoría. RN-09: coordinación asigna. RN-10: responsable finaliza. RN-11: corrección/cancelación del solicitante solo en registrada. RN-12: duplicados conservan historia y propietario. RN-13: prioridad y plazo por servicio.

No se aceptan propietario, fechas, hashes, autorías, radicado o estado desde entradas genéricas. Las acciones incluyen versión optimista. Los límites de longitud, plazos calendario y decisiones de reapertura son acuerdos de implementación de la estudiante. No son políticas reales del cliente. Detalle completo en alcance_autorizado.txt y esquemas Pydantic.

## Prioridad y aceptación
Todos los RF-01 a RF-19 pertenecen al alcance autorizado; se implementaron por dependencias. La implementación y pruebas de API no sustituyen aprobación docente ni demostración visual. PF-12 y prueba visual de texto malicioso están pendientes por permiso de navegador denegado.
