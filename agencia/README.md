# Aurora — Agencia Autónoma de Marketing y Contenido

Agencia de marketing y creación de contenido operada por agentes de IA, con Waldemar como dueño y aprobador final.

## Cómo se usa
- En Claude Code: `/agencia <encargo>` — Aurora (directora) recibe el encargo, lo divide y lo delega a los subagentes.
- Como agente principal: `claude --agent aurora`.
- Un área puntual: pedir "usa a Pluma para…" (o cualquier otro nombre del equipo).

## Equipo
| Agente | Área | Archivo |
|---|---|---|
| **Aurora** | Dirección general y orquestación | `.claude/agents/aurora.md` |
| **Atlas** | Estrategia e investigación de mercado | `.claude/agents/atlas.md` |
| **Pluma** | Copywriting y contenido escrito | `.claude/agents/pluma.md` |
| **Prisma** | Dirección de arte y diseño | `.claude/agents/prisma.md` |
| **Lumen** | Video y producción audiovisual | `.claude/agents/lumen.md` |
| **Eco** | Redes sociales y comunidad | `.claude/agents/eco.md` |
| **Raíz** | SEO y web | `.claude/agents/raiz.md` |
| **Chispa** | Publicidad pagada (performance) | `.claude/agents/chispa.md` |
| **Sextante** | Analítica y reportes | `.claude/agents/sextante.md` |
| **Puente** | Ventas y captación de clientes | `.claude/agents/puente.md` |
| **Ancla** | Control de calidad y operaciones | `.claude/agents/ancla.md` |

## Estructura
- `PLAN_DE_NEGOCIO.md` — modelo de negocio, servicios, precios y hoja de ruta.
- `OPERACION.md` — flujo de trabajo, reglas de autonomía y aprobaciones.
- `videos/` — registro de videos fuente y las ideas extraídas de cada uno.
- `clientes/<cliente>/` — ficha de marca y contexto de cada cliente.
- `briefs/` — encargos abiertos (uno por archivo, `AAAA-MM-DD-cliente-tema.md`).
- `entregables/` — piezas terminadas y aprobadas por Ancla.
- `reportes/` — reportes de resultados de Sextante.
