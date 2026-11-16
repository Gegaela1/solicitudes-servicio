# Sustentación de 20 minutos

Distribución de la fuente: problema/alcance 3 min; diseño 3; implementación 4; demostración 5; pruebas 3; GitHub/cierre 2. La presentación tiene 10 diapositivas con notas editables. No mostrar código ni credenciales durante la exposición.

## Diapositiva 1

Gestión de solicitudes de servicio

Proyecto Final 01

Aplicaciones y Servicios Web

Trabajo individual

Notas: 1 min · Problema y alcance. Presentar el problema de información dispersa y la necesidad de recuperar cada caso. No afirmar aprobación final del docente. Fuente: guía PF-01 v002, 04-11-2026, texto suministrado.

## Diapositiva 2

Problema y alcance

Recepción, revisión, atención y respuesta

Solicitante, atención y coordinación

Sin adjuntos, pagos ni correo real

Notas: 2 min · Explicar que los cinco servicios son categorías administrativas, no expedición automática de certificados. La aplicación conserva trazabilidad y permite supervisar varios casos. Fuente: docs/requisitos.md y docs/entrevista.md.

## Diapositiva 3

Arquitectura de la aplicación

Interfaz web con HTML, CSS y JavaScript

API REST con FastAPI y permisos JWT

Persistencia relacional con SQLAlchemy y SQLite

Notas: 1,5 min · Describir navegador, API, reglas y base de datos. Una misma aplicación sirve frontend y API. Alembic conserva el esquema. No mostrar código. Fuente: docs/diseno.md.

## Diapositiva 4

Datos y ciclos de atención

Solicitud vinculada a propietario y servicio

Intervenciones, preguntas y decisiones conservadas

Cada reapertura crea un ciclo y preserva el anterior

Notas: 1,5 min · Explicar relaciones, claves foráneas y por qué ciclos_atencion evita perder respuestas anteriores o mezclar tiempos. Radicado inmutable generado con identidad de BD. Fuente: modelo implementado y docs/diseno.md.

## Diapositiva 5

Acceso y permisos

Autorregistro concede solo solicitante

Atención gestiona casos asignados

Coordinación administra y supervisa

Inicio y cierre requieren ser responsable

Notas: 2 min · JWT firmado de 30 minutos, Argon2, validación de permisos vigentes. Cambiar contraseña invalida tokens anteriores. El frontend conserva el token solo en memoria. Logout no revoca una copia emitida. Fuente: docs/api.md y pruebas RF-08/09/10/11.

## Diapositiva 6

Estados y trazabilidad

Registrar, revisar y aceptar

Asignar, iniciar atención y finalizar

Pedir información con retorno a la etapa anterior

Correcciones y reaperturas dejan evidencia

Notas: 2 min · Explicar acciones específicas, no edición libre del estado. Cada cambio conserva actor, fecha UTC e historial; una versión evita sobrescribir cambios ajenos. Las notas internas no salen en respuesta de solicitante. Fuente: docs/diseno.md y pruebas.

## Diapositiva 7

Demostración del caso

Solicitante registra y obtiene radicado

Atención revisa y coordinación asigna

Responsable registra respuesta y resultado

Solicitante consulta el cierre

Notas: 5 min · Guion de demostración en vivo. El flujo HTTP real fue ejecutado; el recorrido visual completo permanece pendiente por permiso de navegador denegado. No presentarlo como prueba visual aprobada. Preparar previamente servidor y cuentas demo sin proyectar contraseñas. Mostrar además un error 403 o 409 controlado. Fuente: evidencias/flujo-http-real.json.

## Diapositiva 8

Pruebas ejecutadas

26 pruebas aprobadas en el entorno habitual

26 aprobadas en instalación limpia

JWT, permisos, integridad y concurrencia

PF-12 visual pendiente

Notas: 2 min · Explicar ejemplos: JWT alterado 401, caso ajeno 404, transición o versión inválida 409, entrada inválida 422. El fallo controlado de notificación revierte estado e historial. Fuente: evidencias/validacion-integral.xml e instalacion-limpia.xml.

## Diapositiva 9

Instalación y verificación

Dependencias fijadas y migración aplicada

Base nueva de prueba sin borrar datos del usuario

Flujo HTTP real y persistencia comprobados

Revisión visual y acceso GitHub pendientes

Notas: 1 min · Explicar separación de configuración y secretos, comando interactivo de coordinación y datos demo generados localmente. Los archivos de credenciales no se publican. No hay despliegue cloud. Fuente: README.md, docs/pruebas.md.

## Diapositiva 10

Git y estado de entrega

19 ramas de requisitos con commits reales

Integraciones y autorrevisión locales

Publicación y PR requieren autenticación GitHub

README, manual y evidencias en el proyecto

Notas: 2 min · Mostrar git log y ramas reales. No afirmar PR remotos ni revisión de otras personas. GitHub no tiene credencial utilizable sin interacción y la existencia privada del repositorio no está confirmada. Cerrar indicando pendientes: PF-12 y aprobación académica final. Fuente: git local, evidencias/github-estado.json y docs/github.md.

## Guion detallado de demostración (5 minutos)

1. Preparar servidor en 8001 y cuentas demo; abrir credenciales localmente sin proyectarlas. Crear un caso nuevo como solicitante, mostrar radicado y persistencia al consultar.
2. Salir e ingresar como atención, iniciar revisión y aceptar. Cambiar a coordinación, asignar a atención con motivo.
3. Volver a atención, iniciar atención, mostrar historial y finalizar con respuesta y resultado.
4. Volver al solicitante, mostrar cierre y resultado. En coordinación mostrar consolidado con varias solicitudes.
5. Mostrar un error controlado: entrada inválida 422 o acción de versión anterior 409 mediante documentación API. No mostrar tokens en capturas. Explicar que ocultar botones no sustituye autorización.

Este es el recorrido previsto, no un resultado visual observado: PF-12 quedó bloqueada por permiso de navegador denegado. El flujo HTTP y persistencia sí se ejecutaron.

## Preguntas de preparación

¿Por qué SQLite? Base relacional local sencilla y suficiente para esta entrega; claves foráneas activadas. No se prometen capacidades no medidas.

¿Por qué ciclos_atencion? Preserva respuesta y tiempos de finalizaciones anteriores y separa el promedio por ciclo resuelto.

¿Cómo impides acceso a casos ajenos? Identidad del JWT y comprobación de propiedad/rol en servidor; 404 para no revelar existencia. Radicado no es credencial.

¿Qué pasa con dos operadores? Versión optimista, 409 si cambió el caso y transacción para no guardar historia parcial.

¿Qué pasa al cambiar roles/contraseña? Se consulta cuenta activa y permisos vigentes; auth_version invalida tokens anteriores.

¿Por qué no hay PR? No hubo credencial GitHub utilizable sin interacción. Las ramas, commits, autorrevisiones y merges son locales reales; no se presentan como PR remotos.

¿Qué falta para aceptar la entrega? Prueba visual completa, responsive/teclado/texto malicioso, acceso GitHub/PR y confirmación académica del alcance.

## Respaldo ante fallos

Sin Internet, la aplicación funciona localmente; /docs puede requerir recursos Swagger externos. Tener servidor, Python y BD preparados. Consultar evidencias/flujo-http-real.json y los XML de pruebas como evidencia previa, identificándola expresamente como ejecución anterior. No sustituir demo en vivo por una afirmación de que funcionó. No se grabaron videos ni se fabricaron capturas.

Conservar copia ZIP del código sin secretos, presentación editable y este guion. Ensayar tiempos y confirmar si las preguntas están dentro de los 20 minutos.
