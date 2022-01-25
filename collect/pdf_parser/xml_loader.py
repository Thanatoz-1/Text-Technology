import lxml
from bs4 import BeautifulSoup

# We use XMLLoader to load all raw xml files
class XMLLoader:
    """
    Load XML files into bs4 content
    """
    def __init__(self):
        self.xmls = []
        self.items = []
        
    def read_xmls(self, xmls_path):
        """
        xmls_path contains all the xmls files's paths
        one line for one xml path
        each xml file will be parsed and stored as a BeautifulSoup
        parsed object in self.xmls
        """
        print('loading...')
        with open(xmls_path, 'r') as f:
            for xml_path in f:
                self.xmls.append(self._read_one_xml(xml_path))
                
        # serialize items, just load it to the memory
        for bs_content in self.xmls:
            for item in bs_content.find_all('item'):
                title = item.title.get_text()
                abstract = item.abstract.get_text()
                author = item.author.get_text()
                url = item.url.get_text()
                self.items.append((title, abstract, author, url))
        print('done')
                
    def _read_one_xml(self, xml_path):
        """
        return the BeautifulSoup parsed result of a given xml file
        """
        xml_path = xml_path.strip()
        with open(xml_path, 'r') as f:
            content = f.read()
            bs_content = BeautifulSoup(content, 'lxml')
            return bs_content