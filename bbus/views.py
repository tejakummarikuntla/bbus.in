from django.conf import settings
if not settings.configured:
    settings.configure()
import json
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
import requests
from lxml import html
from BeautifulSoup import BeautifulSoup
from bbus_utils import *

def index(request):
    return render(request, 'index.html')

def search(request):
    if request.method != 'POST':
        return HttpResponseRedirect('/')
    src = request.POST.get('from')
    dst = request.POST.get('to')
    how = request.POST.get('how')
    page = requests.post(settings.DATA_URL,
        data={'from': src, 'to': dst, 'how': how},
        headers={"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:19.0) Gecko/20100101 Firefox/19.0"})
    soup = BeautifulSoup(page.text)
    tables = soup.findAll('table')
    bus_routes = []
    routes = 0
    for table in tables:
        routes += 1
        bus_routes.append(table2json(table.findAll('tr')))
    return render(request, 'search.html', {'routes':bus_routes})

def api(request):
    src = request.GET.get('from')
    dst = request.GET.get('to')
    how = request.GET.get('how')
    page = requests.post(settings.DATA_URL,
        data={'from': src, 'to': dst, 'how': how},
        headers={"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:19.0) Gecko/20100101 Firefox/19.0"})
    soup = BeautifulSoup(page.text)
    tables = soup.findAll('table')
    bus_routes = {}
    routes = 0
    for table in tables:
        routes += 1
        bus_routes['route'+str(routes)] = table2json(table.findAll('tr'))

    return HttpResponse(json.dumps(bus_routes), content_type="application/json")


