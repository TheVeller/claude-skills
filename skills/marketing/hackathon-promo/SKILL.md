---
name: "hackathon-promo"
description: "Usa esta skill cuando el usuario quiera promocionar un hackathon presencial o híbrido (full day, multi-ciudad, cupo con aprobación) y necesite el kit de copy. Dispara con: 'promo del hackathon', 'copy The Next Craft', 'textos para el hackathon', 'kit hackathon', 'blasts del hackathon', 'descripción Luma hackathon', 'mensajes de aceptación / waitlist / rechazo'. También cuando pega un link de Luma de un hackathon (no webinar) y pide la promo. El output es SIEMPRE un archivo .md con estrategia, emails, descripción Luma + 3 mensajes post-registro, un post corto multi-canal, stories, LinkedIn, blasts B1–B4 y calendario. NO usar para webinars/masterclass en vivo online (para eso está promo-webinar ni su trilogía de recordatorios día D)."
---

# Promo de hackathon — kit multicanal

Convierte un brief (o link Luma) en el kit de promoción de un **hackathon**: inscripción, sede/horario de venue, rutas, un post corto reutilizable, LinkedIn, secuencia de **blasts** (no recordatorios de webinar) y **tres mensajes post-registro** (aceptado / en espera / no aceptado).

Si el evento es un webinar online con trilogía “unas horas / minutos / en vivo”, usa `promo-webinar` en su lugar.

---

## Paso 1 — Capturar el brief

Variables mínimas:

| Variable | Qué es |
|---|---|
| `hackathon_title` | Título del evento (como en Luma) |
| `hackathon_context` | Descripción, rutas, multi-ciudad vs sede local, partners, tono |
| `city_or_venue` | Ciudad + venue + dirección corta |
| `start_local` / `end_local` | Fecha y horario **del venue** (no inventar; si Luma dice otra cosa y el humano corrige, gana el venue) |
| `timezone` | Ej. `America/Lima` |
| `registration_url` | Link Luma u otro |
| `info_url` | Sitio de más info (ej. https://thenextcraft.org/) si existe |
| `approval_required` | true/false — cupo con aprobación del host |
| `organizers` | Orgs / hosts (sin inventar credenciales) |
| `output_language` | `es` o `en` (default: idioma del usuario) |

**No hagas ronda de preguntas** si pegó un Luma URL o brief suficiente: fetch/extrae y asume con criterio. Solo pregunta si faltan título o contexto entero.

Datos duros faltantes → marcadores `[FECHA]`, `[HORA]`, `[VENUE]`, `[LINK DE REGISTRO]`. No inventes cupos, precios ni partners.

Si hay **narrativa multi-ciudad** (ej. “12 horas / 120 personas”) y **horario local de venue** distinto, documenta ambos: copy global puede usar la narrativa; copy de sede usa el horario real del venue.

---

## Paso 2 — Estrategia (antes del copy)

Escríbela al inicio del entregable:

1. **Ángulo** — por qué este hackathon *ahora* / esta sede (3–5 líneas)
2. **Deseos** — mínimo 5
3. **Objeciones** — mínimo 5 (equipo, intensidad, “solo networking”, aprobación, etc.)
4. **Tagline central** — una línea que unifique canales

---

## Paso 3 — Mapa de canales

Incluye tabla ajustada al caso. Canales base:

| Canal | Objetivo | CTA típico |
|---|---|---|
| Email principal | Registros fríos/tibios | Registrarme / Aplicar |
| Email comunidad | Asistencia local / comunidad | Aplicar |
| Página Luma | Conversión | Reservar cupo |
| Post corto único | TG / FB / comunidad / X | Link registro |
| Stories | Recordar + humanizar | Sticker link |
| LinkedIn | Autoridad + alcance | Registro |
| Blasts B1–B4 | Inscripción → equipo → víspera → mañana | Link / llegar |
| Post-registro ×3 | Aceptado / espera / no aceptado | Info / waitlist |

**Prohibido** en esta skill: trilogía webinar “Empezamos en unas horas / Arrancamos en minutos / SESIÓN EN VIVO”.

---

## Paso 4 — Escribir los assets

Idioma = `output_language`. Lee `references/ejemplos-voz.md` e imita **registro**, no contenido.

### 1. Email principal
3 asuntos · 2 preheaders · cuerpo corto · logística (fecha, hora venue, lugar) · un CTA · `info_url` si existe.

### 2. Email comunidad
2 asuntos · tono cercano · por qué esta sede/comunidad · CTA aplicar.

### 3. Página Luma
- **Descripción** lista para pegar: narrativa del hackathon → sede local → cuándo/dónde (horario venue) → rutas → para quién → más info → CTA registro.
- **Justo después**, obligatorios los **3 mensajes post-registro**:

#### 3a. Aceptado / registrado con éxito
Confirma que está dentro · fecha/hora/venue · qué traer (laptop, equipo) · link evento + info.

#### 3b. En espera de aprobación
Recibimos solicitud · en revisión · no re-aplicar · arma equipo mientras · te avisamos.

#### 3c. No aceptado / sin cupo
Agradece · no hay cupo (capacidad/balance) · no atacar el perfil · apunta a `info_url` / próximas ediciones · oferta waitlist u otro evento si aplica.

### 4. Post corto único
**Un solo bloque** reusable en Telegram, Facebook, comunidad y X. No seis variantes.

### 5. Stories pre-evento (5–7)
Tabla: # · visual · texto en pantalla · interactivo. Incluye venue, horario, rutas, CTA.

### 6. LinkedIn (uno solo, fuerte)
220–400 palabras. Creencia rota → qué es el hackathon → sede/horario → rutas → logística → CTA + pregunta opcional de engagement.

### 7. Secuencia de blasts (hackathon)
WhatsApp / Telegram / comunidad. Exactamente **B1–B4**:

| Blast | Timing | Job |
|---|---|---|
| B1 | −10 a −7 días | Apertura de cupo / sede |
| B2 | −5 a −3 días | Arma tu equipo / elige ruta |
| B3 | −1 día | Víspera: qué traer, revisar Luma |
| B4 | Mañana del evento (~30–60 min antes de doors) | Hoy: venue + hora de llegada |

---

## Paso 5 — Calendario

Tabla práctica alineada a B1–B4 + email/LinkedIn/stories/post corto. Sin filas de “recordatorio webinar −3h/−5min”.

---

## Reglas de escritura

1. Una idea, un CTA por pieza (excepto post-registro, donde el CTA es implícito: presentarse / esperar / seguir info)
2. Horario **venue** siempre que hables de esa sede
3. `Más info: [info_url]` en descripción Luma y piezas clave si existe
4. No inventar partners, cupos ni credenciales
5. Concreto > abstracto; “tú” > “nosotros”
6. Tono persona, no departamento de marketing
7. Si `approval_required`, dilo en registro/CTA

---

## Entrega

Un archivo `.md` por evento en la carpeta de salida del proyecto (ej. `promos/`):

`promos/YYYY-MM-DD-slug/promo.md`

- `YYYY-MM-DD` = fecha de inicio del evento (`America/Lima`)
- `slug` = kebab de ciudad/evento / id Luma (sin prefijo `promo-`)
- Crear la carpeta del evento si no existe; extras opcionales van en el mismo folder

Contenido del kit (`promo.md`):

```
# Promo — [hackathon_title]

## Estrategia
## Mapa de canales
## 1. Email principal
## 2. Email comunidad
## 3. Página de evento (Luma)
### Descripción
### Mensajes post-registro
#### Aceptado
#### En espera
#### No aceptado
## 4. Post corto único
## 5. Stories pre-evento
## 6. LinkedIn
## 7. Secuencia de blasts (B1–B4)
## Calendario de publicación
```

Copy listo para pegar; notas al usuario en cursiva debajo del bloque, nunca dentro.

Después de entregar el archivo: **un resumen de una línea** en el chat. No reimprimas el kit.
