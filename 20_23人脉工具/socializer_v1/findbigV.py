import re
from agents.weibo_agent import lookup_v
from tools.scraping_tool import get_data

if __name__ == '__main__':
    response_uid = lookup_v('牡丹')
    print(response_uid)

    UID = re.findall(pattern=r'\d+', string=response_uid, )[0]
    print('大V的UID是', UID)

    data = get_data(UID)
    print(data)
