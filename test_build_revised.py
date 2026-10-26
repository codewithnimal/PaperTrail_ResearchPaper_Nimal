# test_build_revised.py
# Prototype script to test building the revised document and verifying page count with Word COM.

import os
import shutil
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
import win32com.client
import fitz

from report_helpers import set_cell_border, set_cell_margins, set_cell_shading
from chapters_data_shortened import get_chapters_shortened
from chapters_data_part3 import get_references
from tables_data import get_tables_dict

TEMPLATE_PATH = r"C:\Users\Nimal V\Downloads\Sample Project_Report.docx"
OUTPUT_DIR = r"c:\Users\Nimal V\OneDrive\Desktop\nimalprojects\paperTrial\frontend\documentation"
OUTPUT_DOCX = os.path.join(OUTPUT_DIR, "PaperTrail_Project_Report_Revised.docx")
OUTPUT_PDF = os.path.join(OUTPUT_DIR, "PaperTrail_Project_Report_Revised.pdf")

OFFICIAL_TITLE_L1 = "AN AI-POWERED RESEARCH PAPER COMPARISON AND"
OFFICIAL_TITLE_L2 = "EVIDENCE VERIFICATION SYSTEM USING"
OFFICIAL_TITLE_L3 = "RETRIEVAL-AUGMENTED GENERATION (RAG)"
OFFICIAL_TITLE_FULL = f"{OFFICIAL_TITLE_L1} {OFFICIAL_TITLE_L2} {OFFICIAL_TITLE_L3}"

RIGHT_MARGIN_TWIPS = 9000

print("Script template ready.")
