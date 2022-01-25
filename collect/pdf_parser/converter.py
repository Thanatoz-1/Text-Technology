#!/usr/bin/env python
# coding: utf-8

# the following code can convert a list of python dictionary objects
# to an xml files, which could be verified by the schema
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from xml.etree import ElementTree
from xml.dom import minidom
from copy import deepcopy
import logging 

class Paper:
    keys = ["conf", "year", "title", "abstract", "authors", "affiliations", "keywords", "url"]
    status = dict(ok=0, missing_key=1, invalid_value=2)

    def __init__(self):
        pass
    
    def accept(self, res_dict):
        self.conf = res_dict['conf']
        self.year = str(res_dict['year'])
        self.title = res_dict['title']
        self.abstract = res_dict['abstract']
        self.authors = res_dict['authors']
        self.affiliations = res_dict['affiliations']
        self.keywords = res_dict['keywords']
        self.url = res_dict['url']

    @staticmethod
    def validate(res_dict):
        """
        validate whether the res_dict has the needed keys and types
        TODO: validate using a xsd file
        """
        for key in Paper.keys:
            if key not in res_dict:
                logging.warning(f'key [{key}] is missing in sample {res_dict}')
                return Paper.status['missing_key']
        if type(res_dict['year']) is not int:
            logging.warning(f'key [year] should be int in sample {res_dict}')
            return Paper.status['invalid_value']
        return Paper.status['ok']
                
        
class Converter:
    conf_to_abbr = {
        'INTERSPEECH': 'interspeech',
        'Association for Computational Linguistics': 'acl'
    }

    
    def __init__(self, query_results):
        """
        This class accepts the query_results, and return the xml string
        via dump() function.
        query_results is a list of dict, containing the user's query 
        results
        Example input:
            query_result = [{'conf': 'INTERSPEECH', 
                    'year': 2020, 
                    'title': 'paper title', 
                    'abstract': 'this is an abstract', 
                    'authors': ['alice', 'bob'],
                    'affiliations': ['uni stuttgart', 'uni freiburgh'],
                    'keywords': ['speaker verification', 'x-vector'],
                    'url':'https://isitnewyearsday.com'}]
        """
        self.query_results = query_results
        self.error = set()
        self._input_validation()
        self.root = None

    def _input_validation(self):
        all_ok = []
        for paper in self.query_results:
            status = Paper.validate(paper)
            if status != Paper.status['ok']:
                self.error.add(status)
            else:
                all_ok.append(paper)
            
        ori_len = len(self.query_results)
        new_len = len(all_ok)
        if new_len != ori_len:
            logging.info(f'{ori_len - new_len} results have been removed due to missing keys')
            self.query_results = all_ok
    
    def dump(self):
        """
        This function convert the query results to xml string which can be 
        verified by [papers_schema.xsd](https://github.com/Thanatoz-1/Text-Technology/blob/yixuan-feat/data/papers_schema.xsd)
        """
        self.root = Element('conferences')
        self.query_results = sorted(self.query_results, key=lambda x:(x['conf'], x['year']))
        pre_paper = None
        cur_paper = Paper()
        paper_list = None
        for sample in self.query_results:
            cur_paper.accept(sample)
            if pre_paper is None or cur_paper.conf != pre_paper.conf or cur_paper.year != pre_paper.year:
                paper_list = self._add_with_new_conf(cur_paper)
                pre_paper = deepcopy(cur_paper)
            else:
                self._add_paper_to_conf(cur_paper, paper_list)
        return self._prettify()
    
    def _prettify(self):
        rough_string = ElementTree.tostring(self.root, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")
    
    def _add_with_new_conf(self, paper):
        conf_node = SubElement(self.root, 'conference')
        metadata = SubElement(conf_node, 'metadata')
        papers = SubElement(conf_node, 'papers')
        
        conf_name = self._add_xml_node(metadata, 'confName', paper.conf)
        conf_name.set('abbr', Converter.conf_to_abbr[paper.conf])
        self._add_xml_node(metadata, 'year', paper.year)
        self._add_paper_to_conf(paper, papers)
        return papers
    
    def _add_paper_to_conf(self, paper, papers):
        pnode = SubElement(papers, 'paper')
        self._add_xml_node(pnode, 'title', paper.title)
        self._add_xml_node(pnode, 'abstract', paper.abstract)
        self._add_xml_list(pnode, 'authors', 'author', paper.authors)
        self._add_xml_list(pnode, 'affiliations', 'affiliation', paper.affiliations)
        self._add_xml_list(pnode, 'keywords', 'keyword', paper.keywords)
        self._add_xml_node(pnode, 'url', paper.url)
        
    def _add_xml_node(self, parent, name, text):
        kid = SubElement(parent, name)
        kid.text = text
        return kid
        
    def _add_xml_list(self, parent, name, list_name, elements):
        kid = SubElement(parent, name)
        for ele in elements:
            self._add_xml_node(kid, list_name, ele)
