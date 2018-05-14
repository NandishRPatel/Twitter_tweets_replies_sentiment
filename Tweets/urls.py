from django.conf.urls import url,include
from . import views

urlpatterns = [
    url(r'^$', views.index,name='index'),
    url(r'^search_res/$', views.form_result,name='form_result'),
    url(r'^search_res/Tweet_\d+/[a-zA-Z0-9_]+/\d+$', views.reply_result,name='reply_result')


]