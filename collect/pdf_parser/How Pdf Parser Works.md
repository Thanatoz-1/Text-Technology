# How Pdf Parser Works

Firstly, lauch the **Grobid Service** with ```./gradlew run```. The default service url is ```http://localhost:8070```. We also use a [XMLLoader](xml_loader.py) object to load all items in a **year.xml** produced by [Step 1](../README.md)

**Grobid api** will return the pdf parsing results in xml format. However, we only need the **affiliations** and **index term**. So we use a [Formatter](grobid_formatter.py) ojbect to:
- read a pdf link from **XMLLoader** 
- download the pdf and sent the bytes to **Grobid api** 
- extract only **affiliations** and **index terms** from the parsing results 
- combine **affiliations**, **index term** and other metadata from the original XML files into a python dictionary object. 

Finally, we use a [Converter](converter.py) object to convert all those python dictionary objects into one single XML file, and this XML file can be verified by [a general schema](schema/papers_schema.xsd). 

> A gerneral schema is needed here becase we might want to coleect papers from other sources and conferences, we wish all data could be stored in the same format, making it easier for further processing. 