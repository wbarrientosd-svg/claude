# Operación de la agencia

## Flujo estándar de un encargo
1. **Ingreso.** Aurora recibe el encargo y crea un brief en `briefs/AAAA-MM-DD-cliente-tema.md` con el objetivo, el público, el canal, la fecha y la referencia a la ficha del cliente.
2. **Estrategia.** Atlas define el ángulo, los mensajes clave y los referentes.
3. **Producción en paralelo.** Pluma escribe, Prisma diseña, Lumen produce video, Raíz optimiza para búsqueda y Chispa arma campañas, según lo que pida el brief.
4. **Distribución.** Eco arma el calendario y adapta cada pieza a su red.
5. **Control de calidad.** Ancla revisa la marca, la ortografía, los datos, las afirmaciones legales y el formato. Si algo falla, la pieza vuelve a su autor.
6. **Aprobación.** Aurora presenta a Waldemar un resumen de las piezas listas.
7. **Medición.** Sextante reporta los resultados y Atlas ajusta la estrategia del ciclo siguiente.

## Reglas de autonomía
Los agentes **pueden hacer solos**: investigar, redactar, diseñar, planificar, crear borradores, guardar archivos en `agencia/` y proponer acciones.

Los agentes **siempre piden aprobación de Waldemar** antes de:
- publicar en cualquier red o sitio, o cambiar algo en Shopify;
- enviar correos o mensajes a clientes o prospectos;
- gastar dinero (pauta, herramientas o contrataciones);
- firmar o comprometer precios, plazos o resultados.

## Reglas de contenido
- No inventar cifras, testimonios ni reseñas. Todo dato lleva su fuente o queda marcado como `[POR CONFIRMAR]`.
- No usar marcas, logos ni imágenes de terceros sin derechos.
- Escribir en español de Chile, salvo que el cliente pida otra cosa.
- Seguir siempre `clientes/<cliente>/marca.md`. Si no existe, Atlas la crea primero.

## Nombres de archivo
- Briefs: `briefs/2026-11-23-catan-campana-verano.md`
- Entregables: `entregables/<cliente>/<fecha>-<pieza>.md` (más los recursos asociados)
- Reportes: `reportes/<cliente>/<AAAA-MM>.md`
