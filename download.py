#!/usr/bin/env python3
import requests
import argparse


def download(url, filename):
    try:
        print('[+] Downloading...')
        response = requests.get(url)
        with open(filename, 'wb') as file:
            file.write(response.content)
    except Exception as e:
        print('[!] Exception - {}'.format(e))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', dest='url', help='Download URL.', required=True)
    parser.add_argument('-f', dest='filename', help='Filename and extension.', required=True)
    args = parser.parse_args()
    download(args.url, args.filename)
