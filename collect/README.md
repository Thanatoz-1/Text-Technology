# Collect 

## Introduction
This module includes two steps, [Step 1](#step1-crawl-a-website) downloads paper metadata to an XML file. [Step 2](#step2-process-pdf-files) further extract the **affliations** and **index terms** from the paper pdf files, and integrate and format all information into a single XML file([an example](examples/2010.xml)), which can be verified by a [pre-defined XSD schema](pdf_parser/schema/papers_schema.xsd).

## Step1: crawl a website

- Description: This tool can download paper metadata to an xml file. The metadata includes the **title**, **abtract**, **author** and **url**. 
- Requirements: 
  - [Scrapy](https://scrapy.org/)
  - Website: [Interspeech archive](https://www.isca-speech.org/archive/))
- Code path: `collect/spider`
- Usage:
```xdg
# download paper metadata from 2010 to 2022
sh run.sh 2010 2022
```
- Example outputs: 
  - [2010.xml](examples/2010.xml): raw Scrapy's output
  - [papers.xml](examples/step1_papers.xml): formatted Scrapy's output, lacking index terms and affiliations.
- Detailed implementation: `collect/spider/getpdf/spiders/pdf_spider.py`
  
## Step2: process pdf files
- Description: This tool further extract the **affiliations** and **index terms** from the paper pdf files.
- Requirements: 
  - [Grobid service api](https://grobid.readthedocs.io/en/latest/Grobid-service/)
  - [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) + [lxml](https://lxml.de/) packages for easier XML parsing
  - [TIKA](https://pypi.org/project/tika/)
  - [pdftotext](https://pypi.org/project/pdftotext/)
- Code path: `collect/pdf_parser`
- Detailed implementation: [workflow and implementation document](pdf_parser/How%20Pdf%20Parser%20Works.md)
- Usage:
  1. launch the Grobid server at `http://localhost:8070` 
  2. prepare all the XML files generated at [step 1](#step1-crawl-a-website) under the **xmls** directory
  3. `mkdir checkpoint` for information backup
  4. `python main.py`, results are stored in `papers.xml` and `checkpoint/final.pkl`. The latter is an `XMLLoader` object, which makes it easier for latter operations. **NOTE** might need to edit the range of the years in the `main.py` based on how many years of data are prepared.
- Example output:
  - [papers.xml](examples/step2_papers.xml)