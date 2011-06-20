from pyparsing import Word, alphas, alphanums, oneOf, Forward, Optional, Group, Suppress
from collections import defaultdict

class BibTeXParser(object):
    """Class used to parse BibTeX entries to Python objects."""
    at = Suppress('@')
    left_brace = Suppress('{')
    right_brace = Suppress('}')
    comma = Suppress(',')
    quote = Suppress('"')
    equal = Suppress('=')
    delimeter = Suppress(oneOf(" ".join('{ } "')))

    # TODO: delimeters can be mixed with this definition!
    entry_type = Word(alphas)('entry_type')
    value = Word(alphanums)
    field_value = value
    key = value('key')
    field_name = Word(alphanums)
    field = (field_name('field_name') + equal + delimeter + field_value('field_value') + delimeter)('field')
    fields = Forward()
    fields << field + Optional(comma + fields)
    bib_entry = at + entry_type + left_brace + key + Optional(comma + fields) + right_brace
    
    # Based On BNR form of BibTeX entries:
    def __init__(self):
        """Constructs the parser"""
        pass
    
    def parse_to_bibtex(self, bibtex_string):
        """Will parse a supplied bibtex string to a dict."""
        if not bibtex_string:
            raise ValueError("Supplied string was not a valid BibTeX entry.")
        else:
            result = self.bib_entry.parseString(bibtex_string)
            dictionary = defaultdict(list)
            dictionary[result.key] = [result.entry_type]
            value_dictionary = dict()
            for item in result.field:
                print "List item is %s " % (item)
                value_dictionary[item[0]] = item[1] 
            dictionary[result.key].append(value_dictionary)
            return dictionary 

