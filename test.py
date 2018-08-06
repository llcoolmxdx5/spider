import requests
import os
def get_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'
    }
    response = requests.get(url, headers)
    response.encoding = 'gbk'
    # print(response.status_code)
    if response.status_code == 200:
        return response.text
    return None
    

def main():
    url = 'http://www.biqukan.com/1_1094/17967303.html'
    html = get_page(url)
    print(html)
    # with open('1.txt', 'a', encoding='utf-8') as f:
    #     f.write(html)
        

if __name__ == '__main__':
    main()
