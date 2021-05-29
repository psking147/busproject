# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.core.paginator import Paginator
from django.db.models import Q
import time
import folium
from folium.plugins import MarkerCluster, MiniMap
from folium import IFrame
from django.http import HttpResponse
import csv
import pandas as pd
import numpy as np
from haversine import haversine

def start(request):
    return render(request, 'sbclc/start.html')


def stop_index(request):
    page = request.GET.get('page', '1')
    kw = request.GET.get('kw', '')

    stop_list = StopCongestion.objects.order_by('-stop__ars')

    m = folium.Map(location=[37.53259896192619, 126.98341369628906], zoom_start=11)
    '''
    mc = MarkerCluster(name='abcd')
    stops = Stop.objects.all()
    for stop in stops:
        html = """
            <iframe src="./stop/""" + str(stop.ars) + """" width='100%' height='300vh'; style="border:none;"></iframe>
             """
        popup = folium.Popup(html, max_width=1000, min_width=600)
        icon = folium.Icon(icon='info-sign')
        location = [stop.y, stop.x]
        mc.add_child(folium.Marker(location=location, popup=popup, icon=icon))
    minimap = MiniMap()
    m.add_child(minimap)
    m.add_child(mc)
    m.add_child(folium.LatLngPopup())
    m.save('map.html')
    
    m = m._repr_html_()
    '''
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
    line = request.GET.get('line', '')

    line_list = LineCongestion.objects.order_by('-line')
    line_stops = Line.objects.filter(line_num=line)
    if line:
        start_stop = Stop.objects.filter(ars=line_stops[0].stop)
        if len(start_stop) > 0:
            start_location = [start_stop[0].y, start_stop[0].x]
            m = folium.Map(location=start_location, zoom_start=14)
        else:
            start_location = [37.53259896192619, 126.98341369628906]
            m = folium.Map(location=start_location, zoom_start=12)
    else:
        start_location = [37.53259896192619, 126.98341369628906]
        m = folium.Map(location=start_location, zoom_start=12)
    points = []
    for line_stop in line_stops:
        stops = Stop.objects.filter(ars=line_stop.stop)
        if len(stops) > 0:
            html = """
                <iframe src="./stop/""" + str(stops[0].ars) + """" width='100%' height='300vh'; style="border:none;"></iframe>
                """
            location = [stops[0].y, stops[0].x]
            points.append(location)
            popup = folium.Popup(html, max_width=1000, min_width=600)
            icon = folium.Icon(color='blue', icon='home', prefix='glyphicon')
            m.add_child(folium.Circle(location=location,
                                      radius=5,
                                      fill_color='black',
                                      popup=popup,
                                      icon=icon))
    minimap = MiniMap()
    m.add_child(minimap)
    m.add_child(folium.LatLngPopup())
    if len(points) >0:
        folium.PolyLine(points, color="blue", weight=5, opacity=1).add_to(m)
    m = m._repr_html_()

    if kw:
        line_list = line_list.filter(
            Q(line__icontains=kw)
            ).distinct()

    paginator = Paginator(line_list, 10)
    page_obj = paginator.get_page(page)
    context = {'line_list': page_obj, 'page': page, 'kw': kw, 'line': line, 'm': m}
    return render(request, 'sbclc/line_list.html', context)


def line_detail(request, line_line):
    line = Line.objects.filter(line_num=line_line)
    line_con = get_object_or_404(LineCongestion, line=line_line)
    allstops = Stop.objects.values_list('ars', flat=True)
    context = {'line': line, 'congestion': line_con, 'allstops': allstops}
    return render(request, 'sbclc/line_detail.html', context)


def maps(request):
    return render(request, 'sbclc/map.html')


def newline(request):
    context = {}
    return render(request, "sbclc/newline.html", context)


def confirm(request):
    gu = request.GET.get('gu', '')
    distance = request.GET.get('distance', '')

    if gu == "강남구":
        source_ars = 23458
        returns = [23366]
    elif gu == "강동구":
        source_ars = 25101
        returns = [25102]
    elif gu == "강북구":
        source_ars = 9102
        returns = [9104]
    elif gu == "강서구":
        source_ars = 16435
        returns = [16434]
    elif gu == "관악구":
        source_ars = 21809
        returns = [21337]
    elif gu == "광진구":
        source_ars = 5189
        returns = [5209]
    elif gu == "구로구":
        source_ars = 17290
        returns = [17289]
    elif gu == "금천구":
        source_ars = 18219
        returns = [18708]
    elif gu == "노원구":
        source_ars = 11193
        returns = [11209]
    elif gu == "도봉구":
        source_ars = 10340
        returns = [10341]
    elif gu == "마포구":
        source_ars = 14271
        returns = [14272]
    elif gu == "서초구":
        source_ars = 22367
        returns = [22378]
    elif gu == "성북구":
        source_ars = 8161
        returns = [8162]
    elif gu == "송파구":
        source_ars = 24503
        returns = [24658]
    elif gu == "양천구":
        source_ars = 15718
        returns = [15373]
    elif gu == "은평구":
        source_ars = 12469
        returns = [12470]
    elif gu == "중랑구":
        source_ars = 7418
        returns = [7550]
    line_length = int(distance)
    stops_label = pd.read_csv('data/정류장분류_혼잡도_방향_짝.csv', encoding="CP949")

    candidate = []
    max_cong = 0
    max_dist = 0
    dest_ars = 0

    source_row = stops_label.index[stops_label['ARS-ID'] == source_ars][0]
    source = [stops_label.iloc[source_row, 5], stops_label.iloc[source_row, 4]]
    for i in range(len(stops_label)):
        temp = [stops_label.iloc[i, 5], stops_label.iloc[i, 4]]  # 좌표
        dist = haversine(source, temp)  # 거리
        label = stops_label.iloc[i, 6]  # 레이블
        cong = stops_label.iloc[i, 7]  # 혼잡도
        ars = stops_label.iloc[i, 2]  # ars번호

        if dist < (line_length / 2) * 0.85 and dist > (line_length / 2) * 0.75:
            if label != 2:
                if cong > max_cong:
                    max_cong = cong
                    max_dist = dist
                    dest_ars = ars
                    dest = temp

    return_ars = dest_ars
    return_xy = dest
    max_x = max(source[1], dest[1])
    min_x = min(source[1], dest[1])
    max_y = max(source[0], dest[0])
    min_y = min(source[0], dest[0])
    x_diff = max_x - min_x
    y_diff = max_y - min_y
    if max_x == source[1] and min_y == source[0] and x_diff > y_diff:
        stops = stops_label[(stops_label['X좌표'] > min_x - 0.02) & (stops_label['X좌표'] < max_x + 0.02) &
                            (stops_label['Y좌표'] > min_y - 0.05) & (stops_label['Y좌표'] < max_y + 0.05)][
            'ARS-ID'].tolist()
    elif max_x == source[1] and min_y == source[0] and x_diff <= y_diff:
        stops = stops_label[(stops_label['X좌표'] > min_x - 0.05) & (stops_label['X좌표'] < max_x + 0.05) &
                            (stops_label['Y좌표'] > min_y - 0.02) & (stops_label['Y좌표'] < max_y + 0.02)][
            'ARS-ID'].tolist()
    elif max_x == dest[1] and min_y == dest[0] and x_diff <= y_diff:
        stops = stops_label[(stops_label['X좌표'] > min_x - 0.05) & (stops_label['X좌표'] < max_x + 0.05) &
                            (stops_label['Y좌표'] > min_y - 0.02) & (stops_label['Y좌표'] < max_y + 0.02)][
            'ARS-ID'].tolist()
    elif max_x == dest[1] and min_y == dest[0] and x_diff > y_diff:
        stops = stops_label[(stops_label['X좌표'] > min_x - 0.02) & (stops_label['X좌표'] < max_x + 0.02) &
                            (stops_label['Y좌표'] > min_y - 0.05) & (stops_label['Y좌표'] < max_y + 0.05)][
            'ARS-ID'].tolist()
    elif max_x == dest[1] and min_y == source[0] and x_diff > y_diff:
        stops = stops_label[(stops_label['X좌표'] > min_x - 0.02) & (stops_label['X좌표'] < max_x + 0.02) &
                            (stops_label['Y좌표'] > min_y - 0.05) & (stops_label['Y좌표'] < max_y + 0.05)][
            'ARS-ID'].tolist()
    elif max_x == dest[1] and min_y == source[0] and x_diff <= y_diff:
        stops = stops_label[(stops_label['X좌표'] > min_x - 0.05) & (stops_label['X좌표'] < max_x + 0.05) &
                            (stops_label['Y좌표'] > min_y - 0.02) & (stops_label['Y좌표'] < max_y + 0.02)][
            'ARS-ID'].tolist()
    elif max_x == source[1] and min_y == dest[0] and x_diff > y_diff:
        stops = stops_label[(stops_label['X좌표'] > min_x - 0.02) & (stops_label['X좌표'] < max_x + 0.02) &
                            (stops_label['Y좌표'] > min_y - 0.05) & (stops_label['Y좌표'] < max_y + 0.05)][
            'ARS-ID'].tolist()
    else:
        stops = stops_label[(stops_label['X좌표'] > min_x - 0.05) & (stops_label['X좌표'] < max_x + 0.05) &
                            (stops_label['Y좌표'] > min_y - 0.02) & (stops_label['Y좌표'] < max_y + 0.02)][
            'ARS-ID'].tolist()

    src_ars = source_ars
    dest_ars = return_ars
    dest = return_xy
    before_ars = 0
    next_ars = 0

    line_stops = []
    line_stops.append(source_ars)
    total_dist = 0
    local_dist = 0
    start = time.time()
    while src_ars != dest_ars:
        max_con = 0
        # 800m 이하
        ars_0, dist_0, con_0 = [], [], []
        ars_1, dist_1, con_1 = [], [], []
        ars_3, dist_3, con_3 = [], [], []
        # 800m~1.5km
        ars_0_over8, dist_0_over8, con_0_over8 = [], [], []
        ars_1_over8, dist_1_over8, con_1_over8 = [], [], []
        ars_3_over8, dist_3_over8, con_3_over8 = [], [], []
        # 1.5km 이상
        ars_0_over15, dist_0_over15, con_0_over15 = [], [], []
        ars_1_over15, dist_1_over15, con_1_over15 = [], [], []
        ars_3_over15, dist_3_over15, con_3_over15 = [], [], []

        src_row = stops_label.index[stops_label['ARS-ID'] == src_ars][0]
        src = [stops_label.iloc[src_row, 5], stops_label.iloc[src_row, 4]]  # src(현재 정류장) 좌표 [위도(y), 경도(x)]

        if before_ars != 0:  # 기점이 아닌경우
            before_row = stops_label.index[stops_label['ARS-ID'] == before_ars][0]
            before = [stops_label.iloc[before_row, 5],
                      stops_label.iloc[before_row, 4]]  # before(이전 정류장) 좌표 [위도(y), 경도(x)]
        num = 0
        isReturn = 0  # 회차지점 여부
        error = 0
        for stop in stops[::]:
            next_row = stops_label.index[stops_label['ARS-ID'] == stop][0]
            nexts = [stops_label.iloc[next_row, 5], stops_label.iloc[next_row, 4]]  # 다음 후보 정류장 좌표 [위도(y), 경도(x)]
            before_dist = local_dist
            dist = haversine(src, nexts)
            if nexts == src:  # 후보 정류장이 지금 현재 정류장인 경우 패스
                continue

            ars = stops_label.iloc[next_row, 2]
            if before_ars == 0:  # 현재 정류장이 기점일때
                # dist = haversine(src, nexts)
                a = haversine(src, dest)
                b = haversine(nexts, dest)
                cos = (a ** 2 + dist ** 2 - b ** 2) / (2 * a * dist)
                if dist > a * 1.01:  # 거리상 불가능한곳 후보에서 제거
                    stops.remove(stop)
                    continue
                if cos < 0:  # 각도상 먼경우 후보에서 제거
                    stops.remove(stop)
                    continue
                if dist > 2.3:  # 후보 정류장이 먼 경우 패스
                    continue
                    # 상하행 구분
                src_vector = [stops_label.iloc[src_row, 10], stops_label.iloc[src_row, 11]]  # 현재 정류장 방향 벡터 (x,y)
                next_vector = [stops_label.iloc[next_row, 10], stops_label.iloc[next_row, 11]]  # 후보 정류장 방향 벡터 (x,y)
                sn_vector = [nexts[1] - src[1], nexts[0] - src[0]]  # 현재 정류장, 후보 정류장 좌표를 이용한 벡터 (x, y)
                dot1 = sn_vector[0] * next_vector[0] + sn_vector[1] * next_vector[1]
                dot2 = sn_vector[0] * src_vector[0] + sn_vector[1] * src_vector[1]
                dot3 = next_vector[0] * src_vector[0] + next_vector[1] * src_vector[1]
                if dot1 < 0 or dot2 < 0 or dot3 < 0:  # 정류장 상하행 방향이 다른 경우 패스 ->  벡터 내적 이용
                    continue


            else:  # 현재 정류장이 기점이 아닐때
                if source_ars == 18219 and ars == 21114:
                    continue
                elif source_ars == 12469 and (ars == 14750 or ars == 4189):
                    continue
                if dist <= 1.5 and ars == dest_ars:  # 회차 지점이 일정 거리 내에 있을 때
                    isReturn = 1
                    break
                if source_ars == 18219 and ars == 21114:
                    continue
                if source_ars == 8161 and (ars == 14750 or ars == 4189):
                    continue

                a = haversine(src, dest)
                b = haversine(nexts, dest)
                cos = (a ** 2 + dist ** 2 - b ** 2) / (2 * a * dist)  # 코사인 제2법칙
                if a < 10:  # 회차지까지 거리가 10Km미만 남았을 때
                    if cos < -0.05:
                        stops.remove(stop)
                        continue
                    if source_ars == 23458:
                        angle = 0.6
                    elif source_ars == 18219 or source_ars == 14271 or (source_ars == 8161 and line_length > 45):
                        angle = 0.5
                    else:
                        angle = 0.77
                    if cos < angle:
                        continue
                    if dist > 2.3:
                        continue

                else:  # 회차지 까지 거리가 10km 이상 남았을때
                    if cos < -0.05:
                        stops.remove(stop)
                        continue
                    if source_ars == 25101 or source_ars == 21809 or source_ars == 5189 or source_ars ==22367:
                        if cos < 0.5:
                            continue
                    elif source_ars == 23458 or source_ars == 18219:
                        if cos < 0.1:
                            continue
                    elif source_ars == 8161:
                        if line_length >= 45:
                            if cos < 0.3:
                                continue
                    elif source_ars == 12469:
                        if line_length < 45:
                            if cos < 0:
                                continue
                        else:
                            if cos < 0.7:
                                continue
                    if dist > 2.3:
                        continue

                # 이전 정류장과 각도 비교
                c = haversine(nexts, before)
                cos_before = (before_dist ** 2 + dist ** 2 - c ** 2) / (2 * before_dist * dist)
                if cos_before > 0.05:
                    continue

                # 상하행 구분
                src_vector = [stops_label.iloc[src_row, 10], stops_label.iloc[src_row, 11]]  # 현재 정류장 방향 벡터 (x,y)
                next_vector = [stops_label.iloc[next_row, 10], stops_label.iloc[next_row, 11]]  # 후보 정류장 방향 벡터 (x,y)
                sn_vector = [nexts[1] - src[1], nexts[0] - src[0]]  # 현재 정류장, 후보 정류장 좌표를 이용한 벡터 (x, y)
                sr_vector = [dest[1] - src[1], dest[0] - dest[0]]  # 현재 정류장, 회차지 좌표를 이용한 벡터(x,y)
                dot1 = sn_vector[0] * next_vector[0] + sn_vector[1] * next_vector[1]
                dot2 = sn_vector[0] * src_vector[0] + sn_vector[1] * src_vector[1]
                dot3 = next_vector[0] * src_vector[0] + next_vector[1] * src_vector[1]

                if dot1 < 0 or dot2 < 0 or dot3 < 0:  # or dot4 < 0:  #정류장 상하행 방향이 다른 경우 패스 ->  벡터 내적 이용
                    continue

            label = stops_label.iloc[next_row, 6]
            cong = stops_label.iloc[next_row, 7]

            if 0.9 >= dist > 0.35:
                if label == 0:
                    ars_0.append(ars)
                    dist_0.append(dist)
                    con_0.append(cong)
                elif label == 1:
                    ars_1.append(ars)
                    dist_1.append(dist)
                    con_1.append(cong)
                elif label == 3:
                    ars_3.append(ars)
                    dist_3.append(dist)
                    con_3.append(cong)
            elif 0.9 < dist <= 1.5:
                if label == 0:
                    ars_0_over8.append(ars)
                    dist_0_over8.append(dist)
                    con_0_over8.append(cong)
                elif label == 1:
                    ars_1_over8.append(ars)
                    dist_1_over8.append(dist)
                    con_1_over8.append(cong)
                elif label == 3:
                    ars_3_over8.append(ars)
                    dist_3_over8.append(dist)
                    con_3_over8.append(cong)
            elif 1.5 < dist <= 2.3:
                if label == 0:
                    ars_0_over15.append(ars)
                    dist_0_over15.append(dist)
                    con_0_over15.append(cong)
                elif label == 1:
                    ars_1_over15.append(ars)
                    dist_1_over15.append(dist)
                    con_1_over15.append(cong)
                elif label == 3:
                    ars_3_over15.append(ars)
                    dist_3_over15.append(dist)
                    con_3_over15.append(cong)
            num += 1

        if isReturn == 1:
            next_ars = dest_ars
            local_dist = haversine(src, dest)
        elif len(ars_1) != 0:  # 1 label < 800m
            idx = con_1.index(max(con_1))
            next_ars = ars_1[idx]
            local_dist = dist_1[idx]
        elif len(ars_3) != 0:  # 3 label < 800m
            idx = con_3.index(max(con_3))
            next_ars = ars_3[idx]
            local_dist = dist_3[idx]
        elif len(ars_1_over8) != 0:  # 800m < 1 label < 1500m
            idx = con_1_over8.index(max(con_1_over8))
            next_ars = ars_1_over8[idx]
            local_dist = dist_1_over8[idx]
        elif len(ars_3_over8) != 0:  # 800m < 3 label < 1500m
            idx = con_3_over8.index(max(con_3_over8))
            next_ars = ars_3_over8[idx]
            local_dist = dist_3_over8[idx]
        elif len(ars_1_over15) != 0:  # 1 label > 1500m
            idx = con_1_over15.index(max(con_1_over15))
            next_ars = ars_1_over15[idx]
            local_dist = dist_1_over15[idx]
        elif len(ars_3_over15) != 0:  # 3 label > 1500m
            idx = con_3_over15.index(max(con_3_over15))
            next_ars = ars_3_over15[idx]
            local_dist = dist_3_over15[idx]
        elif len(ars_0) != 0:  # 0 label < 800m
            idx = con_0.index(max(con_0))
            next_ars = ars_0[idx]
            local_dist = dist_0[idx]
        elif len(ars_0_over8) != 0:  # 800m < 0 label < 1500m
            idx = con_0_over8.index(max(con_0_over8))
            next_ars = ars_0_over8[idx]
            local_dist = dist_0_over8[idx]
        elif len(ars_0_over15) != 0:  # 0 label > 1500m
            idx = con_0_over15.index(max(con_0_over15))
            next_ars = ars_0_over15[idx]
            local_dist = dist_0_over15[idx]
        else:
            print('nothing-error', error)

        before_ars = src_ars
        if next_ars != dest_ars:
            pairstop = stops_label[stops_label['ARS-ID'] == next_ars].reset_index(drop=True).iloc[0, 12]
            returns.insert(0, pairstop)
        src_ars = next_ars
        line_stops.append(src_ars)
        total_dist += local_dist
        stops.remove(src_ars)
        print(src_ars, total_dist, len(stops), num)
    for s in returns:
        line_stops.append(s)


    #make the map
    start_location = [37.53259896192619, 126.98341369628906]
    m = folium.Map(location=start_location, zoom_start=12)
    points = []
    for line_stop in line_stops:
        stops = Stop.objects.filter(ars=line_stop)
        if len(stops) > 0:
            html = """
                <iframe src="./stop/""" + str(stops[0].ars) + """" width='100%' height='300vh'; style="border:none;"></iframe>
                """
            location = [stops[0].y, stops[0].x]
            points.append(location)
            popup = folium.Popup(html, max_width=1000, min_width=600)
            icon = folium.Icon(color='blue', icon='home', prefix='glyphicon')
            m.add_child(folium.Circle(location=location,
                                      radius=5,
                                      fill_color='black',
                                      popup=popup,
                                      icon=icon))
    minimap = MiniMap()
    m.add_child(minimap)
    m.add_child(folium.LatLngPopup())
    if len(points) > 0:
        folium.PolyLine(points, color="blue", weight=5, opacity=1).add_to(m)
    m = m._repr_html_()
    stop_list = []
    for s in line_stops:
        stop_list = stop_list + list(Stop.objects.filter(ars=s))
    list_int = list(map(str, line_stops))
    request.session['list'] = list_int

    context = {'m': m, 'stop_list': stop_list, "distance": round(total_dist, 2)*2}
    return render(request, "sbclc/confirm.html", context)


def newcong(request):
    newLineStationList = request.session.get('list')

    def makeNewLineDirectODList(rdr, newLineStationList, newLineDirectODList, transferStationCandidateList, dayFactor):
        for ODData in rdr:
            if ODData[2] in newLineStationList:
                if ODData[4] in newLineStationList:
                    """새 노선과 일치하는 기존 노선 구간"""
                    directFlag = True
                    appendFlag = True
                    for k in newLineDirectODList:
                        if k[0] == ODData[2] and k[1] == ODData[4]:
                            k[2] += dayFactor * int(ODData[8])
                            if ODData[1] not in k[3]:
                                k[3].append(ODData[1])
                            appendFlag = False
                            break;
                    if appendFlag:
                        newLineDirectODList.append([ODData[2], ODData[4], dayFactor * int(ODData[8]), [ODData[1]]])
                else:
                    appendFlag = True
                    for k in transferStationCandidateList:
                        if k[0] == ODData[2] and k[1] == ODData[4]:
                            k[2] += dayFactor * int(ODData[8])
                            if ODData[1] not in k[3]:
                                k[3].append(ODData[1])
                            appendFlag = False
                            break;
                    if appendFlag:
                        transferStationCandidateList.append(
                            [ODData[2], ODData[4], dayFactor * int(ODData[8]), [ODData[1]]])

    def makeNewLineTransferODList(rdr, transferStationCandidateList, newLineStationList, newLineTransferODList,
                                  dayFactor):
        transferStationCandidateList.sort(key=lambda station: station[0])
        transferStationCandidateListLookup = []
        for i in transferStationCandidateList:
            transferStationCandidateListLookup.append(i[1])

        for ODData in rdr:
            if ODData[2] not in transferStationCandidateListLookup:
                continue
            for idx in range(transferStationCandidateListLookup.index(ODData[2]), len(transferStationCandidateList)):
                if ODData[2] == transferStationCandidateListLookup[idx]:
                    if ODData[4] in newLineStationList:
                        if ODData[1] in transferStationCandidateList[idx][3]:
                            continue;
                        appendFlag = True
                        for k in newLineTransferODList:
                            if k[4] == ODData[2] and k[5] == ODData[4]:
                                k[6] += dayFactor * int(ODData[8])
                                if ODData[1] not in k[7]:
                                    k[7].append(ODData[1])
                                appendFlag = False
                                break;
                        if appendFlag:
                            i = transferStationCandidateList[idx]
                            newLineTransferODList.append(
                                [i[0], i[1], i[2], i[3], ODData[2], ODData[4], dayFactor * int(ODData[8]), [ODData[1]]])
                else:
                    break

    def modifyLineCongestion(rdr, newLineDirectODList, newLineTransferODList, modifiedLineCongestion,
                             lineCongestionDiffList, transferFactor):
        lineNameList = []
        temp_lineCongestionDiffList = []
        lineOldPassengerList = []
        congestionDecreaseRatioLimit = 0.25

        next(rdr)
        for oldCongestion in rdr:
            modifiedLineCongestion.append(oldCongestion)
            if oldCongestion[0] == '110A':
                lineNameList.append('110A고려대')
            elif oldCongestion[0] == '110B':
                lineNameList.append('110B국민대')
            else:
                lineNameList.append(oldCongestion[0])
            temp_lineCongestionDiffList.append([oldCongestion[0], 0, 0])
            lineOldPassengerList.append(oldCongestion[1])

        for directOD in newLineDirectODList:
            nOfOldLine = len(directOD[3])
            passengerDiff = directOD[2] / (nOfOldLine + 1) / nOfOldLine
            # passengerDiff = abs(passengerDiff)
            for oldLine in directOD[3]:
                lineIdx = lineNameList.index(oldLine)
                if int(modifiedLineCongestion[lineIdx][1]) - passengerDiff < congestionDecreaseRatioLimit * int(
                        lineOldPassengerList[lineIdx]):
                    continue
                modifiedLineCongestion[lineIdx][1] = int(modifiedLineCongestion[lineIdx][1]) - passengerDiff / 30
                temp_lineCongestionDiffList[lineIdx][1] += passengerDiff / 30
                temp_lineCongestionDiffList[lineIdx][2] += passengerDiff / 30 / int(lineOldPassengerList[lineIdx])

        for transferOD in newLineTransferODList:
            passengerDiff = min(transferOD[2], transferOD[6]) * transferFactor
            abs(passengerDiff)
            for oldLine in transferOD[3]:
                lineIdx = lineNameList.index(oldLine)
                if int(modifiedLineCongestion[lineIdx][1]) - passengerDiff < congestionDecreaseRatioLimit * int(
                        lineOldPassengerList[lineIdx]):
                    continue
                modifiedLineCongestion[lineIdx][1] = int(modifiedLineCongestion[lineIdx][1]) - passengerDiff / 30
                temp_lineCongestionDiffList[lineIdx][1] += passengerDiff / 30
                temp_lineCongestionDiffList[lineIdx][2] += passengerDiff / 30 / int(lineOldPassengerList[lineIdx])
            for oldLine in transferOD[7]:
                lineIdx = lineNameList.index(oldLine)
                if int(modifiedLineCongestion[lineIdx][1]) - passengerDiff < congestionDecreaseRatioLimit * int(
                        lineOldPassengerList[lineIdx]):
                    continue
                modifiedLineCongestion[lineIdx][1] = int(modifiedLineCongestion[lineIdx][1]) - passengerDiff / 30
                temp_lineCongestionDiffList[lineIdx][1] += passengerDiff / 30
                temp_lineCongestionDiffList[lineIdx][2] += passengerDiff / 30 / int(lineOldPassengerList[lineIdx])

        for t in temp_lineCongestionDiffList:
            if (t[1] == 0):
                continue

            lineCongestionDiffList.append(t)

    def modifyStationCongestion(rdr, newLineTransferODList, modifiedStationCongestion, stationCongestionDiffList,
                                transferFactor):
        stationARSList = []
        temp_stationCongestionDiffList = []
        oldStationPassengerList = []
        congestionDecreaseRatioLimit = 0.25

        next(rdr)
        for oldCongestion in rdr:
            modifiedStationCongestion.append(oldCongestion)
            if (len(oldCongestion[0]) == 4):
                stationARSList.append('0' + oldCongestion[0])
            else:
                stationARSList.append(oldCongestion[0])
            temp_stationCongestionDiffList.append(
                [oldCongestion[0], 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
            passengerPerStation = 0
            for hour in range(1, 25):
                passengerPerStation += int(oldCongestion[hour])
            oldStationPassenger_temp = oldCongestion[1:25]
            oldStationPassenger_temp.append(passengerPerStation)
            oldStationPassengerList.append(
                oldStationPassenger_temp)  # oldStationPassengerList의 마지막 원소는 각 정류장의 시간대별 승차량 합=각 정류장 월 승차량

        for transferOD in newLineTransferODList:
            passengerDiff = min(transferOD[2], transferOD[6]) / transferFactor
            # passengerDiff = abs(passengerDiff)
            if len(transferOD[1]) == 0:
                continue;
            stationIdx = stationARSList.index(transferOD[1])
            passengerPerStation = oldStationPassengerList[stationIdx][-1]
            if sum(list(map(int, modifiedStationCongestion[stationIdx][
                                 1:25]))) - passengerDiff < congestionDecreaseRatioLimit * passengerPerStation:
                continue;
            for hours in range(0, 24):
                ratio = int(oldStationPassengerList[stationIdx][hours]) / passengerPerStation
                modifiedStationCongestion[stationIdx][hours + 1] = float(
                    modifiedStationCongestion[stationIdx][hours + 1]) - passengerDiff * ratio
                temp_stationCongestionDiffList[stationIdx][hours + 1] += passengerDiff * ratio

            temp_stationCongestionDiffList[stationIdx][-1] += passengerDiff / passengerPerStation

        for t in temp_stationCongestionDiffList:
            if (t[1] == 0):
                continue

            stationCongestionDiffList.append(t)

    # 환승 안하는 경우
    csv0316 = open('data/노선별_OD_20210316.csv', 'r', encoding='euc-kr')
    csv0320 = open('data/노선별_OD_20210320.csv', 'r', encoding='euc-kr')
    csv0321 = open('data/노선별_OD_20210321.csv', 'r', encoding='euc-kr')

    rdr0 = csv.reader(csv0316)
    rdr1 = csv.reader(csv0320)
    rdr2 = csv.reader(csv0321)
    newLineDirectODList = []
    transferStationCandidateList = []
    newLineTransferODList = []

    makeNewLineDirectODList(rdr0, newLineStationList, newLineDirectODList, transferStationCandidateList, 5)
    makeNewLineDirectODList(rdr1, newLineStationList, newLineDirectODList, transferStationCandidateList, 1)
    makeNewLineDirectODList(rdr2, newLineStationList, newLineDirectODList, transferStationCandidateList, 1)

    csv0316.close()
    csv0320.close()
    csv0321.close()

    # 환승 하는 경우
    csv0316 = open('data/노선별_OD_20210316.csv', 'r', encoding='euc-kr')
    csv0320 = open('data/노선별_OD_20210320.csv', 'r', encoding='euc-kr')
    csv0321 = open('data/노선별_OD_20210321.csv', 'r', encoding='euc-kr')

    rdr0 = csv.reader(csv0316)
    rdr1 = csv.reader(csv0320)
    rdr2 = csv.reader(csv0321)

    makeNewLineTransferODList(rdr0, transferStationCandidateList, newLineStationList, newLineTransferODList, 5)
    makeNewLineTransferODList(rdr1, transferStationCandidateList, newLineStationList, newLineTransferODList, 1)
    makeNewLineTransferODList(rdr2, transferStationCandidateList, newLineStationList, newLineTransferODList, 1)

    csv0316.close()
    csv0320.close()
    csv0321.close()

    for i in newLineDirectODList:
        i[2] /= 7
        i[2] *= 30
    for i in newLineTransferODList:
        i[2] /= 7
        i[2] *= 30
        i[6] /= 7
        i[6] *= 30

    csvLine = open('data/bus_line_com.csv', 'r', encoding='CP949')
    csvStation = open('data/bus_station_com.csv', 'r', encoding='CP949')

    rdr10 = csv.reader(csvLine)
    rdr11 = csv.reader(csvStation)

    modifiedLineCongestion = []
    modifiedStationCongestion = []

    lineCongestionDiffList = []
    stationCongestionDiffList = []

    modifyLineCongestion(rdr10, newLineDirectODList, newLineTransferODList, modifiedLineCongestion,
                         lineCongestionDiffList, 0.10)  # 마지막 인자는 환승객 변화량의 예상 비율
    modifyStationCongestion(rdr11, newLineTransferODList, modifiedStationCongestion, stationCongestionDiffList,
                            0.10)  # 마지막 인자는 환승객 변화량의 예상 비율

    linediffsum = 0
    linediffpsum = 0
    for line in lineCongestionDiffList:
        line[1] = round(line[1], 4)
        line[2] = round(line[2] * 100, 4)
        linediffsum += line[1]
        linediffpsum += line[2]
    linediffavg = round((linediffsum / len(lineCongestionDiffList)), 4)
    linediffpavg = round((linediffpsum / len(lineCongestionDiffList)), 4)


    stationCongestionDiffList2 = []
    stationdiffsum = 0
    stationdiffpsum = 0
    for stop in stationCongestionDiffList:
        a = []
        a.append(stop[0])
        a.append(round(sum(stop[1:25]), 4))
        a.append(round(stop[25] * 100, 4))
        stationCongestionDiffList2.append(a)
        stationdiffsum += round(sum(stop[1:25]), 4)
        stationdiffpsum += round(stop[25] * 100, 4)

    stationdiffavg = round((stationdiffsum / len(stationCongestionDiffList)), 4)
    stationdiffpavg = round((stationdiffpsum / len(stationCongestionDiffList)), 4)


    context = {'linediff': lineCongestionDiffList, 'stopdiff': stationCongestionDiffList2,
               'linediffavg': linediffavg, 'linediffpavg': linediffpavg,
               'stopdiffavg': stationdiffavg, 'stopdiffpavg': stationdiffpavg
               }
    return render(request, "sbclc/newcong.html", context)

'''
def csvtomodel(request):
    path1 = '/projects/mysite/data/정류장분류_혼잡도_방향_짝.csv'
    print('start2')
    with open(path1, newline='', encoding='CP949') as csvfile:
        data_reader = csv.DictReader(csvfile)
        for row in data_reader:
            t = Stop.objects.get(ars=row['ARS-ID'])
            t.pair = int(row['pair'])  # change field
            t.save()  # this will update only
            print(row)

    
    #stop table
    print('start')
    path1 = '/home/ubuntu/projects/mysite/data/정류장분류_혼잡도_방향_짝.csv'
    print('start2')
    with open(path1, newline='', encoding='CP949') as csvfile:
        data_reader = csv.DictReader(csvfile)
        for row in data_reader:
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
                yVector=row['yVector'],
                pair=row['pair']
            )


    #line congestion table
    path3 = '/home/ubuntu/projects/mysite/data/bus_line_com.csv'
    with open(path3, newline='', encoding='CP949') as csvfile:
        data_reader = csv.DictReader(csvfile)
        for row in data_reader:
            print(row)
            LineCongestion.objects.create(
                line=row['버스번호'],
                congestion=row['혼잡도']
            )

    #stop congestion table
    path4 = '/home/ubuntu/projects/mysite/data/bus_station_com.csv'
    with open(path4, newline='', encoding='CP949') as csvfile:
        data_reader = csv.DictReader(csvfile)
        for row in data_reader:
            print(row)
            if int(row['정류장ARS']) > 19535:
                StopCongestion.objects.create(
                    stop=Stop.objects.get(ars=row['정류장ARS']),
                    c0=row['0시'],
                    c1=row['1시'],
                    c2=row['2시'],
                    c3=row['3시'],
                    c4=row['4시'],
                    c5=row['5시'],
                    c6=row['6시'],
                    c7=row['7시'],
                    c8=row['8시'],
                    c9=row['9시'],
                    c10=row['10시'],
                    c11=row['11시'],
                    c12=row['12시'],
                    c13=row['13시'],
                    c14=row['14시'],
                    c15=row['15시'],
                    c16=row['16시'],
                    c17=row['17시'],
                    c18=row['18시'],
                    c19=row['19시'],
                    c20=row['20시'],
                    c21=row['21시'],
                    c22=row['22시'],
                    c23=row['23시'],
                )

    #line table
    path2 = '/home/ubuntu/projects/mysite/data/stationlist.csv'
    with open(path2, newline='', encoding='CP949') as csvfile:
        data_reader = csv.DictReader(csvfile)
        for row in data_reader:
            print(row)
            if int(row['index']) > 28896:
                Line.objects.create(
                    line_num=row['노선명'],
                    order=row['순번'],
                    stop=row['정류소번호'],
                    stop_name=row['정류소명']
                )
    return HttpResponse('create models~~')
    '''