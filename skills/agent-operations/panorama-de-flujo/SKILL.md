---
name: panorama-de-flujo
description: >-
  Usar cuando el usuario pide la visión completa de un flujo o sistema que se
  está construyendo (contenido, ventas, distribución, un OS): flujograma,
  owners, tooling, links, estado y decisiones pendientes, antes de que alguien
  lo tome y lo ejecute.
---
# Panorama de un flujo en construcción

Objetivo: dar al usuario, en una sola entrega de lectura, el mapa completo de un flujo y quién lo opera, para que decida y luego se ejecute. Solo lectura: no editar bots, rutinas ni bases ajenas, no enviar nada externo.

## Pasos
1. **Delimita el flujo.** Nombre, objetivo, marcas o clientes que cubre y qué se considera "terminado".
2. **Recolecta fuentes reales.** Notion (bases, páginas, relaciones), Lovable y GitHub (apps y repos), vault y archivos de estado de la computadora, transcripts y chats de los bots, rutinas existentes, Drive. Todo dato con su fuente. Nada inventado: si no se puede verificar, queda marcado ⚠️.
3. **Arma las etapas.** Insumos, Estrategia, Formatos o definición, Producción, Aprobación humana (A3), Distribución, Medición y aprendizaje, Transversal (rutinas, orquestación, creación de bots).
4. **Mapea cada nodo.** Estado (vivo, parcial, pendiente, bloqueado), owner (bot o persona), tooling (Notion, Drive, NotebookLM, app custom, API), link exacto, y rutina asociada si existe.
5. **Dibuja un diagrama mermaid** `flowchart TB` con un subgraph por etapa y clases de color por estado: verde vivo, amarillo parcial, gris punteado pendiente, rojo bloqueado, azul grueso para la puerta humana. Flecha continua para flujo, punteada para retroalimentación.
6. **Entrega** en este orden: diagrama, leyenda, tabla de owners/tooling/links, rutinas que existen, decisiones pendientes del usuario en orden, siguiente paso recomendado, y lista de lo no verificado. Español, markdown legible con títulos con emoji y bullets cortos.
7. **Pregunta** si se deja como Página para ir actualizándola. Si el flujo cambia después, se edita la misma Página.

## Reglas
- Todo bot pertenece a un equipo y su manager. Verifica que cada bot del flujo esté en el grupo de su división.
- Cada bot puede tener espacio en Notion, Drive, un NotebookLM y apps custom: inclúyelos en la tabla.
- Nada sale a publicación sin el sí explícito del usuario.
- Si el flujo cambia algo del organigrama, el inventario de bots o los sistemas publicados, anótalo y avisa al responsable del inventario.
