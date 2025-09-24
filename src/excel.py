import pandas as pd
from datetime import datetime
from pathlib import Path
import xlsxwriter

BLUE_HDR   = '#4F81BD'
BLUE_TOTAL = '#305496'
YELLOW     = '#FFFF00'
GREEN_L    = '#C6EFCE'

def export_to_excel(df: pd.DataFrame, filename: str):
    # garante que a pasta exista
    Path(filename).parent.mkdir(parents=True, exist_ok=True)

    with pd.ExcelWriter(filename, engine="xlsxwriter") as writer:
        df.to_excel(writer, sheet_name="Relatório", index=False, startrow=3)

        workbook  = writer.book
        worksheet = writer.sheets["Relatório"]

        # ===== FORMATAÇÕES =====
        title_fmt = workbook.add_format({
            "bold": True, "font_size": 16, "align": "center",
            "valign": "vcenter", "font_color": BLUE_TOTAL
        })
        header_fmt = workbook.add_format({
            "bold": True, "fg_color": BLUE_HDR, "font_color": "white",
            "align": "center", "valign": "vcenter", "border": 1
        })
        money_fmt = workbook.add_format({"num_format": 'R$ #,##0.00', "border": 1})
        date_fmt = workbook.add_format({"num_format": 'dd/mm/yyyy', "border": 1})
        normal_fmt = workbook.add_format({"border": 1})
        yellow_fmt = workbook.add_format({"bg_color": YELLOW, "border": 1})
        yellow_date_fmt = workbook.add_format({"bg_color": YELLOW, "num_format": "dd/mm/yyyy", "border": 1})
        green_fmt  = workbook.add_format({"bg_color": GREEN_L, "num_format": 'R$ #,##0.00', "border": 1})
        total_label_fmt = workbook.add_format({
            "bold": True, "align": "right", "fg_color": BLUE_TOTAL,
            "font_color": "white", "border": 1
        })
        total_sum_fmt = workbook.add_format({
            "bold": True, "fg_color": BLUE_TOTAL, "font_color": "white",
            "num_format": 'R$ #,##0.00', "border": 1
        })

        # ===== TÍTULO (ocupa 2 linhas) =====
        ncols = len(df.columns)
        title = f"PEDIDOS PARA FATURAR (RELATÓRIO DO DIA {datetime.today():%d/%m/%Y})"
        worksheet.merge_range(0, 0, 1, ncols-1, title, title_fmt)
        worksheet.set_row(0, 25)  # altura linha 1
        worksheet.set_row(1, 25)  # altura linha 2

        # ===== CABEÇALHO (linha 4, pois startrow=3) =====
        for col_num, col_name in enumerate(df.columns):
            worksheet.write(3, col_num, col_name, header_fmt)

        # ===== FORMATAÇÃO POR COLUNA =====
        colmap = {name: i for i, name in enumerate(df.columns)}
        DATA_COLS   = ["Data de entrega", "Data do documento"]
        MOEDA_COLS  = ["Total sem imposto", "Total com imposto", "Frete", "Total com frete incluso"]

        for row_num in range(len(df)):
            row_values = df.iloc[row_num]
            use_yellow = (row_values.get("Utilização") == "S-Rem a Ordem Futura")

            for col_num, value in enumerate(row_values):
                fmt = normal_fmt

                if df.columns[col_num] in DATA_COLS and pd.notna(value):
                    fmt = date_fmt
                if df.columns[col_num] in MOEDA_COLS and isinstance(value, (int, float)):
                    fmt = money_fmt
                if "Frete" in colmap and col_num == colmap["Frete"] and isinstance(value, (int, float)) and value != 0:
                    fmt = green_fmt
                if use_yellow:
                    if df.columns[col_num] in DATA_COLS and pd.notna(value):
                        fmt = yellow_date_fmt
                    else:
                        fmt = yellow_fmt

                worksheet.write(row_num+4, col_num, value, fmt)

        # ===== TOTAL =====
        if "Total com frete incluso" in colmap:
            col_tot = colmap["Total com frete incluso"]
            last_row = len(df) + 4
            worksheet.write(last_row, col_tot-1, "TOTAL:", total_label_fmt)
            worksheet.write_formula(
                last_row, col_tot,
                f"SUM({xlsxwriter.utility.xl_col_to_name(col_tot)}5:{xlsxwriter.utility.xl_col_to_name(col_tot)}{last_row})",
                total_sum_fmt
            )

        # ===== LARGURA AUTOMÁTICA =====
        for i, col in enumerate(df.columns):
            maxlen = max(df[col].astype(str).map(len).max(), len(col)) + 2
            worksheet.set_column(i, i, max(12, maxlen))    
        # ===== ZOOM PRÉ-DEFINIDO =====
        worksheet.set_zoom(120)