import re
from agents.weibo_agent import lookup_v
from tools.scraping_tool import get_person_info

from tools.textgen_tool import generate_letter


def find_big_v(flower_type: str) -> dict:
    response_uid = lookup_v(flower_type)
    print(response_uid)
    matches = re.findall(pattern=r'\d+', string=response_uid, )
    print(matches)
    uid = matches[0]
    print('大V的UID是', uid)
    person_info = get_person_info(uid)
    print(person_info)
    result = generate_letter(person_info)
    print(f'result={result}')
    return result.to_dict()


if __name__ == '__main__':
    find_big_v('牵牛花')
