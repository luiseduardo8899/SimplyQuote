"""SimplyQuote URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url#, include
from django.conf import settings
from django.contrib.auth.views import LoginView
from django.conf.urls.static import static
from QuoteApp.views import registro, wiew_form_Account
#from QuoteApp.views import wiew_form_Account

urlpatterns = [
    path('admin/', admin.site.urls),
    path('quotes/', include("QuoteApp.urls")),
    path('accounts/', include('django.contrib.auth.urls')),
    path('registro/', registro, name='registro'),
    path('addaccount/', wiew_form_Account.index, name='addaccount'),
    path('saveaccount/', wiew_form_Account.process_form, name='saveaccount'),
]
