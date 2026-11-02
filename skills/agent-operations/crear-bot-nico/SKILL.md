---
name: crear-bot-nico
description: >-
  Usar al crear un Grok Bot nuevo o al auditar bots vivos: oficio sin overlap,
  escritura UX, workspace Notion a nivel vendible estilo Sales OS (icon x.ai/bot
  en roster, originales/vistas/dashboard/All-in-One, ilustraciones unDraw
  obligatorias, My Templates por vistas enlazadas, favicon tienda + foto real en
  ítems).
---
# Crear bot único

## Antes de crear
1. Lee todos los `profile.json` en `/home/box/agent-data/agents` y anota nombre + descripción de cada agente vivo.
2. Compara el oficio propuesto contra ese roster. Si ya existe alguien que cubre lo mismo (aunque el nombre sea distinto), no crees: reporta el overlap y propone ajustar al existente.
3. Fronteras fijas a respetar: Cazador Vivienda = alquiler para vivir en Arequipa (no compraventa); Cazador Inmobiliario = compraventa/inversión en Perú (no alquiler para vivir); Cazador de Canales = descubrir canales de distribución y primer envío para GPT-Chain + The Veller (no demanda, no competencia, no mantenimiento continuo de tiendas); Cazador de Demanda = deals Núcleo Lab (nucleo.la) en LATAM hispano, Perú primero; Competitor Watcher = competencia de las marcas vivas; Cazador de Vuelos = vuelos desde AQP; Directorios = datasets/directorios de fuentes públicas; Forja = propone huecos de ingreso, no caza; Grok Bot = roster + nombra el oficio; Bot Father = CreateAgent.
4. Slots: tope ~50 bots en Grok. Si no hay slot, usar la skill Exportar bot para mover uno a otra plataforma antes de crear.

## Brief del nuevo
- Un oficio, una entrega, una exclusión explícita (qué NO hace y a quién no pisa).
- Idioma y tono acordes al usuario.
- **Escritura a Ignacio (obligatoria en la descripción / contrato de cada bot):** markdown legible; título con emoji en cada sección; bullets; explicación corta (qué / para qué / qué falta); párrafos claros, no una sola línea densa ni “schemable”. Misma regla en Kit OS y en 1:1. En salas, además familia formato-hallazgo. No meter leyenda ⭐/🤖/🙋 ni “Propongo” (solo Orq/Cockpit).
- Si necesita routine de oficio, cadence en horas de Ignacio (America/Lima), weekdays por defecto, una corrida con tope y criterio de parada, silencio cuando no hay nada.

## Alta
1. Crea el agente con nombre corto y descripción operativa (qué busca, qué entrega, qué no hace) **incluyendo el bloque de escritura a Ignacio**.
2. Grok Bot es SSOT del roster vivo; no inventes un ledger paralelo de “bots que creé”.
3. Avisa a Ignacio: nombre, oficio, a quién no pisa, y si quedó con routine.
4. Si Forja lo propuso, confírmale el alta para que no lo vuelva a crear.

## Notion — fila + workspace (en cada alta con página propia)
Base viva: Roster (propiedades en inglés desde 28-oct-2026: Type Agent/Room/Channel, Status Active/Paused/Archived, Category, Priority High/Medium/Low/Intake, Maturity Idea/Set up/Operating/Mature, Role, Description, Platform, Always on, Maintains own page, Bot ID, Reports to, Connectors), ahora en la fila-hub Roster de 🌐 Databases (Agentic OS), https://app.notion.com/p/9a9f74ccb1684af2b6a6015e67c771c4, data source `collection://8087c2ec-e782-48b6-964a-fd9225a87c33`, dentro de ROSTER.

No inventes mails, fichas ni filas fuera del flujo acordado. Regla vigente de Grok Bot: los bots no crean DBs nuevas por su cuenta; Ignacio las crea o aprueba explícitamente.

### Siempre (cualquier bot con página propia)
1. Fila en el Roster con **Maintains own page = YES**. La fila ES el home operativo del bot.
2. Subpágina **Evergreen**: hechos estables del oficio. No duplicar listas que viven en otra SoT.
3. **1–N DBs originales** que el bot lea/escriba de verdad. Nombres y columnas salen del oficio, no clonar otro cazador.
4. **SoT externas:** si ya existe fuera del roster, no crear DB duplicada; va como **un** linked DB con N vistas.
5. Routine que mantenga esa página + entorno.

## 📐 Estándar vendible (Sales OS)
Cada workspace de agente debe poder venderse como plantilla Notion (referencia: Sales OS de The Veller). Spec: `/workspace/exports/reglas-workspace-notion.md`.

### Arquitectura en 3 capas
- **Originales:** cada DB vive en una sola página (su página de entidad o el hub de bases), con relaciones nombradas con el emoji del destino.
- **Vistas:** Dashboard, All-in-One y Archived solo tienen linked views.
- **Accesorios sincronizados:** onboarding, divisor, navegación, índice y footer son synced blocks: se editan una vez.

### Layout verificado
- **Home:**
  1. Toggle Onboarding → synced → callout (qué es, para qué, cómo, quién mantiene).
  2. **Divisor de imagen** (Normal_Divider.png) en un **synced block**, reutilizado entre secciones. Los `---` nativos solo van dentro de columnas.
  3. **Navegación numerada arriba**: synced con 3 columnas de 33.33.
  4. Una sección por página, una por fila, 50/50, con la **ilustración alternando** izq/der.
  5. Toggle índice sincronizado junto a la ilustración de "búsqueda/mapa".
  6. **Footer del creador solo en el home.**
- **Subpáginas** (entidad, All-in-One, Cómo funciona, Agent Guide): columnas **18.75 / 81.25**. Izquierda: toggle índice sincronizado. Derecha: contenido o base. Divisor al final. Sin nav numerada ni footer.
- **Dashboard:** **3 columnas 16.67 / 66.67 / 16.67**.
  - Angosta izquierda: 📌Index (TOC) + índice.
  - Centro: lo diario.
  - Angosta derecha: widgets en vista lista.
- **Archived:** el mismo esqueleto que el Dashboard, con 📌Index.
- **Las linked views SÍ pueden ir dentro de columnas.**
  1. Créalas.
  2. Haz fetch para obtener su tag `<database …>`.
  3. Muévelas dentro de `<columns>` con replace_content. Mantienen los filtros.

### Las 4 experiencias
| Experiencia | Qué es |
|---|---|
| 🏛️ Real (Ignacio) | Usa linked views de las bases del hub. |
| 💎 Premium | Plantilla autocontenida. |
| 🆓 FREE | El núcleo del flujo. |
| 🤖 Agente | Fila del Roster + 🌱 Evergreen + 🤖 Agent Guide (bases con collection id, valores válidos, qué hacer y qué no; sin imágenes). |

### My Templates y productos
- **My Templates nunca se mueve ni se le cambia el esquema.** Se trae a cada workspace con vistas enlazadas.
- Cada directorio o producto = **una fila en My Templates que solo enlaza** a la página real; la página no se mueve.
- **Fichas Gumroad (toggle Description/CTA):**
  - En **inglés**, salvo una excepción local aprobada.
  - Siempre como BORRADOR hasta que Ignacio apruebe.
  - Solo datos reales.
  - Visuales de la ficha: brief a Musa Designer.

### 🖼️ Ilustraciones (paso OBLIGATORIO de todo workspace)
- **Dónde:** 1 ilustración unDraw por sección del home, en la columna 50 % opuesta al texto.
- **Spec:**
  - Plano estilo unDraw: personaje + objeto de la sección.
  - Sin contornos, sin degradados, sin texto.
  - #3f3d56 con acento negro, fondo blanco.
- **Proceso:**
  1. **Reusa primero la biblioteca** (dashboard, all_in_one, evergreen, agent_guide, archivados, como_funciona, index…).
  2. Genera solo las que falten con GenerateImage, con 2 ilustraciones existentes como referencia de estilo.
  3. Quita el fondo (blanco >235 → transparente; si hay blancos internos, solo el conectado al borde), recorta y deja máx. 640 px. Nombre: `<seccion>_nobg.png`.
  4. Revisa cada una a ojo y regenera si tiene texto o se ve mal.
  5. Escribe un manifest (página, texto exacto de la marca, archivo).
  6. **Súbelas por conector** (probado 2026-10-10, queda como bloque de archivo alojado en Notion, no caduca). Una por una, en serie:
     - `notion-create-file-upload` con `{"filename":"<seccion>_nobg.png"}`. El `upload_url` dura unos 10 min y sirve para un solo archivo.
     - `curl -X POST "<upload_url>" -F "file=@<ruta>;type=image/png"` + todos los `upload_headers` como `-H`. Máx. 20 MiB.
     - `notion-update-page` reemplazando la marca por el `suggested_markdown` devuelto.
     - El navegador queda solo como respaldo si el conector falla.
- **El workspace NO está "hecho" mientras quede una marca "Ilustración pendiente".**

### Límites del conector Notion
- No sube imágenes de forma fiable, no crea botones ni plantillas de DB y no borra (se archiva).
- Las vistas nuevas caen al final de la página; luego se mueven a columnas (ver arriba).
- **Synced references:** si llevan hijos, escriben sobre el original.
  1. Usa placeholders.
  2. Haz update_content para insertar la referencia.
  3. Haz insert_content al final.
- Haz las inserciones en serie, no en paralelo.
- update_content no matchea líneas de imagen.
- Confirma a ojo covers, iconos e imágenes.

## Iconos y covers — tres capas
### A) Página del agente en Roster (Platform = Grok Bot)
- Icon = logo Grok Bot: `https://t1.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://x.ai/bot&size=128`.
- No emoji genérico, no favicon de `grok.com`.
- Cover Unsplash temático del oficio (verificar HTTP 200).
### B) Evergreen y DBs/páginas hijas
- Icon nativo (emoji Notion). Cover Unsplash temático.
### C) Filas de compras / productos
- Icon = favicon de la tienda. Cover = foto real del artículo (`og:image`). No Unsplash genérico.
- Fotos propias para vender: prop **Fotos** (files) + checkbox **Listo FB**.

## Inventario propio vs SoT externa (Wishlist y similares)
- Filas ya adquiridas (Owned) → ledger hijo **Inventario personal** con Status, Source, Paid S/, Where, Purchased, url, Priority, Categoría, Condición, Notas internas, Notas venta, **Resale S/**, **Fotos**, **Listo FB**.
- La SoT externa sigue como **1** linked DB.

## Plantilla mínima al crear
Home (icon x.ai/bot + cover + Onboarding + navegación arriba + secciones 50/50 con ilustración + footer) + Evergreen + 🤖 Agent Guide + 1 DB original en su página (icon, cover, props nativas, Archivado, vistas útiles) + 📊 Dashboard + 💎 All-in-One + 🗄️ Archived + ⚙️ Cómo funciona + ilustraciones subidas + Mantiene = YES + routine. Si las DBs aún no existen (regla de no crear DBs), dejar la home lista y anotar qué DB falta.

## Qué NO hacer
- No copiar nombres de DB de otros bots.
- No duplicar SoT del usuario como DB hija; no 2+ linked DBs de la misma SoT.
- No emoji ni favicon grok.com en páginas de agente Grok Bot.
- No Unsplash en filas de producto.
- No texto libre cuando cabe select / url / date / number.
- No crear DB que el bot no vaya a escribir, ni DBs sin OK de Ignacio.
- No inventar filas ni contenido de ledgers.

## Auditoría de bots vivos
Mismo patrón para bots existentes: dar propósito + workspace vendible cuando falte.

### Qué mirar por bot
1. Role claro (entrega + anti-oficio).
2. Escritura a Ignacio.
3. Página del roster: Maintains own page = YES; icon x.ai/bot; cover.
4. Evergreen.
5. Criterios Sales OS 1–10 (puntaje /10).
6. Ítems producto: favicon tienda + foto real.
7. Inventario vs SoT.
8. Routine.
9. Overlap: Grok Bot nombra oficio.
10. Drift: el texto de la home coincide con lo que existe (p. ej. no dice "pendiente" si la DB ya existe).
11. Ilustraciones: cero marcas "Ilustración pendiente".

### Entrega de una auditoría
Tabla por agente: puntaje /10 · qué tiene · qué falta · fix principal. Más conteos (vendibles, vacías, icon correcto) y 2–3 referencias.

Canon 35/7: no altas sin Grok Bot + hueco o “fuera de canon”.
