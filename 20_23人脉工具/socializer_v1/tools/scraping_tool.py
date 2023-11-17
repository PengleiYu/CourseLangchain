import json
import requests
import time
from .general_tool import remove_non_chinese_fields


def scrape_weibo(url: str):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
        "Referer": "https://weibo.com",
    }
    cookies = {
        "cookie": '''XSRF-TOKEN=n47E81sZ0KEpetH9hbVLTl35; PC_TOKEN=3df6c6d090; login_sid_t=170d94881f4aaec6b212b23e11e1a3d4; cross_origin_proto=SSL; wb_view_log=1440*25601; _s_tentry=-; SCF=Arj7ATp1iKcMrNzCLtt-CF-Zn_5PK1N5-sGJdorhq_J-Xam3V99RhAa7GJll2QsJP5bJz7cxv86kCVKN0_H00Cg.; SUB=_2A25IUmb_DeRhGeVP6FIW8i_KzT-IHXVrLuY3rDV8PUNbmtANLWLMkW9NTUFzo2AmglKdQAa0McYIdBzr6iEd8lqI; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWs5d8ilTVK6SfXkTFEGeWJ5JpX5KzhUgL.Foepe05Neo2cSoe2dJLoIpxNIs8XTg8E9Cf4dN-_9rHoIcLV97tt; ALF=1731676718; SSOLoginState=1700140719; WBPSESS=us-MydWfL57Gj1YajCUqa1hJZEtHvokWheBUmRCwrcgAM419WA6Lb4d1ePpqIAKRfpX5J9c-jgctHFEOyk19mO2py1ueWKSQUWnyQ6-DN1vywMir0lgl8pXHJUaO7HsPp9EexKH1hp3sQwzngrJ3EQ==''',
    }
    response = requests.get(url, headers=headers, cookies=cookies)
    time.sleep(3)
    return response.text


def get_data(id: str):
    url = f"https://weibo.com/ajax/profile/detail?uid={id}"
    response = scrape_weibo(url)
    person_info = json.loads(response)
    remove_non_chinese_fields(person_info)
    return person_info
