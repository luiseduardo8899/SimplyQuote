from django.conf.urls import url
from . import views

app_name = 'QuoteApp'
urlpatterns = [
    # ex: /QuoteApp/
    url(r'^generate_quote/$', views.generate_quote, name='generate_quote'),
    url(r'^view_all_quotes/$', views.view_all_quotes, name='view_all_quotes'),
    url(r'^view_quote/(?P<id>[0-9]+)/$', views.view_quote, name='view_quote'),
    ]
