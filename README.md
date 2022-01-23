# Pre-Final Project Documentation

#LectureTextTech 
#project-research-trend

- [Pre-Final Project Documentation](#pre-final-project-documentation)
  - [collect](#collect)
    - [Step1: crawl a website](#step1-crawl-a-website)
      - [Description](#description)
      - [Workflow](#workflow)
      - [Usage](#usage)
      - [TODO](#todo)
    - [Step2: process pdf files](#step2-process-pdf-files)
      - [Description](#description-1)
      - [Workflow](#workflow-1)
      - [Usage](#usage-1)
      - [Issue](#issue)
  - [process](#process)
    - [step1: keyword extraction](#step1-keyword-extraction)
      - [Description](#description-2)
      - [Workflow](#workflow-2)
        - [Text Normalisation](#text-normalisation)
        - [Methods](#methods)
      - [Usage:](#usage-2)
      - [Issue](#issue-1)
      - [TODO](#todo-1)
    - [step2: xml to json](#step2-xml-to-json)
      - [Description](#description-3)
      - [Workflow](#workflow-3)
      - [Usage](#usage-3)
  - [access](#access)
      - [Description](#description-4)
      - [Data loading](#data-loading)
      - [Query](#query)

## collect 
input: a website 
output: a xml file containing the following information of each paper
- title 
- author 
- affiliation 
- abstract 
- index term 
- url

### Step1: crawl a website 
website: [interspeech archive](https://www.isca-speech.org/archive/)
requirement: [scrapy](https://scrapy.org/)
code path: `collect/spider`

#### Description 
This tool can download paper metadata to an xml file. 

The metadata includes the **title**, **abtract**, **author** and **url**. One example output could be found in the *example* directory.

The xml file is named by the year. e.g. *2010.xml*

#### Workflow
The main functions could be found in `collect/spider/getpdf/spiders/pdf_spider.py`

Firstly, we start our requests at the [root website](https://www.isca-speech.org/archive/), and then we use *xpath* to locate the block which contains all the links to each year's archive websides. We loop over each year's archive link, and only process the target year's link at one time.

After moving to the target year's archive link(an [example](https://www.isca-speech.org/archive/interspeech_2016/index.html)), we use *xpath* to locate the block that contains all the paper links. 

For each paper link, we navigate to its description page like [this](https://www.isca-speech.org/archive/interspeech_2016/medennikov16_interspeech.html). And again with *xapth*, we locate and extract the content needed(e.g. title, author, abstract, url), and return a python dictionary object containing all this information. 

Scrapy will automatically transform the python dictionary outputs to XML files. 

However, the *affiliations* and *index terms* are presented at the paper description pages, we need to extract such information from the PDF files at [step 2](#Step2-process-pdf-files). 

#### Usage
```xdg
# download paper metadata from 2010 to 2022
sh run.sh 2010 2022
```

#### TODO
- [ ] enable pre-defined output directory and output file name

### Step2: process pdf files 
pdf: [example](https://www.isca-speech.org/archive/pdfs/interspeech_2016/medennikov16_interspeech.pdf)
requirement: 
- use [grobid service api](https://grobid.readthedocs.io/en/latest/Grobid-service/)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) + [lxml](https://lxml.de/) packages for easier xml parsing

code path: `collect/pdf_parser` 

#### Description 
This tool further extract the **affliations** and **inder terms** from the paper pdf files.

#### Workflow 
Firstly, lauch the **Grobid Service** with ```./gradlew run```. The default service url is ```http://localhost:8070```. We also use a **XMLLoader** object to load all items in a **year.xml** produced by [Step 1](#step1-crawl-a-website). 

**Grobid api** will return the pdf parsing results in xml format. However, we only need the **affiliations** and **index term**. So we use a **Formatter** ojbect to:
- read a pdf link from **XMLLoader** 
- download the pdf and sent the bytes to **Grobid api** 
- extract only **affiliations** and **index terms** from the parsing results 
- combine **affiliations**, **index term** and other metadata from the original XML files into a python dictionary object. 

finally, we use a **Converter** object to convert all those python dictionary objects into one single XML file, and this XML file can be verified by a general schema. 

A gerneral schema is needed here becase we might want to coleect papers from other sources and conferences, we wish all data could be stored in the same format, making it easier for further processing. 

#### Usage 
1. lauch the Grobid server at `http://localhost:8070` 
2. prepare all the XML files generated at [step 1](#step1-crawl-a-website) under the **xmls** directo
3. might need to edit the `start_year` and `end_year` in `main.py` depending on which year's data do we have under the **xmls** directory. 
4. `mkdir backup` for backing up intermediate results
5. `python main.py`, results are stored in `all_years.xml`
   
#### Issue
- [ ] Grobid sometimes failed to process a pdf file, need to re-process those failed links. The reason might be we are not using the official Grobid client for sending our requests, but only using the default **request** packages, which triggers unexpected bugs.

## process 
input: a xml file 
output: json files that can be easily imported into a sql database  

### step1: keyword extraction 
4 methods: tfidf, topic modelling, keyword clustering, all-cap 
requirements: 
- packages: sklearn, pandas, numpy, re, nltk, space, gensim 
- the output results from [collect](#collect)

#### Description 
Since the index terms dataset is sparse and has long-tail phenomemnon, we would like to find another way to extract keywords from a paper. 

#### Workflow 

##### Text Normalisation
The text normalisation for all methods includes:
- lowercase(except for the **All-Cap** method), tokenisation, punctuation removement, lowercase using **gensim simple_preprocess** function 
- lemmatization using **spacy**, we keep only the open classes including noun, verb, adj, and adv.

##### Methods
To keep it simple, we only apply the following methods on the **abtract** part. Some methods might work better on the full text, but we haven't tried it yet.
- **TfIdf**: Computed via **sklearn**'s **TfidfVectorizer** with default parameter setting. 
- **Topic Modelling**: 
  - For the word vector representation, we use **sklearn.feature_etraction.text.CountVectorizer**. 
  - **sklearn**'s **LatentDirichletAllocation** module is used to compute the topics. `n_component` is set to 50, `max_iter` is set to 20. During the analysis phrase, we only look at the top 20 words for each topic.

In addition to extract keywords from abtract, we also try to cluster many index terms into one group, and represent those words with the most frequent word within the group.
- **Clustering**: 
  - For the word vector representation, we use the pretained [GloVe](https://nlp.stanford.edu/projects/glove/) model `glove-wiki-gigaword-50`. For those phrases, its vector representation is the element-wise summation of all the words in it. If one of word in that phrases is an out-of-vocabulary(OOV) word for the pretrained model, we skip these phrase. 
  - Cluster: we use **sklearn.cluster.KMeans** for clustering, `n_clusters` is set to 100, and `init` method is `k-means++`. 

The naive and most straight-forward way is to use all-cap words(e.g. LSTM, DNN) as keywords.
- **All-Cap**: after text normalisation(without **lowercase**), extract those all-cap words and append them to the original keyword list.

#### Usage: 
- The implementation and analysis of the first three methods can be found respectively in `tfidf.ipynb`, `topic_modelling.ipynb` and `clustering.ipynb`. 
- To replace the keywords with all-cap words, prepare the formatted XML produced in the [previous step](#step2-process-pdf-files), and run:`python all_cap.py formatted.xml output.xml`. The replaced version will be stored as `output.xml`. 

#### Issue
- It might happen that one paper doesn't have any all-cap words, and all the index-terms contain OOV words, then it has to use the original index terms as its keywords. 
  
#### TODO 
- [ ] Maybe we should also use word embedding for topic modelling. 
- [ ] Need to replace index terms with the most frequent word in the corresponding cluster. 
  
### step2: xml to json 
#### Description
We use a relational database and **Django** for the **access** part, therefore we need to decouple the XML files into 5 tables: **conference**, **author**, **affiliations**, **keywords**, and **paper**. 
Since **Django** can automatically migrate a **Json** file into any backend relational database, so we use **JSON** to represent these 5 tables. 

#### Workflow 
Here's the database design:
*refer to the slide*
Since a **paper** instance need to reference instances in other tables, we first load **conference**, **author**, **affiliations**, and **keywords** into four independant tables, and assign an unique ID for each instance. 

Then we finialize the **paper** table, replace the dependant  field's value with its ID in the corresponding table. 

Each row is a JSON object, and the whole table is stored in one single JSON file. 

#### Usage 
prepare the formatted XML file produced in [step 1](#step1-keyword-extraction) and run the following command, the results will be stored in the *tables* directory, they're `conference.json, author.json, aff.json, keywords.json, paper.json`
   ```
   mkdir tables
   python to_json.py input.xml
   ```

## access 
input: database 
output: website 
requirement: 
- **Django**(https://www.djangoproject.com/)
- **Chart.js**(https://www.chartjs.org/)

#### Description
We use **Django** for better interraction and data accessing. **Chart.js** is used to plot the query results in the webpage. 

#### Data loading 
Clear the database and then load the produced JSON files into database.
   ```
   python manage.py flush 
   python manage.py loaddata conference.json 
   python manage.py loaddata author.json 
   ...
   ```

#### Query 
1. How do the publication number of top k keywords change over years?
   - filters: start year, end year, top k 
   - return: line chart 
2. How do the publication number of a given keyword change over years?
   - filters: start year, end year, keyword 
   - return: line chart 
3. What's the research interest distribution of a researcher within the given years?
   - filters: start year, end year, researcher 
   - return: line chart 
4. What's the research interest distribution of an affiliation within the given years?
   - filters: start year, end year, affiliation 
   - return: line chart 
