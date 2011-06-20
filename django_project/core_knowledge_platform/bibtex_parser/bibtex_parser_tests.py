import unittest
from bibtex_parser import BibTeXParser

class BibTeXParserTests(unittest.TestCase):
    """Class to store BibTeXParser unittests"""

    def setUp(self):
        self.parser = BibTeXParser()

    def test_empty_bibtex_entry(self):
        """Parsing nothing will return nothing."""
        self.assertRaises(ValueError, self.parser.parse_to_bibtex, "")

    def test_entry_without_attribute(self):
        """Parsing only the key."""
        bibtex = "@book{none}"
        parsed = self.parser.parse_to_bibtex(bibtex)
        self.assertEqual({'none': ['book', {}]}, parsed)

    def test_entry_with_single_attribute_in_quotes(self):
        """docstring for test_entry_with_single_attribute"""
        bibtex = """@book{key,
                    value = "test"
                    }"""
        parsed = self.parser.parse_to_bibtex(bibtex)
        result_dict = {'key': ['book', {'value': 'test'}]}
        self.assertEqual(result_dict, parsed)

    def test_entry_with_single_attribute_in_braces(self):
        """docstring for test_entry_with_single_attribute"""
        bibtex = """@book{key,
                    value = {test}
                    }"""
        parsed = self.parser.parse_to_bibtex(bibtex)
        result_dict = {'key': ['book', {'value': 'test'}]}
        self.assertEqual(result_dict, parsed)

    def test_entry_with_multiple_attributes(self):
        """Multiple attributes with equal delimeters."""
        bibtex = """@book{key,
                          value = {test},
                          value2 = {test2}
                          }"""
        parsed = self.parser.parse_to_bibtex(bibtex)
        result_dict = {'key': ['book', {'value': 'test', 'value2': 'test2'}]}
        self.assertEqual(result_dict, parsed)

    def test_delimeters_can_not_be_mixed(self):
        """docstring for test_delimeters_can_not_be_mixed"""
        pass
    
    def test_parse_single_field(self):
        field = "name = {value}"
        parsed = self.parser.field.parseString(field).asList()
        self.assertEqual([['name', 'value']], parsed)

if __name__ == '__main__':
    unittest.main()
