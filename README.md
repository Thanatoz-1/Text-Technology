![Research Trends](./static/banner.jpg)

This project is designed to help you select and analyse your research interests in a visually appealing way. With this project, you will be able to carry out the following tasks:
- Examine trends for a particularly interesting area of research and follow its trend over a period of time and in various conferences. 
- View topics a particular researcher has been researching, based on his or her history of published research.
- Target a particular institution and see the latest and most popular research being conducted there.

## Quick links to Research Trends documentations:

- [Quick links to Research Trends documentations:](#quick-links-to-research-trends-documentations)
- [Data Collection](#data-collection)
- [Data Processing](#data-processing)
  - [Keyword Extraction](#keyword-extraction)
  - [XML to JSON](#xml-to-json)
- [Accessing the Application](#accessing-the-application)
- [Running the application](#running-the-application)
- [System Diagram](#system-diagram)

## Data Collection 

- [Documentation](collect/README.md)
- Directory: `./collect`

The aim of data collection was to build a corpus of all the publically available research publications from research conference websites. In order to achieve this goal, we used the following flow:

![](static/collect%20diagram.svg)

From each research publication, we collected the following data-points:
- Title of the paper
- Abstract of the paper 
- List of authors 
- URL
- Lis of Affliliated Institutions 
- Keywords/Index terms 


## Data Processing 
- [Documentation](process/README.md)
- Directory: `./process`

This module compares the write and read efficiency of three database types: [MySQL](https://www.mysql.com/), [MangoDB](https://www.mongodb.com/) and [ElasticSearch](https://www.elastic.co/). This comparison gives us insights as to which database backend we should plug in to the Django framework.

### Keyword Extraction 
In addition to extracting information using the above mentioned techniques, we also employed several techniques to enhance our collection of keywords and to make the spectrum of keywords even wider. We applied the following techniques for Keyword extraction.
- Tf-IDf based Keyword
- Capitalized words extraction
- Topic Modelling
- Clustering

Since the index terms dataset is sparse and has the long-tail phenomenon, it was necessary to employ the above-mentioned techniques for the dataset. 

Workflow:
![](static/keyward%20extraction.svg)

### XML to JSON 

We use a relational database and **Django** for **accessing the application**, therefore we needed to decouple the XML files into 5 tables: **conference**, **author**, **affiliations**, **keywords**, and **paper**. 
Because **Django** comes with its own modelling functionality for **JSON** files in the databases, we used **JSON** to represent these 5 tables. 


## Accessing the Application 

- [Documentation](research_trends/README.md)
- Directory: `./research_trends`
  
Finally, to make our entire pipeline accessable to the end-user, we used the python **Django** Framework as it is based on Model View Architecture [(MVC)](https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller). For Rendering the visual features, charts, and plots in our project, we also used [Chart.js](https://www.chartjs.org/).


## Running the application
The application is based on Django framework and this means that running the application is exactly the same. However, in order to install the dependencies of the project, we advise you to install a [virtual environment](https://docs.python.org/3/library/venv.html) and create the virtual environment as follows:
```bash
pip install -r requirements.txt
```
The required file _requirements.txt_ can be found in the project folder itself.

Once all the packages have been installed, you can navigate to the `research_trends` directory, follow the **Usage** session in the [document](./research_trends/README.md) to run our application. 

## System Diagram

![system](./static/system_diagram.svg)

---
