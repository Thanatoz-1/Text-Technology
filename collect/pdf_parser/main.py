#!/usr/bin/env python
# coding: utf-8

import time
import os
from xml_loader import XMLLoader
from info_extractor import InfoExtractor
from converter import Converter
import pickle

""" This file will extract index terms and affiliation list from the paper's
pdf file. The pdf file could be accessed by the url link. 
The final results are an XMLLoader binary object and an XML file. 
The object stores a list of papers, with each paper's published year and conference, 
title, abstract, author list, affiliation list, keywords(index terms), and url.
The object could be dumped to an XML file with Converter and the XML file 
could be verified by 'papers_schema.xsd'
"""

def load_raw_data():
    """Load raw xml files data into xml loader. A raw xml file only includes 
    the following information:
    - conference name
    - conference year
    - paper's title
    - paper's abstract
    - author list
    - paper's url
    Such information will be stored in a python dictionary
    """
    xml_loader = XMLLoader()
    for yr in range(2010, 2022):
        xml_path = f'xmls/{yr}.xml'
        xml_loader.read_xml(yr, xml_path)
    return xml_loader
    

if __name__ == '__main__':
    xml_loader = load_raw_data()
    info_extractor = InfoExtractor()
    checkpoint_path = 'checkpoints'
    if not os.path.exists(checkpoint_path):
        os.makedirs(checkpoint_path)

    # the following process will take a lot of time. Around 8hrs for 9989 papers, 
    # 98.00% are successfully loaded and processed.
    for i, item in enumerate(tqdm(xml_loader.items)):
        title, author, url = item['title'], item['authors'], item['url']
        try:
            affs, iterms = info_extractor.extract_affiliation_iterms(title, author, url)
            if affs is None:
                # invalid url links
                continue
            # insert aff and index term to the ith item
            xml_loader.add_ans(i, affs, iterms)
            # prevent this program from sending too many queries to the remote server
            time.sleep(1)
        except:
            info_extractor.failed_list.append([url, title])

        # in case the program crashs due to unk reasons
        if i and i % 100 == 0:
            with open(os.path.join('checkpoints', f'{i}_xml.pkl'), 'wb') as f:
                pickle.dump(xml_loader, f)

    # dump the binary object because it makes later operations convient
    with open(os.path.join('checkpoints', 'final.pkl'), 'wb') as f:
        pickle.dump(xml_loader, f)

    # also dump the xml file for easier observation
    cvter = Converter(xml_loader.items)
    with open('papers.xml', 'w') as f:
        f.write(cvter.dump())
    