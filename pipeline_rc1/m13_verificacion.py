from __future__ import annotations

from pathlib import Path
import zipfile

from docx import Document


def _normalize(text: str) -> str:
    return " ".join(str(text).replace("\n", " ").split()).strip()


def _verify_p_values_in_word(docx_path: Path) -> list[str]:
    """Comprueba ceros únicamente dentro de columnas de valores p.

    La validación anterior buscaba cualquier celda con texto "0" en el XML,
    lo cual producía falsos positivos en datos legítimos como precipitación,
    RIC o valores descriptivos. Esta versión identifica primero las columnas
    cuyos encabezados contienen "Valor p" y revisa exclusivamente esas celdas.
    """
    errors: list[str] = []
    document = Document(docx_path)

    forbidden_p_values = {
        "0",
        "0.0",
        "0.00",
        "0.000",
        "0.0000",
        "0,0",
        "0,00",
        "0,000",
        "0,0000",
    }

    for table_number, table in enumerate(document.tables, start=1):
        if not table.rows:
            continue

        headers = [_normalize(cell.text).lower() for cell in table.rows[0].cells]
        p_columns = [
            index
            for index, header in enumerate(headers)
            if "valor p" in header
        ]

        for row_number, row in enumerate(table.rows[1:], start=2):
            for column_index in p_columns:
                if column_index >= len(row.cells):
                    continue

                value = _normalize(row.cells[column_index].text)
                if value in forbidden_p_values:
                    errors.append(
                        f"Tabla Word {table_number}, fila {row_number}, "
                        f"columna '{headers[column_index]}': valor p mostrado como {value}."
                    )

    return errors


def verify_outputs(docx_path: Path, xlsx_path: Path, figures) -> None:
    errors: list[str] = []

    figure_paths = (
        list(figures.values())
        if isinstance(figures, dict)
        else list(figures)
    )

    for path in [docx_path, xlsx_path, *figure_paths]:
        if not path.exists() or path.stat().st_size == 0:
            errors.append(f"Archivo ausente o vacío: {path}")

    if docx_path.exists():
        # Validación semántica de valores p.
        errors.extend(_verify_p_values_in_word(docx_path))

        # Validaciones generales de contenido prohibido.
        with zipfile.ZipFile(docx_path, "r") as zf:
            document_xml = zf.read(
                "word/document.xml"
            ).decode("utf-8", errors="ignore")

            forbidden_general = [
                "RSSI CV",
                "coeficiente de variación del RSSI",
                "Liberation Sans",
            ]
            for item in forbidden_general:
                if item.lower() in document_xml.lower():
                    errors.append(
                        f"Contenido prohibido detectado en Word: {item}"
                    )

    if errors:
        raise RuntimeError(
            "Verificación RC5.3 fallida:\n- " + "\n- ".join(errors)
        )
