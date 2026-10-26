"""
MASTER document editing script for B.Tech mini project report.
Performs ALL edits in one pass:
1. Backs up original
2. Removes duplicate chapter headers  
3. Applies consistent chapter-opening layout (matching reference image)
4. Fixes page numbering (Roman for front matter, Arabic for main chapters)
5. Reduces excessive blank space
6. Saves as PaperTrail_Report_Revised.docx

Reference image layout:
- Dedicated page for each chapter
- Text vertically centered (slightly below page middle, ~55-65% down)
- "CHAPTER - N" on line 1, chapter title on line 2
- Large Times New Roman (~22pt), centered horizontally
- Clean white page, no borders or decorations
"""

import shutil, re, copy
from docx import Document
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_SECTION_START
import lxml.etree as etree

SRC = r"c:\Users\Nimal V\OneDrive\Desktop\nimalprojects\paperTrial\frontend\documentation\PaperTrail_Project_Documentation.docx"
DST = r"c:\Users\Nimal V\OneDrive\Desktop\nimalprojects\paperTrial\frontend\documentation\PaperTrail_Report_Revised.docx"

# ────────────────────────────────────────────────────────────────────────────
# 1. BACKUP & COPY
# ────────────────────────────────────────────────────────────────────────────
import os
if not os.path.exists(SRC + ".bak"):
    shutil.copy2(SRC, SRC + ".bak")
    print(f"[OK] Backed up original → {SRC}.bak")
else:
    print(f"[OK] Backup already exists")

shutil.copy2(SRC, DST)
print(f"[OK] Working copy → {DST}")

doc = Document(DST)
body = doc.element.body

# ────────────────────────────────────────────────────────────────────────────
# HELPER FUNCTIONS
# ────────────────────────────────────────────────────────────────────────────

def make_page_num_field(numfmt="decimal"):
    """Create a PAGE field run element."""
    r = OxmlElement('w:r')
    fldChar1 = OxmlElement('w:fldChar')
    fldChar1.set(qn('w:fldCharType'), 'begin')
    instrText = OxmlElement('w:instrText')
    instrText.set(qn('xml:space'), 'preserve')
    fmt_str = "ROMAN" if numfmt == "lowerRoman" else "ARABIC"
    # Use standard PAGE field
    instrText.text = f' PAGE '
    fldChar2 = OxmlElement('w:fldChar')
    fldChar2.set(qn('w:fldCharType'), 'separate')
    fldChar3 = OxmlElement('w:fldChar')
    fldChar3.set(qn('w:fldCharType'), 'end')
    r.append(fldChar1)
    r.append(instrText)
    r.append(fldChar2)
    r.append(fldChar3)
    return r

def set_footer_page_number(section, numfmt="decimal", font_size_pt=10):
    """Set footer to contain a proper PAGE field, centered."""
    footer = section.footer
    # Clear existing content
    for para in footer.paragraphs:
        for run in para.runs:
            run.text = ""
        # Remove all children of paragraph
        p_elem = para._element
        # Keep the pPr if it exists
        pPr = p_elem.find(qn('w:pPr'))
        # Remove all runs and fields
        for child in list(p_elem):
            if child.tag != qn('w:pPr'):
                p_elem.remove(child)
    
    # Use first paragraph of footer
    if footer.paragraphs:
        fp = footer.paragraphs[0]
    else:
        fp = footer.add_paragraph()
    
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # Add run with PAGE field
    r = OxmlElement('w:r')
    # Run properties (font size)
    rPr = OxmlElement('w:rPr')
    sz = OxmlElement('w:sz')
    sz.set(qn('w:val'), str(int(font_size_pt * 2)))
    rPr.append(sz)
    r.append(rPr)
    
    fldChar1 = OxmlElement('w:fldChar')
    fldChar1.set(qn('w:fldCharType'), 'begin')
    r.append(fldChar1)
    
    instrText = OxmlElement('w:instrText')
    instrText.set(qn('xml:space'), 'preserve')
    instrText.text = ' PAGE '
    r.append(instrText)
    
    fldChar2 = OxmlElement('w:fldChar')
    fldChar2.set(qn('w:fldCharType'), 'separate')
    r.append(fldChar2)
    
    # Cached value (will be updated on open)
    cached_r = OxmlElement('w:r')
    cached_t = OxmlElement('w:t')
    cached_t.text = "1"
    cached_r.append(cached_t)
    
    fldChar3 = OxmlElement('w:fldChar')
    fldChar3.set(qn('w:fldCharType'), 'end')
    r.append(fldChar3)
    
    fp._element.append(r)

def set_sectPr_page_num(sectPr, start=1, fmt="decimal"):
    """Set page number start and format in a sectPr element."""
    for old in sectPr.findall(qn('w:pgNumType')):
        sectPr.remove(old)
    pgNumType = OxmlElement('w:pgNumType')
    pgNumType.set(qn('w:start'), str(start))
    pgNumType.set(qn('w:fmt'), fmt)
    sectPr.append(pgNumType)

def get_sectPr_for_para(para):
    """Get the sectPr element embedded in this paragraph's pPr (if any)."""
    pPr = para._element.find(qn('w:pPr'))
    if pPr is not None:
        return pPr.find(qn('w:sectPr'))
    return None

def remove_page_break_from_para(para):
    """Remove manual page breaks (w:br type=page) from a paragraph."""
    for r in para._element.findall(qn('w:r')):
        for br in r.findall(qn('w:br')):
            if br.get(qn('w:type')) == 'page':
                r.remove(br)
        # Remove empty runs
        if not r.find(qn('w:t')) and not r.find(qn('w:br')) and not r.find(qn('w:fldChar')):
            pass  # keep other content

def para_has_page_break(para):
    """Check if paragraph contains a manual page break."""
    for r in para._element.findall(qn('w:r')):
        for br in r.findall(qn('w:br')):
            if br.get(qn('w:type')) == 'page':
                return True
    return False

def apply_chapter_title_page_format(para_ch_num, para_ch_title):
    """
    Format the two paragraphs as the chapter title page.
    - para_ch_num: paragraph with "CHAPTER - N" 
    - para_ch_title: paragraph with chapter title
    Matches reference image: text in lower-center of an otherwise blank page.
    """
    # Format chapter number paragraph
    pf = para_ch_num.paragraph_format
    pf.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pf.space_before = Pt(300)  # ~4.2 inches from top, placing text ~60% down A4
    pf.space_after = Pt(0)
    pf.line_spacing = Pt(28)
    
    # Clear and reformat runs
    for run in para_ch_num.runs:
        run.font.name = "Times New Roman"
        run.font.size = Pt(22)
        run.font.bold = False
        run.font.italic = False
        run.font.color.rgb = None  # auto color (black)
        # Fix rFonts
        rPr = run._r.get_or_add_rPr()
        rFonts = rPr.find(qn('w:rFonts'))
        if rFonts is None:
            rFonts = OxmlElement('w:rFonts')
            rPr.insert(0, rFonts)
        rFonts.set(qn('w:ascii'), 'Times New Roman')
        rFonts.set(qn('w:hAnsi'), 'Times New Roman')
        rFonts.set(qn('w:cs'), 'Times New Roman')
    
    # If no runs, add one
    if not para_ch_num.runs:
        run = para_ch_num.add_run(para_ch_num.text)
        run.font.name = "Times New Roman"
        run.font.size = Pt(22)
    
    # Format chapter title paragraph
    pf2 = para_ch_title.paragraph_format
    pf2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pf2.space_before = Pt(0)
    pf2.space_after = Pt(0)
    pf2.line_spacing = Pt(28)
    
    for run in para_ch_title.runs:
        run.font.name = "Times New Roman"
        run.font.size = Pt(22)
        run.font.bold = False
        run.font.italic = False
        run.font.color.rgb = None
        rPr = run._r.get_or_add_rPr()
        rFonts = rPr.find(qn('w:rFonts'))
        if rFonts is None:
            rFonts = OxmlElement('w:rFonts')
            rPr.insert(0, rFonts)
        rFonts.set(qn('w:ascii'), 'Times New Roman')
        rFonts.set(qn('w:hAnsi'), 'Times New Roman')
        rFonts.set(qn('w:cs'), 'Times New Roman')
    
    if not para_ch_title.runs:
        run = para_ch_title.add_run(para_ch_title.text)
        run.font.name = "Times New Roman"
        run.font.size = Pt(22)

def insert_page_break_before_para(para):
    """Insert a page break before a paragraph using paragraph's pPr pageBreakBefore."""
    pPr = para._element.find(qn('w:pPr'))
    if pPr is None:
        pPr = OxmlElement('w:pPr')
        para._element.insert(0, pPr)
    # Remove existing pageBreakBefore
    for old in pPr.findall(qn('w:pageBreakBefore')):
        pPr.remove(old)
    pb = OxmlElement('w:pageBreakBefore')
    pb.set(qn('w:val'), '1')
    pPr.append(pb)

def remove_para_page_break_before(para):
    """Remove pageBreakBefore from paragraph pPr."""
    pPr = para._element.find(qn('w:pPr'))
    if pPr is not None:
        for old in pPr.findall(qn('w:pageBreakBefore')):
            pPr.remove(old)

def set_para_spacing(para, before_pt=0, after_pt=8, line_spacing_pt=None):
    """Set spacing on a paragraph."""
    pf = para.paragraph_format
    pf.space_before = Pt(before_pt)
    pf.space_after = Pt(after_pt)
    if line_spacing_pt:
        pf.line_spacing = Pt(line_spacing_pt)

# ────────────────────────────────────────────────────────────────────────────
# 2. IDENTIFY STRUCTURE
# ────────────────────────────────────────────────────────────────────────────
print("\n=== IDENTIFYING DOCUMENT STRUCTURE ===")

paras = doc.paragraphs
n = len(paras)
print(f"Total paragraphs: {n}")

# Find all chapter headings
chapter_heading_positions = []  # (para_idx, text)
for i, para in enumerate(paras):
    text = para.text.strip()
    if re.match(r'^CHAPTER\s*[-–]?\s*\d+$', text) or re.match(r'^CHAPTER\s+\d+$', text):
        chapter_heading_positions.append((i, text))
        print(f"  Para {i}: |{text}|")

print(f"\nFound {len(chapter_heading_positions)} chapter heading paragraphs")

# ────────────────────────────────────────────────────────────────────────────
# 3. FIND AND REMOVE DUPLICATE CHAPTER - 1 HEADERS
# ────────────────────────────────────────────────────────────────────────────
# We have:
# Para 254: "CHAPTER - 1" (title page - keep, reformat)
# Para 255: "INTRODUCTION" + SECT break (title page - keep, reformat)
# Para 256: "CHAPTER 1" ← REMOVE
# Para 257: "INTRODUCTION" ← REMOVE

# Find the "CHAPTER - 1" entry
ch1_title_page_idx = None
ch1_dup_idx = None

for i, (idx, text) in enumerate(chapter_heading_positions):
    if 'CHAPTER - 1' in text or 'CHAPTER -1' in text:
        ch1_title_page_idx = idx
    elif text == 'CHAPTER 1':
        ch1_dup_idx = idx

print(f"\nChapter 1 title page at: {ch1_title_page_idx}")
print(f"Chapter 1 duplicate at: {ch1_dup_idx}")

# Paragraphs to remove (will collect indices, then remove in reverse order)
paras_to_remove = set()

if ch1_dup_idx is not None:
    # Remove "CHAPTER 1" and the following "INTRODUCTION" duplicate
    paras_to_remove.add(ch1_dup_idx)
    if ch1_dup_idx + 1 < n and paras[ch1_dup_idx + 1].text.strip() == "INTRODUCTION":
        paras_to_remove.add(ch1_dup_idx + 1)
        print(f"Will remove paras {ch1_dup_idx} and {ch1_dup_idx + 1} (duplicate ch1 heading)")

# ────────────────────────────────────────────────────────────────────────────
# 4. IDENTIFY CONTENT TO CONDENSE (remove redundant paragraphs)
# ────────────────────────────────────────────────────────────────────────────
# Strategy: Remove some verbose/redundant paragraphs from technical chapters
# to bring the document to ~42-45 pages while keeping all essential content

# These are identified redundant paragraphs based on inspection:
# - Some repetitive algorithm descriptions in Ch4
# - Verbose repetitive descriptions in Ch6 that repeat Ch3 info
# - Some over-explanatory sentences in Ch7

# Let's find and remove truly redundant content:

redundant_to_remove = []

for i, para in enumerate(paras):
    text = para.text.strip()
    
    # Skip empty paragraphs (they contribute to page count)
    # We won't remove all empty paragraphs, just unnecessary ones
    
    # Remove empty/whitespace-only paragraphs that appear in clusters
    # (more than one consecutive empty paragraph is wasteful)
    pass

# Actually let's be conservative - just remove the identified duplicates
# and rely on page break fixes and formatting to hit page count

print(f"\nTotal paragraphs to remove: {len(paras_to_remove)}")

# ────────────────────────────────────────────────────────────────────────────
# 5. REMOVE IDENTIFIED PARAGRAPHS
# ────────────────────────────────────────────────────────────────────────────
removed_indices_sorted = sorted(paras_to_remove, reverse=True)
for idx in removed_indices_sorted:
    if idx < len(doc.paragraphs):
        elem = doc.paragraphs[idx]._element
        parent = elem.getparent()
        if parent is not None:
            parent.remove(elem)
            print(f"[OK] Removed para {idx}")

# Save and reload
doc.save(DST)
doc = Document(DST)
paras = doc.paragraphs
print(f"\n[OK] After removal: {len(paras)} paragraphs")

# ────────────────────────────────────────────────────────────────────────────
# 6. FIND ALL CHAPTER HEADING POSITIONS (after removal)
# ────────────────────────────────────────────────────────────────────────────
print("\n=== CHAPTER HEADINGS AFTER CLEANUP ===")
chapter_positions = []  # List of (num_idx, title_idx, num_text, title_text)
paras = doc.paragraphs

for i in range(len(paras) - 1):
    text = paras[i].text.strip()
    next_text = paras[i+1].text.strip()
    
    # Match "CHAPTER - N" or "CHAPTER N"
    m = re.match(r'^CHAPTER\s*[-–]?\s*(\d+)$', text)
    if m:
        ch_num = int(m.group(1))
        num_str = f"CHAPTER - {ch_num}"
        print(f"  Para {i}: |{text}| → next: |{next_text[:50]}|")
        chapter_positions.append((i, i+1, num_str, next_text))

print(f"Found {len(chapter_positions)} chapter title pairs")

# ────────────────────────────────────────────────────────────────────────────
# 7. APPLY CHAPTER TITLE PAGE FORMATTING
# ────────────────────────────────────────────────────────────────────────────
print("\n=== APPLYING CHAPTER TITLE PAGE FORMATTING ===")

for (num_idx, title_idx, num_str, title_str) in chapter_positions:
    para_num = paras[num_idx]
    para_title = paras[title_idx]
    
    # Fix the text of chapter number to use "CHAPTER - N" format
    # Clear runs and set correct text
    p_elem = para_num._element
    # Remove all runs
    for r in p_elem.findall(qn('w:r')):
        p_elem.remove(r)
    # Add new run with correct text
    new_r = OxmlElement('w:r')
    new_rPr = OxmlElement('w:rPr')
    new_rFonts = OxmlElement('w:rFonts')
    new_rFonts.set(qn('w:ascii'), 'Times New Roman')
    new_rFonts.set(qn('w:hAnsi'), 'Times New Roman')
    new_rFonts.set(qn('w:cs'), 'Times New Roman')
    new_rPr.append(new_rFonts)
    new_sz = OxmlElement('w:sz')
    new_sz.set(qn('w:val'), '44')  # 22pt
    new_rPr.append(new_sz)
    new_szCs = OxmlElement('w:szCs')
    new_szCs.set(qn('w:val'), '44')
    new_rPr.append(new_szCs)
    new_r.append(new_rPr)
    new_t = OxmlElement('w:t')
    new_t.set(qn('xml:space'), 'preserve')
    new_t.text = num_str
    new_r.append(new_t)
    p_elem.append(new_r)
    
    # Set paragraph format for chapter number
    pPr = p_elem.find(qn('w:pPr'))
    if pPr is None:
        pPr = OxmlElement('w:pPr')
        p_elem.insert(0, pPr)
    
    # Set justification
    for old_jc in pPr.findall(qn('w:jc')):
        pPr.remove(old_jc)
    jc = OxmlElement('w:jc')
    jc.set(qn('w:val'), 'center')
    pPr.append(jc)
    
    # Set spacing: large space_before to push ~60% down the page
    # A4 body height with 1in margins ≈ 9.5 inches = 684pt
    # 60% down = 410pt from top. Already have content above (header etc.) ~50pt
    # So space_before ≈ 360pt = 7200 twips
    for old_sp in pPr.findall(qn('w:spacing')):
        pPr.remove(old_sp)
    spacing = OxmlElement('w:spacing')
    spacing.set(qn('w:before'), '7200')   # 360pt (pushes text ~60% down page)
    spacing.set(qn('w:after'), '0')
    spacing.set(qn('w:line'), '552')      # 27.6pt line spacing
    spacing.set(qn('w:lineRule'), 'exact')
    pPr.append(spacing)
    
    # Set paragraph style to Normal
    for old_pStyle in pPr.findall(qn('w:pStyle')):
        pPr.remove(old_pStyle)
    pStyle = OxmlElement('w:pStyle')
    pStyle.set(qn('w:val'), 'Normal')
    pPr.insert(0, pStyle)
    
    # Also add pageBreakBefore to ensure new page
    for old_pb in pPr.findall(qn('w:pageBreakBefore')):
        pPr.remove(old_pb)
    pb = OxmlElement('w:pageBreakBefore')
    pb.set(qn('w:val'), '1')
    pPr.append(pb)
    
    # ---- Format title paragraph ----
    p_title_elem = para_title._element
    
    # Fix text to ensure it's correct
    title_runs = p_title_elem.findall(qn('w:r'))
    for r in title_runs:
        p_title_elem.remove(r)
    
    new_r2 = OxmlElement('w:r')
    new_rPr2 = OxmlElement('w:rPr')
    new_rFonts2 = OxmlElement('w:rFonts')
    new_rFonts2.set(qn('w:ascii'), 'Times New Roman')
    new_rFonts2.set(qn('w:hAnsi'), 'Times New Roman')
    new_rFonts2.set(qn('w:cs'), 'Times New Roman')
    new_rPr2.append(new_rFonts2)
    new_sz2 = OxmlElement('w:sz')
    new_sz2.set(qn('w:val'), '44')
    new_rPr2.append(new_sz2)
    new_szCs2 = OxmlElement('w:szCs')
    new_szCs2.set(qn('w:val'), '44')
    new_rPr2.append(new_szCs2)
    new_r2.append(new_rPr2)
    new_t2 = OxmlElement('w:t')
    new_t2.set(qn('xml:space'), 'preserve')
    new_t2.text = title_str
    new_r2.append(new_t2)
    p_title_elem.append(new_r2)
    
    pPr2 = p_title_elem.find(qn('w:pPr'))
    if pPr2 is None:
        pPr2 = OxmlElement('w:pPr')
        p_title_elem.insert(0, pPr2)
    
    for old_jc in pPr2.findall(qn('w:jc')):
        pPr2.remove(old_jc)
    jc2 = OxmlElement('w:jc')
    jc2.set(qn('w:val'), 'center')
    pPr2.append(jc2)
    
    for old_sp in pPr2.findall(qn('w:spacing')):
        pPr2.remove(old_sp)
    spacing2 = OxmlElement('w:spacing')
    spacing2.set(qn('w:before'), '0')
    spacing2.set(qn('w:after'), '0')
    spacing2.set(qn('w:line'), '552')
    spacing2.set(qn('w:lineRule'), 'exact')
    pPr2.append(spacing2)
    
    for old_pStyle in pPr2.findall(qn('w:pStyle')):
        pPr2.remove(old_pStyle)
    pStyle2 = OxmlElement('w:pStyle')
    pStyle2.set(qn('w:val'), 'Normal')
    pPr2.insert(0, pStyle2)
    
    print(f"  [OK] Formatted chapter title: {num_str} | {title_str[:40]}")

# ────────────────────────────────────────────────────────────────────────────
# 8. FIX PAGE NUMBERING
# ────────────────────────────────────────────────────────────────────────────
print("\n=== FIXING PAGE NUMBERING ===")

sections = doc.sections
print(f"Total sections: {len(sections)}")

for si, section in enumerate(sections):
    sectPr = section._sectPr
    # Remove existing pgNumType
    for old in sectPr.findall(qn('w:pgNumType')):
        sectPr.remove(old)
    
    if si <= 2:
        # Front matter sections (0, 1, 2) - Roman numerals
        # Section 0: title page (no number)
        # Section 1: bonafide/declaration (no number)
        # Section 2: acknowledgement onward (roman numerals starting at i)
        if si == 0:
            pgNumType = OxmlElement('w:pgNumType')
            pgNumType.set(qn('w:fmt'), 'none')
            pgNumType.set(qn('w:start'), '1')
            sectPr.append(pgNumType)
            print(f"  Section {si}: no page numbers (title pages)")
        elif si == 1:
            pgNumType = OxmlElement('w:pgNumType')
            pgNumType.set(qn('w:fmt'), 'none')
            pgNumType.set(qn('w:start'), '1')
            sectPr.append(pgNumType)
            print(f"  Section {si}: no page numbers (bonafide)")
        else:  # si == 2
            pgNumType = OxmlElement('w:pgNumType')
            pgNumType.set(qn('w:fmt'), 'lowerRoman')
            pgNumType.set(qn('w:start'), '1')
            sectPr.append(pgNumType)
            print(f"  Section {si}: Roman numerals starting at i")
            # Fix footer
            set_footer_page_number(section, numfmt="lowerRoman", font_size_pt=10)
    
    elif si == 3:
        # Section 3 is TOC / list sections - continue Roman numerals
        pgNumType = OxmlElement('w:pgNumType')
        pgNumType.set(qn('w:fmt'), 'lowerRoman')
        pgNumType.set(qn('w:start'), '1')  # Will be linked/continued
        sectPr.append(pgNumType)
        print(f"  Section {si}: Roman numerals (TOC section)")
        set_footer_page_number(section, numfmt="lowerRoman", font_size_pt=10)
    
    elif si == 4:
        # Section 4 was the old chapter title page section - now remove it
        # (section breaks in para 255 and para 232 - we need to check)
        pgNumType = OxmlElement('w:pgNumType')
        pgNumType.set(qn('w:fmt'), 'lowerRoman')
        pgNumType.set(qn('w:start'), '1')
        sectPr.append(pgNumType)
        print(f"  Section {si}: Roman numerals continued")
    
    elif si == 5:
        # Main content section - Arabic numerals starting at 1
        pgNumType = OxmlElement('w:pgNumType')
        pgNumType.set(qn('w:fmt'), 'decimal')
        pgNumType.set(qn('w:start'), '1')
        sectPr.append(pgNumType)
        print(f"  Section {si}: Arabic numerals starting at 1")
        set_footer_page_number(section, numfmt="decimal", font_size_pt=10)
    
    else:
        # Any additional sections - continue Arabic
        pgNumType = OxmlElement('w:pgNumType')
        pgNumType.set(qn('w:fmt'), 'decimal')
        pgNumType.set(qn('w:start'), '1')
        sectPr.append(pgNumType)
        print(f"  Section {si}: Arabic numerals")

# Also fix the sectPr embedded in paragraphs (inline section breaks)
for i, para in enumerate(doc.paragraphs):
    pPr = para._element.find(qn('w:pPr'))
    if pPr is not None:
        inline_sectPr = pPr.find(qn('w:sectPr'))
        if inline_sectPr is not None:
            # Check which section this is part of
            # Para 17: end of section 0 (title pages) → no numbers
            # Para 57: end of section 1 → no numbers
            # Para 73: end of section 2 → roman numerals
            # Para 232: end of section 3 → roman numerals
            # Para 255: end of section 4 → this is the transition to main content!
            
            for old in inline_sectPr.findall(qn('w:pgNumType')):
                inline_sectPr.remove(old)
            
            if i <= 57:
                pgNumType = OxmlElement('w:pgNumType')
                pgNumType.set(qn('w:fmt'), 'none')
                pgNumType.set(qn('w:start'), '1')
                inline_sectPr.append(pgNumType)
                print(f"  Para {i} inline sectPr: no page numbers")
            elif i <= 232:
                pgNumType = OxmlElement('w:pgNumType')
                pgNumType.set(qn('w:fmt'), 'lowerRoman')
                pgNumType.set(qn('w:start'), '1')
                inline_sectPr.append(pgNumType)
                print(f"  Para {i} inline sectPr: Roman numerals")
            else:
                # This is the transition sectPr (was para 255) - after removing dup, might be 253
                # Make this Arabic page 1 restart
                pgNumType = OxmlElement('w:pgNumType')
                pgNumType.set(qn('w:fmt'), 'decimal')
                pgNumType.set(qn('w:start'), '1')
                inline_sectPr.append(pgNumType)
                print(f"  Para {i} inline sectPr: Arabic numerals restart at 1")

# ────────────────────────────────────────────────────────────────────────────
# 9. FIX HEADERS - ensure no page numbers in headers (use footers only)
# ────────────────────────────────────────────────────────────────────────────
print("\n=== CLEANING HEADERS ===")
for si, section in enumerate(sections):
    try:
        header = section.header
        if header and not header.is_linked_to_previous:
            for para in header.paragraphs:
                # Remove any hardcoded page numbers from headers
                for run in para.runs:
                    txt = run.text.strip()
                    if txt.isdigit():
                        run.text = run.text.replace(txt, "")
                        print(f"  Removed hardcoded page num '{txt}' from section {si} header")
    except Exception as e:
        print(f"  Warning: Could not process header in section {si}: {e}")

# ────────────────────────────────────────────────────────────────────────────
# 10. FIX EXCESSIVE BLANK SPACE IN CONTENT PARAGRAPHS
# ────────────────────────────────────────────────────────────────────────────
print("\n=== FIXING EXCESSIVE SPACING IN CONTENT PARAGRAPHS ===")

paras = doc.paragraphs
fixed_spacing_count = 0

for i, para in enumerate(paras):
    text = para.text.strip()
    style = para.style.name
    pf = para.paragraph_format
    
    # Skip chapter title paragraphs (we already formatted them)
    is_chapter_num = bool(re.match(r'^CHAPTER\s*[-–]?\s*\d+$', text))
    is_chapter_title = False
    if i > 0:
        prev_text = paras[i-1].text.strip()
        if re.match(r'^CHAPTER\s*[-–]?\s*\d+$', prev_text):
            is_chapter_title = True
    
    if is_chapter_num or is_chapter_title:
        continue
    
    # For normal content paragraphs, reduce excessive spacing
    try:
        sb = pf.space_before
        sa = pf.space_after
        # If space before is more than 18pt in content paragraphs, reduce it
        if sb and sb.pt and sb.pt > 18 and not is_chapter_num:
            pf.space_before = Pt(6)
            fixed_spacing_count += 1
        if sa and sa.pt and sa.pt > 18 and not is_chapter_num:
            pf.space_after = Pt(6)
            fixed_spacing_count += 1
    except (AttributeError, TypeError):
        pass

print(f"  Fixed spacing on {fixed_spacing_count} paragraphs")

# ────────────────────────────────────────────────────────────────────────────
# 11. REMOVE CONSECUTIVE EMPTY PARAGRAPHS (reduce blank space)
# ────────────────────────────────────────────────────────────────────────────
print("\n=== REMOVING CONSECUTIVE EMPTY PARAGRAPHS ===")
paras = doc.paragraphs
empty_to_remove = []
prev_was_empty = False

for i, para in enumerate(paras):
    text = para.text.strip()
    # Check for section breaks or page breaks - don't remove these
    has_sect = 'sectPr' in para._element.xml
    has_pb = para_has_page_break(para)
    
    if not text and not has_sect and not has_pb:
        if prev_was_empty:
            empty_to_remove.append(i)
        prev_was_empty = True
    else:
        prev_was_empty = False

print(f"  Found {len(empty_to_remove)} consecutive empty paragraphs to remove")

# Remove in reverse
for idx in sorted(empty_to_remove, reverse=True):
    if idx < len(doc.paragraphs):
        elem = doc.paragraphs[idx]._element
        parent = elem.getparent()
        if parent is not None:
            parent.remove(elem)

print(f"  Removed {len(empty_to_remove)} empty paragraphs")

# ────────────────────────────────────────────────────────────────────────────
# 12. SAVE FINAL DOCUMENT
# ────────────────────────────────────────────────────────────────────────────
doc.save(DST)
print(f"\n[OK] Saved revised document → {DST}")
print(f"[OK] Total paragraphs in final document: {len(doc.paragraphs)}")

# ────────────────────────────────────────────────────────────────────────────
# 13. VERIFY CHAPTER TITLE PAGES
# ────────────────────────────────────────────────────────────────────────────
doc_check = Document(DST)
print("\n=== FINAL CHAPTER HEADING VERIFICATION ===")
for i, para in enumerate(doc_check.paragraphs):
    text = para.text.strip()
    if re.match(r'^CHAPTER\s*[-–]\s*\d+$', text):
        pf = para.paragraph_format
        sb = pf.space_before
        print(f"  Para {i}: |{text}| space_before={sb}")
        if i + 1 < len(doc_check.paragraphs):
            print(f"    Next: |{doc_check.paragraphs[i+1].text.strip()[:60]}|")

print("\n✅ DOCUMENT EDITING COMPLETE")
print(f"   Original:  {SRC}")
print(f"   Backup:    {SRC}.bak")
print(f"   Revised:   {DST}")
print("\nNext: Open the revised document in Word to verify and export to PDF.")
