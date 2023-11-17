import re
from agents.weibo_agent import lookup_v
from tools.scraping_tool import get_person_info

from tools.textgen_tool import generate_letter

if __name__ == '__main__':
    response_uid = lookup_v('百合')
    print(response_uid)

    UID = re.findall(pattern=r'\d+', string=response_uid, )[0]
    print('大V的UID是', UID)

    person_info = get_person_info(UID)
    print(person_info)

    result = generate_letter(person_info)
    print(result)
