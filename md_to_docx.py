import os
import re
import time
from typing import Optional, Set

import markdown
from bs4 import BeautifulSoup
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Inches, Pt, RGBColor

# Constants
FONT_NAME = "Times New Roman"
FONT_SIZE = Pt(14)
CODE_FONT_NAME = "Courier New"
CODE_FONT_SIZE = Pt(12)
LINE_SPACING = 1.5
FIRST_LINE_INDENT = Cm(1.5)
TOP_MARGIN = Cm(2.0)
BOTTOM_MARGIN = Cm(2.0)
LEFT_MARGIN = Cm(3.0)
RIGHT_MARGIN = Cm(1.0)
FOOTER_DISTANCE = Cm(1.0)
LIST_INDENT = Cm(0.63)
IMAGE_WIDTH = Inches(6)
HYPERLINK_COLOR = RGBColor(0, 0, 255)
HEADING_COLOR = RGBColor(0, 0, 0)  # Black color for headings
TABLE_STYLE = "Table Grid"
MARKDOWN_EXTENSIONS = ["extra", "fenced_code", "tables"]
README_FILE = "README.md"
CONTENT_DIR = "./content"
OUTPUT_FILE = f"Lesovoy_{int(time.time())}.docx"
MD_EXT = ".md"
PY_EXT = ".py"
CODE_BLOCK_SPACING = Pt(10)
HEADING_BASE_SIZE = 28  # Base font size for H1 in points
HEADING_SIZE_REDUCTION = 2  # Size reduction per heading level
ERROR_PY_NOT_FOUND = "[Python file not found: {}]"
ERROR_MD_NOT_FOUND = "[Markdown file not found: {}]"
ERROR_IMAGE_NOT_FOUND = "[Image not found: {}]"
MAX_HEADING_LEVEL = 9  # Maximum heading level


def configure_document_style(document: Document) -> None:
    """Configure the document style with predefined settings, including headings."""
    # Configure the Normal style
    style = document.styles["Normal"]
    font = style.font
    font.name = FONT_NAME
    font.size = FONT_SIZE

    paragraph_format = style.paragraph_format
    paragraph_format.line_spacing = LINE_SPACING
    paragraph_format.first_line_indent = FIRST_LINE_INDENT

    for level in range(1, 10):
        heading_style = document.styles[f"Heading {level}"]
        heading_font = heading_style.font
        heading_font.name = FONT_NAME
        heading_font.size = Pt(HEADING_BASE_SIZE - level * HEADING_SIZE_REDUCTION)
        heading_font.color.rgb = HEADING_COLOR
        heading_font.bold = True if level <= 3 else False

        rPr = heading_style.element.rPr
        if rPr is None:
            rPr = OxmlElement("w:rPr")
            heading_style.element.append(rPr)
        rFonts = rPr.find(qn("w:rFonts"))
        if rFonts is None:
            rFonts = OxmlElement("w:rFonts")
            rPr.append(rFonts)
        rFonts.set(qn("w:ascii"), FONT_NAME)
        rFonts.set(qn("w:hAnsi"), FONT_NAME)
        rFonts.set(qn("w:cs"), FONT_NAME)
        rFonts.set(qn("w:eastAsia"), FONT_NAME)

    # Configure document margins and footer
    for section in document.sections:
        section.top_margin = TOP_MARGIN
        section.bottom_margin = BOTTOM_MARGIN
        section.left_margin = LEFT_MARGIN
        section.right_margin = RIGHT_MARGIN

    section = document.sections[0]
    footer = section.footer
    footer.paragraphs[0].text = "\t"
    run = footer.paragraphs[0].add_run()
    fld = OxmlElement("w:fldSimple")
    fld.set(qn("w:instr"), "PAGE")
    run._r.append(fld)
    section.footer_distance = FOOTER_DISTANCE
    section.different_first_page_header_footer = True
    document.sections[0].first_page_footer.paragraphs[0].text = ""


def add_hyperlink(paragraph, url: str, text: str) -> None:
    """Add a clickable hyperlink to a paragraph."""
    part = paragraph.part
    r_id = part.relate_to(
        url,
        "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink",
        is_external=True,
    )

    run = paragraph.add_run(text)
    run.font.color.rgb = HYPERLINK_COLOR
    run.font.underline = True

    run_xml = run._r
    paragraph._p.remove(run_xml)
    hyperlink = OxmlElement("w:hyperlink")
    hyperlink.set(qn("r:id"), r_id)
    hyperlink.append(run_xml)
    paragraph._p.append(hyperlink)


def format_heading(heading, level: int) -> None:
    """Apply formatting to a heading paragraph."""
    for run in heading.runs:
        run.font.name = FONT_NAME
        run.font.size = Pt(HEADING_BASE_SIZE - level * HEADING_SIZE_REDUCTION)
        run.font.color.rgb = HEADING_COLOR


def handle_link(
    href: str,
    base_path: str,
    document: Document,
    paragraph,
    content_directory: str,
    root_directory: str,
    level_increase: int,
    processed_files: Set[str],
    link_text: str,
    heading_level: Optional[int] = None,
) -> bool:
    """Handle Markdown links to .py, .md files, or external URLs."""
    if href.endswith(PY_EXT):
        py_path = os.path.join(base_path, href)
        if os.path.exists(py_path):
            with open(py_path, "r", encoding="utf-8") as f:
                code_content = f.read()
            insert_code_block(document, code_content)
        else:
            paragraph.add_run(ERROR_PY_NOT_FOUND.format(href))
        return True
    elif href.endswith(MD_EXT):
        md_path = os.path.join(base_path, href)
        if os.path.exists(md_path):
            heading_text = extract_h1_from_markdown(md_path, link_text)
            new_level = (
                heading_level if heading_level is not None else level_increase + 1
            )
            new_level = min(new_level, MAX_HEADING_LEVEL)  # Limit to max level
            heading = document.add_heading(heading_text, level=new_level)
            format_heading(heading, new_level)
            adjusted_level_increase = (
                new_level if heading_level is not None else level_increase
            )
            process_markdown(
                md_path,
                root_directory,
                document,
                content_directory,
                level_increase=adjusted_level_increase,
                skip_h1=True,
                processed_files=processed_files,
            )
        else:
            paragraph.add_run(ERROR_MD_NOT_FOUND.format(href))
        return True
    elif href:
        add_hyperlink(paragraph, href, link_text)
        return True
    return False


def extract_h1_from_markdown(
    file_path: str, fallback_text: Optional[str] = None
) -> str:
    """Extract the first H1 heading from a Markdown file or return a fallback."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            markdown_content = f.read()
        if not markdown_content.strip():
            return fallback_text or os.path.basename(file_path)
        md = markdown.Markdown(extensions=MARKDOWN_EXTENSIONS)
        html_content = md.convert(markdown_content)
        soup = BeautifulSoup(html_content, "html.parser")
        h1 = soup.find("h1")
        return h1.get_text() if h1 else (fallback_text or os.path.basename(file_path))
    except Exception:
        return fallback_text or os.path.basename(file_path)


def adjust_headers(html_content: str, level_increase: int) -> str:
    soup = BeautifulSoup(html_content, "html.parser")
    for header in soup.find_all(re.compile("^h[1-9]$")):
        current_level = int(header.name[1])
        new_level = min(current_level + level_increase, MAX_HEADING_LEVEL)
        header.name = f"h{new_level}"
    return str(soup)


def insert_image(
    document: Document, image_path: str, width: Inches = IMAGE_WIDTH
) -> None:
    """Insert an image into the document with specified width."""
    if os.path.exists(image_path):
        paragraph = document.add_paragraph()
        run = paragraph.add_run()
        run.add_picture(image_path, width=width)
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    else:
        document.add_paragraph(ERROR_IMAGE_NOT_FOUND.format(image_path))


def insert_code_block(document: Document, code_content: str) -> None:
    """Insert a code block into the document within a table without extra line breaks."""
    table = document.add_table(rows=1, cols=1)
    table.style = TABLE_STYLE
    cell = table.rows[0].cells[0]
    cell.text = code_content.rstrip()
    for paragraph in cell.paragraphs:
        for run in paragraph.runs:
            run.font.name = CODE_FONT_NAME
            run.font.size = CODE_FONT_SIZE
    cell.paragraphs[0].paragraph_format.space_before = Pt(0)
    cell.paragraphs[0].paragraph_format.space_after = CODE_BLOCK_SPACING
    cell.paragraphs[0].paragraph_format.line_spacing = 1.0
    cell.paragraphs[0].paragraph_format.first_line_indent = Cm(0)


def insert_table(document: Document, table_html: str) -> None:
    """Convert an HTML table to a DOCX table."""
    soup = BeautifulSoup(table_html, "html.parser")
    table = soup.find("table")
    if not table:
        return

    rows = table.find_all("tr")
    if not rows:
        return

    num_rows = len(rows)
    num_cols = max(len(row.find_all(["td", "th"])) for row in rows)
    doc_table = document.add_table(rows=num_rows, cols=num_cols)
    doc_table.style = TABLE_STYLE

    for i, row in enumerate(rows):
        cells = row.find_all(["td", "th"])
        for j, cell in enumerate(cells):
            cell_text = cell.get_text(strip=True)
            doc_table.rows[i].cells[j].text = cell_text
            if cell.name == "th":
                for paragraph in doc_table.rows[i].cells[j].paragraphs:
                    for run in paragraph.runs:
                        run.font.bold = True


def process_list_element(
    list_element,
    document: Document,
    content_directory: str,
    level_increase: int,
    processed_files: Set[str],
    list_type: str,
    nesting_level: int,
    markdown_file_path: str,
    root_directory: str,
) -> None:
    """Process nested lists and add them to the document."""
    for li in list_element.find_all("li", recursive=False):
        paragraph = document.add_paragraph(
            style="ListBullet" if list_type == "bullet" else "ListNumber"
        )
        paragraph.paragraph_format.left_indent = LIST_INDENT * nesting_level

        for child in li.children:
            if child.name == "a":
                href = child.get("href", "")
                link_text = child.get_text()
                handled = handle_link(
                    href,
                    os.path.dirname(markdown_file_path),
                    document,
                    paragraph,
                    content_directory,
                    root_directory,
                    level_increase,
                    processed_files,
                    link_text,
                )
                if handled:
                    continue
                paragraph.add_run(link_text)
            elif child.name == "strong":
                run = paragraph.add_run(child.get_text())
                run.bold = True
            elif child.name == "em":
                run = paragraph.add_run(child.get_text())
                run.italic = True
            elif child.name == "code":
                run = paragraph.add_run(child.get_text())
                run.font.name = CODE_FONT_NAME
                run.font.size = CODE_FONT_SIZE
            elif child.name == "img":
                img_src = child.get("src", "")
                img_path = (
                    os.path.join(content_directory, img_src)
                    if not os.path.isabs(img_src)
                    else img_src
                )
                insert_image(document, img_path)
            elif child.name == "ul":
                process_list_element(
                    child,
                    document,
                    content_directory,
                    level_increase,
                    processed_files,
                    list_type="bullet",
                    nesting_level=nesting_level + 1,
                    markdown_file_path=markdown_file_path,
                    root_directory=root_directory,
                )
            elif child.name == "ol":
                process_list_element(
                    child,
                    document,
                    content_directory,
                    level_increase,
                    processed_files,
                    list_type="number",
                    nesting_level=nesting_level + 1,
                    markdown_file_path=markdown_file_path,
                    root_directory=root_directory,
                )
            else:
                paragraph.add_run(str(child))


def process_markdown(
    markdown_file_path: str,
    root_directory: str,
    document: Document,
    content_directory: str,
    level_increase: int = 0,
    skip_h1: bool = False,
    processed_files: Optional[Set[str]] = None,
) -> None:
    """Process a Markdown file and add its content to the document."""
    if processed_files is None:
        processed_files = set()

    if markdown_file_path in processed_files:
        return
    processed_files.add(markdown_file_path)

    with open(markdown_file_path, "r", encoding="utf-8") as f:
        markdown_content = f.read()

    md = markdown.Markdown(extensions=MARKDOWN_EXTENSIONS)
    html_content = md.convert(markdown_content)

    soup = BeautifulSoup(html_content, "html.parser")

    if skip_h1:
        for h1 in soup.find_all("h1"):
            h1.decompose()

    html_content = adjust_headers(str(soup), level_increase)
    soup = BeautifulSoup(html_content, "html.parser")

    for element in soup.children:
        if element.name in ["h1", "h2", "h3", "h4", "h5", "h6"]:
            level = int(element.name[1])
            heading_text = ""
            has_md_link = False

            for child in element.children:
                if child.name == "a" and child.get("href", "").endswith(MD_EXT):
                    href = child.get("href", "")
                    link_text = child.get_text()
                    paragraph = document.add_paragraph()
                    handled = handle_link(
                        href,
                        os.path.dirname(markdown_file_path),
                        document,
                        paragraph,
                        content_directory,
                        root_directory,
                        level_increase,
                        processed_files,
                        link_text,
                        heading_level=level,
                    )
                    if handled:
                        has_md_link = True
                        if paragraph.text:
                            document.paragraphs[-1]._element.getparent().remove(
                                document.paragraphs[-1]._element
                            )
                else:
                    heading_text += (
                        str(child) if child.name is None else child.get_text()
                    )

            if heading_text or not has_md_link:
                heading = document.add_heading(heading_text, level=level)
                format_heading(heading, level)

        elif element.name == "p":
            paragraph = document.add_paragraph()
            for child in element.children:
                if child.name == "a":
                    href = child.get("href", "")
                    link_text = child.get_text()
                    handled = handle_link(
                        href,
                        os.path.dirname(markdown_file_path),
                        document,
                        paragraph,
                        content_directory,
                        root_directory,
                        level_increase,
                        processed_files,
                        link_text,
                    )
                    if handled:
                        continue
                    paragraph.add_run(link_text)
                elif child.name == "strong":
                    run = paragraph.add_run(child.get_text())
                    run.bold = True
                elif child.name == "em":
                    run = paragraph.add_run(child.get_text())
                    run.italic = True
                elif child.name == "code":
                    run = paragraph.add_run(child.get_text())
                    run.font.name = CODE_FONT_NAME
                    run.font.size = CODE_FONT_SIZE
                elif child.name == "img":
                    img_src = child.get("src", "")
                    img_path = (
                        os.path.join(content_directory, img_src)
                        if not os.path.isabs(img_src)
                        else img_src
                    )
                    insert_image(document, img_path)
                else:
                    paragraph.add_run(str(child))
        elif element.name == "ul":
            process_list_element(
                element,
                document,
                content_directory,
                level_increase,
                processed_files,
                list_type="bullet",
                nesting_level=0,
                markdown_file_path=markdown_file_path,
                root_directory=root_directory,
            )
        elif element.name == "ol":
            process_list_element(
                element,
                document,
                content_directory,
                level_increase,
                processed_files,
                list_type="number",
                nesting_level=0,
                markdown_file_path=markdown_file_path,
                root_directory=root_directory,
            )
        elif element.name == "table":
            insert_table(document, str(element))
        elif element.name == "pre":
            code = element.find("code")
            if code:
                insert_code_block(document, code.get_text())


def convert_markdown_to_docx(
    root_directory: str, output_docx: str, content_directory: str
) -> None:
    """Convert Markdown files to a single DOCX file."""
    # Create a new document with custom styles
    document = Document()
    configure_document_style(document)

    readme_path = os.path.join(root_directory, README_FILE)

    if not os.path.exists(readme_path):
        print(f"{README_FILE} not found!")
        return

    with open(readme_path, "r", encoding="utf-8") as f:
        readme_content = f.read()

    md = markdown.Markdown(extensions=MARKDOWN_EXTENSIONS)
    html_content = md.convert(readme_content)
    soup = BeautifulSoup(html_content, "html.parser")

    processed_files = set()
    current_heading_level = 1

    for element in soup.children:
        if element.name in ["h1", "h2", "h3", "h4", "h5", "h6"]:
            level = int(element.name[1])
            heading_text = ""
            has_md_link = False

            for child in element.children:
                if child.name == "a" and child.get("href", "").endswith(MD_EXT):
                    href = child.get("href", "")
                    link_text = child.get_text()
                    paragraph = document.add_paragraph()
                    handled = handle_link(
                        href,
                        root_directory,
                        document,
                        paragraph,
                        content_directory,
                        root_directory,
                        current_heading_level,
                        processed_files,
                        link_text,
                        heading_level=level,
                    )
                    if handled:
                        has_md_link = True
                        if paragraph.text:
                            document.paragraphs[-1]._element.getparent().remove(
                                document.paragraphs[-1]._element
                            )
                else:
                    heading_text += (
                        str(child) if child.name is None else child.get_text()
                    )

            if heading_text or not has_md_link:
                heading = document.add_heading(heading_text, level=level)
                format_heading(heading, level)

        elif element.name == "p":
            paragraph = document.add_paragraph()
            for child in element.children:
                if child.name == "a":
                    href = child.get("href", "")
                    link_text = child.get_text()
                    handled = handle_link(
                        href,
                        root_directory,
                        document,
                        paragraph,
                        content_directory,
                        root_directory,
                        current_heading_level,
                        processed_files,
                        link_text,
                    )
                    if handled:
                        continue
                    paragraph.add_run(link_text)
                elif child.name == "strong":
                    run = paragraph.add_run(child.get_text())
                    run.bold = True
                elif child.name == "em":
                    run = paragraph.add_run(child.get_text())
                    run.italic = True
                elif child.name == "code":
                    run = paragraph.add_run(child.get_text())
                    run.font.name = CODE_FONT_NAME
                    run.font.size = CODE_FONT_SIZE
                elif child.name == "img":
                    img_src = child.get("src", "")
                    img_path = (
                        os.path.join(content_directory, img_src)
                        if not os.path.isabs(img_src)
                        else img_src
                    )
                    insert_image(document, img_path)
                else:
                    paragraph.add_run(str(child))
        elif element.name == "ul":
            process_list_element(
                element,
                document,
                content_directory,
                current_heading_level,
                processed_files,
                list_type="bullet",
                nesting_level=0,
                markdown_file_path=readme_path,
                root_directory=root_directory,
            )
        elif element.name == "ol":
            process_list_element(
                element,
                document,
                content_directory,
                current_heading_level,
                processed_files,
                list_type="number",
                nesting_level=0,
                markdown_file_path=readme_path,
                root_directory=root_directory,
            )
        elif element.name == "table":
            insert_table(document, str(element))
        elif element.name == "pre":
            code = element.find("code")
            if code:
                insert_code_block(document, code.get_text())

    document.save(output_docx)
    print(f"Document saved as {output_docx}")


if __name__ == "__main__":
    root_directory = "."
    content_directory = CONTENT_DIR
    output_docx_file = OUTPUT_FILE
    convert_markdown_to_docx(root_directory, output_docx_file, content_directory)
