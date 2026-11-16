# Requisitos y alcance

Estado: contexto aportado por la estudiante; aprobación definitiva del alcance pendiente. Ningún RF implementado todavía.

Fuentes: guía PF-01 versión 002 del 04-11-2026 (texto pegado), respuestas y propuestas del contexto de trabajo. El README original de la guía no fue adjuntado como archivo independiente.

4. CONDICIONES OBLIGATORIAS DE LA GUÍA

CA-01:
Una persona puede presentar una solicitud.
Debe persistirse y poder recuperarse.

CA-02:
Personal autorizado puede evaluar y gestionar una solicitud.
Una gestión válida queda registrada.

CA-03:
Se puede consultar el estado durante la atención.
Debe ser coherente con las acciones realizadas.

CA-04:
Se conserva la trazabilidad de las acciones.
Se consultan intervenciones asociadas al caso.

CA-05:
El solicitante consulta la respuesta y finalización.
Se visualiza el resultado de un caso finalizado.

CA-06:
Coordinación consulta información consolidada.
Debe integrar varias solicitudes.

Es obligatorio:
- Interfaz web.
- Backend con API REST.
- Base de datos relacional y persistencia.
- Comunicación real interfaz → API → base de datos.
- Validaciones en el servidor.
- Permisos y manejo de errores.
- Flujo completo, no solamente CRUD aislado.
- Autenticación y autorización con JWT, confirmadas adicionalmente por el profesor.

La guía no exige:
- Docker.
- CI.
- Pruebas automatizadas.
- Despliegue en la nube.

Existe un apunte de clase que menciona desplegar en “nerocu”, posiblemente Heroku, pero NO está confirmado. No contrates servicios ni prometas alojamiento gratuito.

Fuera del alcance obligatorio:
- Facturación y pagos.
- WhatsApp.
- Envíos reales de correo.
- Integraciones institucionales externas.

5. RESPUESTAS REALES DEL CLIENTE

Servicios:
- Expedición de certificados.
- Actualización de información.
- Solicitudes de documentos.
- Consultas sobre trámites.
- Peticiones generales.

Datos obligatorios de solicitud:
- Nombre.
- Documento de identificación.
- Correo electrónico.
- Tipo de servicio.
- Asunto.
- Descripción.

Al registrar:
- Generar número de radicado.
- El usuario NO carga archivos, imágenes ni documentos.

Roles:
- Solicitante.
- Personal de atención.
- Coordinación.
- Una persona puede tener varias funciones mediante permisos.

Cuentas:
- Solicitantes se registran solos.
- Un administrador crea cuentas del personal y determina permisos.

Visibilidad:
- Solicitante solo ve sus casos.
- Personal ve todas las solicitudes.
- Coordinación puede intervenir y consultar.

Atención:
- Personal revisa integridad y pertinencia del servicio.
- Si está completa y corresponde, se acepta.
- Coordinación asigna el responsable.
- Si falta información, se pide al solicitante y se continúa.
- Si el servicio no corresponde, se rechaza indicando motivo.

Finalización:
- El responsable registra respuesta y resultado.
- El solicitante puede pedir reapertura.

Modificación:
- Solicitante puede corregir o cancelar antes de que comience la atención.

Duplicados:
- Se identifican y cierran con justificación.
- Se conserva el historial.

Supervisión:
- Coordinación define prioridad y tiempos según trámite.
- Consulta por estado, responsable, servicio, prioridad y fechas.
- Identifica pendientes y tiempos de atención.

El cliente mencionó notificaciones sin definir el canal.

7. CATÁLOGO DE REQUISITOS FUNCIONALES

Mantén identificadores estables:

RF-01 Registrar solicitud, seis datos obligatorios y radicado.
RF-02 Evaluar, aceptar o rechazar con motivo.
RF-03 Consultar solicitudes y estado según visibilidad.
RF-04 Registrar y consultar historial de intervenciones.
RF-05 Registrar respuesta y resultado y finalizar.
RF-06 Consultar respuesta y finalización como solicitante.
RF-07 Consultas consolidadas y filtros de coordinación.
RF-08 Autenticación JWT.
RF-09 Autorización en el servidor.
RF-10 Autorregistro de solicitantes.
RF-11 Crear personal y asignar múltiples roles.
RF-12 Asignar responsable desde coordinación.
RF-13 Pedir y responder información adicional.
RF-14 Corregir solicitud antes de revisión.
RF-15 Cancelar solicitud antes de revisión.
RF-16 Solicitar y resolver reapertura.
RF-17 Cerrar duplicados con motivo e historial.
RF-18 Configurar prioridades y plazos por servicio.
RF-19 Notificaciones internas.

No añadas funciones nuevas sin explicar su necesidad y relación con requisitos.

Por cada RF, completa criterios verificables con identificadores:
AC-RF-XX-YY.

8. REQUISITOS NO FUNCIONALES

RNF-01 Validación efectiva en servidor, incluso sin interfaz.
RNF-02 Integridad de relaciones y persistencia.
RNF-03 Respuestas HTTP y errores coherentes.
RNF-04 No revelar secretos en respuestas ni registros.
RNF-05 Instalación y ejecución reproducibles.
RNF-06 Pruebas documentadas y reproducibles.

No inventes métricas de rendimiento o disponibilidad.

9. REGLAS DE NEGOCIO

RN-01 Intervenciones vinculadas al caso.
RN-02 Respuesta y resultado vinculados al caso.
RN-03 Estado coherente con acciones.
RN-04 Seis datos obligatorios.
RN-05 Radicado único e inmutable: restricción de diseño propuesta.
RN-06 Solicitante consulta únicamente sus casos.
RN-07 Usuario puede tener múltiples roles.
RN-08 Servicio no procedente se rechaza con motivo.
RN-09 Coordinación asigna responsables.
RN-10 Responsable registra respuesta y resultado al finalizar.
RN-11 Corrección y cancelación antes de revisión.
RN-12 Duplicados se cierran con justificación sin perder historial.
RN-13 Coordinación define prioridades y tiempos por trámite.

Aclara cómo se combina un catálogo de servicios con el rechazo por servicio no procedente; no inventes una función de captura libre sin justificarla.

Los criterios AC-RF-XX-YY se detallarán antes de implementar cada RF. El incremento 0 solo contribuye a RNF-03, RNF-05 y RNF-06; no satisface CA-01 a CA-06.

### RF-08 — autenticacion JWT y cambio seguro de contrasena
AC-RF-08-01: Credenciales válidas permiten acceso; JWT alterado o expirado falla; cambiar contraseña invalida el JWT previo.
Fuente: alcance autorizado por la estudiante; no aprobación del docente.

### RF-09 — aplicar permisos acumulables con propiedad y responsabilidad
AC-RF-09-01: Un caso ajeno se oculta con 404; múltiples roles acumulan permisos sin omitir la condición de responsable.
Fuente: alcance autorizado por la estudiante; no aprobación del docente.

### RF-10 — autorregistro de solicitantes sin inyeccion de privilegios
AC-RF-10-01: Correo normalizado único; autorregistro asigna exclusivamente solicitante y rechaza roles o hashes adicionales.
Fuente: alcance autorizado por la estudiante; no aprobación del docente.
