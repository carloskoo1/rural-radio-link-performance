"""
10_generar_reporte_tesis.py
===========================

Genera automáticamente dos productos reproducibles a partir de las tablas
y figuras del proyecto:

1. outputs/reportes/resultados_tesis.xlsx
2. outputs/reportes/Resultados_Tesis.docx

El script:
- lee todos los CSV ubicados en outputs/tables;
- ordena las tablas por nombre;
- crea una hoja por tabla en Excel;
- aplica formato profesional;
- inserta las tablas en Word;
- inserta las figuras PNG/JPG/PDF convertibles ubicadas en outputs/figures;
- agrega títulos, notas y pies de figura;
- crea un registro de archivos incorporados.

Requisitos:
    python -m pip install pandas xlsxwriter python-docx pillow

Ejecución:
    python scripts/10_generar_reporte_tesis.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Iterable

import pandas as pd
from docx import Document
from docx.enum.section import WD_ORIENT
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt


BASE_DIR = Path(__file__).resolve().parent.parent
TABLAS_DIR = BASE_DIR / "outputs" / "tables"
FIGURAS_DIR = BASE_DIR / "outputs" / "figures"
REPORTES_DIR = BASE_DIR / "outputs" / "reportes"

XLSX_SALIDA = REPORTES_DIR / "resultados_tesis.xlsx"
DOCX_SALIDA = REPORTES_DIR / "Resultados_Tesis.docx"

EXTENSIONES_FIGURA = {".png", ".jpg", ".jpeg"}


TITULOS_TABLAS = {
    "tabla_4_1_descriptivos_principales": (
        "Tabla 4.1. Estadísticos descriptivos principales por escenario"
    ),
    "tabla_4_2_kruskal_wallis": (
        "Tabla 4.2. Resultados de la prueba de Kruskal-Wallis"
    ),
    "tabla_4_3_conteo_lluvia": (
        "Tabla 4.3. Distribución de registros según condición de precipitación"
    ),
    "tabla_4_3_dunn_completa": (
        "Tabla 4.3-A. Comparaciones post hoc de Dunn completas"
    ),
    "tabla_4_3_dunn_significativas": (
        "Tabla 4.3-B. Comparaciones post hoc de Dunn significativas"
    ),
    "tabla_4_4_desempeno_lluvia": (
        "Tabla 4.4. Desempeño técnico según condición de precipitación"
    ),
    "tabla_4_5_correlacion_precipitacion": (
        "Tabla 4.5. Correlación entre precipitación y métricas técnicas"
    ),
    "tabla_4_6_estabilidad_por_escenario": (
        "Tabla 4.6. Indicadores de estabilidad operativa por escenario"
    ),
}

NOTAS_TABLAS = {
    "tabla_4_2_kruskal_wallis": (
        "Nota. El escenario E0 se excluyó del análisis de throughput por no "
        "disponer de registros equivalentes a cnMaestro."
    ),
    "tabla_4_3_dunn_completa": (
        "Nota. Los valores p fueron ajustados mediante el procedimiento de Holm."
    ),
    "tabla_4_3_dunn_significativas": (
        "Nota. Se consideró diferencia significativa cuando p ajustado < 0.05."
    ),
}


def orden_natural(texto: str) -> list[object]:
    """Permite ordenar nombres como tabla_4_2 antes de tabla_4_10."""
    return [
        int(fragmento) if fragmento.isdigit() else fragmento.lower()
        for fragmento in re.split(r"(\d+)", texto)
    ]


def normalizar_nombre_hoja(nombre: str, usados: set[str]) -> str:
    """Genera nombres válidos y únicos para hojas Excel."""
    nombre = re.sub(r"[\[\]:*?/\\]", "_", nombre)
    nombre = nombre[:31]
    base = nombre
    contador = 1

    while nombre in usados:
        sufijo = f"_{contador}"
        nombre = f"{base[:31-len(sufijo)]}{sufijo}"
        contador += 1

    usados.add(nombre)
    return nombre


def listar_csv() -> list[Path]:
    if not TABLAS_DIR.exists():
        raise FileNotFoundError(
            f"No existe la carpeta de tablas: {TABLAS_DIR}"
        )

    archivos = sorted(
        TABLAS_DIR.glob("*.csv"),
        key=lambda p: orden_natural(p.stem),
    )

    if not archivos:
        raise FileNotFoundError(
            f"No se encontraron archivos CSV en: {TABLAS_DIR}"
        )

    return archivos


def listar_figuras() -> list[Path]:
    if not FIGURAS_DIR.exists():
        return []

    return sorted(
        [
            ruta
            for ruta in FIGURAS_DIR.iterdir()
            if ruta.suffix.lower() in EXTENSIONES_FIGURA
        ],
        key=lambda p: orden_natural(p.stem),
    )


def leer_csv(ruta: Path) -> pd.DataFrame:
    """Lee CSV con tolerancia a separadores y codificaciones comunes."""
    intentos = [
        {"encoding": "utf-8-sig", "sep": ","},
        {"encoding": "utf-8", "sep": ","},
        {"encoding": "latin-1", "sep": ","},
        {"encoding": "utf-8-sig", "sep": ";"},
        {"encoding": "latin-1", "sep": ";"},
    ]

    ultimo_error: Exception | None = None

    for opciones in intentos:
        try:
            df = pd.read_csv(ruta, **opciones)
            if len(df.columns) > 1:
                return df
        except Exception as exc:
            ultimo_error = exc

    raise RuntimeError(
        f"No se pudo leer el archivo {ruta.name}: {ultimo_error}"
    )


def titulo_tabla(ruta: Path) -> str:
    return TITULOS_TABLAS.get(
        ruta.stem,
        ruta.stem.replace("_", " ").title(),
    )


def crear_excel(tablas: Iterable[tuple[Path, pd.DataFrame]]) -> None:
    """Crea un libro Excel con una hoja por tabla y hoja índice."""
    usados: set[str] = set()

    with pd.ExcelWriter(
        XLSX_SALIDA,
        engine="xlsxwriter",
    ) as writer:
        workbook = writer.book

        formato_titulo = workbook.add_format(
            {
                "bold": True,
                "font_size": 14,
                "align": "left",
                "valign": "vcenter",
            }
        )
        formato_encabezado = workbook.add_format(
            {
                "bold": True,
                "text_wrap": True,
                "align": "center",
                "valign": "vcenter",
                "border": 1,
            }
        )
        formato_celda = workbook.add_format(
            {
                "border": 1,
                "valign": "top",
            }
        )
        formato_nota = workbook.add_format(
            {
                "italic": True,
                "text_wrap": True,
                "valign": "top",
            }
        )
        formato_enlace = workbook.add_format(
            {
                "font_color": "blue",
                "underline": True,
            }
        )

        indice = workbook.add_worksheet("Índice")
        usados.add("Índice")
        indice.write(0, 0, "Productos estadísticos de la investigación", formato_titulo)
        indice.write_row(
            2,
            0,
            ["N.º", "Hoja", "Título", "Archivo de origen"],
            formato_encabezado,
        )

        fila_indice = 3

        for numero, (ruta, df) in enumerate(tablas, start=1):
            nombre_hoja = normalizar_nombre_hoja(ruta.stem, usados)
            df.to_excel(
                writer,
                sheet_name=nombre_hoja,
                startrow=3,
                index=False,
            )
            worksheet = writer.sheets[nombre_hoja]

            worksheet.write(0, 0, titulo_tabla(ruta), formato_titulo)
            worksheet.write(1, 0, f"Fuente: {ruta.name}", formato_nota)

            filas, columnas = df.shape
            if columnas > 0:
                worksheet.add_table(
                    3,
                    0,
                    3 + max(filas, 1),
                    columnas - 1,
                    {
                        "name": f"Tbl_{numero}",
                        "columns": [
                            {"header": str(columna)}
                            for columna in df.columns
                        ],
                        "style": "Table Style Medium 2",
                    },
                )

            for indice_columna, columna in enumerate(df.columns):
                serie = df[columna]

                if serie.empty:
                    longitud_maxima = 12
                else:
                    longitud_maxima = int(
                        serie.map(
                            lambda valor: (
                                len(str(valor))
                                if pd.notna(valor)
                                else 0
                            )
                        ).max()
                    )

                ancho = min(
                    max(
                        len(str(columna)) + 2,
                        longitud_maxima + 2,
                    ),
                    38,
                )

                worksheet.set_column(
                    indice_columna,
                    indice_columna,
                    ancho,
                    formato_celda,
                )

            worksheet.freeze_panes(4, 0)
            worksheet.set_row(0, 24)
            worksheet.set_row(3, 32)

            nota = NOTAS_TABLAS.get(ruta.stem)
            if nota:
                worksheet.write(5 + filas, 0, nota, formato_nota)
                worksheet.merge_range(
                    5 + filas,
                    0,
                    5 + filas,
                    max(columnas - 1, 0),
                    nota,
                    formato_nota,
                )

            indice.write(fila_indice, 0, numero)
            indice.write_url(
                fila_indice,
                1,
                f"internal:'{nombre_hoja}'!A1",
                formato_enlace,
                nombre_hoja,
            )
            indice.write(fila_indice, 2, titulo_tabla(ruta))
            indice.write(fila_indice, 3, ruta.name)
            fila_indice += 1

        indice.set_column("A:A", 7)
        indice.set_column("B:B", 31)
        indice.set_column("C:C", 65)
        indice.set_column("D:D", 45)
        indice.freeze_panes(3, 0)


def establecer_bordes_celda(celda) -> None:
    """Agrega bordes finos a una celda Word."""
    tc_pr = celda._tc.get_or_add_tcPr()
    tc_borders = tc_pr.first_child_found_in("w:tcBorders")

    if tc_borders is None:
        tc_borders = OxmlElement("w:tcBorders")
        tc_pr.append(tc_borders)

    for lado in ("top", "left", "bottom", "right", "insideH", "insideV"):
        elemento = OxmlElement(f"w:{lado}")
        elemento.set(qn("w:val"), "single")
        elemento.set(qn("w:sz"), "4")
        elemento.set(qn("w:space"), "0")
        elemento.set(qn("w:color"), "B7B7B7")
        tc_borders.append(elemento)


def sombrear_celda(celda, relleno: str) -> None:
    tc_pr = celda._tc.get_or_add_tcPr()
    shd = tc_pr.find(qn("w:shd"))

    if shd is None:
        shd = OxmlElement("w:shd")
        tc_pr.append(shd)

    shd.set(qn("w:fill"), relleno)


def agregar_tabla_word(documento: Document, ruta: Path, df: pd.DataFrame) -> None:
    """Inserta una tabla con formato académico en Word."""
    parrafo_titulo = documento.add_paragraph()
    parrafo_titulo.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = parrafo_titulo.add_run(titulo_tabla(ruta))
    run.bold = True
    run.font.size = Pt(10)

    if df.empty:
        documento.add_paragraph("No se registraron datos en esta tabla.")
        return

    tabla = documento.add_table(
        rows=1,
        cols=len(df.columns),
    )
    tabla.alignment = WD_TABLE_ALIGNMENT.CENTER
    tabla.autofit = True

    encabezado = tabla.rows[0].cells
    for indice, columna in enumerate(df.columns):
        encabezado[indice].text = str(columna)
        encabezado[indice].vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        sombrear_celda(encabezado[indice], "D9EAF7")
        establecer_bordes_celda(encabezado[indice])

        for parrafo in encabezado[indice].paragraphs:
            parrafo.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for run in parrafo.runs:
                run.bold = True
                run.font.size = Pt(8)

    for _, fila in df.iterrows():
        celdas = tabla.add_row().cells

        for indice, valor in enumerate(fila.tolist()):
            texto = "" if pd.isna(valor) else str(valor)
            celdas[indice].text = texto
            celdas[indice].vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            establecer_bordes_celda(celdas[indice])

            for parrafo in celdas[indice].paragraphs:
                parrafo.alignment = WD_ALIGN_PARAGRAPH.CENTER
                for run in parrafo.runs:
                    run.font.size = Pt(8)

    nota = NOTAS_TABLAS.get(ruta.stem)
    if nota:
        parrafo_nota = documento.add_paragraph()
        run = parrafo_nota.add_run(nota)
        run.italic = True
        run.font.size = Pt(8)

    documento.add_paragraph()


def titulo_figura_desde_nombre(ruta: Path, numero: int) -> str:
    texto = ruta.stem.replace("_", " ").replace("-", " ")
    texto = re.sub(r"\bfig(?:ura)?\s*\d+(?:\s+\d+)?\b", "", texto, flags=re.I)
    texto = re.sub(r"\s+", " ", texto).strip()

    if not texto:
        texto = "Resultado gráfico del análisis"

    return f"Fig. {numero}. {texto[0].upper() + texto[1:]}."


def crear_word(
    tablas: Iterable[tuple[Path, pd.DataFrame]],
    figuras: list[Path],
) -> None:
    documento = Document()

    seccion = documento.sections[0]
    seccion.top_margin = Cm(2.5)
    seccion.bottom_margin = Cm(2.5)
    seccion.left_margin = Cm(2.5)
    seccion.right_margin = Cm(2.5)

    estilos = documento.styles
    estilos["Normal"].font.name = "Arial"
    estilos["Normal"].font.size = Pt(10)

    titulo = documento.add_paragraph()
    titulo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = titulo.add_run("RESULTADOS ESTADÍSTICOS REPRODUCIBLES")
    run.bold = True
    run.font.size = Pt(14)

    subtitulo = documento.add_paragraph()
    subtitulo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = subtitulo.add_run(
        "Evaluación experimental del desempeño técnico del radioenlace"
    )
    run.italic = True
    run.font.size = Pt(11)

    introduccion = documento.add_paragraph()
    introduccion.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    introduccion.add_run(
        "El presente documento fue generado automáticamente a partir de las "
        "tablas y figuras producidas por el flujo reproducible de análisis. "
        "Su finalidad es facilitar la revisión, auditoría e incorporación de "
        "los resultados en el informe de investigación."
    )

    documento.add_heading("1. Tablas de resultados", level=1)

    for ruta, df in tablas:
        if len(df.columns) > 8:
            seccion_actual = documento.add_section(start_type=1)
            seccion_actual.orientation = WD_ORIENT.LANDSCAPE
            seccion_actual.page_width, seccion_actual.page_height = (
                seccion_actual.page_height,
                seccion_actual.page_width,
            )
            seccion_actual.top_margin = Cm(1.8)
            seccion_actual.bottom_margin = Cm(1.8)
            seccion_actual.left_margin = Cm(1.5)
            seccion_actual.right_margin = Cm(1.5)

            agregar_tabla_word(documento, ruta, df)

            seccion_retorno = documento.add_section(start_type=1)
            seccion_retorno.orientation = WD_ORIENT.PORTRAIT
            seccion_retorno.page_width, seccion_retorno.page_height = (
                seccion_retorno.page_height,
                seccion_retorno.page_width,
            )
            seccion_retorno.top_margin = Cm(2.5)
            seccion_retorno.bottom_margin = Cm(2.5)
            seccion_retorno.left_margin = Cm(2.5)
            seccion_retorno.right_margin = Cm(2.5)
        else:
            agregar_tabla_word(documento, ruta, df)

    documento.add_heading("2. Figuras de resultados", level=1)

    if not figuras:
        documento.add_paragraph(
            "No se encontraron figuras en outputs/figures."
        )
    else:
        for numero, figura in enumerate(figuras, start=1):
            parrafo_imagen = documento.add_paragraph()
            parrafo_imagen.alignment = WD_ALIGN_PARAGRAPH.CENTER

            try:
                parrafo_imagen.add_run().add_picture(
                    str(figura),
                    width=Cm(15.5),
                )
            except Exception as exc:
                documento.add_paragraph(
                    f"No se pudo insertar {figura.name}: {exc}"
                )
                continue

            pie = documento.add_paragraph()
            pie.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = pie.add_run(titulo_figura_desde_nombre(figura, numero))
            run.bold = True
            run.font.size = Pt(9)

            fuente = documento.add_paragraph()
            fuente.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = fuente.add_run("Fuente: Elaboración propia.")
            run.italic = True
            run.font.size = Pt(8)

            documento.add_paragraph()

    documento.add_heading("3. Trazabilidad de archivos", level=1)

    for ruta, _ in tablas:
        documento.add_paragraph(
            f"Tabla incorporada: outputs/tables/{ruta.name}",
            style="List Bullet",
        )

    for figura in figuras:
        documento.add_paragraph(
            f"Figura incorporada: outputs/figures/{figura.name}",
            style="List Bullet",
        )

    documento.save(DOCX_SALIDA)


def main() -> None:
    REPORTES_DIR.mkdir(parents=True, exist_ok=True)

    rutas_csv = listar_csv()
    tablas = [(ruta, leer_csv(ruta)) for ruta in rutas_csv]
    figuras = listar_figuras()

    print(f"Tablas encontradas: {len(tablas)}")
    print(f"Figuras encontradas: {len(figuras)}")

    print("Generando Excel...")
    crear_excel(tablas)

    print("Generando Word...")
    crear_word(tablas, figuras)

    print("\nProductos generados:")
    print(f" - {XLSX_SALIDA}")
    print(f" - {DOCX_SALIDA}")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"\nERROR: {error}", file=sys.stderr)
        raise
