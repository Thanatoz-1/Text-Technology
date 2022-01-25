#!/usr/bin/env python
# coding: utf-8

from grobid_formatter import Formatter
from xml_loader import XMLLoader
from converter import Converter
import pickle


if __name__ == '__main__':
    yr_format = {}
    start_year = 2010
    end_year = 2022
    results = []
    for yr in range(start_year, end_year):
        # create a file with all the xml files that
        # needed to be processed by XMLLoader later
        # TODO: this is a bad design, XMLLoader is designed
        # to process multiple xml files, but in 
        # practice, we only process xml files one by
        # one
        with open('xml_paths', 'w') as f:
            f.write(f'xmls/{yr}.xml')
    
        xml_loader = XMLLoader()
        xml_loader.read_xmls('xml_paths')
        print(f'processing {yr}')

        # use Formatter to extract affliation and index term from 
        # the pdf files, and combine all info, including title, 
        # abstract, authors, affiliations, index terms and url, 
        # in a python dictionary. 
        formatter = Formatter(xml_loader.items, yr)
        yr_format[yr] = formatter
        # temporarily save the object locally in case we're  
        # going to reuse such info later
        with open(f'backup/{yr}_formatter', 'wb') as f:
            pickle.dump(formatter, f)
        # Grobid sometimes failed to process a pdf, write those
        # links locally as well for re-processing.
        formatter.upload_failed()
        # append all years' result to [results] list
        results += formatter.results

    # results is a list of python dictionary object, each object contains
    # all info descibring a paper(title, abstract, etc)
    # Converter can dump such objects a one single xml files
    cvter = Converter(results)
    with open('all_years.xml', 'w') as f:
        f.write(cvter.dump())

