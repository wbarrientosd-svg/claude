# Instalación única del agente de rendiciones (≈10 minutos, mejor desde el computador)

## 1. Puente que escribe en la planilla (Apps Script)

1. Entra a <https://script.google.com> con **wbarrientosd@gmail.com** → **Nuevo proyecto** → nómbralo "Puente Rendiciones".
2. ⚙️ *Configuración del proyecto* → marca **"Mostrar el archivo de manifiesto appsscript.json"**.
3. En el editor reemplaza `Código.gs` por el contenido de `Code.gs` y `appsscript.json` por el de este directorio. Guarda.
4. Arriba elige la función **`crearToken`** → **Ejecutar** → autoriza los permisos (Drive y Hojas de cálculo de tu cuenta).
   En *Registro de ejecución* aparece `TOKEN: ...` → cópialo.
5. **Implementar → Nueva implementación → Aplicación web**
   - Ejecutar como: **Yo (wbarrientosd@gmail.com)**
   - Quién tiene acceso: **Cualquier usuario**
   → **Implementar** → copia la **URL de la aplicación web** (termina en `/exec`).
6. Prueba: abre en el navegador `URL?token=TU_TOKEN` → debe responder `{"ok":true,"archivo":"Rendiciones Waldemar 2026.xlsx",...}`.

Qué hace: recibe las filas que tú apruebas y las agrega al final de la hoja del mes en **el mismo archivo**
(mismo link e ID; Luis lo sigue viendo igual). Cada escritura deja una versión en *Administrar versiones* de Drive,
así que cualquier error se puede revertir. Solo escribe en esa planilla, solo agrega filas, omite duplicados
(misma fecha y monto) y no hace nada sin el token.

## 2. Guardar la URL y el token en el entorno de Claude Code

En claude.ai/code → tu entorno → **Variables de entorno**, agrega:

```
RENDICIONES_WEBAPP_URL=https://script.google.com/macros/s/.../exec
RENDICIONES_TOKEN=el_token_del_paso_4
```

El entorno también debe permitir los hosts `script.google.com` y `script.googleusercontent.com`
(el agente te pedirá aprobarlo la primera vez).

## 3. Reenvío de avisos bancarios de la empresa

Los avisos de las cuentas de empresa llegan a **catandistribuidora@gmail.com**, que el agente no puede leer directamente.
En Gmail de catandistribuidora (versión web):

1. ⚙️ → *Ver toda la configuración* → **Reenvío y correo POP/IMAP** → *Agregar dirección de reenvío* → `wbarrientosd@gmail.com` → confirma el código que llega a wbarrientosd.
2. Crea un filtro: **De:** `bci.cl OR santander.cl OR mercadopago.com OR mercadopago.cl OR scotiabank.cl OR servipag.cl OR bancochile.cl`
   → *Reenviar a* `wbarrientosd@gmail.com`. (Opcional: marca también *Aplicar el filtro a conversaciones coincidentes* no reenvía lo antiguo; para meses pasados, reenvía las cartolas a mano.)

## 4. Uso desde el teléfono

- **Mandar un respaldo:** foto de la boleta/factura → envíala a `wbarrientosd@gmail.com` con asunto **rendicion**
  y, si quieres, una línea de contexto ("combustible camioneta", "materiales local Maipú", "pagado en efectivo").
  También puedes reenviar facturas electrónicas con ese asunto.
- **Rendir:** app Claude → **Code** → nueva sesión en el repo `wbarrientosd-svg/claude` → escribe
  "rinde los gastos de noviembre" (o adjunta la foto ahí mismo). El agente arma la propuesta, tú respondes
  "ok" o corriges, y escribe en la planilla.
