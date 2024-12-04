import os
import http.client
import threading
import time
import sys
from urllib.parse import urlparse

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

HTTPS_SCHEME = 'https'

HTTP_SCHEME = 'http'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def main(url):
    parsed_url = urlparse(url)
    print(parsed_url)

    if parsed_url.scheme == '':
        url = HTTPS_SCHEME + "://" + url
        parsed_url = urlparse(url)

    host = parsed_url.netloc
    path = parsed_url.path

    if parsed_url.scheme == HTTPS_SCHEME:
        conn = http.client.HTTPSConnection(host)
    else:
        conn = http.client.HTTPConnection(host)

    conn.request("GET", path, headers={"Host": host, 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})
    response = conn.getresponse()

    if not str(response.status).startswith('2'):
        url = HTTP_SCHEME + "://" + url
        parsed_url = urlparse(url)
        conn = http.client.HTTPConnection(host)
        conn.request("GET", path, headers={'Host': host, 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})
        response = conn.getresponse()

    content_length = int(response.getheader('content-length', 0))
    print(f"Content length: {content_length}")

    filename = "test"  #todo создавать рандомное? или можно как-то сразу получить?
    file_path = os.path.join(PROJECT_ROOT, filename)

    downloaded_size = 0

    with open(file_path + '.jpg', 'wb') as file:
        while True:
            chunk = response.read(8192)
            if not chunk:
                break

            file.write(chunk)
            update(downloaded_size, content_length, chunk)
            time.sleep(1)

    print(response.headers)

    print(response.status, response.reason)


def update(downloaded_size, total_size, chunk):
    with threading.Lock():
        downloaded_size += len(chunk)
        if total_size == 0:
            total_size = downloaded_size
        print(f"\rСкачано {downloaded_size} байт из {total_size}", end="")


if __name__ == "__main__":
    main('testurl')
