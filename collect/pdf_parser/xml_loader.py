import lxml
from bs4 import BeautifulSoup
import pickle

# We use XMLLoader to load all raw xml files
class XMLLoader:
    """
    Load XML files
    """

    def __init__(self):
        self.xmls = []
        self.items = []
        
    def add_ans(self, i, affs, iterms):
        self.items[i]['affiliations'] = affs
        self.items[i]['keywords'] = iterms
        
    def dump(self, path):
        with open(path, 'wb') as f:
            pickle.dump(self.items, f)
                
    def read_xml(self, year, xml_path):
        """
        return the BeautifulSoup parsed result of a given xml file
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