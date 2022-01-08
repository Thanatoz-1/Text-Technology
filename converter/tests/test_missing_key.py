#!/usr/bin/env python
# coding: utf-8
import unittest 
from converter import Converter, Paper

class MissingKeyTest(unittest.TestCase):
    def test(self):
        query_result = [{'conf': 'INTERSPEECH', 
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
                        'abstract': 'this is another abstract', 
                        'authors': ['jane', 'john'],
                        'affiliations': ['IMS'],
                        'keywords': ['speech recognition', 'LAS'],
                        'url':'https://isitnewyearsday.com'}]
        converter = Converter(query_result)
        self.assertTrue(len(converter.error))
        for error in converter.error:
            self.assertEqual(error, Paper.status['missing_key'])

