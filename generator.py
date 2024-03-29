from pathlib import Path
import pandas as pd
from fpdf import FPDF
from inflection import titleize


def parse_path(string):
    file_name = Path(string).stem
    nr, date = file_name.split('-')

    return nr, date


def generate_pdf(path):
    nr, date = parse_path(path)

    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()

    pdf.set_font(family='Times', size=20, style='B')
    pdf.cell(w=0, h=10, txt=f'Invoice nr.{nr}', ln=1)
    pdf.set_font(family='Times', size=16, style='B')
    pdf.cell(w=0, h=6, txt=f'Date: {date}.', ln=1)
    pdf.cell(w=0, h=5, ln=1)

    df = pd.read_excel(path, sheet_name='Sheet 1')
    pdf.set_font(family='Times', size=10)
    for i, c_name in enumerate(list(df.columns)):
        pdf.cell(
            w=60 if i == 1 else 30,
            h=5,
            txt=titleize(c_name),
            border=1,
            ln=0 if i < len(df.columns) - 1 else 1
        )

    for i, row in df.iterrows():
        pdf.set_text_color(100, 0, 0)
        pdf.cell(w=30, h=5, txt=str(row['product_id']), border=1)
        pdf.cell(w=60, h=5, txt=row['product_name'], border=1)
        pdf.cell(w=30, h=5, txt=str(row['amount_purchased']), border=1)
        pdf.cell(w=30, h=5, txt=str(row['price_per_unit']), border=1)
        pdf.cell(w=30, h=5, txt=str(row['total_price']), ln=1, border=1)

    total_price = str(df['total_price'].sum())
    for i, c_name in enumerate(list(df.columns)):
        pdf.cell(
            w=60 if i == 1 else 30,
            h=5,
            txt=total_price if i == len(df.columns) -1 else '',
            border=1,
            ln=0 if i < len(df.columns) - 1 else 1
        )

    pdf.cell(w=0, h=5, ln=1)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font(family='Times', size=20, style='B')
    pdf.cell(w=0, h=10, txt=f'Total due amount is {total_price} Euros', ln=1)
    pdf.cell(w=40, h=10, txt='Antal Bako')
    pdf.image('pythonhow.png', w=10)


    pdf.output(f'PDFs/{f"{nr}-{date}"}.pdf')
