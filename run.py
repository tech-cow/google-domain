#!/usr/bin/env python3
from termcolor import colored
import json
import datetime
import random
import pprint
import re
import sys
import tldextract
import requests
sys.path.insert(0, '/Users/yui/Dropbox')
import config


def get_dom():
    """Get Domain List and parse into an array"""
    res = []
    with open('list.txt') as f:
        lines = f.readlines()
        for line in lines:
            url = "".join(
                re.findall(
                    'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+',
                    line))
            domain = tldextract.extract(url).domain
            res.append("".join(domain))
        return res


def dom_check(names):
    """Check Availibility of the array"""
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
            symbol = '✓'
            output(company, symbol)
        else:
            symbol = 'x'
            output(company, symbol)


def output(name, status):
    with open('richlist.txt', 'a') as f:
        f.write(name + ' ' + status + ' ' + '\n')

# url = 'http://maps.googleapis.com/maps/api/directions/json'


def sort():
    with open('richlist.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            if "✓" in line:
                with open('rich.txt', 'a') as f:
                    f.write(line[:-5] + '\n')


if __name__ == '__main__':
    # print(dom_check())
    # name = get_dom()
    # dom_check(name)
    sort()
