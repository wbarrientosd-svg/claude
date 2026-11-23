# Reglas de clasificación de rendiciones

Derivadas del historial de "Rendiciones Waldemar 2026.xlsx" (enero–octubre 2026).
Cuando Waldemar corrija una clasificación, **agregar o ajustar la regla aquí** para que la próxima vez salga bien.

## Valores permitidos (listas desplegables de la planilla)

| Campo | Valores |
|---|---|
| Tipo De Documento | Boleta, Factura, Otro |
| Estado Pago | Rendido, Pendiente |
| Metodo De Pago | Transferencia, Servipag, Efectivo, Debito, Otro, Credito |
| Institucion Financiera | Santander, BCI, Mercado Pago, Caja, Otros, SCOTIABANK |
| Local | Ancahual, Maipu, Las Flores, Los Valles, Todas las Tiendas, Mercado Publico |
| Centro de Costo Area | Gerencia y Administracion, Operaciones, Logistica, Ventas, Marketing |

Escribir los valores **exactamente** así (mayúsculas incluidas). El historial tiene variantes
("REndido", "TRAnsferencia", "catanweb"): no repetirlas.

## Correspondencia medio de pago → columnas

| Origen del movimiento | Metodo De Pago | Institucion Financiera |
|---|---|---|
| Aviso "uso de tu tarjeta de débito" BCI | Debito | BCI |
| Aviso "Transferencia de Fondos" BCI (enviada) | Transferencia | BCI |
| Comprobante transferencia Santander (enviada) | Transferencia | Santander |
| Pago en línea Servipag (desde Santander) | Servipag | Santander |
| PAC / cargo automático Santander | Debito | Santander |
| Cartola Mercado Pago (débito/QR) | Debito | Mercado Pago |
| Transferencia desde Mercado Pago | Transferencia | Mercado Pago |
| Cartola Scotiabank (REDCOMPRA / TEF) | Debito / Transferencia | SCOTIABANK |
| Tarjeta de crédito | Credito | banco emisor |

## Qué NO es gasto de la empresa (no rendir, o dejar "Pendiente" para consultar)

- **Movimientos de las cuentas personales de Waldemar** (avisos dirigidos solo a wbarrientosd@gmail.com):
  confirmado por Waldemar que son casi todos personales. Solo se rinden si él manda el respaldo con asunto
  "rendicion" o lo indica expresamente. Las cuentas de empresa notifican a catandistribuidora@gmail.com.
  Ejemplos de nov-2026 confirmados personales: Karin Gutiérrez, Vanessa Reyes, Jaime Carbonell, Maritza Púa,
  Norma Domínguez, Uber, Copec, botillería, barbería.
- Transferencias **recibidas** (abonos) y traspasos entre cuentas propias de Waldemar.
- Gastos familiares/personales evidentes: colegio (Liceo Mater Purissima, "polera mater",
  Syscol), supermercado del hogar, salud personal, compras personales en MercadoLibre.
  En septiembre se registraron como "COMPRA PERSONAL PAGADA CON TARJETA PERSONAL" con
  estado Pendiente — usar ese criterio solo si Waldemar pide dejarlo registrado.
- Avisos de notificaciones automáticas de marketing de bancos.
- En caso de duda: **preguntar**, nunca suponer que es gasto de empresa.

## Proveedores y gastos recurrentes conocidos

| Contraparte (como aparece en el banco) | Observaciones típicas | Tipo Doc | Local | Área |
|---|---|---|---|---|
| Octavio Leon Ortiz | Arriendo Ancahual MES AÑO / luz o agua local Ancahual | Otro | Ancahual | Operaciones |
| Yasna Godoy | Arriendo local Las Flores MES AÑO | Otro | Las Flores | Operaciones |
| Francisco Ortiz Aravena | Arriendo Los Valles MES AÑO | Otro | Los Valles | Operaciones |
| Graciela Bustamante | Gastos comunes Los Valles | Otro | Los Valles | Operaciones |
| Edith Jeannette Dominguez Sepulveda | Arriendo local Vespucio Maipú MES AÑO | Otro | Maipu | Operaciones |
| Luis Moises Riquelme | "Imposiciones MES AÑO" o "Honorarios contabilidad" (según monto/mensaje) | Otro | Todas las Tiendas | Gerencia y Administracion |
| Eduardo Gonzalez (RUT 13.470.109-9) | Abono comisiones ventas Mercado Público MES AÑO | Otro | Mercado Publico | Ventas |
| Valentina Contreras Pacheco | Honorarios marketing MES AÑO | Boleta | Todas las Tiendas | Marketing |
| Medialab Spa | Honorarios diseño gráfico MES AÑO | Otro | Todas las Tiendas | Marketing |
| Matias Soto | Honorarios asesoría e-commerce | Boleta | Todas las Tiendas | Marketing |
| Gerente de Finanzas SpA | Servicios CFO externo | Factura | Todas las Tiendas | Gerencia y Administracion |
| Fernando Rodriguez | Mano de obra reparación/remodelación (indicar local) | Otro | según local | Gerencia y Administracion |
| Waldemar Barrientos (sueldo) | SUELDO WALDEMAR BARRIENTOS / Retiro | Otro | Todas las Tiendas | Gerencia y Administracion |
| LICI | Mensualidad plataforma LICI uso Mercado Público | Factura | Mercado Publico | Operaciones |
| Copec / JVL Contingencia / Comercial Santa... / Juan Alejandro Villanueva | Combustible camioneta Honda CLYJ42 | Factura (Copec: Otro) | Todas las Tiendas | Logistica |
| Autoplanet / Soc. Comercializadora de Repuestos / LB Motors / MercadoLibre repuestos | Repuestos camioneta Honda CLYJ42 | Factura | Todas las Tiendas | Logistica |
| Invi Ltda | Mantención camioneta Honda CLYJ42 | Factura | Todas las Tiendas | Logistica |
| Servipag – TAG (Ruta 78, Vespucio Sur/Norte, Autopista Central, Sur) | TAG + nombre autopista | Otro | Todas las Tiendas | Logistica |
| Servipag / Entel – Internet | Internet local X | Otro/Factura | local que corresponda | Operaciones |
| Servipag – Movistar celulares | Teléfonos Movistar | Factura | Todas las Tiendas | Operaciones |
| Servipag – Luz/Agua Vespucio Maipú | Luz/Agua local Vespucio Maipú | Boleta/Otro | Maipu | Operaciones |
| PAC Zenit | Seguro vehículos Catán | Factura | Todas las Tiendas | Logistica |
| PAC Seg. Hogar | Seguro local Ancahual | Factura | Ancahual | Gerencia y Administracion |
| MERPAGO*VERISURE | Verisure local (Ancahual/Maipú) | Otro | según local | Gerencia y Administracion |
| Pago en línea S.I.I. | F29 SII MES / Pago SII | Otro | Todas las Tiendas | Gerencia y Administracion |
| Google Ads | Campañas Google Ads | Otro | Todas las Tiendas | Marketing |
| Shopify | Plan Shopify / página web | Otro | Todas las Tiendas | Marketing |
| Google Workspace | Plan Google Workspace | Factura | Todas las Tiendas | Marketing |
| Defontana | ERP Defontana | Factura | Todas las Tiendas | Gerencia y Administracion |
| Nubox | Sistema RRHH Nubox | Factura | Todas las Tiendas | Gerencia y Administracion |
| Estacionamiento (Señal Parking, etc.) | Gasto estacionamiento | Boleta | Todas las Tiendas | Gerencia y Administracion |
| Bluexpress / Azul Punto | Pago flete Bluexpress Mercado Público | Boleta | Mercado Publico | Operaciones |
| Uber | Traslado Uber Waldemar Barrientos | Otro | Todas las Tiendas | Gerencia y Administracion |

## Convenciones de redacción

- **Razón Social Cliente**: nombre del comercio o destinatario tal como aparece en el banco
  (p. ej. "Transferencia enviada a Octavio leon ortiz", "copec s.a").
- **Observaciones**: en qué se gastó + mes al que corresponde + n° de factura/boleta si se conoce
  (ej. "Arriendo Ancahual noviembre 2026", "combustible camioneta honda CLYJ42").
- **RUT** y **N° Documento**: solo si salen del documento (factura/boleta); no inventar.
- **Fecha Emisión**: fecha del movimiento bancario.
- **Estado Pago**: "Rendido" para gastos de empresa confirmados; "Pendiente" si falta respaldo o confirmación.
- **Local**: el local específico si el gasto es de un local; "Todas las Tiendas" si es transversal.
