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
- [Running the application](#running-the-application)

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
#### Step1: Keyword Extraction
Apart from extracting different information using the above mentioned techniques, we also tried to perform few techniques to enhance our collection of keywords to make the spectrum of keywords even wider. We applied the following techniques for Keyword extraction.
- Tf-IDf based Keyword
- Capitalized words extraction
- Topic Modelling
- Clustering

Since the index terms dataset is sparse and has long-tail phenomemnon, the need for trying other techniques still prevails for the dataset. 

#### Step2: Text Normalization
The text normalisation for all methods includes:
- lowercase(except for the **All-Cap** method), tokenisation, punctuation removement, lowercase using **gensim simple_preprocess** function 
- lemmatization using **spacy**, we keep only the open classes including noun, verb, adj, and adv.

### step3: XML to JSON 

We use a relational database and **Django** for **accessing the appliaction**, therefore we needed to decouple the XML files into 5 tables: **conference**, **author**, **affiliations**, **keywords**, and **paper**. 
Since **Django** comes with its own modelling functionality for **Json** file into the databases, so we used **JSON** to represent these 5 tables. 

#### Usage 
prepare the formatted XML file produced in [step 1](#step1-keyword-extraction) and run the following command, the results will be stored in the *tables* directory, they're `conference.json, author.json, aff.json, keywords.json, paper.json`
   ```
   mkdir tables
   python to_json.py input.xml
   ```

## Accessing the Application 
Finally to make our entire pipeline accessing by end-user, we used the python **Django** Framework as it is based on Model View Architure [(MVC)](https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller). For Rendering the visual features, the charts and plots, in our project we also used [Chart.js](https://www.chartjs.org/).


## Running the application
The application is based on Django framework and this means that running the application is exactly the same. But in order to install the dependencies of the project, we advice you to install some [virtual environment](https://docs.python.org/3/library/venv.html) and create the virtual environment as follows:
```bash
pip install -r requirements.txt
```
The reqruied file _requirements.txt_ could be found in the project folder itself.

Once all the packages have been installed, you can run our application by running the following command
```bash
python manage.py runserver
```
## System Diagram


![system](./static/system_diagram.svg)

---