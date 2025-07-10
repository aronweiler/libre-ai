# --- Search & Analysis ---
def find_text(query: str, match_case: bool = False, whole_words: bool = False) -> list[tuple[int, int]]:
    doc = get_document()
    search = doc.createSearchDescriptor()
    search.SearchString = query
    search.SearchCaseSensitive = match_case
    search.SearchWords = whole_words
    found = doc.findAll(search)
    results = []
    for i in range(found.getCount()):
        item = found.getByIndex(i)
        start = item.getStart()
        end = item.getEnd()
        results.append((start.getOffset(), end.getOffset()))
    return results

def count_words() -> int:
    doc = get_document()
    return len(doc.Text.getString().split())

def count_paragraphs() -> int:
    doc = get_document()
    enum = doc.Text.createEnumeration()
    count = 0
    while enum.hasMoreElements():
        enum.nextElement()
        count += 1
    return count
# --- Undo, Redo, and Document Management ---
def undo_last_action() -> bool:
    try:
        doc = get_document()
        dispatcher = doc.CurrentController.Frame.queryDispatch(
            uno.createUnoStruct('com.sun.star.util.URL'), '', 0)
        dispatcher.executeDispatch(doc.CurrentController.Frame, ".uno:Undo", "", 0, tuple())
        return True
    except Exception:
        return False

def redo_last_action() -> bool:
    try:
        doc = get_document()
        dispatcher = doc.CurrentController.Frame.queryDispatch(
            uno.createUnoStruct('com.sun.star.util.URL'), '', 0)
        dispatcher.executeDispatch(doc.CurrentController.Frame, ".uno:Redo", "", 0, tuple())
        return True
    except Exception:
        return False

def save_document() -> bool:
    try:
        doc = get_document()
        doc.store()
        return True
    except UnoException:
        return False
# --- Sections, Headers, and Footers ---
def insert_section(name: str, position = None) -> bool:
    try:
        doc = get_document()
        text = doc.Text
        cursor = text.createTextCursor()
        if position is not None:
            cursor.goRight(position, False)
        section = doc.createInstance("com.sun.star.text.TextSection")
        section.setName(name)
        text.insertTextContent(cursor, section, False)
        return True
    except UnoException:
        return False

def delete_section(name: str) -> bool:
    try:
        doc = get_document()
        sections = doc.getTextSections()
        if not sections.hasByName(name):
            return False
        section = sections.getByName(name)
        section.dispose()
        return True
    except UnoException:
        return False

def set_header(text: str, page_style: str = 'Default') -> bool:
    try:
        doc = get_document()
        style = doc.StyleFamilies.getByName('PageStyles').getByName(page_style)
        style.HeaderIsOn = True
        style.HeaderText = text
        return True
    except UnoException:
        return False

def set_footer(text: str, page_style: str = 'Default') -> bool:
    try:
        doc = get_document()
        style = doc.StyleFamilies.getByName('PageStyles').getByName(page_style)
        style.FooterIsOn = True
        style.FooterText = text
        return True
    except UnoException:
        return False
# --- Document Structure & Navigation ---
def get_document_structure() -> dict:
    doc = get_document()
    structure = {"headings": [], "paragraphs": [], "tables": [], "images": []}
    # Headings and paragraphs
    enum = doc.Text.createEnumeration()
    idx = 0
    while enum.hasMoreElements():
        para = enum.nextElement()
        style = getattr(para, 'ParaStyleName', '')
        text = para.getString()
        if style.startswith("Heading"):
            structure["headings"].append({"index": idx, "text": text, "style": style})
        else:
            structure["paragraphs"].append({"index": idx, "text": text, "style": style})
        idx += 1
    # Tables
    tables = doc.getTextTables()
    for name in tables.getElementNames():
        structure["tables"].append(name)
    # Images
    graphics = doc.getGraphicObjects()
    for name in graphics.getElementNames():
        structure["images"].append(name)
    return structure

def get_text(start: int, end: int) -> str:
    doc = get_document()
    cursor = doc.Text.createTextCursor()
    cursor.goRight(start, False)
    cursor.goRight(end - start, True)
    return cursor.getString()

def get_paragraph_text(paragraph_index: int) -> str:
    doc = get_document()
    enum = doc.Text.createEnumeration()
    idx = 0
    while enum.hasMoreElements():
        para = enum.nextElement()
        if idx == paragraph_index:
            return para.getString()
        idx += 1
    return ""

def get_current_cursor_position() -> int:
    doc = get_document()
    view_cursor = doc.CurrentController.getViewCursor()
    return view_cursor.getPosition()

def move_cursor_to_position(position: int) -> bool:
    try:
        doc = get_document()
        view_cursor = doc.CurrentController.getViewCursor()
        view_cursor.gotoStart(False)
        view_cursor.goRight(position, False)
        return True
    except UnoException:
        return False
# --- Images ---
def insert_image(image_path: str, position = None, width = None, height = None) -> bool:
    try:
        doc = get_document()
        text = doc.Text
        cursor = text.createTextCursor()
        if position is not None:
            cursor.goRight(position, False)
        graphic = doc.createInstance("com.sun.star.text.TextGraphicObject")
        graphic.GraphicURL = uno.systemPathToFileUrl(image_path)
        if width:
            graphic.Width = width
        if height:
            graphic.Height = height
        text.insertTextContent(cursor, graphic, False)
        return True
    except UnoException:
        return False

def delete_image(image_index: int) -> bool:
    try:
        doc = get_document()
        graphics = doc.getGraphicObjects()
        names = graphics.getElementNames()
        if image_index >= len(names):
            return False
        graphic = graphics.getByName(names[image_index])
        graphic.dispose()
        return True
    except UnoException:
        return False
# --- Tables ---
def insert_table(rows: int, columns: int, position = None, data = None) -> bool:
    try:
        doc = get_document()
        text = doc.Text
        cursor = text.createTextCursor()
        if position is not None:
            cursor.goRight(position, False)
        table = doc.createInstance("com.sun.star.text.TextTable")
        table.initialize(rows, columns)
        text.insertTextContent(cursor, table, False)
        if data:
            for r, row in enumerate(data):
                for c, value in enumerate(row):
                    table.getCellByPosition(c, r).setString(value)
        return True
    except UnoException:
        return False

def set_table_cell_text(table_index: int, row: int, column: int, text: str) -> bool:
    try:
        doc = get_document()
        tables = doc.getTextTables()
        names = tables.getElementNames()
        if table_index >= len(names):
            return False
        table = tables.getByName(names[table_index])
        cell = table.getCellByPosition(column, row)
        cell.setString(text)
        return True
    except UnoException:
        return False

def delete_table(table_index: int) -> bool:
    try:
        doc = get_document()
        tables = doc.getTextTables()
        names = tables.getElementNames()
        if table_index >= len(names):
            return False
        table = tables.getByName(names[table_index])
        table.dispose()
        return True
    except UnoException:
        return False
# --- Lists & Headings ---
def insert_bullet_list(items, position = None) -> bool:
    try:
        doc = get_document()
        cursor = doc.Text.createTextCursor()
        if position is not None:
            cursor.goRight(position, False)
        for item in items:
            doc.Text.insertString(cursor, f"• {item}\n", False)
        return True
    except UnoException:
        return False

def insert_numbered_list(items, position = None) -> bool:
    try:
        doc = get_document()
        cursor = doc.Text.createTextCursor()
        if position is not None:
            cursor.goRight(position, False)
        for i, item in enumerate(items, 1):
            doc.Text.insertString(cursor, f"{i}. {item}\n", False)
        return True
    except UnoException:
        return False

def insert_heading(text: str, level: int = 1, position = None) -> bool:
    try:
        doc = get_document()
        cursor = doc.Text.createTextCursor()
        if position is not None:
            cursor.goRight(position, False)
        doc.Text.insertString(cursor, text + "\n", False)
        cursor.gotoStartOfParagraph(False)
        cursor.gotoEndOfParagraph(True)
        cursor.ParaStyleName = f"Heading {level}"
        return True
    except UnoException:
        return False
"""
Document Editing Toolset: Python functions to manipulate Writer documents via UNO API.
"""

# --- UNO API imports ---
import uno
from com.sun.star.uno import Exception as UnoException
from com.sun.star.beans import PropertyValue
from com.sun.star.text.ControlCharacter import PARAGRAPH_BREAK

def get_document():
    """Get the current Writer document via UNO."""
    ctx = uno.getComponentContext()
    smgr = ctx.ServiceManager
    desktop = smgr.createInstanceWithContext("com.sun.star.frame.Desktop", ctx)
    model = desktop.getCurrentComponent()
    if not model or not hasattr(model, 'Text'):  # Not a Writer doc
        raise RuntimeError("No Writer document is open.")
    return model

def get_document_context() -> dict:
    """Extract basic context: word count, paragraph count, etc."""
    doc = get_document()
    text = doc.Text
    paragraphs = text.createEnumeration()
    para_count = 0
    for _ in paragraphs:
        para_count += 1
    word_count = len(text.getString().split())
    return {"word_count": word_count, "paragraph_count": para_count}

def insert_text_at_cursor(text: str) -> bool:
    """Insert the given text at the current cursor position."""
    try:
        doc = get_document()
        view_cursor = doc.CurrentController.getViewCursor()
        view_cursor.setString(text)
        return True
    except UnoException:
        return False

def insert_text_at_position(text: str, position: int) -> bool:
    """Insert text at the specified character position."""
    try:
        doc = get_document()
        cursor = doc.Text.createTextCursor()
        cursor.goRight(position, False)
        doc.Text.insertString(cursor, text, False)
        return True
    except UnoException:
        return False

def replace_text(old: str, new: str, match_case: bool = False, whole_words: bool = False) -> int:
    """Replace all occurrences of 'old' with 'new'. Returns the number of replacements made."""
    doc = get_document()
    search = doc.createSearchDescriptor()
    search.SearchString = old
    search.SearchCaseSensitive = match_case
    search.SearchWords = whole_words
    found = doc.findAll(search)
    count = found.getCount()
    for i in range(count):
        found_item = found.getByIndex(i)
        found_item.setString(new)
    return count

def delete_text_range(start: int, end: int) -> bool:
    """Delete text between the specified character positions."""
    try:
        doc = get_document()
        cursor = doc.Text.createTextCursor()
        cursor.goRight(start, False)
        cursor.goRight(end - start, True)
        cursor.setString("")
        return True
    except UnoException:
        return False

# --- Formatting & Styles ---
def apply_character_style(style_name: str, start: int, end: int) -> bool:
    try:
        doc = get_document()
        cursor = doc.Text.createTextCursor()
        cursor.goRight(start, False)
        cursor.goRight(end - start, True)
        cursor.CharStyleName = style_name
        return True
    except UnoException:
        return False

def apply_paragraph_style(style_name: str, paragraph_index: int) -> bool:
    try:
        doc = get_document()
        enum = doc.Text.createEnumeration()
        idx = 0
        while enum.hasMoreElements():
            para = enum.nextElement()
            if idx == paragraph_index:
                para.ParaStyleName = style_name
                return True
            idx += 1
        return False
    except UnoException:
        return False

def set_bold(start: int, end: int, bold: bool = True) -> bool:
    try:
        doc = get_document()
        cursor = doc.Text.createTextCursor()
        cursor.goRight(start, False)
        cursor.goRight(end - start, True)
        cursor.CharWeight = 150 if bold else 100
        return True
    except UnoException:
        return False

def set_italic(start: int, end: int, italic: bool = True) -> bool:
    try:
        doc = get_document()
        cursor = doc.Text.createTextCursor()
        cursor.goRight(start, False)
        cursor.goRight(end - start, True)
        cursor.CharPosture = 2 if italic else 0
        return True
    except UnoException:
        return False

def set_underline(start: int, end: int, underline: bool = True) -> bool:
    try:
        doc = get_document()
        cursor = doc.Text.createTextCursor()
        cursor.goRight(start, False)
        cursor.goRight(end - start, True)
        cursor.CharUnderline = 1 if underline else 0
        return True
    except UnoException:
        return False

def set_font_size(start: int, end: int, size: float) -> bool:
    try:
        doc = get_document()
        cursor = doc.Text.createTextCursor()
        cursor.goRight(start, False)
        cursor.goRight(end - start, True)
        cursor.CharHeight = size
        return True
    except UnoException:
        return False

def set_font_color(start: int, end: int, color: str) -> bool:
    try:
        doc = get_document()
        cursor = doc.Text.createTextCursor()
        cursor.goRight(start, False)
        cursor.goRight(end - start, True)
        cursor.CharColor = int(color.lstrip('#'), 16)
        return True
    except UnoException:
        return False
