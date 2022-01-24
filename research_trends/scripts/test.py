from collections import Counter
from bs4 import BeautifulSoup
import sqlite3
import json
# from ver0.models import *

froot = BeautifulSoup(open('format.xml', 'rb'), 'lxml')

def name_to_id(item_count):
    return {x[0]:i for i, x in enumerate(item_count)}

def load_and_count(root, item_name):
    nodes = root.findAll(item_name)
    items = Counter()
    for item in nodes:
        items[item.text] += 1
    
    res = []
    for item in items:
        res.append((item, items[item]))
    return res

def load_author(root):
    authors = load_and_count(root, 'author')
    author_dict = [{'model':'ver0.author', 'pk':i, 'fields': {'name':x[0], 'count':x[1]}} for i, x in enumerate(authors)]
    with open('scripts/data/author.json', 'w') as f:
        f.write(json.dumps(author_dict))
    return name_to_id(authors)

def load_aff(root):
    affs = load_count(root, 'affiliation')
    aff_dict = [{'model':'ver0.affiliation', 'pk':i, 'fields':{'name': x[0]}} for i, x in enumerate(affs)]
    with open('scripts/data/aff.json', 'w') as f:
        f.write(json.dumps(aff_dict))
    return name_to_id(affs)

def load_interspeech(root):
    yrs = load_and_count(root, 'year')
    yr_dict = [{'model': 'ver0.conference', 'pk':i, 'fields':{'name':'INTERSPEECH', 'year':int(x[0]), 'abbr': 'interspeech'}} for i, x in enumerate(yrs)]
    with open('scripts/data/conf.json', 'w') as f:
        f.write(json.dumps(yr_dict))
    return name_to_id(yrs)

def load_key(root):
    keys = load_and_count(root, 'keyword')
    key_dict = [{'model': 'ver0.keyword', 'pk':i, 'fields': {'name': x[0]}} for i, x in enumerate(keys)]
    with open('scripts/data/key.json', 'w') as f:
        f.write(json.dumps(key_dict))
    return name_to_id(keys)

author_dict = load_author(froot)
aff_dict = load_aff(froot)
conf_dict = load_interspeech(froot)
key_dict = load_key(froot)






