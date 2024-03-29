import glob
import os
from generator import generate_pdf

filepaths = glob.glob('invoices/*.xlsx')
os.makedirs('PDFs', exist_ok=True)

for path in filepaths:
    generate_pdf(path)