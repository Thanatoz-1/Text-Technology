#!/usr/bin/env python
# coding: utf-8

# The functions abelow are used to parse the grobid results, and format them to 
# a python dictionary object

import re
import os
import sys
from glob import glob
import urllib
import subprocess
import json
import requests
import lxml
from bs4 import BeautifulSoup
from tqdm import tqdm

# We need to run ```./gradlew run``` in the grobid installation dir first
# the default url is as below:
grobid_url = "http://localhost:8070"
url = "%s/api/processFulltextDocument" % grobid_url


def get_root(pdf_url):
    page = urllib.request.urlopen(pdf_url).read()
    parsed_article = requests.post(url, files={"input": page}).text
    root = BeautifulSoup(parsed_article, 'lxml')
    return root

def get_authors(root):
    author_names = root.find("sourcedesc").findAll("persname")
    authors = set()
    for author in author_names:
        firstname = author.find("forename", {"type": "first"})
        firstname = firstname.text.strip() if firstname is not None else ""
        middlename = author.find("forename", {"type": "middle"})
        middlename = middlename.text.strip() if middlename is not None else ""
        lastname = author.find("surname")
        lastname = lastname.text.strip() if lastname is not None else ""
        if middlename is not "":
            authors.add(firstname + " " + middlename + " " + lastname)
        else:
            authors.add(firstname + " " + lastname)
    authors = list(authors)
    return authors

def get_affs(root):
    aff_nodes = root.find("sourcedesc").findAll("orgname")
    affs = set()
    for aff in aff_nodes:
        affs.add(aff.text.strip())
    return list(affs)

def get_keywords(root):
    key_nodes = root.find("profiledesc").find("keywords").findAll("term")
    kwords = set()
    for kword in key_nodes:
        kwords.add(kword.text.strip())
    return list(kwords)


# A formatter will get url from xml_loader.items, and send the url to grobid web api, 
# and use the predefined functions to parse the results, the results are store as a 
# list of dictionary, which can be further transformed to std xml by Converter
# Due to some unknown problems, Grobid might fails to process some pdfs. Such files
# are collected in the self.failed list for further re-processing.
class Formatter:
    def __init__(self, items, year=2019, conf_name='INTERSPEECH'):
        self.items = items
        self.year = year
        self.conf_name = conf_name
        self.results = []
        self.failed = []
        self.format()
        
    def upload_failed(self):
        with open('failed.lst', 'a') as f:
            for x in self.failed:
                f.write(f'{x}\n')
        
    def format(self):
        for x in tqdm(self.items):
            title, abstract, author, url = x
            if not url.endswith('pdf'):
                print(f'not pdf failed!{url}')
                self.failed.append(url)
                continue
                
            root = get_root(url)
            try:
                test_root = root.find("sourcedesc")
                if test_root is None:
                    print(f'failed!{url}')
                    self.failed.append(url)
                    continue
                    
                authors = get_authors(root)
                affs = get_affs(root)
                keys = get_keywords(root)
                format_x = {'conf': self.conf_name, 
                        'year': self.year, 
                        'title': title, 
                        'abstract': abstract, 
                        'authors': authors,
                        'affiliations': affs,
                        'keywords': keys,
                        'url':url}
                self.results.append(format_x)
            except:
                print(f'failed!{url}')
                self.failed.append(url)
            # break
