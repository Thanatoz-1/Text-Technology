from django import forms

class KeywordsFilterForm(forms.Form):
    topk = forms.IntegerField(label="topk")
    keywords = forms.CharField(label="keywords")
    st_year = forms.IntegerField(label="start year", min_value=2010, max_value=2021)
    ed_year = forms.IntegerField(label="end year", min_value=2010, max_value=2021)