#!/usr/bin/env python
# coding: utf-8
from converter import Converter

if __name__ == "__main__":
    query_result = [{'conf': 'INTERSPEECH', 
                    'year': 2020, 
                    'title': 'paper title', 
                    'abstract': 'this is an abstract', 
                    'authors': ['alice', 'bob'],
                    'affiliations': ['uni stuttgart', 'uni freiburgh'],
                    'keywords': ['speaker verification', 'x-vector'],
                    'url':'https://isitnewyearsday.com'}, 
                    {'conf': 'INTERSPEECH', 
                    'year': 2020, 
                    'title': 'paper title', 
                    'abstract': 'this is an abstract', 
                    'authors': ['alice'],
                    'affiliations': ['uni stuttgart', 'uni freiburgh'],
                    'keywords': ['speaker verification', 'x-vector'],
                    'url':'https://isitnewyearsday.com'}, 
                    {'conf': 'Association for Computational Linguistics', 
                    'year': 2021, 
                    'title': 'another paper title', 
                    'abstract': 'this is another abstract', 
                    'authors': ['jane', 'john'],
                    'affiliations': ['IMS'],
                    'keywords': ['speech recognition', 'LAS'],
                    'url':'https://isitnewyearsday.com'}]
    converter = Converter(query_result)
    print(converter.dump())
