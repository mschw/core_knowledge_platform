import re
import pdb

def parse_further_arguments(request_dict):
    pdb.set_trace()
    copy_request = request_dict.copy()
    last_item = copy_request.popitem()
    argu_reg = re.compile('(?P<last_argument>[\w\d%]+)?(/author/\?(?P<auth_search>[\w\d%=&]+))?(/keyword/\?(?P<key_search>[\w\d%=&]+))?')
    further_arguments = argu_reg.split(last_item[1])
