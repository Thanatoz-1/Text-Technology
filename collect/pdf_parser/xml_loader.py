import lxml
from bs4 import BeautifulSoup
import pickle

class XMLLoader:
    """
    Load raw XML files to the list.
    Input xml is the result of Scrapy. It has the following structure:
    <items>
        <item>
            <title>text</title>
            <abstract>text</abstract>
            <author>text,text,text</author>
            <url>link</url>
        </item>
        ...
    </items>

    A member of the self.items list is a python dictionary. 
    An example member:
    {'conf': 'INTERSPEECH', 
        'year': 2020, 
        'title': 'paper title', 
        'abstract': 'this is an abstract', 
        'authors': ['alice', 'bob'],
        'affiliations': ['uni stuttgart', 'uni freiburgh'],
        'keywords': ['speaker verification', 'x-vector'],
        'url':'https://isitnewyearsday.com'}
    """

    def __init__(self):
        self.items = []
        
    def add_ans(self, i, affs, iterms):
        """ Insert the affiliation list and index term list to 
        the i_th item.
        """
        self.items[i]['affiliations'] = affs
        self.items[i]['keywords'] = iterms
        
    def dump(self, path):
        with open(path, 'wb') as f:
            pickle.dump(self.items, f)
                
    def read_xml(self, year, xml_path):
        """ Load the Scrapy outputs(the results scrawled down from the 
        year_th archive) to a python dictionary.
        """
        xml_path = xml_path.strip()
        with open(xml_path, 'r') as f:
            content = f.read()
            bs_content = BeautifulSoup(content, 'lxml')
            
            for item in bs_content.find_all('item'):
                title = item.title.get_text()
                abstract = item.abstract.get_text()
                author = item.author.get_text().split(',')
                url = item.url.get_text()
                ans = {'conf': 'INTERSPEECH', 
                   'year': year, 
                   'title': title, 
                   'abstract': abstract, 
                   'authors': author, 
                   'affiliations': [], 
                   'keywords': [], 
                   'url': url}
                self.items.append(ans)