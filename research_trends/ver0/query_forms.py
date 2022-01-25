from django import forms
# The following forms represents all kinds of query we support form now 

class KeywordsFilterForm(forms.Form):
    """ 
    topk: for querying top k keywords trends, keywords are sorted by the number of papers related to it
    keywords: for querying some specific keywords trends
        - notice, if the value is 'x', its value will be ignored, the page will only plot topk keywords
          trend
    st_year, ed_year: the start year and end year of the trend
    """
    topk = forms.IntegerField(label="topk", initial=5)
    keywords = forms.CharField(label="keywords", initial='x')
    st_year = forms.IntegerField(label="start year", min_value=2010, max_value=2021, initial=2015)
    ed_year = forms.IntegerField(label="end year", min_value=2010, max_value=2021, initial=2020)

class ResearchFilterForm(forms.Form):
    """ For querying the research interst distribution of an author
    topk: only present top k fields of interest
    author: the name of one author
    """
    topk = forms.IntegerField(label="topk", initial=5)
    author = forms.CharField(label="author")

class AffiliationFilterForm(forms.Form):
    """ For querying the research interst distribution of an affiliation
    topk: only present top k fields of interest
    affiliation: the name of one affiliation
    """
    topk = forms.IntegerField(label="topk", initial=5)
    affiliation = forms.CharField(label="affiliation")