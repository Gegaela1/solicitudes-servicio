# Diseño

## Base transversal antes de migración

Navegador (HTML/CSS/JS) → rutas API → esquemas Pydantic → servicios de negocio → SQLAlchemy → SQLite. Un origen, sin CORS abierto. UTC sin zona almacenado en SQLite; serialización ISO con Z y presentación America/Bogota.

Se incorpora ciclos_atencion: cada reapertura conserva el ciclo finalizado con respuesta, resultado e inicio/fin; el nuevo ciclo permite calcular plazos y promedio solo de ciclos realmente resueltos. No sustituye el historial inmutable. Los servicios copian prioridad y plazo al registrar; su configuración posterior no cambia casos antiguos.

Restricciones: correo/radicado únicos; claves foráneas activadas; asociaciones usuario-rol con PK compuesta; índices por propietario, estado, servicio, responsable y prioridad. Índices parciales únicos impiden dos requerimientos abiertos y dos reaperturas pendientes. Control optimista con version_id_col en solicitudes. No hay cascadas de eliminación.

El esquema compartido prepara relaciones; los RF se implementan en ramas propias. La migración inicial se generará desde este esquema y se conservará como definición explícita independiente de cambios futuros del ORM.
