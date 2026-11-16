# Publicación pendiente en GitHub

No se encontró gh instalado ni una credencial de GitHub utilizable sin interacción. No se ha comprobado si solicitudes-servicio existe de forma privada. No se creó remoto ni se publicó. La evidencia es evidencias/github-estado.json.

## Después de autenticarte tú

Instala GitHub CLI desde su fuente oficial, abre PowerShell en el proyecto y ejecuta:

```powershell
gh auth login
gh api user --jq .login
gh repo view Gegaela1/solicitudes-servicio --json nameWithOwner,isPrivate,url
git remote -v
```

Comprueba que la cuenta sea Gegaela1. Si `repo view` falla, distingue falta de acceso de repositorio inexistente antes de crear. Si se confirma inexistente:

```powershell
gh repo create Gegaela1/solicitudes-servicio --private
```

Si ya existe, conserva su visibilidad y revisa su contenido e historial antes de conectar. No sobrescribas un remoto ni hagas force push.

## Publicar el historial local existente

Si confirmaste que el remoto está vacío, agrega origin solo si aún no existe. La URL siguiente es el destino previsto, NO una URL de repositorio verificado:

```powershell
git remote add origin https://github.com/Gegaela1/solicitudes-servicio.git
git push -u origin main
git push origin --all
```

Esto publica ramas y merges locales reales, pero NO crea PR retroactivos: sus cambios ya están en main. No abras PR vacíos ni afirmes haberlos usado. Documenta esta limitación académica y solicita al docente aceptar la evidencia local por el bloqueo de autenticación. Para cambios futuros:

```powershell
git switch main
git switch -c feature/cambio-concreto
# Implementar, probar, revisar diff y confirmar cambios reales.
git push -u origin feature/cambio-concreto
gh pr create --base main --head feature/cambio-concreto --title 'Título concreto' --body-file docs/pr_actual.md
# Revisar diff y resultados reales; registrar autorrevisión antes de integrar.
gh pr merge --merge
```

El archivo de descripción debe redactarse según el cambio real; no se incluye uno ficticio. El evaluador necesita acceso al repositorio privado. No se debe atribuir una revisión a otra persona.
