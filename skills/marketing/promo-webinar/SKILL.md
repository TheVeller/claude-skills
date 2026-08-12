---
name: "promo-webinar"
description: "Usa esta skill siempre que el usuario quiera promocionar un webinar, workshop, masterclass, clase en vivo o sesión online y necesite el copy para difundirlo. Dispara con: 'promoción del webinar', 'copy para mi workshop', 'arma la promo', 'necesito los textos para difundir la sesión', 'emails y posts para el webinar', 'kit de promoción', 'cómo promociono mi masterclass', 'textos para llenar el evento', 'stories del webinar', 'broadcast del día del evento', 'post de LinkedIn para la clase en vivo'. También cuando el usuario solo pega el título y la descripción de un evento y pide 'los textos', 'la promo' o 'todo el copy'. El output es SIEMPRE un archivo .md con los 9 assets multicanal más el calendario de publicación. NO usar para newsletters de contenido, lead magnets, ni para una secuencia de emails de venta de un curso (para eso está campanas-email)."
---

# Promo de webinar — kit multicanal

Convierte un solo brief en **todos** los textos para llenar un webinar: emails, página de evento, posts, stories, broadcasts y el mensaje de "estamos en vivo". Todo sale del mismo análisis estratégico para que la promo suene a una sola voz en todos los canales.

---

## Paso 1 — Capturar el brief

Necesitas exactamente 4 variables:

| Variable | Qué es |
|---|---|
| `webinar_title` | Título del webinar tal como se anuncia |
| `webinar_context` | Texto libre: descripción, audiencia, beneficios, fecha, hora, zonas horarias, link de registro, tono, lo que sea |
| `speaker_name` | Quién dicta la sesión |
| `output_language` | `es` o `en`. Por defecto, el idioma en que escribe el usuario |

**No hagas ronda de preguntas.** Si el usuario pegó un brief, extrae lo que puedas y asume el resto con criterio. Solo usa AskUserQuestion si faltan el título o el contexto entero — sin eso no hay copy posible.

Cuando falte un dato duro (link de registro, hora exacta, plataforma), no lo inventes: deja un marcador visible como `[LINK DE REGISTRO]` o `[HORA]` para que el usuario lo complete de un vistazo. Un número inventado en un email que sale a miles de personas es un error caro; un corchete es un minuto de trabajo.

---

## Paso 2 — Definir la estrategia (antes de escribir nada)

Este paso es el que hace que los 9 assets se sientan como una campaña y no como nueve textos sueltos. Hazlo mentalmente y déjalo escrito al inicio del entregable:

1. **Ángulo de promoción** — qué problema resuelve y por qué importa *ahora*. 3-5 líneas.
2. **Deseos de la audiencia** — mínimo 5. Qué quieren conseguir de verdad.
3. **Objeciones** — mínimo 5. "No tengo tiempo", "ya vi algo así", "esto es muy técnico para mí", "seguro es una venta encubierta". Cada asset debe desactivar al menos una.
4. **Tagline central** — una línea corta que se repite (o se parafrasea) en todos los canales. Es lo que da unidad.

Todo lo que escribas después sale de aquí. Si un asset no conecta con un deseo o una objeción de esta lista, sobra.

---

## Paso 3 — Mapa de canales

Cada canal tiene un trabajo distinto. Incluye esta tabla en el entregable, ajustada al caso:

| Canal | Objetivo | Estilo de hook | Urgencia | CTA |
|---|---|---|---|---|
| Email principal | Registros en frío/tibio | Problema o deseo | Media | Registrarme |
| Email comunidad | Asistencia de miembros | Personal, agradecido | Media | Confirmar asistencia |
| Página de evento | Convertir al que ya llegó | Promesa concreta | Baja | Reservar cupo |
| Posts cortos | Alcance | Insight o pregunta | Baja-media | Pedir link / registrarse |
| Stories pre-evento | Recordar y humanizar | Cara, voz, detrás de cámara | Media | Sticker de link |
| LinkedIn largo | Autoridad | Historia o creencia rota | Baja | Registro en el post |
| Broadcast día D | Asistencia | Recordatorio directo | Alta | Entrar aquí |
| Story "empezamos" | Rescatar al distraído | Urgencia pura | Máxima | Unirme ahora |
| Post "en vivo" | Empujar al que dudaba | Anuncio seco | Máxima | Link de entrada |

---

## Paso 4 — Escribir los 9 assets

Escríbelos todos en `output_language`. Antes de empezar lee `references/ejemplos-voz.md`: son piezas reales que ya funcionaron y marcan el tono (directo, cálido, con emojis funcionales, sin relleno corporativo). Imítalas en registro, **no** en contenido.

### 1. Email principal — invitación a la lista
- 3 opciones de asunto · 2 de preheader
- Cuerpo: hook con el dolor o deseo → qué es el webinar y por qué ahora → `speaker_name` con 1-3 líneas de credibilidad → 3-5 aprendizajes concretos en bullets → fecha, hora y formato → **un solo CTA** al link de registro
- Párrafos de 1-3 líneas. Nada de bloques densos.

### 2. Email comunidad — audiencia caliente
- 2 opciones de asunto
- Primera persona, informal, agradecido. Habla de por qué esta sesión le sirve *específicamente* a quien ya está dentro
- 1-2 párrafos + bullets con 3-5 razones + CTA para confirmar asistencia

### 3. Página de evento (Luma / Eventbrite) + recordatorio automático
- Descripción: párrafo hook → 3 bullets de resultados → "¿Para quién es?" muy corto → logística
- Recordatorio automático: 1-3 líneas. Recuerda que ya está registrado, cuándo empieza y dónde entrar

### 4. Posts cortos ×6
- 2 LinkedIn (80-140 palabras) · 2 X/Telegram (máx. 280 caracteres) · 2 grupos de Facebook/comunidades (50-100 palabras, conversacional)
- Cada uno abre con un hook distinto. Seis posts con el mismo arranque no sirven para nada

### 5. Secuencia de Stories pre-evento (5-7)
Por cada story: número · tipo de visual (selfie, slide de texto, screenshot, encuesta, cuenta regresiva) · texto exacto en pantalla · elemento interactivo sugerido.
La secuencia completa presenta tema y speaker, muestra beneficios, desactiva 1-2 objeciones y repite fecha y cómo entrar sin sonar a robot.

### 6. Post largo de LinkedIn (220-400 palabras)
Hook sobre el problema o la creencia equivocada → historia o insight que posiciona a `speaker_name` → transición natural a la invitación → 3-5 bullets de lo que se llevan → fecha, hora y link → CTA claro.

### 7. Broadcast WhatsApp / Telegram — día del evento
Un bloque de texto listo para copiar y pegar. Saludo a la comunidad → recuerda que es hoy con `speaker_name` → 3-4 cosas que van a poder hacer → hora y formato → línea final con el link. Compacto y legible en móvil.

### 8. Story "empezamos ya"
Headline · subline con el webinar y el speaker · línea extra de urgencia o beneficio · texto del botón/sticker. Todo cortísimo, tiene que caber en una pantalla.

### 9. Post de comunidad "estamos en vivo"
Título corto + 1-3 frases de que la sesión de `webinar_title` con `speaker_name` está por empezar + dónde hacer clic. Escaneable en 2 segundos.

---

## Paso 5 — Calendario de publicación

Cierra con una tabla práctica. Infiere la línea de tiempo desde el contexto (o usa 7/3/1 días antes + día del evento):

| Día | Asset | Canal | Objetivo |
|---|---|---|---|
| -7 | Email principal + página de evento | Email, Luma | Registros |
| -5 | Post largo LinkedIn | LinkedIn | Autoridad |
| -3 | Posts cortos | X, grupos | Alcance |
| -2 a -1 | Stories pre-evento | Instagram | Recordatorio |
| -1 | Email comunidad | Email | Asistencia |
| Día D (-3h) | Broadcast | WhatsApp, Telegram | Última llamada |
| Día D (-5min) | Story + post en vivo | Instagram, comunidad | Entrada |

---

## Reglas de escritura

1. Una idea, un CTA por pieza
2. Asuntos de 30-45 caracteres, sentence case, máximo 1 emoji, sin MAYÚSCULAS ni palabras spam
3. Emojis como señales de lectura (📅 🔗 🎯), no como decoración
4. Concreto sobre abstracto: "monta un RAG de punta a punta" gana a "aprende sobre IA"
5. Gana el "tú" sobre el "nosotros"
6. Repite fecha, hora y zonas horarias en cada asset del día del evento — es el dato que más se pierde
7. Nunca inventes cifras, testimonios ni credenciales del speaker. Si no las tienes, usa `[CREDENCIAL]`
8. Que suene a una persona escribiendo, no a un departamento de marketing

---

## Entrega

**Un solo archivo `.md`** en la carpeta de salida, nombrado `promo-[slug-del-webinar].md`, con esta estructura:

```
# Promo — [webinar_title]

## Estrategia
Ángulo · Deseos · Objeciones · Tagline central

## Mapa de canales
[tabla]

## 1. Email principal
## 2. Email comunidad
## 3. Página de evento + recordatorio
## 4. Posts cortos
## 5. Stories pre-evento
## 6. Post largo de LinkedIn
## 7. Broadcast WhatsApp/Telegram
## 8. Story "empezamos ya"
## 9. Post "en vivo"

## Calendario de publicación
[tabla]
```

Cada asset va listo para copiar y pegar, sin instrucciones intercaladas dentro del copy. Las notas para el usuario (si las hay) van como línea en cursiva debajo del bloque, nunca dentro.

Después de entregar el archivo, no repitas el contenido en el chat. Un resumen de una línea basta.
