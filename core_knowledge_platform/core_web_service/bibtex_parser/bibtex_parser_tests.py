import unittest
from bibtex_parser import BibtexParser
from pyparsing import ParseException

class BibTeXParserTests(unittest.TestCase):
    """Class to store BibTeXParser unittests"""

    def setUp(self):
        self.parser = BibtexParser()
        self.book_bibtex = """@book{Anderson2007,
    title = {{What is Web 2.0?: ideas, technologies and implications for education}},
    publisher = {Citeseer},
    year = {2007},
    author = {Andersen, P.},
    booktitle = {Technology},
    file = {:media/datapart/Dokumente/eBooks/master\_thesis/Articles/10.1.1.108.9995.pdf:pdf},
    keywords = {Web 2.0},
    url = {http://www.jisc.ac.uk/media/documents/techwatch/tsw0701b.pdf}
}"""
        self.book_dict = {'Anderson2007': ['book', {
            'title': 'What is Web 2.0?: ideas, technologies and implications for education',
            'publisher': 'Citeseer',
            'year': '2007',
            'author': 'Andersen, P.',
            'booktitle': 'Technology',
            'file': ':media/datapart/Dokumente/eBooks/master\_thesis/Articles/10.1.1.108.9995.pdf:pdf',
            'keywords': 'Web 2.0',
            'url': 'http://www.jisc.ac.uk/media/documents/techwatch/tsw0701b.pdf'
            }]
            }

    def test_empty_bibtex_entry(self):
        """Parsing nothing will return nothing."""
        self.assertRaises(ValueError, self.parser.parse_to_bibtex, "")

    def test_entry_without_attribute(self):
        """Parsing only the key."""
        bibtex = "@book{none}"
        parsed = self.parser.parse_to_bibtex(bibtex)
        self.assertEqual({'none': ['book', {}]}, parsed)

    def test_parse_single_field(self):
        """Parsing a single key = value pair."""
        field = "name = {value}"
        parsed = self.parser.field.parseString(field).asList()
        self.assertEqual(['name', 'value'], parsed)

    def test_entry_with_single_attribute_in_quotes(self):
        """Parsing an attribute enclosed in quotes."""
        bibtex = """@book{key,
                    value = "test"
                    }"""
        parsed = self.parser.parse_to_bibtex(bibtex)
        result_dict = {'key': ['book', {'value': 'test'}]}
        self.assertEqual(result_dict, parsed)

    def test_entry_with_single_attribute_in_braces(self):
        """Parsing an attribute enclosed in braces."""
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

    def test_braces_within_delimeters(self):
        """docstring for test_braces_within_delimeters"""
        bibtex = """@book{key,
                          value = {t{e}st},
                          value2 = "t{e}st2"
                          }"""
        parsed = self.parser.parse_to_bibtex(bibtex)
        result_dict = {'key': ['book', {'value': 't{e}st', 'value2': 't{e}st2'}]}
        self.assertEqual(result_dict, parsed)

    def test_number_can_be_unquoted(self):
        """docstring for test_number_can_be_unquoted"""
        bibtex = """@book{key,
                          value2 = 2008
                          }"""
        parsed = self.parser.parse_to_bibtex(bibtex)
        result_dict = {'key': ['book', {'value2': '2008'}]}
        self.assertEqual(result_dict, parsed)

    def test_delimeters_can_not_be_mixed(self):
        """docstring for test_delimeters_can_not_be_mixed"""
        bibtex = """@book{key,
                    value = "test},
                    value2 = {test2"
                    }"""
        self.assertRaises(ParseException, self.parser.parse_to_bibtex, bibtex)

    def test_complex_book_insertion(self):
        parsed = self.parser.parse_to_bibtex(self.book_bibtex)
        print parsed
        self.assertEqual(self.book_dict, parsed)


    #def test_parsing_multiple_entries(self):
    #    bibtex = """@book{key,
    #                value = "test",
    #                value2 = "test2"
    #                }
    #                
    #                @book{key2,
    #                value = "test",
    #                value2 = "test2"
    #                }"""
    #    parsed = self.parser.parse_to_bibtex(bibtex)
    #    result_dict = {'key': ['book', {'value2', '2008'}], 'key2': ['book', {'value2', '2008'}]}
    #    self.assertEqual(result_dict, parsed)

if __name__ == '__main__':
    unittest.main()
