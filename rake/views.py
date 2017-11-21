from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone

from rake.models import QueryResultItem


def index(request):
    context = {"items": range(1, 10)}
    return HttpResponse(render(request, 'rake/index.html', context))


# todo
def query(request, query_string, page):
    results = []
    for i in range(1, 10):
        results.append(QueryResultItem(
            title='News Title',
            url='http://www.baidu.com',
            digest='Lorem ipsum dolor sit amet, consectetur adipiscing elit.\n'
                      'Mauris sagittis pellentesque lacus eleifend lacinia...',
            keywords='keyword',
            source='XinHua',
            datetime=timezone.now()
        ))
    context = {"query_string": query_string, "current_page": 2, "total_page": 10, "results": results}
    return HttpResponse(render(request, 'rake/news_list.html', context))
