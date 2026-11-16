# Trazabilidad

| CA | RF y criterio | Componente | Rama real | PR | Evidencia |
|---|---|---|---|---|---|
| CA-01 | RF-01, AC-RF-01-01 | app/services/operations_cases.py; frontend app.js | feature/RF-01-registrar-solicitud | Pendiente (sin autenticación) | evidencias/RF-01.xml; pruebas finales en validacion-integral.xml |
| CA-02 | RF-02, AC-RF-02-01 | app/services/operations_workflow.py; frontend app.js | feature/RF-02-evaluar-solicitud | Pendiente (sin autenticación) | evidencias/RF-02.xml; pruebas finales en validacion-integral.xml |
| CA-03 | RF-03, AC-RF-03-01 | app/services/operations_cases.py; frontend app.js | feature/RF-03-consultar-solicitudes | Pendiente (sin autenticación) | evidencias/RF-03.xml; pruebas finales en validacion-integral.xml |
| CA-04 | RF-04, AC-RF-04-01 | app/services/operations_history.py; frontend app.js | feature/RF-04-historial-atencion | Pendiente (sin autenticación) | evidencias/RF-04.xml; pruebas finales en validacion-integral.xml |
| CA-05 | RF-05, AC-RF-05-01 | app/services/operations_workflow.py; frontend app.js | feature/RF-05-finalizar-solicitud | Pendiente (sin autenticación) | evidencias/RF-05.xml; pruebas finales en validacion-integral.xml |
| CA-05 | RF-06, AC-RF-06-01 | app/services/operations_cases.py; frontend app.js | feature/RF-06-consultar-resultado | Pendiente (sin autenticación) | evidencias/RF-06.xml; pruebas finales en validacion-integral.xml |
| CA-06 | RF-07, AC-RF-07-01 | app/services/operations_reports.py; frontend app.js | feature/RF-07-consolidado | Pendiente (sin autenticación) | evidencias/RF-07.xml; pruebas finales en validacion-integral.xml |
| Transversal | RF-08, AC-RF-08-01 | app/services/operations_auth.py; frontend app.js | feature/RF-08-autenticacion-jwt | Pendiente (sin autenticación) | evidencias/RF-08.xml; pruebas finales en validacion-integral.xml |
| Transversal | RF-09, AC-RF-09-01 | app/services/permissions.py; frontend app.js | feature/RF-09-autorizacion | Pendiente (sin autenticación) | evidencias/RF-09.xml; pruebas finales en validacion-integral.xml |
| Transversal | RF-10, AC-RF-10-01 | app/services/operations_auth.py; frontend app.js | feature/RF-10-autorregistro | Pendiente (sin autenticación) | evidencias/RF-10.xml; pruebas finales en validacion-integral.xml |
| Transversal | RF-11, AC-RF-11-01 | app/services/operations_users.py; frontend app.js | feature/RF-11-administrar-usuarios | Pendiente (sin autenticación) | evidencias/RF-11.xml; pruebas finales en validacion-integral.xml |
| Transversal | RF-12, AC-RF-12-01 | app/services/operations_workflow.py; frontend app.js | feature/RF-12-asignar-responsable | Pendiente (sin autenticación) | evidencias/RF-12.xml; pruebas finales en validacion-integral.xml |
| Transversal | RF-13, AC-RF-13-01 | app/services/operations_questions.py; frontend app.js | feature/RF-13-informacion-adicional | Pendiente (sin autenticación) | evidencias/RF-13.xml; pruebas finales en validacion-integral.xml |
| Transversal | RF-14, AC-RF-14-01 | app/services/operations_cases.py; frontend app.js | feature/RF-14-corregir-solicitud | Pendiente (sin autenticación) | evidencias/RF-14.xml; pruebas finales en validacion-integral.xml |
| Transversal | RF-15, AC-RF-15-01 | app/services/operations_workflow.py; frontend app.js | feature/RF-15-cancelar-solicitud | Pendiente (sin autenticación) | evidencias/RF-15.xml; pruebas finales en validacion-integral.xml |
| Transversal | RF-16, AC-RF-16-01 | app/services/operations_reopen.py; frontend app.js | feature/RF-16-reapertura | Pendiente (sin autenticación) | evidencias/RF-16.xml; pruebas finales en validacion-integral.xml |
| Transversal | RF-17, AC-RF-17-01 | app/services/operations_workflow.py; frontend app.js | feature/RF-17-duplicados | Pendiente (sin autenticación) | evidencias/RF-17.xml; pruebas finales en validacion-integral.xml |
| Transversal | RF-18, AC-RF-18-01 | app/services/operations_cases.py; frontend app.js | feature/RF-18-prioridades-plazos | Pendiente (sin autenticación) | evidencias/RF-18.xml; pruebas finales en validacion-integral.xml |
| Transversal | RF-19, AC-RF-19-01 | app/services/operations_notifications.py; frontend app.js | feature/RF-19-notificaciones | Pendiente (sin autenticación) | evidencias/RF-19.xml; pruebas finales en validacion-integral.xml |

Las evidencias por RF fueron ejecutadas antes de la separación final de capas y se conservan como historia. validacion-integral.xml y instalacion-limpia.xml comprueban el código final. PF-12 y revisión visual completa están bloqueadas por navegador; no se declaran aprobadas por tener pruebas HTTP.
