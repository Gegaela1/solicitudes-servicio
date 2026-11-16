import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from pathlib import Path

BASE = "http://127.0.0.1:8001/api/v1"
access = json.loads(Path("work/demo-acceso.json").read_text(encoding="utf-8"))
evidence = []


def request(path, method="GET", data=None, token=None):
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = "Bearer " + token
    req = Request(
        BASE + path,
        data=json.dumps(data).encode() if data is not None else None,
        headers=headers,
        method=method,
    )
    try:
        with urlopen(req, timeout=20) as r:
            status = r.status
            body = json.load(r)
    except HTTPError as e:
        status = e.code
        body = json.load(e)
    if not path.startswith("/auth/"):
        evidence.append({"metodo": method, "ruta": path, "http": status, "respuesta": body})
    assert status < 400, (path, status, body)
    return body


tokens = {}
for a in access:
    tokens[a["rol"]] = request(
        "/auth/token", "POST", {"correo": a["correo"], "contrasena": a["contrasena"]}
    )["access_token"]
s = tokens["solicitante"]
co = tokens["coordinacion"]
st = tokens["atencion"]
services = request("/servicios", token=s)
users = request("/usuarios?size=100", token=co)["items"]
staff = next(u for u in users if u["correo"] == "demo.atencion@example.com")
c = request(
    "/solicitudes",
    "POST",
    {
        "nombre": "Demo Solicitante",
        "documento": "DEMO-001",
        "correo": "demo.solicitante@example.com",
        "servicio_id": services[0]["id"],
        "asunto": "Solicitud para demostración integral",
        "descripcion": "Necesito orientación administrativa sobre el procedimiento de expedición.",
    },
    s,
)
case_id = c["id"]
for action, tok, extra, method in [
    ("revision", st, {}, "POST"),
    ("aceptacion", st, {}, "POST"),
    (
        "responsable",
        co,
        {"responsable_id": staff["id"], "motivo": "Asignación de demostración integral"},
        "PUT",
    ),
    ("inicio-atencion", st, {}, "POST"),
    (
        "finalizacion",
        st,
        {
            "respuesta": "Se proporcionó orientación sobre el procedimiento solicitado.",
            "resultado": "Orientación administrativa completada",
        },
        "POST",
    ),
]:
    c = request(f"/solicitudes/{case_id}/{action}", method, {"version": c["version"], **extra}, tok)
request(f"/solicitudes/{case_id}/resultado", token=s)
request(f"/solicitudes/{case_id}/historial", token=s)
request("/reportes/solicitudes", token=co)
Path("evidencias/flujo-http-real.json").write_text(
    json.dumps(
        {
            "nota": "Datos ficticios; sin tokens ni contraseñas; ejecución HTTP real, no navegador.",
            "pasos": evidence,
        },
        ensure_ascii=False,
        indent=2,
    ),
    encoding="utf-8",
)
Path("work/persistencia-id.txt").write_text(str(case_id), encoding="utf-8")
print("Flujo HTTP completo aprobado; evidencia guardada sin credenciales. Caso:", c["radicado"])
