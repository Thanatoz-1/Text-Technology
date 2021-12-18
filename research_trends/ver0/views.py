from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from .models import *
import random
from collections import Counter

# the homepage, readme and documentation
def index(request):
    return render(request, "ver0/index.html")

def ran_color():
    color = "#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
    return color

def fetch_keyword_paper_tuple(start_year=2019, end_year=2021, topk=5):
    """
    return a list of tuple(keyword, total_paper_num, paper_num_over_year)
    keyword: the name of a keyword 
    total_paper_num: total num of paper containing the keyword published from 
        start_year to end_year 
    paper_num_over_year: length equals to (end_year-start_year+1), annually
        published papers related to the keyword
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
    key_paper = fetch_keyword_paper_tuple(st_year, ed_year)
    plot_data = display_topk(key_paper, st_year, ed_year, topk)
    print(plot_data)
    return render(request, "ver0/keywords.html", {
        "keyword_data" : plot_data
    })

def display_interest_pie(pie_model, name = None):
    # TODO: add a form to collect names
    name = pie_model.objects.all()[0]
    keys_counter = Counter()

    for paper in name.papers.all():
        for key in paper.keys.all():
            keys_counter[key.name] += 1

    # TODO: allow user to choose top k
    list_keys_count = keys_counter.most_common(5)
    keys, counts = zip(*list_keys_count)
    plot_data = {}
    plot_data["labels"] = keys 

    datasets = {}
    datasets["label"] = "# of papers"
    datasets["data"] = counts
    datasets["backgroundColor"] = [ran_color() for x in counts]
    plot_data["datasets"] = datasets
    return plot_data

def researchers_page(request):
    return render(request, "ver0/researchers.html", {
        "pie_data" : display_interest_pie(Author)
    })


def institutes_page(request):
    return render(request, "ver0/institutes.html", {
        "pie_data" : display_interest_pie(Affiliation)
    })
