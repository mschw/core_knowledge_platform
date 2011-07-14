from core_web_service.business_logic,parse import parse_further_arguments
from django.http import QueryDict

class ParseLogicTests(unittest.TestCase):

    def test_parse_string(self):
        """docstring for test_parse_string"""
        query_dict = QueryDict('?name=test/author/?name=test')
        parse_further_arguments(query_dict)
