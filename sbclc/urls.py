from django.urls import path
from . import views


app_name = 'sbclc'


urlpatterns = [
    path('', views.start, name='start'),
    path('stop', views.stop_index, name='stopindex'),
    path('stop/<int:stop_ars>', views.stop_detail, name='stopdetail'),
    path('line', views.line_index, name='lineindex'),
    path('line/<str:line_line>', views.line_detail, name='linedetail'),
    path('maps', views.maps, name='maps'),
    path('newline', views.newline, name='newline'),
    path('confirm', views.confirm, name='confirm'),
    path('newcong', views.newcong, name='newcong'),
    #path('csvtomodel', views.csvtomodel, name='csvtomodel'),
]


