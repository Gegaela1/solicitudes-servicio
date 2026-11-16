# Pruebas y evidencias

Entorno observado: Windows, Python 3.14.2; dependencias exactas en requirements.txt. Código bajo Git; cada evidencia RF fue generada en su rama antes del commit respectivo. La versión exacta se recupera con `git log --all --oneline`; las pruebas finales corresponden a la rama de preparación de entrega, no a un despliegue remoto.

## Ejecución reproducible

```powershell
Set-Location 'C:\Users\Usuario\Documents\solicitudes-servicio'
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe -m alembic check
.\.venv\Scripts\python.exe -m ruff check app scripts tests
.\.venv\Scripts\python.exe -m pytest -q --junitxml=evidencias/validacion-integral.xml
```

Los tests crean una BD separada y temporal bajo work/tmp, no borran la BD de uso. La fixture reconstruye solo esa BD propia. Para HTTP real, preparar demo, iniciar Uvicorn en 8001 y ejecutar `python -m scripts.verificar_flujo_demo`: crea otro caso ficticio en la BD local. Requiere work/demo-acceso.json y no imprime credenciales.

## Matriz oficial

| ID | RF / criterio | Escenario y precondición | Entrada / pasos | Esperado | Observado | Estado | Evidencia |
|---|---|---|---|---|---|---|---|
| PF-01 | RF-01 / AC-RF-01-01 | Cuenta solicitante autenticada | POST seis datos válidos y recuperar en sesión nueva | 201, radicado persistido | Coincide | aprobada | test_persist_valid_and_invalid; flujo-http-real.json |
| PF-02 | RF-01 / AC-RF-01-01 | Cuenta válida | Descripción corta / propietario extra | 422, sin fila nueva | Coincide | aprobada | test_persist_valid_and_invalid |
| PF-03 | RF-03 / AC-RF-03-01 | Caso propio existente | GET detalle/listado/radicado | 200 con caso correcto | Coincide | aprobada | test_visibility_pagination_and_filters |
| PF-04 | RF-03 / AC-RF-03-01 | Sesión válida | GET ID inexistente | 404 controlado | Coincide | aprobada | test_visibility_pagination_and_filters |
| PF-05 | RF-02 / AC-RF-02-01 | Atención y caso registrado | POST revisión y evaluación | 200, historial y estado | Coincide | aprobada | test_review_states_and_stale_version |
| PF-06 | RF-09 / AC-RF-09-01 | Solicitante sin permisos | POST revisión / consulta ajena | 403 / 404 | Coincide | aprobada | test_review_states_and_stale_version; test_visibility_pagination_and_filters |
| PF-07 | RF-03 / AC-RF-03-01 | Caso en flujo | Consultar tras cada acción | Estado coherente | Coincide | aprobada | flujo-http-real.json |
| PF-08 | RF-04 / AC-RF-04-01 | Notas públicas/internas | GET historial por rol y rectificación | Sin filtración; original conservado | Coincide | aprobada | test_internal_history_and_rectification |
| PF-09 | RF-05/06 / AC-RF-05-01, AC-RF-06-01 | Caso asignado en atención | Finalizar y consultar como propietario | Respuesta/resultado recuperables | Coincide | aprobada | test_finish_requires_assigned_actor; test_owner_result_and_history |
| PF-10 | RF-07 / AC-RF-07-01 | Varias solicitudes | Filtros y reporte coordinación | Listado/métricas coherentes | Coincide | aprobada | test_report_filtered_counts_and_dates |
| PF-11 | RNF-02 / RF-01 | BD propia de prueba | Reiniciar conexión, FK inválida y escrituras concurrentes | Persistencia, FK y conflicto | Coincide | aprobada | test_integrity.py; evidencia reinicio HTTP |
| PF-12 | CA-01 a CA-06 | Navegador y tres roles | Flujo completo desde interfaz hasta BD | Caso finalizado recuperable por interfaz | No ejecutado: permiso navegador denegado | bloqueada | Pendiente de recorrido manual; API real sí verificada |

## Seguridad y reglas adicionales ejecutadas

| Prueba | RF / criterio | Entrada/pasos | Esperado y observado | Estado |
|---|---|---|---|---|
| test_jwt_and_password | RF-08 / AC-RF-08-01 | JWT ausente, alterado, expirado y contraseña nueva | 401 en inválidos; JWT anterior falla; sin secreto en 422 | aprobada |
| test_register_no_privileges | RF-10 / AC-RF-10-01 | Correo con espacios/mayúsculas, correo repetido, roles inyectados | Normalización; 409 duplicado; 422 roles | aprobada |
| test_permissions | RF-09 / AC-RF-09-01 | Roles acumulados y condición responsable | Permisos acumulables sin saltar responsabilidad | aprobada |
| test_staff_and_last_coordinator | RF-11 / AC-RF-11-01 | Quitar última coordinación / crear cuenta multirol | 409 última; 201 multirol; 403 solicitante | aprobada |
| test_assign_and_active_responsible | RF-12 / AC-RF-12-01 | Asignar inválido, deshabilitar responsable, reasignar | 422 inválido; 409 deshabilitar; estado conservado | aprobada |
| test_information_roundtrip | RF-13 / AC-RF-13-01 | Pregunta, duplicado y respuesta repetida | 201, 409 duplicado, retorno coherente y 409 repetición | aprobada |
| test_correction_limits | RF-14 / AC-RF-14-01 | Corrección propia y administrativa tras revisión | Bloqueo propietario; motivo obligatorio coordinación | aprobada |
| test_cancel_before_review_only | RF-15 / AC-RF-15-01 | Cancelar antes/después de revisión | Primera válida; fuera de etapa 409 | aprobada |
| test_reopen_preserves_finalized_cycle | RF-16 / AC-RF-16-01 | Solicitar, repetir, aprobar | 409 petición repetida; nuevo ciclo y versión anterior conservada | aprobada |
| test_rejected_reopening_keeps_result | RF-16 / AC-RF-16-01 | Rechazar reapertura | Sigue finalizada y resultado recuperable | aprobada |
| test_duplicates_preserve_history_and_close_question | RF-17 / AC-RF-17-01 | Cerrar con pregunta abierta, autorreferencia/ciclo | Se conserva historia, se cierra pregunta, enlaces inválidos bloqueados | aprobada |
| test_other_owner_duplicate_not_allowed | RF-17 / AC-RF-17-01 | Original de otro propietario | 422 | aprobada |
| test_service_snapshots_deadline | RF-18 / AC-RF-18-01 | Plazo inválido, cambio de configuración y tiempo avanzado | 422 inválido; copia previa intacta; vencida coherente | aprobada |
| test_report_filtered_counts_and_dates | RF-07 / AC-RF-07-01 | Límites UTC del día Colombia y filtro estado | Conteos coinciden; promedio solo ciclos resueltos | aprobada |
| test_notifications_are_personal | RF-19 / AC-RF-19-01 | Aviso propio y de otro usuario | Lectura propia válida, ajena 404 | aprobada |
| test_real_optimistic_concurrency | RNF-02 / RF-09 | Dos sesiones cambian la misma versión | Segunda falla sin sobrescribir primera | aprobada |
| test_atomic_action_rolls_back_history_and_notice | RNF-02 / RF-19 | Falla controlada antes de crear aviso | Reversión de estado e historial | aprobada |

Detalle completo y resultados: validacion-integral.xml. 26 pruebas aprobadas en entorno habitual y 26 en instalación limpia. Hay un aviso de deprecación de Starlette sobre httpx en TestClient; no hizo fallar la suite. No se sustituyó la biblioteca por una no solicitada para ocultar el aviso.

## Instalación limpia y límites
Se creó .venv-clean, se instalaron requirements exactos, pip check sin incompatibilidades, migración y catálogo en work/instalacion-limpia.db y alembic check sin diferencias. Al primer intento ensurepip falló por temporal del entorno; con TEMP/TMP dentro de work/tmp funcionó. Evidencia: instalacion-limpia.xml y registro de comprobación.

Pendientes: PF-12 desde navegador, responsive/teclado, texto malicioso renderizado literalmente, inspección visual de /docs y validación del evaluador. No se inventaron capturas ni resultados de estas pruebas. Las verificaciones del incremento 0 correspondían a su interfaz anterior; no acreditan la interfaz completa.
