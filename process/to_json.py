#!/usr/bin/env python
# coding: utf-8

# The following code read the format xml, and turns that into a few json files, 
# then in django, use ```python manage.py loaddata x.json``` to load db
# before that, you can use ```python manage.py flush``` to clean the db
# there're five tables in total: author, affilation, keyword, conference, paper
import xml.etree.ElementTree as ET

from collections import Counter
from bs4 import BeautifulSoup
import sqlite3
import json

prefix = 'tables'
def name_to_id(item_count):
    # all id should starts from 1 in mysql
    return {x[0]:i+1 for i, x in enumerate(item_count)}

def load_and_count(root, item_name):
    nodes = root.findall(f'.//{item_name}')
    items = Counter()
    for item in nodes:
        items[item.text] += 1
    
    res = []
    for item in items:
        res.append((item, items[item]))
    return res

tree = ET.parse('format.xml')
froot = tree.getroot()

# write to author table
def load_author(root):
    authors = load_and_count(root, 'author')
    author_dict = [{'model':'ver0.author', 'pk':i+1, 'fields': {'name':x[0]}} for i, x in enumerate(authors)]
    with open(f'{prefix}/author.json', 'w') as f:
        f.write(json.dumps(author_dict))
    return name_to_id(authors)

author_dict = load_author(froot)

# write to affliation table
def load_aff(root):
    affs = load_and_count(root, 'affiliation')
    aff_dict = [{'model':'ver0.affiliation', 'pk':i+1, 'fields':{'name': x[0]}} for i, x in enumerate(affs)]
    with open(f'{prefix}/aff.json', 'w') as f:
        f.write(json.dumps(aff_dict))
    return name_to_id(affs)

aff_dict = load_aff(froot)

# write to conference table
def load_interspeech(root):
    yrs = load_and_count(root, 'year')
    yr_dict = [{'model': 'ver0.conference', 'pk':i+1, 'fields':{'name':'INTERSPEECH', 'year':int(x[0]), 'abbr': 'interspeech'}} for i, x in enumerate(yrs)]
    with open(f'{prefix}/conf.json', 'w') as f:
        f.write(json.dumps(yr_dict))
    return name_to_id(yrs)

conf_dict = load_interspeech(froot)

# write to key table 
def load_key(root):
    keys = load_and_count(root, 'keyword')
    key_dict = [{'model': 'ver0.keyword', 'pk':i+1, 'fields': {'name': x[0]}} for i, x in enumerate(keys)]
    with open(f'{prefix}/key.json', 'w') as f:
        f.write(json.dumps(key_dict))
    return name_to_id(keys)

key_dict = load_key(froot)

def extract_ids(item_node, name, item_dict):
    res = []
    for item in item_node.findall(f'.//{name}'):
        res.append(item_dict[item.text])
    return res

# write to paper table
confs = froot.findall('.//conference')
paper_cnt = 0
papers_dict = []
for conf in confs:
    year = conf.find('.//year').text
    conf_id = conf_dict[year]
    print(conf_id)
    for paper in conf.findall('.//paper'):
        title = paper.find('title').text
        if title is None:
            print(type(title), title)
            print('hey', paper_cnt, paper.text)
        assert(len(title) != 0)
        abst = paper.find('abstract').text
        url = paper.find('url').text
        author = extract_ids(paper.find('authors'), 'author', author_dict)
        affs = extract_ids(paper.find('affiliations'), 'affiliation', aff_dict)
        keys = extract_ids(paper.find('keywords'), 'keyword', key_dict)
        field = {
            'title': title, 
            'abstract': abst,
            'conference': conf_id,
            'authors': author, 
            'affiliations': affs, 
            'keys': keys, 
            'url': url
        }
        paper_dict = {'model': 'ver0.paper', 'pk': paper_cnt+1, 'fields': field}
        papers_dict.append(paper_dict)
        paper_cnt += 1
with open(f'{prefix}/paper.json', 'w') as f:
    f.write(json.dumps(papers_dict))
        
