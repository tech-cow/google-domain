#!/usr/bin/env python3
import re
import sys
import json
import pprint
import datetime
import platform

import requests
import tldextract

"""config.py"""
if platform.system() == "Windows":
    sys.path.insert(0, r'C:\Users\yuzhou\Dropbox')
if platform.system() == "Darwin":
    sys.path.insert(0, '/Users/yui/Dropbox')
import config


def get_dom():
    """
    Parse data from `top_1000_list.txt` and grab companies' URL names
    :rtype: <list>
    """
    res = []
    with open('top_1000_list.txt', encoding='utf-8', mode='r') as f:
        lines = f.readlines()
        for line in lines:
            url = "".join(re.findall(
                'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', line))
            domain = tldextract.extract(url).domain
            res.append("".join(domain))
        return res


def dom_check(names):
    """
    Looping over each company and check availibility of its Google Domain
    :rtype: <txt file>
    """
    for name in names:
        company = name + ".app"
        response = requests.get(
            "https://domainr.p.mashape.com/v2/status?mashape-key=&domain=" +
            company,
            headers={
                "X-Mashape-Key": config.mashape_key,
                "Accept": "application/json"})
        temp_dict = json.loads(response.text)
        status = temp_dict["status"][0]["status"]

        if status.endswith('inactive'):
            symbol = '✓'
            with open('check_list.txt', encoding='utf-8', mode='a') as f:
                f.write(company + ' ' + symbol + ' ' + '\n')


def main():
    names = get_dom()
    dom_check(names)


if __name__ == '__main__':
    main()
