# Avances

## Plan por dependencias
Base transversal → RF-08 → RF-09 → RF-10 → RF-11 → RF-01 → RF-03 → RF-04 → RF-02 → RF-12 → RF-05 → RF-06 → RF-13 → RF-14 → RF-15 → RF-16 → RF-17 → RF-18 → RF-07 → RF-19 → entrega.

Se conserva el incremento 0 como primer commit real. La nueva solicitud autoriza el alcance completo; sustituye el límite anterior de detenerse tras incremento 0. docs/alcance_autorizado.txt conserva las decisiones exactas de la estudiante. No consta aprobación definitiva del profesor, fecha/medio de entrevista ni confirmación de despliegue “nerocu”.

GitHub: gh no instalado. No se ha comprobado existencia privada ni autenticación; el acceso público consultado no devolvió una página verificable. No se inventa remoto. Continuar localmente.

Base: migración aplicada, importación de dependencias y Argon2 verificados; pytest: 1 aprobada. Autorrevisión: sin secretos preparados, relaciones sin borrado en cascada y configuración falla sin clave. Integración local; PR remoto pendiente por acceso GitHub.

RF-08 — autenticacion JWT y cambio seguro de contrasena. Suite ejecutada con resultado aprobado (evidencias/RF-08.xml). Autorrevisión: diff revisado, entradas explícitas, permisos de servidor, sin .env ni BD preparados. Integración local; no se simula PR remoto.

RF-09 — aplicar permisos acumulables con propiedad y responsabilidad. Suite ejecutada con resultado aprobado (evidencias/RF-09.xml). Autorrevisión: diff revisado, entradas explícitas, permisos de servidor, sin .env ni BD preparados. Integración local; no se simula PR remoto.

RF-10 — autorregistro de solicitantes sin inyeccion de privilegios. Suite ejecutada con resultado aprobado (evidencias/RF-10.xml). Autorrevisión: diff revisado, entradas explícitas, permisos de servidor, sin .env ni BD preparados. Integración local; no se simula PR remoto.

RF-11 — administrar cuentas roles y proteccion de ultima coordinacion. Suite ejecutada con resultado aprobado (evidencias/RF-11.xml). Autorrevisión: diff revisado, entradas explícitas, permisos de servidor, sin .env ni BD preparados. Integración local; no se simula PR remoto.

RF-01 — registrar solicitudes persistentes con radicado transaccional. Suite ejecutada con resultado aprobado (evidencias/RF-01.xml). Autorrevisión: diff revisado, entradas explícitas, permisos de servidor, sin .env ni BD preparados. Integración local; no se simula PR remoto.

RF-03 — consultar casos con filtros paginacion y propiedad. Suite ejecutada con resultado aprobado (evidencias/RF-03.xml). Autorrevisión: diff revisado, entradas explícitas, permisos de servidor, sin .env ni BD preparados. Integración local; no se simula PR remoto.

RF-04 — conservar historial con notas privadas y rectificaciones nuevas. Suite ejecutada con resultado aprobado (evidencias/RF-04.xml). Autorrevisión: diff revisado, entradas explícitas, permisos de servidor, sin .env ni BD preparados. Integración local; no se simula PR remoto.

RF-02 — revisar aceptar o rechazar mediante transiciones autorizadas. Suite ejecutada con resultado aprobado (evidencias/RF-02.xml). Autorrevisión: diff revisado, entradas explícitas, permisos de servidor, sin .env ni BD preparados. Integración local; no se simula PR remoto.

RF-12 — asignar y reasignar responsables elegibles con auditoria. Suite ejecutada con resultado aprobado (evidencias/RF-12.xml). Autorrevisión: diff revisado, entradas explícitas, permisos de servidor, sin .env ni BD preparados. Integración local; no se simula PR remoto.

RF-05 — iniciar atencion y finalizar con respuesta resultado y ciclo. Suite ejecutada con resultado aprobado (evidencias/RF-05.xml). Autorrevisión: diff revisado, entradas explícitas, permisos de servidor, sin .env ni BD preparados. Integración local; no se simula PR remoto.

RF-06 — mostrar respuesta y resultado al propietario autorizado. Suite ejecutada con resultado aprobado (evidencias/RF-06.xml). Autorrevisión: diff revisado, entradas explícitas, permisos de servidor, sin .env ni BD preparados. Integración local; no se simula PR remoto.

RF-13 — intercambiar informacion adicional y recuperar etapa anterior. Suite ejecutada con resultado aprobado (evidencias/RF-13.xml). Autorrevisión: diff revisado, entradas explícitas, permisos de servidor, sin .env ni BD preparados. Integración local; no se simula PR remoto.

RF-14 — corregir datos con limites de etapa y auditoria administrativa. Suite ejecutada con resultado aprobado (evidencias/RF-14.xml). Autorrevisión: diff revisado, entradas explícitas, permisos de servidor, sin .env ni BD preparados. Integración local; no se simula PR remoto.

RF-15 — cancelar casos propios solo antes de iniciar revision. Suite ejecutada con resultado aprobado (evidencias/RF-15.xml). Autorrevisión: diff revisado, entradas explícitas, permisos de servidor, sin .env ni BD preparados. Integración local; no se simula PR remoto.

RF-16 — resolver reaperturas conservando radicado historial y ciclos previos. Suite ejecutada con resultado aprobado (evidencias/RF-16.xml). Autorrevisión: diff revisado, entradas explícitas, permisos de servidor, sin .env ni BD preparados. Integración local; no se simula PR remoto.

RF-17 — cerrar duplicados manualmente sin perder historial ni exponer otros propietarios. Suite ejecutada con resultado aprobado (evidencias/RF-17.xml). Autorrevisión: diff revisado, entradas explícitas, permisos de servidor, sin .env ni BD preparados. Integración local; no se simula PR remoto.

RF-18 — configurar plazos por servicio sin alterar casos existentes. Suite ejecutada con resultado aprobado (evidencias/RF-18.xml). Autorrevisión: diff revisado, entradas explícitas, permisos de servidor, sin .env ni BD preparados. Integración local; no se simula PR remoto.

RF-07 — consultar consolidado con filtros coherentes y metricas por ciclo. Suite ejecutada con resultado aprobado (evidencias/RF-07.xml). Autorrevisión: diff revisado, entradas explícitas, permisos de servidor, sin .env ni BD preparados. Integración local; no se simula PR remoto.

RF-19 — notificar acciones dentro de la transaccion y marcar avisos propios. Suite ejecutada con resultado aprobado (evidencias/RF-19.xml). Autorrevisión: diff revisado, entradas explícitas, permisos de servidor, sin .env ni BD preparados. Integración local; no se simula PR remoto.

## Estado final de preparación

RF-01 a RF-19 implementados en 19 ramas reales. Refactor de entrega: rutas como adaptadores HTTP y reglas en servicios; suite repetida tras refactor. 26 pruebas aprobadas, tanto en entorno habitual como en instalación separada. Instalación limpia con versiones fijadas, nueva BD y alembic check correcto. Flujo HTTP completo y consulta del caso tras detener/reiniciar servidor aprobados. Presentación editable preparada con notas y revisión visual de sus diez diapositivas; no se afirma inspección en PowerPoint.

Autorrevisión de entrega: configuración sin secreto funcional predeterminado; JSON de errores no devuelve input; modelos no salen directamente por API; notas internas filtradas en servidor; IDs inmutables fuera de entradas; transacciones y versión conservadas; archivos locales sensibles excluidos. Revisión del frontend por lectura y comprobación de sintaxis, no ejecución visual completa.

Pendientes: PF-12 y pruebas visuales de responsive/teclado/texto malicioso (el navegador no recibió permiso para abrir el origen local 8001); GitHub/PR por falta de credencial utilizable sin interacción. No se eludió la denegación del navegador. No se creó remoto, PR, revisión externa ni despliegue ficticio.
