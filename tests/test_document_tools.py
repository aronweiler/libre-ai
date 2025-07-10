import unittest
from extension.tools import document_tools

class TestDocumentTools(unittest.TestCase):
    def test_get_document_context(self):
        ctx = document_tools.get_document_context()
        self.assertIsInstance(ctx, dict)

    # Add more tests for insert_text, replace_text, delete_text

if __name__ == '__main__':
    unittest.main()
