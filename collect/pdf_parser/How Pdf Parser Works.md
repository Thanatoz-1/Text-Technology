# How PDF Parser Works

Firstly, launch the **Grobid Service** with ```./gradlew run```. The default service url is ```http://localhost:8070```. We also use a [XMLLoader](xml_loader.py) object to load all items in a **year.xml** produced by [Step 1](../README.md)

Two types of information need to be extracted from the PDF file, the affiliations and the keywords(index terms in Interspeech conference).
- For the affiliation part, we use the `api/processAffiliations` of Grobid. Grobid is a machine learning based PDF content recognizer, it can recognize which part is the name of an affiliation. 
- For the index term part, we write a simple rule-based text processor, since the format of index terms is well-structured.

Two other packages are used. [TIKA](https://github.com/chrismattmann/tika-python) parser is used to extract the header area, which contains the affiliation information. [pdftotext](https://pypi.org/project/pdftotext/) is used to extract the column that contains the index terms.

The reason that we use different PDF parse: When extracting the header area, **pdftotext** produces more errors than **TIKA**, it sometimes skip the whole author and affiliation area while such situations are rare in **TIKA**. However, **TIKA** can split the columns. Interspeech papers have two columns of text, **TIKA** will merge these two columns. As a result, the line containing index terms is always concatenated with another line in the Introduction column, making it hard to extract index terms.

> A general schema is needed here because we might want to collect papers from other sources and conferences, we wish all data could be stored in the same format, making it easier for further processing. 