from collections import defaultdict
from pyparsing import Word, alphanums, nums, Optional, Suppress, ZeroOrMore, Group, nestedExpr, QuotedString, originalTextFor 

def remove_parentheses(orig_string, loc, tokens):
    """docstring for remove_parentheses"""
    text = tokens[0]
    text = text.strip()[1:-1]
    if text[0] == '{' and text[-1] == '}':
        text = text.strip()[1:-1]
    return text

class BibtexParser(object):
    """Class used to parse BibTeX entries to Python objects.
    
    Call bib_entry.parseString(string) to parse a single item.
    bib_entry.searchString(string) to parse multiple entries in a single string."""

    at = Suppress('@')
    left_brace = Suppress('{')
    right_brace = Suppress('}')
    comma = Suppress(',')
    quote = Suppress('"')
    equal = Suppress('=')

    braced_value = originalTextFor(nestedExpr('{', '}'))
    braced_value.addParseAction(remove_parentheses)

    quoted_value = QuotedString(quoteChar='"', escChar='\\') 

    number = Word(nums)
    month = Word(alphanums, exact=3)
    value = Word(alphanums+'-.()[]')

    entry_type = value('entry_type')
    field_value = (braced_value | quoted_value | number | month)('field_value')
    key = Suppress(value('key'))
    field_name = value('field_name')
    field = (field_name + equal + field_value)
    fields = Group(field) + ZeroOrMore(comma + Group(field))
    bib_entry = at + entry_type + left_brace + key + ZeroOrMore(comma + fields('fields')) + Optional(comma) + right_brace
    
    # Based On BNR form of BibTeX entries:
    def __init__(self):
        """Constructs the parser"""
        pass
    
    def parse_to_bibtex(self, bibtex_string):
        """Will parse a supplied bibtex string to a dict.

        DEPRECATED: only used for testing purposes."""
        if not bibtex_string:
            raise ValueError("Supplied string was not a valid BibTeX entry.")
        else:
            #result_list = list()
            #single_entries = re.split("(@[\\w\\s]*{[\\w\\s,\\{\\}""\\[\\]]*})", bibtex_string)
            result = self.bib_entry.parseString(bibtex_string)
            dictionary = self._create_nested_dictionaries(result)
            return dictionary

    def _create_nested_dictionaries(self, result):
        dictionary = defaultdict(list)
        dictionary[result.key] = [result.entry_type]
        value_dictionary = dict()
        for item in result.fields:
            value_dictionary[item[0]] = item[1].strip('{}')
        dictionary[result.key].append(value_dictionary)
        return dictionary


