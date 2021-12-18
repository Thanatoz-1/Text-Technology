from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from .models import *
import random
# the homepage, readme and documentation
def index(request):
    return render(request, "ver0/index.html")

def ran_color():
    color = "#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
    return color

def cal_keywords_distribution(start_year=2019, end_year=2021, topk=5):
    """
    return a dictionary, the key of each entry is a keyword, 
    the value is the change of replated papers' number from
    start_year to min_year 
    """
    # TODO: sanity check for the year range
    key_paper = []
    keywords = Keyword.objects.all()
    for keyword in keywords:
        num_papers = []
        for year in range(start_year, end_year+1):
            num_papers.append(keyword.papers.filter(conference__year=year).count())
        key_paper.append((keyword.name, sum(num_papers), num_papers))
    return key_paper

def display_topk(key_paper, start_year, end_year, k):
    """
    return a dict obj for char display
    """
    # TODO: use database to fullfill this feature? 
    key_paper.sort(key=lambda x:x[1], reverse=True)
    key_paper = key_paper[:k]
    plot_data = {}
    plot_data["labels"] = list(range(start_year, end_year+1))
    datasets = []
    for key, _, nums in key_paper:
        key_data = {}
        key_data["data"] = nums 
        key_data["label"] = key 
        key_data["fill"] = False 
        # TODO: random color
        key_data["borderColor"] = ran_color()
        datasets.append(key_data)
    plot_data["datasets"] = datasets
    return plot_data

def keywords_page(request):
    st_year, ed_year, topk = 2019, 2021, 2
    key_paper = cal_keywords_distribution(st_year, ed_year)
    plot_data = display_topk(key_paper, st_year, ed_year, topk)
    print(plot_data)
    return render(request, "ver0/keywords.html", {
        "keyword_data" : plot_data
    })

def researchers_page(request):
    return render(request, "ver0/researchers.html")

def institutes_page(request):
    return render(request, "ver0/institutes.html")
