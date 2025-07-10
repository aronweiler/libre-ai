# **Toolset for LibreOffice Writer AI Editing**

Below are the proposed Python function signatures (with type hints and return types), grouped by category, along with brief descriptions.

Each of these tools should be fully implemented in a cross-platform manner, with proper error handling and relevant return values.

---

## **Text Insertion & Replacement**

```python
def insert_text_at_cursor(text: str) -> bool:
    """Insert the given text at the current cursor position. Returns True if successful."""
    
def insert_text_at_position(text: str, position: int) -> bool:
    """Insert text at the specified character position in the document. Returns True if successful."""

def replace_text(old: str, new: str, match_case: bool = False, whole_words: bool = False) -> int:
    """Replace all occurrences of 'old' with 'new'. Returns the number of replacements made."""

def delete_text_range(start: int, end: int) -> bool:
    """Delete text between the specified character positions. Returns True if successful."""
```

---

## **Formatting & Styles**

```python
def apply_character_style(style_name: str, start: int, end: int) -> bool:
    """Apply a character style to the text between start and end positions."""

def apply_paragraph_style(style_name: str, paragraph_index: int) -> bool:
    """Apply a paragraph style to the specified paragraph index."""

def set_bold(start: int, end: int, bold: bool = True) -> bool:
    """Set or unset bold formatting for the specified text range."""

def set_italic(start: int, end: int, italic: bool = True) -> bool:
    """Set or unset italic formatting for the specified text range."""

def set_underline(start: int, end: int, underline: bool = True) -> bool:
    """Set or unset underline formatting for the specified text range."""

def set_font_size(start: int, end: int, size: float) -> bool:
    """Set the font size for the specified text range."""

def set_font_color(start: int, end: int, color: str) -> bool:
    """Set the font color (hex string, e.g., '#FF0000') for the specified text range."""
```

---

## **Lists & Headings**

```python
def insert_bullet_list(items: list[str], position: int = None) -> bool:
    """Insert a bulleted list at the specified position (or at cursor if None)."""

def insert_numbered_list(items: list[str], position: int = None) -> bool:
    """Insert a numbered list at the specified position (or at cursor if None)."""

def insert_heading(text: str, level: int = 1, position: int = None) -> bool:
    """Insert a heading of the given level (1-6) at the specified position."""
```

---

## **Tables**

```python
def insert_table(rows: int, columns: int, position: int = None, data: list[list[str]] = None) -> bool:
    """Insert a table at the specified position, optionally pre-filled with data."""

def set_table_cell_text(table_index: int, row: int, column: int, text: str) -> bool:
    """Set the text of a specific cell in a table."""

def delete_table(table_index: int) -> bool:
    """Delete the specified table from the document."""
```

---

## **Images**

```python
def insert_image(image_path: str, position: int = None, width: int = None, height: int = None) -> bool:
    """Insert an image from the given path at the specified position, optionally resizing it."""

def delete_image(image_index: int) -> bool:
    """Delete the specified image from the document."""
```

---

## **Document Structure & Navigation**

```python
def get_document_structure() -> dict:
    """Return a structured representation of headings, paragraphs, tables, images, etc."""

def get_text(start: int, end: int) -> str:
    """Return the text between the specified character positions."""

def get_paragraph_text(paragraph_index: int) -> str:
    """Return the text of the specified paragraph."""

def get_current_cursor_position() -> int:
    """Return the current cursor position in the document."""

def move_cursor_to_position(position: int) -> bool:
    """Move the cursor to the specified character position."""
```

---

## **Sections, Headers, and Footers**

```python
def insert_section(name: str, position: int = None) -> bool:
    """Insert a named section at the specified position."""

def delete_section(name: str) -> bool:
    """Delete the section with the given name."""

def set_header(text: str, page_style: str = 'Default') -> bool:
    """Set the header text for the specified page style."""

def set_footer(text: str, page_style: str = 'Default') -> bool:
    """Set the footer text for the specified page style."""
```

---

## **Undo, Redo, and Document Management**

```python
def undo_last_action() -> bool:
    """Undo the last document action."""

def redo_last_action() -> bool:
    """Redo the previously undone action."""

def save_document() -> bool:
    """Save the current document."""
```

---

## **Search & Analysis**

```python
def find_text(query: str, match_case: bool = False, whole_words: bool = False) -> list[tuple[int, int]]:
    """Find all occurrences of the query and return their (start, end) positions."""

def count_words() -> int:
    """Return the total word count of the document."""

def count_paragraphs() -> int:
    """Return the total number of paragraphs in the document."""
```
