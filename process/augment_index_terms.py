import sys
import pickle

sys.path.append('../collect/pdf_parser')
from xml_loader import XMLLoader
from converter import Converter

class KeywordAugment:
    def __init__(self, items, all_cap_dict, cluster_dict):
        """ Given the list of paper items, all cap dict and cluster dict, 
        this class will augment the keyword session with:
        1) all-cap words, if there are any all-cap word in the abstract 
           area and those all-cap words also exist in the all_cap_dict
        2) cluster representative word, if the index term can be replaced 
           by a cluster representative word, add that word to the keyword
           session

        Data Format:
        items: a list of paper dictionary, a paper dictionary includes:
            {'conf': 'INTERSPEECH', 
                   'year': year, 
                   'title': title, 
                   'abstract': abstract, 
                   'authors': author, 
                   'affiliations': [], 
                   'keywords': [], 
                   'url': url}

        all_cap_dict: a set of all cap words 
        cluster_dict: map an index term to a cluster representative word
        """
        self.all_cap_dict = all_cap_dict
        self.cluster_dict = cluster_dict
        for item in items:
            self.add_cluster(item)
            self.add_all_cap(item)
            self.remove_invalid(item)
        self.items = items

    def add_cluster(self, item):
        aug = []
        for index_term in item['keywords']:
            if index_term not in self.cluster_dict:
                print('why', index_term)
            else:
                aug.append(self.cluster_dict[index_term])
        item['keywords'] += aug 
    
    def add_all_cap(self, item):
        aug = []
        abstract = item['abstract']
        """
        for word in abstract.split(' '):
            if word.isupper() and word in self.all_cap_dict:
                aug.append(word)
        """
        # we should use these, for HMMs, HMM. "HMM"
        for allcap in self.all_cap_dict:
            if allcap in abstract:
                aug.append(allcap) 
        
        item['keywords'] += aug

    def remove_invalid(self, item):
        """ Remove invalid keys, which are too long(>128) or 
        too short(0). Such errors are caused by incorrect
        parsing results. Pdftotext and Grobid tools sometimes 
        fail to detect the keyword area.
        """
        keys = []
        for key in item['keywords']:
            if len(key.strip()) == 0: continue
            if len(key.strip()) >= 128: continue
            keys.append(key)
        item['keywords'] = list(set(keys))
        


if __name__ == '__main__':
    xml_load_path, all_cap_path, cluster_dict_path = sys.argv[1], sys.argv[2], sys.argv[3]
    output_path = sys.argv[4]

    with open(xml_load_path, 'rb') as f:
        xml_loader = pickle.load(f)
    with open(all_cap_path, 'rb') as f:
        all_cap_dict = pickle.load(f)
    with open(cluster_dict_path, 'rb') as f:
        cluster_dict = pickle.load(f)
    
    keyword_augment = KeywordAugment(xml_loader.items, all_cap_dict, cluster_dict)
    # also dump the xml file for easier observation
    cvter = Converter(keyword_augment.items)
    with open(output_path, 'w') as f:
        f.write(cvter.dump())
