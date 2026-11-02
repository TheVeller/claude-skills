---
name: video-de-launch-de-producto-borrador
description: >-
  Usar cuando se pide planear, construir y criticar un video corto de
  lanzamiento (20-60 s) de un producto de software en el que el producto hace su
  acción en pantalla. No usar para talking head, limpieza de footage, recaps de
  evento ni para empaquetar un master ya terminado.
---
# Video de launch de producto (borrador)

Basado en el skill `launch-video` de crafter-station/design-skills, del que solo se leyó el SKILL.md (pegado por el usuario). No se leyeron goldenset, taste.md, build.md ni analyze.py: lo que dependa de ellos queda marcado como pendiente. Estado del formato: Propuesto, no aprobado.

## Idea
Un film de launch es una idea, el producto haciendo su verbo, cortes sobre música y un cierre sostenido con la marca.

## Pasos
0. Bucle de trabajo: mostrar un still o tira de frames antes del render completo; comparar contra 2 referencias del mismo arquetipo; tras cada render, pasar el video a un modelo distinto para una crítica dura (frames y archivos más las notas del dueño, nunca la conclusión propia); el ojo del dueño es la puerta; para decisiones de movimiento (cierre, transiciones) armar 3-5 variantes en una página HTML en bucle y dejar que el dueño elija.
1. Conocer el producto desde su código: README, landing y fuente. Anotar el verbo y su atajo, el feedback exacto del app (sonido, flash, toast, duraciones y easings con archivo:línea), el copy real de la landing y la marca (tokens, tipografías, logo, mascota, assets). Si la landing ya simula el producto, reutilizar su markup. Listo cuando: brief corto con verbo, feedback citado, copy y fuentes de UI.
2. Elegir un solo arquetipo y dos referencias. No mezclar arquetipos en menos de 60 s. Si es «objeto como personaje», nombrar el verbo que el personaje ejecuta en pantalla. (El catálogo de arquetipos y referencias está en taste.md y el goldenset del repo: pendiente de leer.)
3. Shot list (tiempo, toma, tipo, movimiento, sonido, por qué) y esperar la aprobación del dueño. Sin código antes.
4. Construir el escenario a pantalla completa con UI real (markup de la landing, capturas reales o simulación medida sobre un screenshot real). Nunca los screenshots personales del dueño. Cada ventana entera y centrada; el texto en su propia tarjeta o sobre fondo vacío, nunca sobre la UI que explica.
5. Sincronizar con la música: elegir la pista primero, hallar su pulso, poner todo corte después del primer downbeat sobre la grilla. Una tarjeta con una frase dura mínimo 2 s. (Medición con analyze.py: pendiente; sin ese script, medir cortes con ffmpeg y marcarlo como medición propia.)
6. Cierre: la marca es un beat de personaje, no un fundido. Nada aparece de golpe; luego la línea «by …» con el logo real del autor y la URL. Retención total del cierre de 4 a 6 s. Listo cuando el dueño eligió el movimiento de las variantes y el último frame muestra cada glifo entero.
7. Medir y comparar: duración, cortes por minuto, toma mediana, cortes por cuarto, loudness, sincronía con el beat, con hoja de contacto junto a las 2 referencias. Cada número con su fuente.
8. Cerrar: dejar registro de versiones, comentarios del dueño y lo que cambió; anotar fricciones.

## Reglas duras
- Sin código antes de aprobar el shot list.
- El producto hace su verbo en pantalla; una cara que solo mira no es un personaje.
- UI, feedback y copy reales; las simulaciones se miden sobre capturas reales.
- Nunca mostrar datos privados del dueño (timeline, chats, cuentas).
- Pantalla completa, componentes enteros, nada cortado.
- Cortes en el beat; tarjetas con tiempo para leerse.
- Desactivar `backdrop-filter` en renders headless: puede cerrar Chrome en ciertos frames.
- No publicar ni programar sin un sí explícito del dueño por pieza y cuenta.

## Referencia observada (un video, no el goldenset)
Un launch de 40 s en 16:9 con 7 beats: gancho con personaje, función central con atajo, demostración con montaje, búsqueda, objeción de privacidad, función con agentes y cierre con logo. Una sola idea de texto por escena, cortes secos, serif itálica con subrayado de acento sobre fondo beige y un solo color de acento. El audio no se pudo analizar.

## Pendiente de verificar
Contenido de taste.md, build.md, goldenset y analyze.py; motor de render (Remotion, HTML grabado o HyperFrames) y su prueba de captura de producto de punta a punta; si el formato lleva música o voz.
