#Research Trends Documentation
---

##Overview

The Research Trends applications allows users to query a database of research papers presented at various conferences from 2012 to 2021. Query results will return graphical representations of changes in key words found in paper abstracts as well as proportional contributions from authors and institutions. In addition, these data are available for download as an XML dataset.

---

## Data Collection



---

##The Database

Our first task was to profile several relational and NoSQL databases to test loading and query efficiency. The databases selected were MySQL, MongoDB, and ElasticSearch. The breakdown of loading speeds can be seen in the below table:

|   | MySQL | MongoDB| ElasticSearch|
|------|------|------| -----|
|**Load 1M Queries (Hrs.)**| 3:58 | 4:08 | 5:51|


We have opted to use a relational database due to quicker query times. This design allows for quicker retrieval of the XML dataset. 


---

##API

*Description of API*

1. Method 1
    *Description*
    >*Syntax*

    *Example description*

    >*Example*

2. Method 2
    *Description*
    >*Syntax*

    *Example description*

    >*Example*

3. Methon n
    *Description*
    >*Syntax*

    *Example description*
    >*Example*


---

##XML Dataset

*Structure/Schema*

>XML SCHEMA

Example:

>Example

###Converter

*Description of Converter*

>Code






