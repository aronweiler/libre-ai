"""
Agentic tool registry and dispatcher for LibreOffice AI extension.
Wraps document_tools.py functions as LangChain tools and exposes a dispatcher for agentic calls.
"""

import logging
from functools import partial, wraps
from langchain.tools import Tool
import extension.tools.document_tools as doc_tools

# Configure logging
logger = logging.getLogger("agentic_tools")
handler = logging.StreamHandler()
formatter = logging.Formatter('[%(asctime)s] %(levelname)s %(name)s: %(message)s')
handler.setFormatter(formatter)
if not logger.hasHandlers():
    logger.addHandler(handler)
logger.setLevel(logging.INFO)

# List of tool functions to expose
TOOL_FUNCTIONS = [
    "insert_section", "delete_section", "set_header", "set_footer",
    "insert_text_at_cursor", "insert_text_at_position", "replace_text",
    "delete_text_range", "apply_character_style", "apply_paragraph_style",
    "set_bold", "set_italic", "set_underline", "set_font_size", "set_font_color",
    "find_text", "count_words", "count_paragraphs", "undo_last_action", "redo_last_action",
    "save_document", "get_document_structure", "get_text", "get_paragraph_text",
    "get_current_cursor_position", "move_cursor_to_position", "insert_image",
    "delete_image", "insert_table", "set_table_cell_text", "delete_table",
    "insert_bullet_list", "insert_numbered_list", "insert_heading"
]

def safe_tool_call(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            logger.info(f"Calling tool: {func.__name__} args={args} kwargs={kwargs}")
            result = func(*args, **kwargs)
            logger.info(f"Tool {func.__name__} result: {result}")
            return result
        except Exception as e:
            logger.error(f"Error in tool {func.__name__}: {e}", exc_info=True)
            raise
    return wrapper

def make_tool(func_name):
    func = getattr(doc_tools, func_name)
    wrapped_func = safe_tool_call(func)
    # Accepts a dict of arguments, unpacks for the function
    def tool_entry(args_dict):
        if not isinstance(args_dict, dict):
            raise ValueError("Tool input must be a dict of arguments.")
        return wrapped_func(**args_dict)
    tool_entry.__doc__ = func.__doc__
    return Tool(
        name=func_name,
        func=tool_entry,
        description=func.__doc__ or f"Call {func_name} from document_tools"
    )

# Registry of LangChain tools
AGENTIC_TOOLS = [make_tool(name) for name in TOOL_FUNCTIONS]
TOOL_REGISTRY = {tool.name: tool for tool in AGENTIC_TOOLS}

def call_tool(tool_name, **kwargs):
    """Call a registered tool by name with keyword arguments. Logs call and errors."""
    tool = TOOL_REGISTRY.get(tool_name)
    if not tool:
        logger.error(f"Tool '{tool_name}' not found.")
        raise ValueError(f"Tool '{tool_name}' not found.")
    try:
        logger.info(f"Dispatching tool '{tool_name}' with args: {kwargs}")
        result = tool.run(kwargs)
        logger.info(f"Tool '{tool_name}' completed successfully.")
        return result
    except Exception as e:
        logger.error(f"Tool '{tool_name}' failed: {e}", exc_info=True)
        raise
