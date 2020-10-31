import requests
from urllib.parse import urlencode
import sys


def download(shared_url, filename):
    base_url = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?'
    final_url = base_url + urlencode(dict(public_key=shared_url))
    
    response = requests.get(final_url)
    download_url = response.json()['href']
    
    download_response = requests.get(download_url)
    
    with open(filename, 'wb') as f:
        f.write(download_response.content)


if __name__ == "__main__":
    shared_url = sys.argv[1]
    filename = sys.argv[2]
    
    download(shared_url, filename)
