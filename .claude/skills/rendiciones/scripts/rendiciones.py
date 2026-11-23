#!/usr/bin/env python3
"""Herramienta de rendiciones de gastos de Waldemar (Distribuidora Catán).

Subcomandos:
  existentes  Vuelca a JSON todas las filas ya registradas en la planilla.
  conciliar   Cruza movimientos bancarios (JSON) contra la planilla y separa
              los ya rendidos de los pendientes.
  generar     Escribe las filas aprobadas en un .xlsx con el formato exacto de
              la hoja mensual (columnas, listas desplegables y formatos).
              Con --planilla, además genera una copia completa de la planilla
              con las filas agregadas en la hoja del mes.

Uso típico:
  python3 rendiciones.py conciliar --xlsx planilla.xlsx --movs movs.json --out pendientes.json
  python3 rendiciones.py generar --filas filas.json --mes 11 --out Rendiciones_Nov.xlsx \
      [--planilla planilla.xlsx --out-planilla planilla_actualizada.xlsx]
"""
import argparse
import datetime as dt
import json
import re
import sys
import unicodedata
import warnings

warnings.filterwarnings("ignore")
import openpyxl  # noqa: E402
from openpyxl.styles import Font, PatternFill  # noqa: E402
from openpyxl.worksheet.datavalidation import DataValidation  # noqa: E402

MESES = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio",
         "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

# Formato vigente (desde Septiembre 2026) de las hojas mensuales.
COLUMNAS = [
    ("N°", "n"),
    ("RUT Cliente *", "rut"),
    ("Razón Social Cliente *", "razon_social"),
    ("Fecha Emisión *", "fecha"),
    ("Fecha Vencimiento *", "fecha_venc"),
    ("Tipo De Documento", "tipo_documento"),
    ("N° Documento", "n_documento"),
    ("Monto Neto *()", "neto"),
    ("IVA ()", "iva"),
    ("Monto Total ()", "monto"),
    ("Estado Pago *", "estado"),
    ("Observaciones", "observaciones"),
    ("Metodo De Pago", "metodo_pago"),
    ("Institucion Financiera", "institucion"),
    ("Local", "local"),
    ("Centro de Costo Area ", "area"),
]

LISTAS = {
    "tipo_documento": ["Boleta", "Factura", "Otro"],
    "estado": ["Rendido", "Pendiente"],
    "metodo_pago": ["Transferencia", "Servipag", "Efectivo", "Debito", "Otro", "Credito"],
    "institucion": ["Santander", "BCI", "Mercado Pago", "Caja", "Otros", "SCOTIABANK"],
    "local": ["Ancahual", "Maipu", "Las Flores", "Los Valles", "Todas las Tiendas", "Mercado Publico"],
    "area": ["Gerencia y Administracion", "Operaciones", "Logistica", "Ventas", "Marketing"],
}


def norm(s):
    s = unicodedata.normalize("NFKD", str(s or "")).encode("ascii", "ignore").decode()
    return re.sub(r"\s+", " ", s).strip().lower()


def a_fecha(v):
    if isinstance(v, dt.datetime):
        return v.date()
    if isinstance(v, dt.date):
        return v
    if not v:
        return None
    s = str(v).strip()
    for f in ("%d/%m/%Y", "%d-%m-%Y", "%Y-%m-%d", "%m/%d/%Y", "%d/%m/%y"):
        try:
            return dt.datetime.strptime(s, f).date()
        except ValueError:
            pass
    return None


def a_monto(v):
    if v is None or v == "":
        return None
    if isinstance(v, (int, float)):
        return int(round(v))
    s = re.sub(r"[^\d,.-]", "", str(v))
    s = s.replace(".", "").replace(",", "")
    return int(s) if s.lstrip("-").isdigit() else None


def leer_planilla(path):
    """Devuelve todas las filas con monto de las 12 hojas mensuales."""
    wb = openpyxl.load_workbook(path, data_only=True)
    filas = []
    for ws in wb.worksheets:
        m = re.match(r"(\d{2})\s", ws.title)
        if not m:
            continue
        mes = int(m.group(1))
        hdr = None
        for i, r in enumerate(ws.iter_rows(values_only=True), start=1):
            if hdr is None:
                if "Razón Social Cliente *" in r:
                    hdr = [str(x).strip() if x is not None else "" for x in r]
                continue
            d = dict(zip(hdr, r))
            monto = a_monto(d.get("Monto Total ()"))
            if not monto or not d.get("Razón Social Cliente *"):
                continue
            filas.append({
                "hoja": ws.title, "fila": i, "mes": mes,
                "fecha": str(a_fecha(d.get("Fecha Emisión *")) or ""),
                "monto": monto,
                "razon_social": str(d.get("Razón Social Cliente *")).strip(),
                "observaciones": str(d.get("Observaciones") or "").strip(),
                "institucion": str(d.get("Institucion Financiera") or "").strip(),
                "estado": str(d.get("Estado Pago *") or "").strip(),
            })
    return filas


def cmd_existentes(a):
    filas = leer_planilla(a.xlsx)
    if a.mes:
        filas = [f for f in filas if f["mes"] == a.mes]
    json.dump(filas, sys.stdout, ensure_ascii=False, indent=1, default=str)


def cmd_conciliar(a):
    existentes = leer_planilla(a.xlsx)
    movs = json.load(open(a.movs, encoding="utf-8"))
    usados = set()
    ya, pend, excl = [], [], []
    for mv in movs:
        tipo = mv.get("tipo", "")
        if tipo in ("transferencia_recibida", "traspaso_propio") and not a.incluir_abonos:
            mv["motivo"] = "abono/traspaso propio: no es gasto"
            excl.append(mv)
            continue
        f = a_fecha(mv.get("fecha"))
        monto = a_monto(mv.get("monto"))
        match = None
        for idx, ex in enumerate(existentes):
            if idx in usados or ex["monto"] != monto:
                continue
            fe = a_fecha(ex["fecha"])
            if f and fe and abs((fe - f).days) > a.tolerancia:
                continue
            match = idx
            break
        if match is not None:
            usados.add(match)
            mv["registrado_en"] = f'{existentes[match]["hoja"]} fila {existentes[match]["fila"]}'
            ya.append(mv)
        else:
            pend.append(mv)
    out = {"pendientes": pend, "ya_rendidos": ya, "excluidos": excl}
    txt = json.dumps(out, ensure_ascii=False, indent=1, default=str)
    if a.out:
        open(a.out, "w", encoding="utf-8").write(txt)
    print(f"pendientes={len(pend)} ya_rendidos={len(ya)} excluidos={len(excl)}", file=sys.stderr)
    if not a.out:
        print(txt)


def escribir_fila(ws, row, fila):
    for col, (_, key) in enumerate(COLUMNAS, start=1):
        v = fila.get(key)
        if key in ("fecha", "fecha_venc"):
            v = a_fecha(v)
            c = ws.cell(row=row, column=col, value=v)
            c.number_format = 'dd"/"mm"/"yyyy'
        elif key in ("monto", "neto", "iva"):
            v = a_monto(v)
            c = ws.cell(row=row, column=col, value=v)
            c.number_format = "#,##0"
        else:
            ws.cell(row=row, column=col, value=(v if v not in ("", None) else None))


def validar(filas):
    errores = []
    for i, f in enumerate(filas, start=1):
        for key, opciones in LISTAS.items():
            v = f.get(key)
            if v and v not in opciones:
                errores.append(f"fila {i}: '{v}' no es válido para {key} ({', '.join(opciones)})")
        if not a_monto(f.get("monto")):
            errores.append(f"fila {i}: falta monto")
        if not a_fecha(f.get("fecha")):
            errores.append(f"fila {i}: fecha inválida '{f.get('fecha')}'")
    return errores


def agregar_validaciones(ws, desde, hasta):
    for col, (_, key) in enumerate(COLUMNAS, start=1):
        if key in LISTAS:
            letra = openpyxl.utils.get_column_letter(col)
            dv = DataValidation(type="list", formula1='"' + ",".join(LISTAS[key]) + '"', allow_blank=True)
            dv.add(f"{letra}{desde}:{letra}{hasta}")
            ws.add_data_validation(dv)


def cmd_generar(a):
    filas = json.load(open(a.filas, encoding="utf-8"))
    errores = validar(filas)
    if errores:
        print("ERRORES DE VALIDACIÓN:\n" + "\n".join(errores), file=sys.stderr)
        sys.exit(1)
    filas.sort(key=lambda f: a_fecha(f["fecha"]))
    nombre_hoja = f"{a.mes:02d} {MESES[a.mes - 1]}"

    # 1) Archivo de propuesta independiente (para pegar o revisar).
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = nombre_hoja
    for col, (titulo, _) in enumerate(COLUMNAS, start=1):
        c = ws.cell(row=1, column=col, value=titulo)
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor="DDEBF7")
    for i, f in enumerate(filas, start=2):
        escribir_fila(ws, i, f)
    agregar_validaciones(ws, 2, max(len(filas) + 1, 50))
    anchos = [5, 13, 38, 12, 12, 11, 13, 12, 10, 13, 11, 55, 14, 15, 18, 26]
    for col, w in enumerate(anchos, start=1):
        ws.column_dimensions[openpyxl.utils.get_column_letter(col)].width = w
    ws.freeze_panes = "A2"
    rev = wb.create_sheet("Respaldo")
    rev.append(["Fecha", "Monto", "Razón Social", "Fuente (correo / cartola)", "Confianza", "Nota"])
    for f in filas:
        rev.append([str(a_fecha(f["fecha"])), a_monto(f["monto"]), f.get("razon_social"),
                    f.get("fuente", ""), f.get("confianza", ""), f.get("nota", "")])
    total = sum(a_monto(f["monto"]) for f in filas)
    ws.cell(row=len(filas) + 3, column=9, value="TOTAL").font = Font(bold=True)
    ws.cell(row=len(filas) + 3, column=10, value=total).number_format = "#,##0"
    wb.save(a.out)
    total_txt = f"{total:,.0f}".replace(",", ".")
    print(f"Propuesta: {a.out} ({len(filas)} filas, total ${total_txt})")

    # 2) Opcional: copia completa de la planilla con las filas agregadas.
    if a.planilla:
        wbp = openpyxl.load_workbook(a.planilla)
        if nombre_hoja not in wbp.sheetnames:
            sys.exit(f"No existe la hoja '{nombre_hoja}' en la planilla")
        wsp = wbp[nombre_hoja]
        hdr_row = next(i for i, r in enumerate(wsp.iter_rows(values_only=True), start=1)
                       if "Razón Social Cliente *" in r)
        hdr = [str(c.value).strip() if c.value else "" for c in wsp[hdr_row]]
        if hdr[:3] != ["N°", "RUT Cliente *", "Razón Social Cliente *"]:
            sys.exit(f"La hoja '{nombre_hoja}' no tiene el formato vigente de 16 columnas; usar solo la propuesta.")
        ultima = hdr_row
        for r in range(hdr_row + 1, wsp.max_row + 1):
            if any(wsp.cell(row=r, column=c).value not in (None, "") for c in (3, 4, 10)):
                ultima = r
        for k, f in enumerate(filas, start=1):
            escribir_fila(wsp, ultima + k, f)
        destino = a.out_planilla or a.planilla.replace(".xlsx", "_actualizada.xlsx")
        wbp.save(destino)
        print(f"Planilla actualizada: {destino} (filas {ultima + 1}-{ultima + len(filas)} de '{nombre_hoja}')")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = p.add_subparsers(dest="cmd", required=True)
    e = sp.add_parser("existentes")
    e.add_argument("--xlsx", required=True)
    e.add_argument("--mes", type=int)
    c = sp.add_parser("conciliar")
    c.add_argument("--xlsx", required=True)
    c.add_argument("--movs", required=True)
    c.add_argument("--out")
    c.add_argument("--tolerancia", type=int, default=4, help="días de diferencia aceptados")
    c.add_argument("--incluir-abonos", action="store_true")
    g = sp.add_parser("generar")
    g.add_argument("--filas", required=True)
    g.add_argument("--mes", type=int, required=True)
    g.add_argument("--out", required=True)
    g.add_argument("--planilla")
    g.add_argument("--out-planilla")
    a = p.parse_args()
    {"existentes": cmd_existentes, "conciliar": cmd_conciliar, "generar": cmd_generar}[a.cmd](a)


if __name__ == "__main__":
    main()
