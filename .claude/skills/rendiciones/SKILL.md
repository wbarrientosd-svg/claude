---
name: rendiciones
description: Agente de rendiciones de gastos de Waldemar para Distribuidora Catán. Toma los movimientos de sus cuentas bancarias (avisos en Gmail y cartolas), los concilia contra la planilla "Rendiciones Waldemar 2026.xlsx" en Drive, clasifica cada gasto según el historial y genera las filas listas para la hoja del mes. Usar cuando Waldemar pida rendir gastos, actualizar/llenar la planilla de rendiciones, conciliar gastos con el banco, o "pasar los gastos a la planilla".
---

# Rendiciones de gastos — Distribuidora Catán

Objetivo: que cada gasto de empresa que Waldemar paga desde sus cuentas quede registrado en la
hoja mensual de la planilla, con su clasificación correcta, **sin duplicados y sin colar gastos personales**.

## Fuentes

| Qué | Dónde | Cómo |
|---|---|---|
| Planilla | Drive, ID `1nqor7iWPW-dURMRFdm873kAQRTxjgNCf` ("Rendiciones Waldemar 2026.xlsx", dueño: contador Luis Riquelme) | `mcp__Google_Drive__download_file_content` → guarda un .xlsx local |
| Avisos bancarios | Gmail | `mcp__Gmail__search_threads` + `mcp__Gmail__get_message` |
| Cartolas (PDF) | Gmail: `bcimail@bci.cl` "Cartola Cuenta Corriente", `cartola@itau.cl` | `mcp__Gmail__download_gmail_attachment` → leer con el skill `pdf` (pueden venir con clave: pedírsela a Waldemar) |
| Reglas de clasificación | `reglas.md` (junto a este archivo) | Leer siempre antes de clasificar |

Remitentes de avisos conocidos: `contacto@bci.cl` (débito y transferencias), `transferencias@bci.cl`,
`mensajeria@santander.cl`, `serviciodetransferencias@bancochile.cl`, `notificaciones@cl.bancofalabella.com`,
`contacto@servipag.cl`.

**Ojo — cobertura:** los avisos de Gmail cubren sobre todo la cuenta **personal BCI** de Waldemar.
Los pagos grandes de empresa (arriendos, imposiciones, honorarios, Servipag, SII, Mercado Pago, Scotiabank)
normalmente **no generan aviso** y solo aparecen en las cartolas. Si en el mes no aparecen los gastos
recurrentes (arriendos de los 4 locales, imposiciones, contabilidad), decirlo y pedir la cartola
(PDF o Excel) de Santander / BCI empresa / Mercado Pago / Scotiabank. No inventar movimientos.
Lo más eficiente: que Waldemar descargue desde BCI Pyme / Mercado Pago / Santander las cartolas del mes en Excel y las
deje en Drive (o las adjunte); se leen con `download_file_content`. En una sesión del escritorio con Claude in Chrome se
pueden descargar desde la web del banco, **solo lectura**: nunca hacer transferencias, pagos ni cambios de datos, y el
login/2FA (Bci Pass, clave dinámica) lo hace Waldemar.

## Flujo

1. **Período.** Por defecto el mes en curso (zona horaria Santiago). Si Waldemar indica otro, usarlo.
2. **Planilla.** Descargar la versión actual de Drive y guardarla en el scratchpad (`planilla.xlsx`).
   Mostrar cuántas filas tiene ya la hoja del mes (`scripts/rendiciones.py existentes --xlsx planilla.xlsx --mes N`).
3. **Movimientos.** Buscar avisos del período, p. ej.
   `after:2026/11/01 before:2026/12/01 from:(bci.cl OR santander.cl OR bancochile.cl OR bancofalabella.com OR servipag.cl OR mercadopago.com OR scotiabank.cl) -subject:(cartola)`.
   Las vistas de búsqueda no traen el cuerpo: leer cada mensaje con `get_message` en `PLAIN_TEXT`
   (el `snippet` corta antes del comercio). Con muchos correos, delegar la extracción a un subagente.
   Sumar las cartolas que Waldemar entregue o que lleguen adjuntas.
   Guardar todo en `movs.json`, una entrada por movimiento:
   `{"message_id","fecha":"DD/MM/YYYY","banco","tipo","monto","contraparte","cuenta_origen","mensaje","comprobante"}`
   con `tipo` ∈ `compra_debito | compra_credito | transferencia_enviada | transferencia_recibida | transferencia_programada | traspaso_propio | pago_servicio | otro`.
4. **Conciliar.** `python3 scripts/rendiciones.py conciliar --xlsx planilla.xlsx --movs movs.json --out pendientes.json`
   - Marca como *ya rendido* lo que coincide en monto exacto y fecha ±4 días con una fila de cualquier hoja.
   - Excluye abonos recibidos y traspasos entre cuentas propias.
5. **Clasificar** cada pendiente con `reglas.md`, en tres grupos:
   - **Empresa (alta confianza):** coincide con un proveedor/patrón conocido → fila completa.
   - **Dudoso:** podría ser de empresa (p. ej. Uber, Copec, estacionamiento, transferencias a personas desconocidas) → proponer fila y preguntar.
   - **Personal:** colegio, barbería, botillería, supermercado, compras familiares → no rendir, solo listar.
6. **Confirmar con Waldemar.** Mostrar una tabla corta por grupo (fecha, monto, contraparte, clasificación propuesta)
   y pedirle que confirme/corrija. **Nunca escribir filas sin su confirmación.** Lo que corrija, agregarlo a `reglas.md`.
7. **Generar.** Escribir las filas confirmadas en `filas.json` (claves: `razon_social, fecha, tipo_documento, monto,
   estado, observaciones, metodo_pago, institucion, local, area`; opcionales: `rut, n_documento, neto, iva, fuente, confianza, nota`) y correr:
   `python3 scripts/rendiciones.py generar --filas filas.json --mes N --out Rendiciones_<Mes>_<Año>.xlsx --planilla planilla.xlsx --out-planilla "Rendiciones Waldemar 2026 (actualizada).xlsx"`
   El script valida que los valores calcen con las listas desplegables de la planilla y aborta si no.
8. **Entregar.** Waldemar tiene permiso de edición (writer) sobre la planilla, pero el conector de Drive solo crea archivos
   nuevos o cambia metadatos: no puede sobrescribir el contenido de un .xlsx existente. Por eso:
   - Subir la copia completa actualizada a Drive y pedirle a Waldemar que la cargue sobre el original con
     Drive → clic derecho en la planilla → "Administrar versiones" → "Subir nueva versión" (conserva link e ID).
     Si la sesión tiene navegador (Claude in Chrome en el equipo de Waldemar), puede hacerse ahí directamente.
   - Además, subir `Rendiciones_<Mes>_<Año>.xlsx` (solo las filas nuevas) a Drive de Waldemar con `mcp__Google_Drive__create_file`
     (`disableConversionToGoogleType: true`) y darle el link.
   - Ofrecer enviar la propuesta a Luis (contador) por correo **solo si Waldemar lo pide** (borrador con `create_draft`).
9. **Resumen final:** total rendido del mes, n° de filas nuevas, pendientes de respaldo (facturas/boletas faltantes)
   y movimientos personales excluidos.

## Reglas duras

- No registrar transferencias recibidas ni traspasos entre cuentas propias como gasto.
- No inventar RUT, folio ni n° de factura; dejarlos vacíos si no vienen en un documento.
- Montos en CLP enteros; fechas como fecha real (no texto).
- Ante la duda personal/empresa: preguntar.
- Los datos bancarios son privados: no enviarlos a servicios externos ni a terceros sin pedido explícito.
