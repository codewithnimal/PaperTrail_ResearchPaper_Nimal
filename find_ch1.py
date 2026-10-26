import docx

doc = docx.Document(r'documentation.docs\Sample Project_Report.docx')
body = doc._body._element

for idx, child in enumerate(body):
    txt = ''.join(child.itertext()).strip()
    if 'CHAPTER' in txt:
        print(f"Body index {idx:3d}: repr={repr(txt)}")
