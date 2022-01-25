# Collect 

## Introduction
This module includes two steps, [Step 1](#step1-crawl-a-website) downloads paper metadata to an XML file. [Step 2](#step2-process-pdf-files) further extract the **affliations** and **index terms** from the paper pdf files, and integrate and format all information into a single XML file([an example](pdf_parser/schema/papers_example.xml)), which can be verified by a [pre-defined XSD schema](pdf_parser/schema/papers_schema.xsd).

## Step1: crawl a website

- This tool can download paper metadata to an xml file. The metadata includes the **title**, **abtract**, **author** and **url**. [An example](spider/example/2010.xml) The xml file is named by the year. e.g. `2010.xml`
- website: [interspeech archive](https://www.isca-speech.org/archive/))
- requirement: [scrapy](https://scrapy.org/)
- code path: `collect/spider`
- usage:
```xdg
# download paper metadata from 2010 to 2022
sh run.sh 2010 2022
```
- detailed implementation and comments: `collect/spider/getpdf/spiders/pdf_spider.py`
  
## Step2: process pdf files
- This tool further extract the **affliations** and **index terms** from the paper pdf files.
- requirements: 
  - [Grobid service api](https://grobid.readthedocs.io/en/latest/Grobid-service/)
  - [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) + [lxml](https://lxml.de/) packages for easier XML parsing
- code path: `collect/pdf_parser`
- [workflow and implementation docuement](pdf_parser/How%20Pdf%20Parser%20Works.md)
- usage:
  1. launch the Grobid server at `http://localhost:8070` 
  2. prepare all the XML files generated at [step 1](#step1-crawl-a-website) under the **xmls** directory
  3. might need to edit the `start_year` and `end_year` in [main.py](pdf_parser/main.py) depending on which year's data do we have under the **xmls** directory. 
  4. `mkdir backup` for backing up intermediate results
  5. `python main.py`, results are stored in `all_years.xml`