"""
Сделай данный код на Python для перевода markdown в docx более читаемым, чистым и понятным.
Вынеси магические числа и строки в константы.
Поработай над неймингом функций, переменных.
Упрости код, если это возможно.

1. Вложенные списки всё также неправильно обрабатываются и получается список без вложенности.
2. Также сделай по умолчанию форматирование всего документа таким: шрифт Times New Romans, 14 пт (для сносок используется 10 пт.). Межстрочный интервал — полуторный. Размер полей: правое 10 мм, верхнее и нижнее — 20 мм, левое — 30 мм. Абзацный отступ — 1,5. Номер страницы ставится внизу по центру. Нумерация — сквозная.
3. В документе сохраняются символы backslash (\\) для переноса строки в markdown. Убери их из документа.
"""

import os
import re
import markdown
from docx import Document
from docx.shared import Inches, Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from bs4 import BeautifulSoup


def set_document_style(doc):
    """Set the default document style as per requirements."""
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(14)

    paragraph_format = style.paragraph_format
    paragraph_format.line_spacing = 1.5
    paragraph_format.first_line_indent = Cm(1.5)

    sections = doc.sections
    for section in sections:
        section.top_margin = Cm(2.0)
        section.bottom_margin = Cm(2.0)
        section.left_margin = Cm(3.0)
        section.right_margin = Cm(1.0)

    section = doc.sections[0]
    footer = section.footer
    footer.paragraphs[0].text = "\t"
    run = footer.paragraphs[0].add_run()
    fld = OxmlElement('w:fldSimple')
    fld.set(qn('w:instr'), 'PAGE')
    run._r.append(fld)
    section.footer_distance = Cm(1.0)
    section.different_first_page_header_footer = True
    doc.sections[0].first_page_footer.paragraphs[0].text = ""


def add_hyperlink(paragraph, url, text):
    """Add a clickable hyperlink to a DOCX paragraph."""
    part = paragraph.part
    r_id = part.relate_to(
        url,
        'http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink',
        is_external=True
    )

    run = paragraph.add_run(text)
    run.font.color.rgb = RGBColor(0, 0, 255)
    run.font.underline = True

    run_xml = run._r
    paragraph._p.remove(run_xml)
    hyperlink = OxmlElement('w:hyperlink')
    hyperlink.set(qn('r:id'), r_id)
    hyperlink.append(run_xml)
    paragraph._p.append(hyperlink)

    return run


def get_h1_from_markdown(file_path, fallback_text=None):
    """Extract the first H1 heading from a Markdown file, or return fallback text if none."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
        if not md_content.strip():
            return fallback_text or os.path.basename(file_path)
        md = markdown.Markdown(extensions=['extra', 'fenced_code', 'tables'])
        html_content = md.convert(md_content)
        soup = BeautifulSoup(html_content, 'html.parser')
        h1 = soup.find('h1')
        return h1.get_text() if h1 else (fallback_text or os.path.basename(file_path))
    except Exception:
        return fallback_text or os.path.basename(file_path)


def adjust_header_level(html_content, level_increase):
    """Adjust header levels in HTML content by increasing the header number."""
    soup = BeautifulSoup(html_content, 'html.parser')
    for header in soup.find_all(re.compile('^h[1-6]$')):
        current_level = int(header.name[1])
        new_level = min(current_level + level_increase, 6)
        header.name = f'h{new_level}'
    return str(soup)


def add_image_to_doc(doc, img_path, width=Inches(6)):
    """Add an image to the DOCX document."""
    if os.path.exists(img_path):
        paragraph = doc.add_paragraph()
        run = paragraph.add_run()
        run.add_picture(img_path, width=width)
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    else:
        doc.add_paragraph(f"[Image not found: {img_path}]")


def add_code_block_to_doc(doc, code_content, language=None):
    """Add a code block to the DOCX document with monospaced font."""
    paragraph = doc.add_paragraph()
    run = paragraph.add_run(code_content)
    run.font.name = 'Courier New'
    run.font.size = Pt(12)
    paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
    paragraph_format = paragraph.paragraph_format
    paragraph_format.space_before = Pt(5)
    paragraph_format.space_after = Pt(5)
    paragraph_format.line_spacing = 1.5  # Полуторный интервал


def add_table_to_doc(doc, table_html):
    """Convert an HTML table to a DOCX table."""
    soup = BeautifulSoup(table_html, 'html.parser')
    table = soup.find('table')
    if not table:
        return

    rows = table.find_all('tr')
    if not rows:
        return

    num_rows = len(rows)
    num_cols = max(len(row.find_all(['td', 'th'])) for row in rows)
    doc_table = doc.add_table(rows=num_rows, cols=num_cols)
    doc_table.style = 'Table Grid'

    for i, row in enumerate(rows):
        cells = row.find_all(['td', 'th'])
        for j, cell in enumerate(cells):
            cell_text = cell.get_text(strip=True)
            doc_table.rows[i].cells[j].text = cell_text
            if cell.name == 'th':
                for paragraph in doc_table.rows[i].cells[j].paragraphs:
                    for run in paragraph.runs:
                        run.font.bold = True


def process_list(
    list_element, doc, content_dir, level_increase, processed_files, list_type,
    nesting_level, file_path, base_path
):
    """Process nested lists (ul or ol) and add them to the DOCX document with proper indentation."""
    for li in list_element.find_all('li', recursive=False):
        paragraph = doc.add_paragraph(
            style='ListBullet' if list_type == 'bullet' else 'ListNumber'
        )
        paragraph.paragraph_format.left_indent = Cm(0.63 * nesting_level)

        for child in li.children:
            if child.name == 'a':
                href = child.get('href', '')
                if href and href.endswith('.md'):
                    md_path = os.path.join(os.path.dirname(file_path), href)
                    if os.path.exists(md_path):
                        link_text = child.get_text()
                        heading_text = get_h1_from_markdown(md_path, link_text)
                        doc.add_heading(heading_text, level=level_increase + 1)
                        process_markdown_file(
                            md_path, base_path, doc, content_dir,
                            level_increase=level_increase + 1, skip_h1=True,
                            processed_files=processed_files
                        )
                    else:
                        paragraph.add_run(f"[Markdown file not found: {href}]")
                elif href:
                    add_hyperlink(paragraph, href, child.get_text())
                else:
                    paragraph.add_run(child.get_text())
            elif child.name == 'strong':
                run = paragraph.add_run(child.get_text())
                run.bold = True
            elif child.name == 'em':
                run = paragraph.add_run(child.get_text())
                run.italic = True
            elif child.name == 'code':
                run = paragraph.add_run(child.get_text())
                run.font.name = 'Courier New'
                run.font.size = Pt(12)
            elif child.name == 'img':
                img_src = child.get('src', '')
                img_path = os.path.join(content_dir, img_src) if not os.path.isabs(
                    img_src
                ) else img_src
                add_image_to_doc(doc, img_path)
            elif child.name == 'ul':
                process_list(
                    child, doc, content_dir, level_increase, processed_files,
                    list_type='bullet', nesting_level=nesting_level + 1,
                    file_path=file_path, base_path=base_path
                )
            elif child.name == 'ol':
                process_list(
                    child, doc, content_dir, level_increase, processed_files,
                    list_type='number', nesting_level=nesting_level + 1,
                    file_path=file_path, base_path=base_path
                )
            else:
                paragraph.add_run(str(child))


def process_markdown_file(
    file_path, base_path, doc, content_dir, level_increase=0, skip_h1=False,
    processed_files=None
):
    """Process a single Markdown file and add its content to the DOCX document."""
    if processed_files is None:
        processed_files = set()

    if file_path in processed_files:
        return
    processed_files.add(file_path)

    with open(file_path, 'r', encoding='utf-8') as f:
        md_content = f.read()

    md = markdown.Markdown(extensions=['extra', 'fenced_code', 'tables'])
    html_content = md.convert(md_content)

    soup = BeautifulSoup(html_content, 'html.parser')

    if skip_h1:
        for h1 in soup.find_all('h1'):
            h1.decompose()

    html_content = adjust_header_level(str(soup), level_increase)
    soup = BeautifulSoup(html_content, 'html.parser')

    for element in soup.children:
        if element.name == 'h1':
            doc.add_heading(element.get_text(), level=1)
        elif element.name == 'h2':
            doc.add_heading(element.get_text(), level=2)
        elif element.name == 'h3':
            doc.add_heading(element.get_text(), level=3)
        elif element.name == 'h4':
            doc.add_heading(element.get_text(), level=4)
        elif element.name == 'h5':
            doc.add_heading(element.get_text(), level=5)
        elif element.name == 'h6':
            doc.add_heading(element.get_text(), level=6)
        elif element.name == 'p':
            paragraph = doc.add_paragraph()
            for child in element.children:
                if child.name == 'a':
                    href = child.get('href', '')
                    if href and href.endswith('.md'):
                        md_path = os.path.join(os.path.dirname(file_path), href)
                        if os.path.exists(md_path):
                            link_text = child.get_text()
                            heading_text = get_h1_from_markdown(md_path, link_text)
                            doc.add_heading(heading_text, level=level_increase + 1)
                            process_markdown_file(
                                md_path, base_path, doc, content_dir,
                                level_increase=level_increase + 1, skip_h1=True,
                                processed_files=processed_files
                            )
                        else:
                            paragraph.add_run(f"[Markdown file not found: {href}]")
                    elif href:
                        add_hyperlink(paragraph, href, child.get_text())
                    else:
                        paragraph.add_run(child.get_text())
                elif child.name == 'strong':
                    run = paragraph.add_run(child.get_text())
                    run.bold = True
                elif child.name == 'em':
                    run = paragraph.add_run(child.get_text())
                    run.italic = True
                elif child.name == 'code':
                    run = paragraph.add_run(child.get_text())
                    run.font.name = 'Courier New'
                    run.font.size = Pt(12)
                elif child.name == 'img':
                    img_src = child.get('src', '')
                    img_path = os.path.join(content_dir, img_src) if not os.path.isabs(
                        img_src
                    ) else img_src
                    add_image_to_doc(doc, img_path)
                else:
                    paragraph.add_run(str(child))
        elif element.name == 'ul':
            process_list(
                element, doc, content_dir, level_increase, processed_files,
                list_type='bullet', nesting_level=0, file_path=file_path,
                base_path=base_path
            )
        elif element.name == 'ol':
            process_list(
                element, doc, content_dir, level_increase, processed_files,
                list_type='number', nesting_level=0, file_path=file_path,
                base_path=base_path
            )
        elif element.name == 'table':
            add_table_to_doc(doc, str(element))
        elif element.name == 'pre':
            code = element.find('code')
            if code:
                add_code_block_to_doc(doc, code.get_text())


def collect_and_convert_to_docx(root_dir, output_docx, content_dir):
    """Collect Markdown files and convert them to a single DOCX file."""
    doc = Document()
    set_document_style(doc)

    readme_path = os.path.join(root_dir, 'README.md')

    if not os.path.exists(readme_path):
        print("README.md not found!")
        return

    with open(readme_path, 'r', encoding='utf-8') as f:
        readme_content = f.read()

    md = markdown.Markdown(extensions=['extra', 'fenced_code', 'tables'])
    html_content = md.convert(readme_content)
    soup = BeautifulSoup(html_content, 'html.parser')

    processed_files = set()
    current_heading_level = 1

    for element in soup.children:
        if element.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            current_heading_level = int(element.name[1])
            doc.add_heading(element.get_text(), level=current_heading_level)
        elif element.name == 'p':
            paragraph = doc.add_paragraph()
            for child in element.children:
                if child.name == 'a':
                    href = child.get('href', '')
                    if href and href.endswith('.md'):
                        md_path = href
                        full_md_path = os.path.join(root_dir, md_path)
                        if os.path.exists(full_md_path):
                            link_text = child.get_text()
                            heading_text = get_h1_from_markdown(full_md_path, link_text)
                            doc.add_heading(
                                heading_text, level=current_heading_level + 1
                            )
                            process_markdown_file(
                                full_md_path, root_dir, doc, content_dir,
                                level_increase=current_heading_level + 1, skip_h1=True,
                                processed_files=processed_files
                            )
                        else:
                            paragraph.add_run(f"[Markdown file not found: {md_path}]")
                    elif href:
                        add_hyperlink(paragraph, href, child.get_text())
                    else:
                        paragraph.add_run(child.get_text())
                elif child.name == 'strong':
                    run = paragraph.add_run(child.get_text())
                    run.bold = True
                elif child.name == 'em':
                    run = paragraph.add_run(child.get_text())
                    run.italic = True
                elif child.name == 'code':
                    run = paragraph.add_run(child.get_text())
                    run.font.name = 'Courier New'
                    run.font.size = Pt(12)
                elif child.name == 'img':
                    img_src = child.get('src', '')
                    img_path = os.path.join(content_dir, img_src) if not os.path.isabs(
                        img_src
                    ) else img_path
                    add_image_to_doc(doc, img_path)
                else:
                    paragraph.add_run(str(child))
        elif element.name == 'ul':
            process_list(
                element, doc, content_dir, current_heading_level, processed_files,
                list_type='bullet', nesting_level=0, file_path=readme_path,
                base_path=root_dir
            )
        elif element.name == 'ol':
            process_list(
                element, doc, content_dir, current_heading_level, processed_files,
                list_type='number', nesting_level=0, file_path=readme_path,
                base_path=root_dir
            )
        elif element.name == 'table':
            add_table_to_doc(doc, str(element))
        elif element.name == 'pre':
            code = element.find('code')
            if code:
                add_code_block_to_doc(doc, code.get_text())

    doc.save(output_docx)
    print(f"Document saved as {output_docx}")


if __name__ == "__main__":
    root_directory = "."
    content_directory = "./content"
    output_docx_file = "output.docx"
    collect_and_convert_to_docx(root_directory, output_docx_file, content_directory)