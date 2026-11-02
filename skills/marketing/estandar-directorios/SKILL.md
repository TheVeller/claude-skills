---
name: estandar-directorios
description: >-
  Usar al crear, empaquetar, auditar o mantener un directorio/dataset vendible
  (Notion + GitHub + web + SEO + newsletter + MCP/API + Gumroad + portales de
  datasets), incluso en modo autónomo nocturno. Copia la referencia dorada
  (Ecosistema Arequipa / Builders AQP), define las capas, la verificación final
  y las reglas de calidad.
---
# Estándar de directorios

Un directorio es informativo y es una máquina de tráfico. Funciona así: el SEO programático atrae visitas, el newsletter captura emails, Gumroad monetiza, y los artículos se reciclan como listicles para cada red. Cada directorio nuevo solo define su **dataset** y su **topic**; todo lo demás es plantilla.

## ⭐ Referencia dorada: copiar, no reinventar
El primer directorio completo es el **molde obligatorio**. Antes de cada capa, abre la pieza equivalente de la referencia y replícala estructura por estructura, cambiando solo los datos y la identidad. Si la referencia tiene algo y el nuevo no, es un error.
- **Notion:** página «Directorio — Ecosistema Arequipa» https://app.notion.com/p/3f2da2435b468151bbadd79211050be0 (va como hija de «Directorios» 3f2da2435b468131bb43d8530eacf444).
  - Layout en dos columnas. La izquierda lleva fecha de actualización, el recuadro «➕ Sumar» que abre el form, «🧭 Cómo usar», «📚 Fuentes» y una galería de categorías con cover. La derecha lleva el directorio.
  - Divisor y footer compartidos.
  - 3 DBs enlazadas: Directorio, Categorías y Fuentes.
  - Estados: Borrador → Por confirmar → Aprobado A3 → Publicado / Descartado. Las vistas públicas muestran solo Publicado.
- **Repo:** crafter-station/awesome-ecosistema-arequipa (README, docs/README-STANDARD.md, data/, assets/covers con imágenes permanentes).
- **Web:** crafter-station/arequipa-sillar-connect → ecosistemarequipa.com (docs/SEO.md, src/lib/seo.ts, docs/NEWSLETTER-STANDARD.md, docs/DIRECTORY-INTEGRATIONS-STANDARD.md).
- **Gumroad:** borrador wteodk. Método en /workspace/directorios/gumroad/CREAR_PRODUCTO.md.
- **Archivos locales:** /workspace/directorios/ (ESTANDAR_GITHUB.md, ESTANDAR_NEWSLETTER.md, brief_swe_lovable.md, ecosistema_arequipa.json).

## 🤖 Modo autónomo
Cuando el dueño entrega un directorio nuevo (una fuente, un tema o una DB), se construye completo, capa por capa, en las corridas nocturnas y sin pedirle intervención, hasta tener la verificación de la capa 11 toda en ✅.
- **Decisiones con default** (se decide, se anota en ESTADO.md y se sigue):
  - **Nombre:** el que ya tenga la fuente o el producto. Si no tiene, «N+ <Nicho> …» con N redondeado hacia abajo.
  - **Repo:** crafter-station/awesome-<slug>.
  - **Licencia:** CC BY 4.0 para los datos y MIT para el código.
  - **Precio:** $0+ (paga lo que quieras) hasta que Forja diga otra cosa.
  - **Ítems dudosos o contra las reglas de una plataforma:** marcados en una columna Excluir y fuera de las vistas públicas.
  - **Identidad:** un emoji y una paleta propios, tomados del tema.
- **Lo único que espera al dueño:** el A3 para publicar, comprar un dominio o pagar algo, y los logins o DNS que solo él puede hacer. Todo lo demás se deja construido en Borrador, privado o apagado, listo para el A3.
- **Reporte:** una sola petición de A3 al final, con la tabla de la capa 11 y los links. Nada de preguntas sueltas.
- **Ritmo:** una o dos capas por noche, sin más de 2 procesos pesados a la vez. El trabajo de código va con cloud agents, no con créditos de Lovable.

## Reglas base
- **Datos:** nunca inventar. Cada fila lleva su fuente.
- **Más es mejor:** se incluyen todos los niveles (S/A/B/C y los que requieren login), con el nivel como etiqueta. Solo se excluyen los sitios **caídos o muertos**.
- **Imágenes:** foto real; si no hay, la og:image o una captura del sitio; si no, el logo. Nada de stock ni de imágenes generadas con IA. Siempre con crédito.
- **Ficha mínima por ítem:** nombre real de la marca, descripción de 1 frase (tomada del meta description o del propio sitio), categoría, URL del sitio, URL de submit aparte, cover, logo y fuente.
- **Publicar** (web, Gumroad, newsletter, envíos, portales de datasets) requiere el A3 del dueño.

## Las capas, en orden de construcción

### 1. Dataset, limpieza y auditoría
- **Preparar:** exportar, deduplicar (por host+path y por nombre normalizado, fusionando variantes) y mapear a unas 10-14 categorías.
- **Limpiar nombres:** marca real; nada de títulos de página, dominios en minúscula, verbos ni textos cortados.
- **Separar URLs:** la URL del sitio va en una columna y la de submit en otra.
- **Quitar notas internas** de las columnas públicas.
- **Chequear que cada link esté vivo:**
  - **Muerto:** DNS caído, 404/410, dominio parqueado o sin conexión.
  - **Vivo:** 401/403 o Cloudflare, con su flag.
- **Enriquecer** con la descripción y las imágenes de la ficha mínima.
- **Salidas:** `product_clean.csv`, `dead_sites.csv` y `MANTENIMIENTO.md`.

### 2. Notion (fuente)
Copiar la página de referencia, con todo lo que tiene:
- **Vistas:** Galería por defecto (Page cover) > Lista > Tabla > Mapa (si hay ubicaciones).
- **Form «Sumar …»**, cuyas respuestas entran como Borrador.
- **Link a Gumroad.**
- **Si la API no deja configurar algo** (por ejemplo el cover de las tarjetas o el orden de las vistas), anotarlo como paso de navegador y hacerlo en el slot nocturno.

### 3. Repo GitHub `awesome-*`
- **README** generado por script, siguiendo el README-STANDARD de la referencia:
  - H1 con keywords;
  - intro con conteos reales;
  - bloque de links (Web, Guía, Notion, Mapa, Ranking, datasets);
  - conteo por categoría, una fuente por entrada, y secciones Contribuir y Licencia.
- **Covers** permanentes en assets/.
- **About** con keywords (~350 caracteres), hasta 20 topics, y Website = el dominio propio.
- **Si el repo es de una org**, la org tiene que aprobar la app OAuth para poder editar los metadatos.

### 4. Web (Lovable, premium)
Partir de la estructura de arequipa-sillar-connect:
- **Identidad:** la del cover de Notion, con Reluma/Refero, mobile-first.
- **Dominio propio**, y **favicon** = el emoji del directorio.
- **Menú Recursos** uniforme.
- **GitHub al nacer:** apenas termina el primer prompt de Lovable, SWE conecta el proyecto a GitHub desde el editor (navegador), en la org crafter-station, sin pedírselo al dueño.
- **Código:** después, todo con cloud agents sobre el repo, con push directo a main (sin PRs). Lovable pagado solo si el dueño lo pide; los errores de preview van con el Try to Fix gratis.
- **Brief para SWE:** /workspace/directorios/brief_swe_lovable.md, que se actualiza en cada directorio.

### 5. SEO programático
- **Páginas:** `/actor|item/<slug>` y `/categoria/<slug>`, prerenderizadas.
- **En cada una:** title y description únicos, canonical, OG, JSON-LD, sitemap y robots.
- **`/guia`:** la «Guía definitiva N+ fuentes», con FAQPage.
- **JSON-LD `Dataset`.**
- **Reciclaje** de los artículos como listicles para cada red.
- Copiar docs/SEO.md y src/lib/seo.ts de la referencia.

### 6. Newsletter evergreen (cuando hay dominio)
Según docs/NEWSLETTER-STANDARD.md:
- **Proveedor:** Lovable Emails, con doble opt-in.
- **Cada 15 días:** 2-3 ítems que el suscriptor no recibió, más «Lo nuevo» con noticias de last30days y un CTA a Gumroad.
- **Al agotarse el pool:** solo noticias.
- **Cumplimiento:** página `/privacidad` y link visible a `/baja`.
- **Queda OFF** hasta el A3, después de una prueba interna.

### 7. Integraciones para agentes
Según docs/DIRECTORY-INTEGRATIONS-STANDARD.md:
- **API** `/api/v1` de solo lectura.
- **MCP** con buscar, listar, ver y submit.
- **Submissions** por form, API o MCP, que entran como Borrador, con anti-spam y rate limit.

### 8. Producto en Gumroad
- **Creación:** API v2 vía el proxy de Composio, con `query_params`. `POST` crea el producto publicado, así que hay que llamar a `/disable` de inmediato. Si ya existe un borrador, reusarlo.
- **Patrón de la tienda:**
  - título «N+ …», precio $0+;
  - gancho, What's included, Who will benefit y FAQ;
  - archivos CSV/JSON, portada y miniatura cuadrada;
  - recibo con pedido de rating.

### 9. Portales de datasets
- **Destinos:** Kaggle (con notebook de ejemplo), Hugging Face, data.world, Zenodo, el portal de datos abiertos local si aplica, y un PR en awesome-public-datasets.
- **Google Dataset Search** se cubre con el JSON-LD de la web.
- **Cuenta y accesos:** revisar primero si Composio los tiene. En modo autónomo se deja el paquete listo y la subida espera el A3.

### 10. Extras visuales (opcional)
- Mapa PamPam con fotos reales.
- TierMaker como ranking público.

### 11. Verificación general hacia atrás (obligatoria)
Recorrer las capas de la última a la primera, en vivo, y además compararlas con la referencia dorada.
- **Números:** el mismo conteo de ítems y categorías en todas las superficies.
- **Nombres:** el mismo nombre, emoji y tagline.
- **Links cruzados:** usan las URLs definitivas y todos responden 200.
- **Identidad visual:** coherente con el cover de Notion.
- **Datos:** sin muertos, duplicados ni nombres sucios, y cada ítem con su ficha mínima completa.
- **Estados:** lo que debe estar apagado o en borrador sigue así hasta el A3.
- **Paridad con la referencia:** cada elemento que tiene Arequipa existe en el nuevo.
- **Salida:** una tabla con ✅/❌. Se corrige, se vuelve a verificar y recién ahí se pide el A3.

### 12. Mantenimiento
- Auditoría mensual de links caídos.
- Revisar las invitaciones de Discord vencidas.
- Refrescar el dataset y repetir la capa 11.

## Checklist de cierre
El directorio está listo cuando:
- tiene paridad completa con la referencia;
- la ficha mínima está al 100% (o el hueco está justificado);
- Notion, el repo, la web, el SEO, el newsletter (OFF), MCP/API, Gumroad (borrador) y el paquete de datasets están listos;
- la capa 11 está toda en ✅;
- se envió una sola petición de A3.
