# Manual de uso

## Preparación y acceso
1. Ejecuta scripts/instalar.ps1 desde PowerShell en la carpeta del proyecto.
2. En una BD nueva crea la primera coordinación con `.\.venv\Scripts\python.exe -m scripts.crear_coordinador`. El comando solicita contraseña sin eco y no acepta una contraseña por argumentos. Si ya existe coordinación activa, administra desde esa cuenta.
3. Para una demostración local, ejecuta `.\.venv\Scripts\python.exe -m scripts.datos_demo`. Las credenciales aleatorias quedan en work/demo-acceso.json (excluido de Git). Ábrelo tú en VS Code; no lo proyectes ni lo publiques. No se reemplazan contraseñas existentes.
4. Inicia el servidor y abre la página. Usa Acceso; al recargar debes iniciar sesión porque el token solo vive en memoria. Salir elimina esa copia. Cambiar contraseña exige la actual y obliga a ingresar de nuevo.

## Solicitante
Crear cuenta concede exclusivamente solicitante. En Nueva solicitud el formulario precarga nombre, documento y correo; corregirlos allí cambia lo presentado, no la cuenta. Elige servicio del catálogo, asunto y descripción; no se adjuntan documentos. El sistema devuelve radicado.

En Solicitudes filtra por estado, radicado y otros campos; abre detalle para estado, vencimiento, duraciones e historial público. En registrada puedes corregir o cancelar con motivo y confirmación. Al iniciar revisión esas acciones se bloquean.

Si hay requerimiento pendiente, lee la pregunta y responde por texto; el caso vuelve a revisión o atención. Finalizado, el detalle muestra respuesta, resultado y fecha. Puedes solicitar reapertura con motivo; la petición espera decisión de coordinación y no cambia estado por sí sola.

## Atención
Consulta la bandeja global. Inicia revisión de un caso registrado y evalúa: aceptar, rechazar con motivo o pedir información. Espera la asignación de coordinación. Si eres responsable, inicia atención, registra intervenciones públicas/internas, pide información y finaliza con respuesta y resultado. No puedes asignarte mediante la interfaz de atención ni finalizar el caso de otra persona.

## Coordinación
Personal permite crear cuentas, asignar roles separados por coma y activar/desactivar. No se permite perder la última coordinación activa ni deshabilitar responsables con casos activos: reasigna primero.

En detalle asigna responsable de un caso aceptado; después puedes reasignar manteniendo estado y dejando motivo. Coordinación puede ser responsable por ese rol. Para iniciar/finalizar debe estar asignada. Corrige administrativamente un caso activo con motivo; notas y auditoría detallada son internas.

Reaperturas: lee motivo, aprueba/rechaza con justificación. Aprobar conserva historial y radicado, inicia nuevo ciclo, quita responsable y limpia resultado vigente. La finalización anterior sigue en historial.

Duplicados: indica ID del original y motivo; solo mismo propietario, original distinto y no duplicado. Confirma el cierre. Se conserva historial y se cierra un requerimiento abierto si lo hubiera.

Servicios permite prioridad y plazo opcional en horas calendario. Vacío significa sin definir. Los cambios afectan solicitudes nuevas. No representan tiempos institucionales confirmados.

Consolidado combina filtros y muestra conteos, pendientes, vencidas y promedio por ciclo finalizado. El filtro hasta incluye el día completo en Colombia. Sin ciclos finalizados, el promedio dice Sin datos. Sin coincidencias, tabla vacía y contadores en cero.

## Notificaciones y errores
Notificaciones muestra solo avisos de tu cuenta y permite marcarlos leídos. No envía correo.

422: corrige campos señalados. 401: vuelve a ingresar. 403: no tienes permiso o responsabilidad. 404: no existe o no es visible. 409: recarga el detalle y comprueba estado/versión; evita repetir ciegamente una acción. Si falla conexión, verifica que Uvicorn siga ejecutándose.

## Comprobación visual pendiente
El navegador del agente no recibió permiso para abrir la aplicación completa. Antes de exponer: recorrer los tres roles, verificar móvil/escritorio, teclado y foco, datos vacíos, formulario inválido y texto como `<img src=x onerror=alert(1)>` mostrado literalmente sin ejecutar. No marcar estas pruebas como aprobadas antes de realizarlas.
