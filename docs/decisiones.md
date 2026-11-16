# Decisiones de implementación

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
