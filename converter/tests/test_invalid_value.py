#!/usr/bin/env python
# coding: utf-8
import unittest 
from converter import Converter, Paper

class InvalidValueTest(unittest.TestCase):
    def test(self):
        query_result = [{'conf': 'INTERSPEECH', 
                        'year': 'hello', 
                        'title': 'paper title', 
                        'abstract': 'this is an abstract', 
                        'authors': ['alice', 'bob'],
                        'affiliations': ['uni stuttgart', 'uni freiburgh'],
                        'keywords': ['speaker verification', 'x-vector'],
                        'url':'https://isitnewyearsday.com'}, 
                        {'conf': 'Association for Computational Linguistics', 
                        'year': 2021, 
                        'title': 'paper two', 
                        'abstract': 'this is another abstract', 
                        'authors': ['jane', 'john'],
                        'affiliations': ['IMS'],
                        'keywords': ['speech recognition', 'LAS'],
                        'url':'https://isitnewyearsday.com'}]
        converter = Converter(query_result)
        self.assertTrue(len(converter.error))
        for error in converter.error:
            self.assertEqual(error, Paper.status['invalid_value'])

