---
name: plantilla-notion-desde-workspace-real
description: >-
  Use this when turning a real Notion workspace or OS into a sellable template
  (Premium and Free) without copying private data: real workspace first (closed
  against the reference OS and the evergreen list), then light example
  databases, duplicate via a second account, bring back to the templates
  database as one card per product.
---
# Plantilla Notion desde un workspace real (v2 · 2026-10-30)

Reglas: archivar (mover a una página Archived), nunca borrar · respaldo antes de cada cambio estructural, registrar cada cambio y verificar con fetch · texto de la plantilla en inglés (el workspace real puede ir en español) · nada se publica ni se comparte fuera sin el sí explícito del dueño · no tocar filas de bases originales salvo lo aprobado · si un código lee una base, revisar el repo antes y solo sumar.

## 0. Primero el workspace real (siempre)
Nunca empezar por el staging de la plantilla. El orden es: workspace real del dueño → cerrado y aprobado → plantilla. Si aparece un hueco en el real, la plantilla se pausa hasta cerrarlo.
1. Partir del sistema real que ya existe (su fila en la base de Workspaces); crear uno nuevo solo si no hay base o la actual no sirve.
2. Auditar, proponer por escrito y esperar el OK del dueño antes de escribir. En el workspace real el dueño es dueño y el bot opera.
3. **Comparar contra el OS de referencia ya cerrado** (hoy Agentic OS), página por página, con una tabla de brechas P1 (visible y rápido) / P2 (estructura) / P3 (opcional), vía (conector o navegador) y riesgo. Lo que el OS nuevo hace mejor se anota como mejora, no se quita.
4. Aplicar el estándar sobre los datos reales, sin borrar ni mover bases originales que lea un código.
5. Antes de cerrar: revisar contra la lista evergreen, el patrón de layout, el registro en el hub Databases y la verificación de propiedades (abajo).
6. Recién con el real cerrado y aprobado sale la Premium y la Free (pasos 1 en adelante). Un staging hecho antes queda solo como borrador.

### 0.1 Patrón de layout (verificado en Agentic OS)
- **Home:** onboarding sincronizado (toggle) → divisor de imagen sincronizado → nav numerado en **3 columnas 33.33** dentro del bloque sincronizado del menú → recursos → secciones 50/50 alternadas (h1 gray_bg + texto + cita + ilustración unDraw) → footer del creador solo en el home. **No** hay bloque 16.67/66.67/16.67 arriba y el home **no** lleva Full Width.
- **Páginas como filas de una base índice** (galería con portada, tabla y lista, ordenada por "#"), dentro del toggle de onboarding. Así el home termina en el footer, sin páginas sueltas. No se mueven a la base índice las páginas que contienen originales que lee un código.
- **Sidebar sincronizado** de las subpáginas: mención del OS → divisor → 2 botones → divisor → vista lista de la base índice (se actualiza sola) + toggle 📌 Index (tabla de contenidos).
- **Subpáginas:** Full Width, 18.75/81.25 con el sidebar a la izquierda, divisor y footer sincronizados, portada.
- **Dashboard:** 18.75/81.25; a la izquierda toggles h2 (Index, Avatar, Marketplace, Tags, Pets); en el centro cada vista con su heading, la cita "The original database lives in…" y un divisor; arriba del centro, fila 50/50 con 2 botones.
- **All-In-One:** un bloque por base principal con pestañas de ciclo de vida: Input → In Process → Output → Error (si aplica) → Favorites → Phone View → Archived.
- **Mobile View:** 2 botones arriba y listas mínimas.

### 0.2 Páginas evergreen obligatorias (en todo OS)
- **Dashboard** y **All-In-One** (con el ciclo de vida de arriba).
- **Mobile View:** listas mínimas (Name y como mucho una propiedad); si hay varias fuentes, un bloque con selector de vistas.
- **Favorites:** vista Favorite = true de la base principal (sumar la casilla si falta, cambio aditivo).
- **Integrations:** galería + lista de la base de integraciones filtrada por el sistema.
- **Archived:** vista de lo completado + copias legacy.
- **📊 Graphs:** vistas chart por estado, por mes, por marca o dueño y de gamificación. La agrupación por mes se pone en el navegador (el conector deja "day").
- **Cómo funciona**, **🤖 Agent Guide** (bases que lee y escribe cada bot, propiedades que no se renombran, reglas de gamificación) y footer estándar.
- **Gamificación (si hay):** Avatar (galería con Level, Total EXP, EXP to Next Level, Level Up Bar y Gold + vista tabla), Gamification Tags y Marketplace con 4 vistas (Table, Gallery, Board por Avatar, List), callout de reglas de Gold en Marketplace, 🐾 Pets con All / by Generation / Invalid assignments, y **un solo saldo**: los puntos del OS nuevo se suman a la fórmula del Leaderboard compartido (respaldar el texto de cada fórmula antes; si el campo base es rollup, crear un campo Total aparte).
- Cada base relacionada lleva su propia página y su entrada en el menú.
- Textos de reglas al día: si cambia una fórmula, actualizar Agent Guide, Cómo funciona y el home en la misma tanda.

### 0.3 Bases originales en el hub 🌐 Databases
- Cada base original del OS tiene **una fila en el hub** con icono, ⚙Workspaces = el OS (sumarlo sin quitar los que ya tenga si la base es compartida), Tags y Área, y dentro la base original o una vista enlazada.
- Las bases sin código que las lea viven **dentro de su fila del hub** (se mueven con OK; los ids se conservan) y la página del OS muestra vistas enlazadas.
- Las bases que lee un código **no se mueven**: se registran con vista enlazada y la cita "notion-publisher la lee: no mover" (o el código que sea).
- Cada página del OS lleva la línea "La base original vive en [fila] (🌐 Databases)" o, si se queda, "vive en esta página y está registrada en [fila]".
- Quedan fuera: bases que son de un producto público, vistas de otro registro y la base índice del OS.
- Verificar que la relación 🌐Databases del home del OS se llena.

### 0.4 Verificación de propiedades y relaciones (antes de cerrar)
- Recorrer todas las bases y vistas del OS: relaciones que apuntan a bases inexistentes (arreglar si hay destino lógico, si no quitar con respaldo), relaciones de un solo sentido que deberían ser de doble vía, valores de selección con nombres distintos para lo mismo (unificar revisando el repo primero), erratas en etiquetas y botones, filtros de vistas.
- Probar fórmulas con una fila marcada TEST en un estado que el código no lee (nunca Published) y archivarla al final; verificar el valor con filtros numéricos o en el navegador.
- Dejar el informe en un archivo con lo resuelto y lo abierto.

### 0.5 Iconos, plantillas de base, botones, automatizaciones y bloques AI
- **Iconos (probado):** toda página y fila de catálogo con icono; logo de la plataforma (simpleicons, icons8) y si no, emoji. Se ponen por conector.
- **Plantillas de base (en prueba):** 1+ plantilla por base, con propiedades por defecto, pasos numerados en H1 con el divisor sincronizado, checklists y un **Custom AI block** con su prompt (sin pulsar Generate; gasta créditos de Notion AI). Nunca predeterminada en una base donde un bot crea filas, ni en bases compartidas; nunca llenar por defecto campos que un código usa para tomar filas (colas de publicación). Bases sensibles (cuentas, canales) arrancan en estado cerrado (pausada, discover).
- **Botones (en prueba):** "+ <base>" con su plantilla, en el Dashboard, en Mobile View y en el sidebar sincronizado; abren en side peek. Botones dentro de plantillas para crear la fila siguiente del flujo (p. ej. idea → pieza).
- **Automatizaciones nativas (en prueba):** solo las que no cambian campos que lee un código: fechas al cambiar de estado, avisos de error, estados derivados (usada, aprobada) y avisos de activación. No automatizar campos que ordenan colas ni asignaciones que tocarían las filas del bot; asumir que también se disparan con lo que escribe la API. Ningún webhook sin OK aparte.
- Lo que está "en prueba" pasa a obligatorio solo cuando funciona en un OS real y el dueño lo confirma.

## 1. Staging (cuenta base, por conector)
1. Crear una página de staging a nivel workspace con el árbol de la plantilla (Home, Dashboard, guía, secciones).
2. Bases ligeras: nunca copiar bases originales pesadas. Crear bases nuevas dentro del staging con el mismo esquema y 3–6 filas "Example · …" de datos ficticios. Relaciones de doble vía con `RELATION('<ds>', DUAL '<nombre>')`, llenadas solo con filas del mismo árbol. En la Free, las relaciones complejas pueden bajar a selección múltiple.
3. Directorios públicos (prompts, inspiración, etc.): solo vista previa de la página pública, sin base.
4. Reapuntar cada vista enlazada a las bases ligeras. `create-view` con parent_page_id deja la vista al final de la página; reubicarla con un solo `update_content` que mueva el tag `<database>`.
5. Antes de duplicar, limpiar en el staging: ids escritos a mano en texto o tablas, botones que apuntan a bases excluidas, datos personales, links privados y footers (cada página tiene su propia copia del footer).
6. Footer estándar: "Made with 🖤 from Peru by <creador>" con link a la web del creador. Links a herramientas personales del creador se consultan con el dueño.
7. Conector: una escritura a la vez, fetch después de cada una (con "service unavailable", fetch antes de reintentar). Verificar por fetch, no por la búsqueda de Notion. Menciones de base: `<mention url="…" type="database"/>`.
8. El conector puede: poner iconos y portadas, mover páginas a una base (conservan ids), crear vistas chart, crear relaciones de doble vía y escribir fórmulas. No puede: leer el texto ni el resultado de fórmulas (leer el texto en el navegador desde el DOM y respaldarlo), filtrar por fórmulas, poner la vista previa de tarjetas de galería, crear o leer botones, crear plantillas de base ni automatizaciones, subir imágenes, archivar ni compartir.
9. Subidas desde el navegador: usar rutas reales, no enlaces simbólicos.

## 2. Duplicar fuera (navegador)
1. Ambas cuentas con sesión en el Chrome; si no, pasar el inicio de sesión al usuario.
2. Compartir el staging con la cuenta secundaria (Can edit). Desde la secundaria: ••• → Duplicate page → su workspace.
3. Verificar la copia: filas Example en cada base, vistas que leen la copia, sin bloques sin acceso, sin links al workspace base, sin páginas sueltas "View of …".
4. No hacer clic en Duplicate dos veces; archivar las extras.

## 3. Traer de vuelta a la base de plantillas (necesita el sí del dueño)
1. Desde la secundaria, compartir la copia limpia con la cuenta base (Full access).
2. Desde la base: Duplicate de la copia compartida y Move to → bajo la card del producto.
3. Quitar el compartido en ambas direcciones y dejar de compartir el staging. Archivar la copia intermedia en "🗃️ Archived" de la secundaria.

## 4. Una sola card por producto en la base de plantillas
Cada producto tiene UNA sola fila. Nunca filas separadas para Premium y Free.
- Cuerpo: copiar la estructura de una fila aprobada del mismo tipo: callout 🧭, embed de la tienda (al publicar), toggles H2 Inspiration / Template / CTA / Description / Links / Tweet. Links lleva FREE, PAID, página de la tienda, PH Launch y donaciones. Lo que falta queda vacío.
- La Premium y la Free son páginas hijas dentro del toggle Template: "<Producto> · Premium" y "<Producto> · Free".
- Propiedades como filas parecidas, Status In progress hasta publicar, portada Unsplash e icono.
- Si los sistemas llegaron como filas de la base: crear la card, mover cada sistema dentro uno a la vez, poner los tags `<page>` en el toggle Template y las menciones en Links, y verificar por fetch.

## 5. Versión Free
Hermana dentro del mismo staging, con sus bases ligeras, páginas recortadas, Full Width y la línea "Upgrade your FREE version to the PRO version" enlazada a la Premium (cambiar a la URL pública al publicar). Las ilustraciones se copian en el navegador desde la Premium (Ctrl+C / Ctrl+V, Dismiss para que no quede sincronizada).

## 6. Limpieza
Archivar (no borrar) las copias de prueba y filas TEST en ambos workspaces y las versiones viejas del Sandbox. Registrar los ids.

## 7. Publicar (solo con sí explícito)
Publicar ambas páginas desde la cuenta base, URLs públicas en Links y en la card, embed de la tienda, link de upgrade de la Free a la URL pública, Status Published y pasar la ficha a quien maneja las tiendas.

## Checklist
- [ ] Workspace real primero: auditado, comparado contra el OS de referencia (tabla P1/P2/P3), OK del dueño, aplicado y cerrado
- [ ] Layout de referencia: nav 3×33.33, páginas como filas de base índice, sidebar con vista del índice, Dashboard 18.75/81.25 con toggles, All-In-One con ciclo de vida, home sin Full Width
- [ ] Evergreen completo: Dashboard, All-In-One, Mobile View, Favorites, Integrations, Archived, 📊 Graphs (por mes), Cómo funciona, Agent Guide, Pets
- [ ] Gamificación con un solo saldo y vistas completas (si aplica)
- [ ] Cada base original registrada en el hub 🌐 Databases y la línea "La base original vive en…" en su página
- [ ] Verificación de propiedades, relaciones, nombres y erratas; fórmulas probadas con fila TEST archivada
- [ ] Iconos en toda página y fila de catálogo; portadas en subpáginas
- [ ] (En prueba) plantillas por base con bloque AI, botones y automatizaciones seguras
- [ ] Bases ligeras + filas Example, mismo esquema
- [ ] Sin ids escritos a mano, botones rotos ni datos personales
- [ ] Footer estándar, links del creador revisados
- [ ] Ambas cuentas en el Chrome; duplicado y verificado
- [ ] Sí para compartir entre cuentas → compartir, duplicar, mover, quitar compartido
- [ ] Una sola card por producto con Premium + Free dentro del toggle Template
- [ ] Free hermana con ilustraciones y Full Width
- [ ] Pruebas archivadas, staging sin compartir
- [ ] Log + fetch
- [ ] Publicar solo con sí
