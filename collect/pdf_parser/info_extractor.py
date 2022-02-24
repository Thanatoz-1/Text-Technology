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

    def __init__(self):
        """ This class will extract affiliations and index terms from pdf url
        using Grobid service and tika pdf parser.

        pre-requirements:
        third-party packages: tike, pdftotext, tqdm, grobid service
        please launch grobid server at port 8070 in advance.
        """
        grobid_url = "http://localhost:8070"
        self.api = "%s/api/processAffiliations" % grobid_url
        self.failed_list = []
        
    def extract_affiliation_iterms(self, title, in_author, url):
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