---
name: readme-commit
description: Use when the user is about to commit and wants the README verified/optimized first — audits or creates from scratch a star-optimized, well-structured GitHub README, then makes the commit. Triggers on "commit con readme", "optimiza el readme y commitea", "ship readme".
argument-hint: "[commit message opcional]"
category: engineering
---

# readme-commit

Verifica/optimiza el `README.md` para GitHub (estructura + estrellas) y luego hace el commit. Sigue `RULES.md`.

## Workflow

1. **Existencia**: si no hay `README.md` en la raíz del repo → crearlo desde cero con la estructura de abajo. Si existe → auditarlo y mejorarlo, no reescribir a ciegas lo que ya está bueno.

2. **Optimizar para estrellas** (estructura mínima de un README que convierte):
   - **Headline + one-liner** claros (qué es, para quién, por qué importa) en las primeras 3 líneas.
   - **Badges** (license, stack, status) — solo reales.
   - **Value prop / features** en bullets escaneables.
   - **Quick start** copy-pasteable (instalación + primer uso en <5 comandos).
   - **Estructura / cómo navegar** (árbol breve + punteros).
   - **Screenshots/demo** si aplica (placeholder si no hay).
   - **Contributing + License** al final.
   - Tono directo, sin marketing vacío ni muros de texto.

3. **Coherencia con el repo (RULES.md)**:
   - **Nunca hardcodear counts** (skills, comandos, tools) → enlazar a los índices vivos (`06_Metadata/Skills/_INDEX.md`, `Tools/_INDEX.md`) en vez de listar números que se pudren.
   - Verificar que los links internos resuelven (no apuntar a archivos borrados).
   - No inventar features: reflejar lo que el repo realmente hace.

4. **Commit**:
   - Si el daemon auto-commit corre y esto es un cambio simple, dejar que el flujo normal aplique; para un commit explícito: `git add README.md` (+ lo que el usuario indique) y commit Conventional Commit:
     `docs(readme): <resumen>` con el trailer `Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>`.
   - Usar el mensaje que pase el usuario en `$ARGUMENTS` si lo da; si no, generar uno descriptivo.
   - Mostrar el diff resumido antes de commitear si el cambio es grande.

## Notas

- Para repos bajo Google Drive, seguir las reglas de daemon/`git rm` de `RULES.md`.
- No forzar estrellas con clickbait; un README honesto y bien estructurado es lo que retiene.
