from django.http import HttpResponse
from django.shortcuts import render

from rake.core.query import *


def index(request):
    context = {"items": range(1, 10)}
    return HttpResponse(render(request, 'rake/index.html', context))


# todo
# def fetch_hot_words(num)->list:
#     words = list()
#     for i in range(0, num):
#         words.append({'word': 'word'+str(i), 'freq': i})
#     return words


def query(request, query_string, page):
    raw_query_string = query_string
    query_string = query_string[1:len(query_string)-1]

    cost = time.time()
    results, total_num = express_query(query_string, int(page), 10)
    state = '为您找到 %d 条新闻，共耗时 %f 秒' % (total_num, time.time()-cost)

    context = {
        "raw_query_string": raw_query_string,
        "query_string": query_string,
        "current_page": int(page),
        "total_page": range(0, 6),
        "results": results,
        'query_state': state
    }
    return HttpResponse(render(request, 'rake/news_list.html', context))
    #
    # context = {"items": range(1, 10)}
    # return HttpResponse(render(request, 'rake/index.html', context))
