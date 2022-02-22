from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from .models import *
import random
from collections import Counter
from .query_forms import *
import time
from django.db.models import Q, Count
import mimetypes

def index(request):
    """ The home page, hosting the documentation
    Inputs: 
    ---
    A request object: [django.http.HttpRequest]

    Outputs:
    ---
    Returns a rendered html template as a response. The render()
    function takes a request object and maps it to the URL pattern
    specified in the second argument place to return the result.

    """
    return render(request, "ver0/index.html")

def ran_color():
    """ Generate a color id for each data point. 
    It's used at the front-end side for plotting charts.

    Inputs:
    ---
    NONE

    Outputs:
    ---
    Returns a randomly generated colour.

    Example: #EB700E
    """
    color = "#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
    return color

def plot_keyword_change_curve(curves, st, ed):
    """ Prepare the dict object for plotting dataset in chart.js 
    one datapoint format: [key, [num of paper at year1, num of paper at year2, ...]
    Example curves:
    ['ASR', [100, 24, 145]],
    ['TTS', [32, 41, 45]],
    ['RNN', [38, 214, 155]]
    """
    plot_data = {}
    plot_data["labels"] = list(range(st, ed+1))
    datasets = []
    for key, papers in curves:
        key_data = {}
        key_data["data"] =papers 
        key_data["label"] = key 
        key_data["fill"] = False 
        key_data["borderColor"] = ran_color()
        datasets.append(key_data)
    plot_data["datasets"] = datasets
    return plot_data


def fetch_display_given_keywords(st, ed, keywords):
    """ Given a list of keywords, find the change curve with those topics 

    Parameters
    ----------
    st: start year
    ed: end year 
    keyword: a list of keywords
    """
    # Naive method, quiry len(keywords) times 
    # TODO: remind users than some keywords doesn't exist

    curves = []
    for key in keywords: 
        key_year_count = Paper.objects.filter(keys__name=key).values('conference__year').filter(Q(conference__year__gte=st)&Q(conference__year__lte=ed)).annotate(total=Count('id')).order_by('conference__year')
        if len(key_year_count) == 0:
            continue 
        cur_year = st
        curve = []
        for sample in key_year_count:
            year = sample['conference__year']
            num_papers = sample['total']
            while cur_year < year:
                curve.append(0)
                cur_year += 1
            curve.append(num_papers)
            cur_year += 1
        curves.append([key, curve])
    return plot_keyword_change_curve(curves, st, ed)

def _fetch_keyword_paper_tuple_impl(st, ed, topk):
    """ An optimized method to obtain keyword paper tuple
    Inputs:
    ---
    st: [Int] The start year to filter results (value between 2010-2021)
    example: 2017
    ed: [Int] End year to filter result (value between 2010-2021)
    example: 2020
    topk: [Int] TopK results to return.
    example: 5


    Outputs:
    A list tuples: [List] containing: [Tuple]:
    Keyword [Str]
    Total num papers [Int] containing keyword between st and ed
    Annually published papers [Int] related to the keyword

    """
    tst = time.time()
    ted = time.time()
    print(f'---fetch keywords {ted - tst} ----')
    tst = time.time()
    key_year_count = Paper.objects.values('keys', 'conference__year').filter(Q(conference__year__gte=st)&Q(conference__year__lte=ed)).annotate(total=Count('id')).order_by('keys', 'conference__year')
    ted = time.time()
    print(f'----fetch key year count {ted - tst} ----')
    # key_year_count = list(key_year_count)
    
    prev_key = None
    prev_yr = 0
    key_paper = []
    tst = time.time()
    for sample in key_year_count:
        key = sample['keys']
        yr = sample['conference__year']
        count = sample['total']
        if key is None: continue 
        # key = keywords[key].name
        if key != prev_key:
            key_paper.append([key, count, [0]*(ed-st+1)])
            key_paper[-1][2][yr-st] = count
            prev_yr = yr 
            prev_key = key
        if yr != prev_yr:
            assert key == key_paper[-1][0]
            key_paper[-1][1] += count 
            key_paper[-1][2][yr-st] = count
    ted = time.time()
    # print(f'----loop over results {ted - tst}----')
    # print(f'year range {st} - {ed}')
    return key_paper

def fetch_keyword_paper_tuple(start_year=2015, end_year=2020, topk=5):
    """
    Inputs:
    ---
    NONE

    Returns: 
    ---
    Result of _fetch_keyword_paper_tuple_impl function
    """
    # TODO: sanity check for the year range

    return _fetch_keyword_paper_tuple_impl(start_year, end_year, topk)


def display_topk(key_paper, st, ed, k, key_set=None):
    """
    Returns a dictionary obj for char display

    Inputs:
    ---
    key_paper: [list] a list of tuples containing keyword [String] and keyword counts [Int] and
    annually published papers [Int] related to the keyword
    start_year: [Int] start year for filter
    Example: 2012
    end_year: [Int] end year for filter
    Example: 2019
    k: [Int] K An integer to obtain slice of 0-k results in key_paper
    Example: 5
    key_set: [None] or [List] list of keywords

    Return:
    plot_data: [Dictionary] a dictionary object to display topk results
    Example:
    
    {datasets: [list] containing key_data dictionary
    [{'data': [integer] nums,
     'label': [string] keyword,
     'fill': [Bool] False,
     'borderColor': Random color e.g. #EB700E}]
     }

    """
    # TODO: use database to fullfill this feature? 
    key_paper.sort(key=lambda x:x[1], reverse=True)
    key_paper = key_paper[:k]
    # keywords = Keyword.objects.all()
    
    curves = []
    for key, _, nums in key_paper:
        name = Keyword.objects.get(id=key).name
        print(key, name, nums)
        curves.append([name, nums])
    return plot_keyword_change_curve(curves, st, ed)

def keywords_page(request):
    """ This function renders the keywords page. 
    Inputs: 
    ---
    A request object: [django.http.HttpRequest]

    Outputs:
    ---
     Returns a rendered html template as a response. The render()
    function takes a request object and maps it to the URL pattern
    specified in the second argument place to return the result. and passes dictionary:
    {
        "keyword_data" : plot_data,
        "form": KeywordsFilterForm(),
        "topk": topk, 
        "st_year": st_year, 
        "ed_year": ed_year
    }

    With KeywordsFilter form for querying top k keywords trends
    """
    st_year, ed_year, topk = 2015, 2020, 5
    keywords = None 
    if request.method == "POST":
        form = KeywordsFilterForm(request.POST)

        if form.is_valid():
            topk = form.cleaned_data["topk"]
            keywords = str(form.cleaned_data["keywords"]).split(';')
            if keywords == ['x']:
                keywords = None
            else:
                topk = len(keywords)
            st_year = form.cleaned_data["st_year"]
            ed_year = form.cleaned_data["ed_year"]

    if keywords is None:
        print(f'------------------fetch_keyword_paper_tuple() start------------------------')
        st = time.time()
        key_paper = fetch_keyword_paper_tuple(st_year, ed_year)
        ed = time.time()
        plot_data = display_topk(key_paper, st_year, ed_year, topk, keywords)
        print(f'------------------fetch_keyword_paper_tuple(): {ed-st}------------------------')
    else:
        plot_data = fetch_display_given_keywords(st_year, ed_year, keywords)
    return render(request, "ver0/keywords.html", {
        "keyword_data" : plot_data,
        "form": KeywordsFilterForm(),
        "topk": topk, 
        "st_year": st_year, 
        "ed_year": ed_year
    })

def generate_empty_pie(name='none', key_name='none'):
    """ For researcher and affiliation page. 
    If the database doesn't contain any data related to
    the given author or affiliation, we need a empty 
    pie object to notify the front end.

    Inputs:
    ---
    key_name: [String] the table name, "author" or "affiliation"
    Example: 'author'
    name: [String] the query, an author or affiliation name given by the user
    Example: 'Michael Smith'

    Outputs:
    ---
    plot_data: [Dictionary] A dictionary object which includes all the data needed 
    to draw the pit chart at the front-end side.
    """
    plot_data = {}
    plot_data['labels'] = []
    datasets = {}
    datasets["label"] = []
    datasets["data"] = []
    datasets["backgroundColor"] = []
    plot_data["datasets"] = datasets
    plot_data[key_name] = name
    return plot_data
    

def display_interest_pie(target_name, topk, model, key_name):
    """ For research and affiliation page. 
    Display the interest distribution pie chart for `target_name`
    Only show the top k fileds of interests.

    Inputs:
    ---
    target_name: [String] the query, an author or affiliation name given by the user
    Example: 'Carnegie Mellon University'
    topk: [Integer] only show top k fileds of interests
    Example: 5
    model: [django.db.models.Model] the table, Django use a "Model" object to represent a table
    key_name: [String] the table name, could be "author" or "affiliation" 
    Example: 'Affiliation'

    Outputs:
    ---
    plot_data: [Dictionary] A dictionary object which includes all the data needed 
    to draw the pie chart at the front-end side.
    """
    target = model.objects.filter(name=target_name)
    if target.count() == 0:
        return generate_empty_pie(target_name, key_name), []
    elif target.count() == 1:
        target = target[0]
    else:
        # TODO: what if more than one user 
        target = target[0]
    
    keys_counter = Counter()
    paper_list = []

    for paper in target.papers.all():
        keynames = []
        for key in paper.keys.all():
            keyname = key.name
            keys_counter[keyname] += 1
            keynames.append(keyname)
        # print(paper.title)
        paper_list.append([paper.title, paper.url, ';'.join(keynames)])

    list_keys_count = keys_counter.most_common(topk)
    keys, counts = zip(*list_keys_count)
    plot_data = {}
    plot_data["labels"] = keys 

    datasets = {}
    datasets["label"] = "# of papers"
    datasets["data"] = counts
    datasets["backgroundColor"] = [ran_color() for x in counts]
    plot_data["datasets"] = datasets
    plot_data[key_name] = target_name 
    return plot_data, paper_list

def researchers_page(request):
    """ Render the researcher page.
     Inputs: 
    ---
    A request object: [django.http.HttpRequest]

    Outputs:
    ---
     Returns a rendered html template as a response. The render()
    function takes a request object and maps it to the URL pattern
    specified in the second argument place to return the result. and passes dictionary:
    {
        "pie_data" : display_interest_pie(author, topk, Author, 'author'),
        "form": ResearchFilterForm()
    }
    With ResearchFilterForm() to query the research interest distribution for a single given author
    """
    author = 'Jay Mahadeokar'
    topk = 5
    
    form = ResearchFilterForm()
    if request.method == "POST":
        form = ResearchFilterForm(request.POST)
    
        if form.is_valid():
            topk = form.cleaned_data["topk"]
            author = form.cleaned_data["author"]

    pie_data, paper_list = display_interest_pie(author, topk, Author, 'author')
    return render(request, "ver0/researchers.html", {
        "pie_data" : pie_data,
        "paper_list": paper_list,
        "form": form
    })


def affiliations_page(request):
    """ Render the affiliation page.
    Inputs: 
    ---
    A request object: [django.http.HttpRequest]

    Outputs:
    ---
     Returns a rendered html template as a response. The render()
    function takes a request object and maps it to the URL pattern
    specified in the second argument place to return the result. and passes dictionary:
    {
        "pie_data" : display_interest_pie(aff, topk, Affiliation, 'affiliation'),
        "form": AffiliationFilterForm()
    }
    With AffiliationFilterForm() to query research interest distribution of an affiliation.
    
    """
    aff = "Google Research"
    topk = 5

    form = AffiliationFilterForm()
    if request.method == "POST":
        form = AffiliationFilterForm(request.POST)
    
        if form.is_valid():
            topk = form.cleaned_data["topk"]
            aff = form.cleaned_data["affiliation"]
        print(f'topk {topk}, aff {aff}') 

    pie_data, paper_list = display_interest_pie(aff, topk, Affiliation, 'affiliation')
    return render(request, "ver0/affiliations.html", {
        "pie_data" : pie_data,
        "paper_list" : paper_list, 
        "form": form
    })

def download_file(request):
    """ WIP: a download link, enable users to download the query results in XML format.
    Inputs: 
    ---
    A request object: [django.http.HttpRequest]

    Outputs:
    ---
    A response object: [django.http.HtttpResonse] with path to download query results in XML format.
    """
    fl_path = 'x' 
    fl_name = 'somename.py'

    fl = open(fl_path, 'r')
    mime_type = mimetypes.guess_type(fl_path)
    response = HttpResponse(fl, content_type=mime_type)
    response['Content-Disposition'] = 'attachment; filename=%s' % fl_name
    return response