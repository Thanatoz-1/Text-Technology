#!/usr/bin/env python
# coding: utf-8

# The following code read the format xml, and load the data to 5 json files, 
# then in django, use ```python manage.py loaddata x.json``` to load db
# before that, you can use ```python manage.py flush``` to clean the db
# there're five tables in total: author, affilation, keyword, conference, paper

# Usage: python to_json.py [input xml] [output_directory]
# Example: python to_json.py examples/papers.xml examples
# in the output_directory, 5 json files are:
# author.json, aff.json, conf.json, key.json and paper.json

import sys
from collections import Counter
import xml.etree.ElementTree as ET
import json


def name_to_id(item_count):
    '''
    Takes list as input and returns dictionary with list items as
    keys and an ID value. 

    Inputs:
    ----
    item_count: [List] List of items to create IDs.
    example: A list of authors

    Outputs:
    ----
    [Dictionary] with list items as keys and IDs (int) as values. 
    '''
    return {x[0]:i+1 for i, x in enumerate(item_count)}

def load_and_count(root, item_name):
    '''
    Finds and returns list of elements and count
    matching item_name in root Element.

    Inputs:
    ----
    prefix: [str] output directory
    root: [xml.etree.ElementTree.Element]
    item_name: [String] Name of item to find.

    Outputs:
    ----
    res: [list] A list of items and count of item.

    '''
    nodes = root.findall(f'.//{item_name}')
    items = Counter()
    for item in nodes:
        items[item.text] += 1
    
    res = []
    for item in items:
        res.append((item, items[item]))
    return res


#Write to authors' table
def load_author(prefix, root):
    '''
    Returns dictionary of authors and IDs. 
    Also dump the json file.

    Inputs:
    ---
    prefix: [str] output directory
    root: [xml.etree.ElementTree.Element]

    Outputs:
    ---
    name_to_id(authors): [Dictionary] Returns dictionary of authors and IDs.  

    '''
    authors = load_and_count(root, 'author')
    author_dict = [{'model':'ver0.author', 'pk':i+1, 'fields': {'name':x[0]}} for i, x in enumerate(authors)]
    with open(f'{prefix}/author.json', 'w') as f:
        f.write(json.dumps(author_dict))
    return name_to_id(authors)


#Write to affilitations table
def load_aff(prefix, root):
    '''
    Returns dictionary of affiliation names and IDs.
    Also dump the json file.

    Inputs:
    ----
    prefix: [str] output directory
    root: [xml.etree.ElementTree.Element]

    Outputs:
    ----
    name_to_id(affs): [Dictionary] Returns dictionary of affiliations and IDs.
    '''
    affs = load_and_count(root, 'affiliation')
    aff_dict = [{'model':'ver0.affiliation', 'pk':i+1, 'fields':{'name': x[0]}} for i, x in enumerate(affs)]
    with open(f'{prefix}/aff.json', 'w') as f:
        f.write(json.dumps(aff_dict))
    return name_to_id(affs)


# Write to conference table
def load_interspeech(prefix, root):
    '''
    Returns dictionary of years and IDs
    Also dump the json file.

    Inputs:
    ----
    prefix: [str] output directory
    root: [xml.etree.ElementTree.Element]
    
    Outputs:
    ----
    name_to_id(yrs): [Dictionary] Returns dictionary of years and IDs.
    '''
    yrs = load_and_count(root, 'year')
    yr_dict = [{'model': 'ver0.conference', 'pk':i+1, 'fields':{'name':'INTERSPEECH', 'year':int(x[0]), 'abbr': 'interspeech'}} for i, x in enumerate(yrs)]
    with open(f'{prefix}/conf.json', 'w') as f:
        f.write(json.dumps(yr_dict))
    return name_to_id(yrs)


# write to key table 
def load_key(prefix, root):
    '''
    Returns dictionary of key words and IDs
    Also dump the json file.

    Inputs:
    ----
    prefix: [str] output directory
    root: [xml.etree.ElementTree.Element]
    
    Outputs:
    ----
    name_to_id(keys): [Dictionary] Returns dictionary of key words and IDs.

    '''

    keys = load_and_count(root, 'keyword')
    key_dict = [{'model': 'ver0.keyword', 'pk':i+1, 'fields': {'name': x[0]}} for i, x in enumerate(keys)]
    with open(f'{prefix}/key.json', 'w') as f:
        f.write(json.dumps(key_dict))
    return name_to_id(keys)


def extract_ids(item_node, name, item_dict):
    '''
    Extract a list IDs from dictionary and return a list as
    result.

    Inputs:
    ----
    item_node: [xml.etree.ElementTree.Element]
    Example: paper.find('authors')
    name: [String] Name of element
    Example: 'author'
    item_dict: [Dictionary] Dicitonary to search for name matches.
    Example: author_dict
    '''
    res = []
    for item in item_node.findall(f'.//{name}'):
        res.append(item_dict[item.text])
    return res

# write to paper table
def load_paper(prefix, author_dict, aff_dict, conf_dict, key_dict, froot):
    '''
    Given the name-to-id dictionaries of author/aff/conf/key tables, build
    the paper table and dump the json file.

    Inputs:
    ----
    prefix: [str] output directory
    author_dict: [dict] map an author to it's primary key/ID.
    aff_dict: [dict] map an affiliation to it's primary key/ID.
    conf_dict: [dict] map a conference to it's primary key/ID.
    key_dict: [dict] map a keyword to it's primary key/ID.
    froot: [xml.etree.ElementTree.Element]
    '''
    confs = froot.findall('.//conference')
    paper_cnt = 0
    papers_dict = []
    for conf in confs:
        year = conf.find('.//year').text
        conf_id = conf_dict[year]
        print(f'Processing the {conf_id}th conference')
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
    

if __name__ == "__main__":
    input_xml = sys.argv[1]
    output_dir_prefix = sys.argv[2]

    tree = ET.parse(input_xml)
    froot = tree.getroot()
    
    author_dict = load_author(output_dir_prefix, froot)
    aff_dict = load_aff(output_dir_prefix, froot)
    conf_dict = load_interspeech(output_dir_prefix, froot)
    key_dict = load_key(output_dir_prefix, froot)
    load_paper(output_dir_prefix, author_dict, aff_dict, conf_dict, key_dict, froot)