import os
import http.client
import threading
import sys
from urllib.parse import urlparse

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

HTTPS_SCHEME = 'https'

HTTP_SCHEME = 'http'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def main(url, file_store_path):
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

    conn.request("GET", path, headers={"Host": host})
    response = conn.getresponse()

    if not str(response.status).startswith('2'):
        url = HTTP_SCHEME + "://" + url
        parsed_url = urlparse(url)
        conn = http.client.HTTPConnection(host)
        conn.request("GET", path, headers={'Host': host})
        response = conn.getresponse()

    content_length = int(response.getheader('content-length', 0))
    print(f"Content length: {content_length}")

    filename = parsed_url.path.split('/')[-1]
    file_path = os.path.join(file_store_path, filename)

    downloaded_size = 0

    with open(file_path, 'wb') as file:
        while True:
            chunk = response.read(1024)
            if not chunk:
                break

            file.write(chunk)
            downloaded_size = update(downloaded_size, content_length, chunk)
        print()

    print(response.status, response.reason)


def update(downloaded_size, total_size, chunk):
    with threading.Lock():
        downloaded_size += len(chunk)
        print(f"\rDownloaded {downloaded_size} bytes out of {total_size}", end="")
    return downloaded_size


if __name__ == "__main__":
    if len(sys.argv) > 1:
        url = sys.argv[1]
        if len(sys.argv) > 2:
            file_store_path = sys.argv[2]
        else:
            file_store_path = PROJECT_ROOT
    main(url)
    else:
        print("Please provide a URL")