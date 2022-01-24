#Research Trends Documentation
---

##Overview

The Research Trends applications allows users to query a database of research papers presented at various conferences from 2012 to 2021. Query results will return graphical representations of changes in key words found in paper abstracts as well as proportional contributions from authors and institutions. In addition, these data are available for download as an XML dataset.

---
##Testing Database

Our first task was to profile several relational and NoSQL databases to test loading and query efficiency. The databases selected were MySQL, MongoDB, and ElasticSearch. The breakdown of loading speeds can be seen in the below table:

|   | MySQL | MongoDB| ElasticSearch|
|------|------|------| -----|
|**Load 1M Queries (Hrs.)**| 3:58 | 4:08 | 5:51|


We have opted to use a relational database due to quicker query times. This design allows for quicker retrieval of the XML dataset. 


---

## Data Collection

Data was collected from the ISCA archive: https://www.isca-speech.org.

For each paper, an XML file was generated containing:

* A Title
* Authors list
* List of affiliate institutions
* Abstract
* Index terms
* URL

### Step 1: Crawling a Website

Website: interspeech archive
Requirement(s): scrapy
Code path: collect/spider

With scrapy, paper metadata can be downloaded to an XML file.

From the metadata, we can obtain:
* Title
* Abstract
* Authors
* URL

**Workflow**

The main functions can be found in collect/spider/getpdf/spiders/pdf_spider.py

Firstly, we start our requests at the root website, and then we use xpath to locate the block which contains all the links to the archives for each individual year. We loop over the archive link for each year. Now we can process each target year link, one at a time.

After moving to the archive link for the target year ([example](https://www.isca-speech.org/archive/interspeech_2016/index.html)), we use xpath to locate the block that contains all the paper links.

For each paper link, we navigate to its description page like [this](https://www.isca-speech.org/archive/interspeech_2016/medennikov16_interspeech.html). And again, with Xpath, we locate and extract the content needed (e.g. title, author, abstract, url), returning a python dictionary object containing all the information.

Scrapy will automatically transform the python dictionary outputs to XML files.

However, the affiliations and index terms are only available in the PDF document. Therefore, we will extract this information in step 2.

### Step 2 Processing the PDF Files

PDF: [example](https://www.isca-speech.org/archive/pdfs/interspeech_2016/medennikov16_interspeech.pdf)
Requirement(s):
    * [Grobid](https://grobid.readthedocs.io/en/latest/Grobid-service/) Service API
    * [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) and [Ixml](https://lxml.de/) packages for easier XML parsing.
code path: collect/pdf_parser

***Description***
This tool allows us to extract the *affiliations* and *index terms* from the PDF files.

Workflow
Firstly, we launch the Grobid Service with ./gradlew run. The default service url is http://localhost:8070. We also use a XMLLoader object to load all items in the year.xml produced by Step 1.

Grobid API will return the pdf parsing results in xml format. However, we only need the affiliations and index terms. So, we use a Formatter ojbect to:
    *Read a pdf link from XMLLoader
    *Download the PDF and sent the bytes to Grobid api
    *Extract only affiliations and index terms from the parsing results
    *Combine affiliations, index term and other metadata from the original XML files into a python dictionary object.

Finally, we use a Converter object to convert all the python dictionary objects into one single XML file, and this XML file can be verified by a general schema.

A gerneral schema is needed here becase we might want to coleect papers from other sources and conferences. We want all the data stored in the same format, making it easier for further processing.

***Usage***
1. Lauch the Grobid server at http://localhost:8070
2. Prepare all the XML files generated at step 1
3. Might need to edit the start_year and end_year in main.py depending on which year’s data we have under the xmls directory.
3. mkdir backup for backing up intermediate results
4. python main.py, results are stored in all_years.xml

***Issue***
Grobid sometimes failed to process a pdf file, need to re-process those failed links. The reason might be we are not using the official Grobid client for sending our requests, but only using the default request packages, which triggers unexpected bugs.

---

## Data Processing
Input: XML File
Output: JSON files that can be easily imported to SQL database

### Step 1: Keyword Extraction

Methods: tfidf, topic modelling, keyword clustering, all-caps

Requirements:
    * Packages: sklearn, pandas, numpy, re, nltk, space, gensim
    * Output results from the data collection stage

***Description***
Since the index terms dataset is sparse and has long-tail phenomenon, we would like to find another way to extract keywords from a paper.

***Workflow***

*Text Normalisation*

The text normalisation for all methods includes:

* Lowercase(except for the All-Cap method), tokenisation, punctuation removement, lowercase using gensim simple_preprocess function
* Lemmatization using spacy, we keep only the open classes including noun, verb, adj, and adv.
Methods

To keep it simple, we only apply the following methods on the abtract. Some methods might work better on the full text, but we have not tried it yet.

* TfIdf: Computed via sklearn’s TfidfVectorizer with default parameter setting.
* Topic Modelling:
  * For the word vector representation, we use sklearn.feature_etraction.text.CountVectorizer.
  * sklearn’s LatentDirichletAllocation module is used to compute the topics. n_component is set to 50, max_iter   is set to 20. During the analysis phrase, we only look at the top 20 words for each topic.
  
In addition to extracting keywords from abtract, we also try to cluster many index terms into one group, and represent those words with the most frequent word within the group.

Clustering:
For the word vector representation, we use the pretained GloVe model glove-wiki-gigaword-50. For those phrases, its vector representation is the element-wise summation of all the words in it. If one of word in that phrases is an out-of-vocabulary(OOV) word for the pretrained model, we skip this phrase.
Cluster: we use sklearn.cluster.KMeans for clustering, n_clusters is set to 100, and init method is k-means++.
The naive and most straight-forward way is to use all-cap words(e.g. LSTM, DNN) as keywords.

All-Cap: after text normalisation(without lowercase), extract those all-cap words and append them to the original keyword list.

Usage:
    *The implementation and analysis of the first three methods can be found respectively in tfidf.ipynb, topic_modelling.ipynb and clustering.ipynb.
    * To replace the keywords with all-cap words, prepare the formatted XML produced in the previous step, and run:python all_cap.py formatted.xml output.xml. The replaced version will be stored as output.xml.

***Issue***
It might happen that one paper doesn’t have any all-cap words, and all the index-terms contain OOV words, then it has to use the original index terms as its keywords.


### Step 2: XML to JSON

***Description***
We use a relational database and Django for to access the data, therefore we need to decouple the XML files into 5 tables: conference, author, affiliations, keywords, and paper. Since Django can automatically migrate a Json file into any backend relational database, we use JSON to represent these 5 tables.

***Workflow***
Since a paper instance needs to reference instances in other tables, we first load conference, author, affiliations, and keywords into four independant tables, and assign an unique ID for each instance.

Then we finialize the paper table, replace the dependant field’s value with its ID in the corresponding table.

Each row is a JSON object, and the whole table is stored in one single JSON file.

***Usage***
Prepare the formatted XML file produced in step 1 and run the following command, the results will be stored in the tables directory, they’re conference.json, author.json, aff.json, keywords.json, paper.json.


>mkdir tables
python to_json.py input.xml

---
### Access

Input: Database
Output: Website
Requirement(s):
* Django(https://www.djangoproject.com/)
* Chart.js(https://www.chartjs.org/)
  
***Description***
We use Django for better interraction and data accessing. Chart.js is used to plot the query results in the webpage.

***Data Loading***
Clear the database and then load the produced JSON files into database.

>python manage.py flush 
python manage.py loaddata conference.json 
python manage.py loaddata author.json 
...

***Query***
1. Change of top key words over time interval:
    filters: start year, end year, top k
    return: line chart
2. Change in number of publications with a given key word over time interval:
    filters: start year, end year, keyword
    return: line chart
3. Research interest distribution for a given researcher over time interval:
    filters: start year, end year, researcher
    return: line chart
3. Research interest distribution for given institution over time interval:
    filters: start year, end year, affiliation
    return: line chart

---
## Using the Database

