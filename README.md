![Research Trends](./static/banner.jpg)

This is the project to help you with selecting and analysing your research interests through a visually appealing way. With this project, you will be able to carry out the following tasks:
- Look at the trends for a particularly interesting research and look its trend over a period of time in various conferences. 
- Look at the topics a particular professor has been researching on based on his research publications
- Target a particular institution and see the latest and most popular researches being carried out there.

## Quick links to Research Trends documentations:

- [Data Collection](#data-collection)
  - [Step1: crawl a website](#step1-crawling-a-website)
  - [Step2: process pdf files](#step2-process-pdf-files)
- [Data Processing](#data-processing)
  - [step1: keyword extraction](#step1-keyword-extraction)
  - [step2: xml to json](#step2-xml-to-json)
- [Accessing the application](#accessing-the-application)

## Data Collection 
The aim of data collection was to build a corpus of all the publically available research publications from research conference websites. In order to achieve this goal, we used the following flow:

Input-website $\rightarrow$ collect data $\rightarrow$ Process data in defined XML format $\rightarrow$ and finally load the data in database.


From each research publication, we collected the following data-points:
- Title of the paper
- List of authors 
- Affiliation 
- Abstract of the paper 
- Keywords/ Index terms 
- url

### Step1: crawling a website 

#### Description 
For this version, we crawled research conference paper's website (particularly [Interspeech archive](https://www.isca-speech.org/archive/)) and collected all their research publications publically available into our collection. We obtained **9989** research publications ranging from year **2010** to **2021** in _pdf_ formats.

#### Workflow
For this, we used the python web-scrapping library [scrapy](https://scrapy.org/). Apart from that, we extracted all the required data-points from the obtained pdf using another tool [Grobid](https://grobid.readthedocs.io/en/latest/). This tool can download paper metadata to an xml file along with the data itself. 

The metadata includes the **title**, **abtract**, **author** and **url**. One example output could be found in the *example* directory.

#### Usage
```xdg
# download paper metadata from 2010 to 2022
sh run.sh 2010 2022
```

### Step2: process pdf files 
As briefly mentioned above, we used [Grobid API](https://grobid.readthedocs.io/en/latest/Grobid-service/) for processing and collecting data from the obtained pdf files. Apart from that, a huge chunk of html tags were also cleaned using another python package that goes by the name of [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) along with [lxml](https://lxml.de/) parser for easier XML parsing.

The code for the processing and collection could be found at `collect/pdf_parser` 

## Data Processing 
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

## Accessing the Database 
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
