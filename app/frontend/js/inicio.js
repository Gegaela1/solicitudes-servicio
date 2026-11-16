const estado = document.querySelector("#estado");
const boton = document.querySelector("#comprobar");

async function comprobarConexion() {
  boton.disabled = true;
  estado.textContent = "Comprobando conexión…";
  delete estado.dataset.resultado;
  try {
    const respuesta = await fetch("/api/v1/salud", {
      cache: "no-store",
      signal: AbortSignal.timeout(8000),
    });
    if (!respuesta.ok) throw new Error("Respuesta HTTP inesperada");
    const datos = await respuesta.json();
    if (datos.estado !== "disponible") throw new Error("Respuesta inválida");
    estado.textContent = "Conexión correcta. El sistema está disponible.";
    estado.dataset.resultado = "exito";
  } catch {
    estado.textContent = "No se pudo conectar con el sistema. Intenta nuevamente.";
    estado.dataset.resultado = "error";
  } finally {
    boton.disabled = false;
  }
}

boton.addEventListener("click", comprobarConexion);
comprobarConexion();
