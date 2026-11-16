# Lista verificable de entrega

| Elemento | Estado observado |
|---|---|
| RF-01 a RF-19 en código | Implementados en ramas reales; pruebas API ejecutadas |
| Frontend y API conectados por fetch | Implementados; recorrido visual completo pendiente |
| SQLite, claves foráneas y migración Alembic | Verificados; alembic check sin diferencias |
| Flujo HTTP de registro a finalización | Ejecutado con cuentas ficticias y evidencia sin credenciales |
| Persistencia tras reinicio del servidor | Ejecutada; reinicio-http.json |
| Suite automatizada | 26 aprobadas en entorno habitual y limpio |
| JWT, autorización, concurrencia y atomicidad | Pruebas ejecutadas |
| Instalación desde requirements | Ejecutada en .venv-clean y BD separada |
| README, requisitos, entrevista y decisiones | Documentados; aprobación docente no inventada |
| ER, modelo relacional, diccionario y clases | Generados desde el modelo implementado |
| API, manual y trazabilidad | Documentados |
| Sustentación | PPTX editable de 10 diapositivas con notas; guion de 20 minutos |
| Historial Git | 19 ramas por RF y commits/merges locales; revisión registrada |
| GitHub y PR | Pendientes: no hay autenticación utilizable ni remoto comprobado |
| PF-12 navegador | Bloqueada por permiso denegado; no se declara aprobada |
| Responsive, teclado y texto malicioso en UI | Pendientes de inspección manual |
| Nombre académico completo y aprobación final | Pendientes de suministrar/confirmar |
| Aclaración “nerocu” y preguntas dentro de 20 min | Pendientes académicos; no se desplegó en nube |

El ZIP de código no incluye .env, BD, .venv, .git ni credenciales demo. El historial local se conserva en la carpeta de trabajo; una copia textual sirve como evidencia adicional, pero no sustituye GitHub. Crear cuentas iniciales mediante comando interactivo en BD nueva o generar datos demo localmente.

Antes de entregar al docente, ejecutar el manual por rol y completar PF-12, configurar GitHub con tu cuenta y acceso del evaluador, y acordar cómo acreditar el bloqueo de PR sin fabricar historial. No presentar estos puntos como ya resueltos.
