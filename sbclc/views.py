# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.core.paginator import Paginator
from django.db.models import Q
import time
import folium
from django.http import HttpResponse
import csv


def start(request):
    return render(request, 'sbclc/start.html')


def stop_index(request):
    page = request.GET.get('page', '1')
    kw = request.GET.get('kw', '')

    stop_list = StopCongestion.objects.order_by('-stop__ars')
    m = folium.Map(location=[37.53259896192619, 126.98341369628906], zoom_start=11)
    folium.Marker(location=[37.53259896192619, 126.98341369628906], tooltip='click for more', popup='test').add_to(m)
    m = m._repr_html_()
    if kw:
        stop_list = stop_list.filter(
            Q(stop__ars__icontains=kw) |
            Q(stop__name__icontains=kw)
            ).distinct()

    paginator = Paginator(stop_list, 10)
    page_obj = paginator.get_page(page)
    context = {'stop_list': page_obj, 'page': page, 'kw': kw, 'm': m}
    return render(request, 'sbclc/stop_list.html', context)


def stop_detail(request, stop_ars):
    stop = get_object_or_404(Stop, ars=stop_ars)
    hour = time.strftime('%H', time.localtime(time.time()))
    stop_con = get_object_or_404(StopCongestion, stop__ars=stop_ars)
    context = {'stop': stop, 'congestion': stop_con, 'hour': hour}
    return render(request, 'sbclc/stop_detail.html', context)


def line_index(request):
    page = request.GET.get('page', '1')
    kw = request.GET.get('kw', '')

    line_list = LineCongestion.objects.order_by('-line')
    m = folium.Map(location=[37.53259896192619, 126.98341369628906], zoom_start=11)
    folium.Marker(location=[37.53259896192619, 126.98341369628906], tooltip='click for more', popup='test').add_to(m)
    m = m._repr_html_()
    if kw:
        line_list = line_list.filter(
            Q(line__icontains=kw)
            ).distinct()
    paginator = Paginator(line_list, 10)
    page_obj = paginator.get_page(page)
    context = {'line_list': page_obj, 'page': page, 'kw': kw, 'm': m}
    return render(request, 'sbclc/line_list.html', context)


def line_detail(request, line_line):
    line = Line.objects.filter(line_num=line_line)
    line_con = get_object_or_404(LineCongestion, line=line_line)
    context = {'line': line, 'congestion': line_con}
    return render(request, 'sbclc/line_detail.html', context)

'''
def maps(request):
    m = folium.Map(location=[37.53259896192619, 126.98341369628906], zoom_start=11)
    folium.Marker(location=[37.53259896192619, 126.98341369628906], tooltip='click for more', popup='test').add_to(m)
    m = m._repr_html_()

    context = {
        'm': m,
    }
    return render(request, 'map.html', context)
def csvtomodel(request):
    path = '/projects/mysite/data/정류장분류_혼잡도_방향.csv'
    with open(path, newline='') as csvfile:
        data_reader = csv.DictReader(csvfile)
        i=0
        for row in data_reader:
            if i == 0:
                i+=1
                continue
            print(row)
            Stop.objects.create(
                index=row['index'],
                standard_id=row['표준ID'],
                ars=row['ARS-ID'],
                name=row['정류소명'],
                x=row['X좌표'],
                y=row['Y좌표'],
                labels=row['labels'],
                congestion=row['congestion'],
                before=row['before'],
                after=row['after'],
                xVector=row['xVector'],
                yVector=row['yVector']
            )
    return HttpResponse('create models~~')

def csvtomodel(request):
    path = '/projects/mysite/data/stationlist.csv'
    with open(path, newline='') as csvfile:
        data_reader = csv.DictReader(csvfile)
        i = 0
        for row in data_reader:
            if i == 0:
                i += 1
                continue
            print(row)
            Line.objects.create(
                line_num=row['노선명'],
                order=row['순번'],
                #stop=Stop.objects.get(ars=row['정류소번호']),
                stop=row['정류소번호']

            )
    return HttpResponse('create models~~')
'''


