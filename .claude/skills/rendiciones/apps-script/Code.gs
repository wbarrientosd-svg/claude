/**
 * Puente de escritura para la planilla "Rendiciones Waldemar 2026.xlsx".
 *
 * Corre con la cuenta de Waldemar (editor del archivo). Recibe filas aprobadas por el
 * agente de rendiciones y las agrega al final de la hoja del mes, conservando el archivo
 * original (mismo ID y link, queda una nueva versión en el historial de Drive).
 *
 * Proceso: xlsx -> Google Sheet temporal -> agrega filas -> exporta xlsx -> reemplaza
 * el contenido del archivo original -> borra el temporal. Es el mismo ciclo que usa
 * Google Sheets al editar un .xlsx en "modo Office".
 *
 * Seguridad: solo escribe en PLANILLA_ID, solo agrega filas (nunca borra ni modifica),
 * exige el TOKEN guardado en Propiedades del script y omite duplicados (misma fecha y monto).
 */

const PLANILLA_ID = '1nqor7iWPW-dURMRFdm873kAQRTxjgNCf';
const MESES = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto',
  'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'];
const XLSX = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet';

// Clave del JSON -> encabezado normalizado de la planilla (sirve para formato nuevo y antiguo).
const CAMPOS = {
  rut: ['rut cliente'],
  razon_social: ['razon social cliente'],
  fecha: ['fecha emision'],
  fecha_venc: ['fecha vencimiento'],
  tipo_documento: ['tipo de documento'],
  n_documento: ['n documento', 'n factura'],
  neto: ['monto neto'],
  iva: ['iva'],
  monto: ['monto total'],
  estado: ['estado pago'],
  observaciones: ['observaciones'],
  metodo_pago: ['metodo de pago'],
  institucion: ['institucion financiera'],
  local: ['local'],
  centro_costo: ['centro de costo'],
  area: ['centro de costo area'],
};

const LISTAS = {
  tipo_documento: ['Boleta', 'Factura', 'Otro'],
  estado: ['Rendido', 'Pendiente'],
  metodo_pago: ['Transferencia', 'Servipag', 'Efectivo', 'Debito', 'Otro', 'Credito'],
  institucion: ['Santander', 'BCI', 'Mercado Pago', 'Caja', 'Otros', 'SCOTIABANK'],
  local: ['Ancahual', 'Maipu', 'Las Flores', 'Los Valles', 'Todas las Tiendas', 'Mercado Publico'],
  area: ['Gerencia y Administracion', 'Operaciones', 'Logistica', 'Ventas', 'Marketing'],
};

function doGet(e) {
  const p = (e && e.parameter) || {};
  if (!tokenValido_(p.token)) return json_({ ok: false, error: 'token inválido' });
  const f = DriveApp.getFileById(PLANILLA_ID);
  return json_({ ok: true, archivo: f.getName(), modificado: f.getLastUpdated() });
}

function doPost(e) {
  let body;
  try {
    body = JSON.parse(e.postData.contents);
  } catch (err) {
    return json_({ ok: false, error: 'JSON inválido' });
  }
  if (!tokenValido_(body.token)) return json_({ ok: false, error: 'token inválido' });
  const lock = LockService.getScriptLock();
  if (!lock.tryLock(60000)) return json_({ ok: false, error: 'otra escritura en curso, reintentar' });
  try {
    return json_(agregarFilas_(Number(body.mes), body.filas || [], !!body.simular));
  } catch (err) {
    return json_({ ok: false, error: String(err && err.message || err) });
  } finally {
    lock.releaseLock();
  }
}

function agregarFilas_(mes, filas, simular) {
  if (!(mes >= 1 && mes <= 12)) throw new Error('mes inválido');
  if (!filas.length) throw new Error('sin filas');
  const errores = validar_(filas);
  if (errores.length) return { ok: false, error: 'validación', detalles: errores };

  const original = DriveApp.getFileById(PLANILLA_ID);
  const versionAntes = original.getLastUpdated().getTime();
  const tmp = Drive.Files.create(
    { name: 'tmp-rendiciones-' + Date.now(), mimeType: 'application/vnd.google-apps.spreadsheet' },
    original.getBlob());
  try {
    const ss = SpreadsheetApp.openById(tmp.id);
    const nombre = ('0' + mes).slice(-2) + ' ' + MESES[mes - 1];
    const sh = ss.getSheetByName(nombre);
    if (!sh) throw new Error('no existe la hoja ' + nombre);

    const datos = sh.getDataRange().getDisplayValues();
    const filaEnc = datos.findIndex(r => r.some(c => norm_(c) === 'razon social cliente'));
    if (filaEnc < 0) throw new Error('no encontré encabezados en ' + nombre);
    const enc = datos[filaEnc].map(norm_);
    const col = {};
    Object.keys(CAMPOS).forEach(k => {
      const i = enc.findIndex(h => CAMPOS[k].indexOf(h) >= 0);
      if (i >= 0) col[k] = i;
    });
    ['razon_social', 'fecha', 'monto'].forEach(k => {
      if (col[k] === undefined) throw new Error('falta columna ' + k + ' en ' + nombre);
    });

    // Última fila con datos reales (razón social, fecha o monto) bajo el encabezado.
    let ultima = filaEnc;
    for (let r = filaEnc + 1; r < datos.length; r++) {
      if (datos[r][col.razon_social] || datos[r][col.monto]) ultima = r;
    }
    // Duplicados ya presentes: fecha + monto.
    const existentes = {};
    const valores = sh.getDataRange().getValues();
    for (let r = filaEnc + 1; r <= ultima; r++) {
      const m = aMonto_(valores[r][col.monto]);
      const f = aFecha_(valores[r][col.fecha]);
      if (m && f) existentes[clave_(f, m)] = true;
    }

    const ancho = enc.length;
    const nuevas = [], omitidas = [];
    filas.forEach(f => {
      const fecha = aFecha_(f.fecha), monto = aMonto_(f.monto);
      if (existentes[clave_(fecha, monto)]) { omitidas.push(f); return; }
      existentes[clave_(fecha, monto)] = true;
      const fila = new Array(ancho).fill('');
      Object.keys(col).forEach(k => {
        let v = f[k];
        if (v === undefined || v === null) return;
        if (k === 'fecha' || k === 'fecha_venc') v = aFecha_(v) || '';
        else if (k === 'monto' || k === 'neto' || k === 'iva') v = aMonto_(v);
        fila[col[k]] = v;
      });
      nuevas.push(fila);
    });

    const resumen = {
      ok: true, hoja: nombre, agregadas: nuevas.length, omitidas_duplicadas: omitidas.length,
      desde_fila: ultima + 2, hasta_fila: ultima + 1 + nuevas.length, simulado: simular,
    };
    if (simular || !nuevas.length) return resumen;

    if (sh.getMaxRows() < ultima + 1 + nuevas.length) sh.insertRowsAfter(sh.getMaxRows(), nuevas.length + 5);
    const rango = sh.getRange(ultima + 2, 1, nuevas.length, ancho);
    rango.setValues(nuevas);
    ['fecha', 'fecha_venc'].forEach(k => {
      if (col[k] !== undefined) sh.getRange(ultima + 2, col[k] + 1, nuevas.length, 1).setNumberFormat('dd/mm/yyyy');
    });
    ['monto', 'neto', 'iva'].forEach(k => {
      if (col[k] !== undefined) sh.getRange(ultima + 2, col[k] + 1, nuevas.length, 1).setNumberFormat('#,##0');
    });
    SpreadsheetApp.flush();

    // Si alguien editó la planilla mientras tanto, no pisar sus cambios.
    if (DriveApp.getFileById(PLANILLA_ID).getLastUpdated().getTime() !== versionAntes) {
      throw new Error('la planilla cambió durante la escritura; reintentar');
    }
    const xlsx = UrlFetchApp.fetch(
      'https://www.googleapis.com/drive/v3/files/' + tmp.id + '/export?mimeType=' + encodeURIComponent(XLSX),
      { headers: { Authorization: 'Bearer ' + ScriptApp.getOAuthToken() } }).getBlob();
    Drive.Files.update({}, PLANILLA_ID, xlsx.setContentType(XLSX), { supportsAllDrives: true });
    return resumen;
  } finally {
    Drive.Files.remove(tmp.id);
  }
}

function validar_(filas) {
  const err = [];
  filas.forEach((f, i) => {
    Object.keys(LISTAS).forEach(k => {
      if (f[k] && LISTAS[k].indexOf(f[k]) < 0) err.push('fila ' + (i + 1) + ': ' + k + ' "' + f[k] + '" no válido');
    });
    if (!aMonto_(f.monto)) err.push('fila ' + (i + 1) + ': falta monto');
    if (!aFecha_(f.fecha)) err.push('fila ' + (i + 1) + ': fecha inválida');
    if (!f.razon_social) err.push('fila ' + (i + 1) + ': falta razón social');
  });
  return err;
}

function tokenValido_(t) {
  const real = PropertiesService.getScriptProperties().getProperty('TOKEN');
  return !!real && t === real;
}

function norm_(s) {
  return String(s || '').normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase()
    .replace(/[^a-z ]/g, ' ').replace(/\s+/g, ' ').trim();
}

function aFecha_(v) {
  if (v instanceof Date) return new Date(v.getFullYear(), v.getMonth(), v.getDate());
  const m = String(v || '').match(/^(\d{1,2})[\/-](\d{1,2})[\/-](\d{4})$/);
  if (m) return new Date(Number(m[3]), Number(m[2]) - 1, Number(m[1]));
  const iso = String(v || '').match(/^(\d{4})-(\d{2})-(\d{2})/);
  if (iso) return new Date(Number(iso[1]), Number(iso[2]) - 1, Number(iso[3]));
  return null;
}

function aMonto_(v) {
  if (typeof v === 'number') return Math.round(v);
  const s = String(v || '').replace(/[^\d-]/g, '');
  return s ? Number(s) : null;
}

function clave_(f, m) {
  return f ? Utilities.formatDate(f, 'America/Santiago', 'yyyy-MM-dd') + '|' + m : 'x|' + m;
}

function json_(o) {
  return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON);
}

/** Ejecutar una vez a mano desde el editor: crea el token y lo muestra en el registro. */
function crearToken() {
  const t = Utilities.getUuid().replace(/-/g, '');
  PropertiesService.getScriptProperties().setProperty('TOKEN', t);
  Logger.log('TOKEN: ' + t);
}
