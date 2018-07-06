
from django.conf.urls import include, url
from hawkeye.views import *
from . import views
app_name = 'hawkeye'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^subcat$',views.subcat,name='subcat'),
    url(r'^nude$',views.nude,name='nude'),
    url(r'^check_text$',views.check_text,name='check_text'),
    url(r'^check_watermark$',views.check_watermark,name='check_watermark')
    #url(r'^result/$', views.result, name='result')
]