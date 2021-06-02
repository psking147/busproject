from django.contrib import admin
from .models import *
# Register your models here.


class StopAdmin(admin.ModelAdmin):
    search_fields = ['ars', 'name']


class LineAdmin(admin.ModelAdmin):
    search_fields = ['line_num', 'stop']


class StopCongestionAdmin(admin.ModelAdmin):
    search_fields = ['stop.ars', 'stop.name']


class LineCongestionAdmin(admin.ModelAdmin):
    search_fields = ['line']


admin.site.register(Stop, StopAdmin)
admin.site.register(Line, LineAdmin)
admin.site.register(StopCongestion, StopCongestionAdmin)
admin.site.register(LineCongestion, LineCongestionAdmin)


