
from pathlib import Path
import pandas as pd


def create_excel(output_path: Path, tables: dict[str, pd.DataFrame]) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(output_path, engine="xlsxwriter") as writer:
        workbook = writer.book
        index = workbook.add_worksheet("Índice")
        header = workbook.add_format({
            "bold": True,
            "align": "center",
            "valign": "vcenter",
            "border": 1,
        })
        index.write_row(0, 0, ["N.º", "Hoja"], header)

        for number, (name, df) in enumerate(tables.items(), start=1):
            sheet_name = name[:31]
            df.to_excel(writer, sheet_name=sheet_name, index=False)
            sheet = writer.sheets[sheet_name]
            sheet.freeze_panes(1, 0)

            for col_index, column in enumerate(df.columns):
                values = df[column].map(
                    lambda value: "" if pd.isna(value) else str(value)
                )
                max_len = max(
                    len(str(column)),
                    int(values.map(len).max()) if not values.empty else 0,
                )
                sheet.set_column(col_index, col_index, min(max_len + 2, 38))

            index.write(number, 0, number)
            index.write_url(
                number,
                1,
                f"internal:'{sheet_name}'!A1",
                string=sheet_name,
            )

        index.set_column("A:A", 7)
        index.set_column("B:B", 32)
