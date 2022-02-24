from django import forms
from ajax_select.fields import AutoCompleteField 
from .models import *
from .lookup import *
# The following forms represents all kinds of query we support form now 

class KeywordsFilterForm(forms.Form):
    """ 
    topk: for querying top k keywords trends, keywords are sorted by the number of papers related to it
    keywords: for querying some specific keywords trends
        - notice, if the value is 'x', its value will be ignored, the page will only plot topk keywords
          trend
    st_year, ed_year: the start year and end year of the trend
    """
    topk = forms.IntegerField(label="topk", min_value=1, max_value=50, initial=5)
    keywords = forms.CharField(label="keywords", initial='x')
    st_year = forms.IntegerField(label="start year", min_value=2010, max_value=2021, initial=2015)
    ed_year = forms.IntegerField(label="end year", min_value=2010, max_value=2021, initial=2020)


class ResearchFilterForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name']
    """ For querying the research interst distribution of an author
    topk: only present top k fields of interest
    author: the name of one author
    """
    topk = forms.IntegerField(min_value=1, max_value=50, widget=forms.NumberInput(attrs={'placeholder': 'topK', 'style': 'width: 300px;', 'class': 'form-control'}))
    name = AutoCompleteField('author-lookup', required=False, help_text=None)


class AffiliationFilterForm(forms.ModelForm):
    """ For querying the research interest distribution of an affiliation
    topk: only present top k fields of interest
    affiliation: the name of one affiliation
    """
    class Meta:
        model = Affiliation
        fields = ['name']
    # name = AutoCompleteField('aff-lookup', required=False, help_text=None, widget=forms.TextInput(attrs={'placeholder': 'affiliation', 'style': 'width: 300px;', 'class': 'form-control'}))
    topk = forms.IntegerField(min_value=1, max_value=50, widget=forms.NumberInput(attrs={'placeholder': 'topK', 'style': 'width: 300px;', 'class': 'form-control'}))
    name = AutoCompleteField('aff-lookup', required=False, help_text=None)