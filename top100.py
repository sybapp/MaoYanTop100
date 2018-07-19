import requests
from requests.exceptions import RequestException
import re
import multiprocessing
import time
import json


def get_page(offset):
    url = 'https://maoyan.com/board/4?offset=' + str(offset)
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      + 'Chrome/67.0.3396.99 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求出错！')
        return None


def parse_page(html):
    pattern = re.compile(r'<dd>.*?board-index.*?>(\d+)</i>'
                         + r'.*?title="(.*?)"'
                         + r'.*?data-src="(.*?)"'
                         + r'.*?star">(.*?)</p>'
                         + r'.*?releasetime">(.*?)</p>'
                         + r'.*?integer">(.*?)</i>.*?fraction">(\d)</i>', re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield {
            '排名': item[0],
            '片名': item[1],
            '海报': item[2],
            '主演': item[3].strip()[3:],
            '上映时间': item[4].strip()[5:],
            '评分': item[5]+item[6]
        }


def result(offset):
    html = get_page(offset)
    for i in parse_page(html):
        print(i)
        save_to_file(i)


def save_to_file(content):
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')
        f.close()


if __name__ == '__main__':
    start = time.time()
    pool = multiprocessing.Pool()
    pool.map(result, [i for i in range(0, 100, 10)])
    pool.close()
    pool.join()
    # for i in range(0, 100, 10):
    #     result(i)
    end = time.time()
    print(end - start)
