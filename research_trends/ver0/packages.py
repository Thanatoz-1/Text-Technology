from django import forms

class KeywordsFilterForm(forms.Form):
    topk = forms.IntegerField(label="topk", initial=5)
    keywords = forms.CharField(label="keywords", initial='x')
    st_year = forms.IntegerField(label="start year", min_value=2010, max_value=2021, initial=2015)
    ed_year = forms.IntegerField(label="end year", min_value=2010, max_value=2021, initial=2020)

class ResearchFilterForm(forms.Form):
    topk = forms.IntegerField(label="topk", initial=5)
    author = forms.CharField(label="author")