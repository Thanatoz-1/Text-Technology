import copy
import io
import urllib
import re
import requests
import xml.etree.ElementTree as ET

from tika import parser
import pdftotext
from tqdm import tqdm


class InfoExtractor:
    """ This class will extract affiliations and index terms from pdf url
    using Grobid service and tika pdf parser.

    pre-requirements:
    third-party packages: tike, pdftotext, tqdm, grobid service
    please launch grobid server at port 8070 in advance.
    """

    def __init__(self):
        grobid_url = "http://localhost:8070"
        self.api = "%s/api/processAffiliations" % grobid_url
        self.failed_list = []
        
    def extract_affiliation_iterms(self, title, in_author, url):
        """ Given the title, author list and pdf url, extract the affiliation
        and index terms from the pdf. The author list is used to locate the 
        affiliation area, which sits between the authors line and the abstract.

        Input:
        ---
        title: [str]
        in_author: [list of str], e.g. ['Alice', 'Bob']
        url: [str]
        """
        if not url.endswith('.pdf'):
            self.failed_list.append([url, title])
            return None, None
        
        author = copy.deepcopy(in_author)
        author = [a.lower() for a in author]
        page = urllib.request.urlopen(url).read()
        
        aff_candidate = self.extract_candidate(page, title, author)
        status = True
        aff, iterms = [], []
        if aff_candidate is False:
            status = False
        else:
            status = self.extract_affiliation(aff_candidate)
            if status is not False:
                aff = status
                status = True
                
        iterms = self.extract_index_terms(page)
        if iterms is False:
            iterms = []
        
        if not status:
            self.failed_list.append([url, title])
        return aff, iterms
        
    def extract_text_from_url(self, url):
        """ Given the pdf url, extract the header area. 
        The header area includes the title, authors, affiliations, and 
        other unwanted information(e.g. emails, conference logo).
        """
        page = urllib.request.urlopen(url).read()
        raw = parser.from_buffer(page)
        lines = raw['content'].split('\n')
        ret = []
        for line in lines:
            line = line.strip()
            if len(line) == 0: continue
            ret.append(line)
        return ret
    
    def extract_candidate(self, page, title, author):
        """ Given the first page of pdf content, the title, and 
        the author, locate the area where includes the affiliation names.
        The author and affiliation sit between title and abstract. After
        extracting the lines between title and abstract, we do a post-process
        to skip all the lines containing an author's name. 
        
        The final result is a list of strings that contains the affiliation names, 
        but they might include other unwanted text like the department and address, 
        e.g. "University of Stuttgart, 1, Faculty 5, Stuttgart, Germany".
        Such lines will be sent to Grobid to remove unwanted proper names and 
        other strings.
        """
        pdf = pdftotext.PDF(io.BytesIO(page))
        lines = pdf[0].strip().split('\n')
        st, ed = 0, -1
        for i, in_line in enumerate(lines):
            line = in_line.strip().lower()
            if len(line) == 0:
                continue
            if title.lower() in line:
                # this line may fail when the title too long, it breaks 
                # into two or more lines
                st = i+1
            if line.startswith('abstract'):
                ed = i
                break
                
        if st == -1 or ed == -1:
            return False
        
        ret = []
        for i in range(st, ed):
            if self.__has_author(lines[i], author):
                continue
            ret.append(lines[i].strip())
        
        if len(ret) == 0:
            return False
        return ret
    
    def __has_author(self, in_line, author):
        line = in_line.lower()
        for a in author:
            if a in line:
                return True
        return False
    
    def extract_affiliation(self, candidate):
        """ Given a list of strings, send them to Grobid to tag which part
        is the institution names. 

        Input:
        ---
        candidate: [list of str]
        e.g. 
            [
                'University of Stuttgart, 1, Faculty 5, Stuttgart, Germany', 
                'University of Edinburgh, 1, 2, department of Computer Science'
            ]

        Output:
        ---
        A list of institution names. 
        e.g. 
        ['University of Stuttgart', 'University of Edinburgh']
        """
        # affiliations
        ret = []
        for aff in candidate:
            parsed_article = requests.post(self.api, 
                                       data={"affiliations": aff}).text
            xml_text = '<root>'+parsed_article.strip()+'</root>'
            root = ET.fromstring(xml_text)
            orgs = root.findall(".//*[@type='institution']")
            if len(orgs) != 1:
                continue
            ret.append(orgs[0].text)

        if len(ret) == 0:
            return False
        return list(set(ret))
    
    def extract_index_terms(self, page):
        """ Given the first page of the pdf, extract the index terms.
        We use TIKA parser for document layout analysis, it could automatically
        seperate the two columns, return a list of text lines.

        The index terms are located between the abstract and introduction.
        """
        raw = parser.from_buffer(page)
        lines = raw['content'].split('\n')
        # locate Index Terms
        iterms = None
        st, ed = -1, -1
        cnt = 0
        for i, line in enumerate(lines):
            line = line.strip()
            if len(line) == 0:
                continue
            cnt += 1
            if cnt > 100:
                # speed up
                break
            if 'index terms' in line.lower():
                st = i
            if '1. introduction' == line.lower():
                ed = i
                break
        if st == -1 or ed == -1:
            return False
        candidate = ' '.join(lines[st:ed]).split(':')[1]
        iterms = candidate.split(',')
        for i, iterm in enumerate(iterms):
            if not iterm.isupper():
                iterm = iterm.lower()
            iterm = re.sub('\s+', ' ', iterm)
            iterm = re.sub('\.', '', iterm)
            iterm = re.sub('- ', '', iterm)
            iterms[i] = iterm.strip()
        return iterms