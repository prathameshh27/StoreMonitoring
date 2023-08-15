"""
URL configuration for StoreMonitoring project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path

from .views import run_report, get_report, debug_code

urlpatterns = [
    path('debug_code/<sid>', debug_code, name="debug_code" ),
    path('trigger_report/', run_report, name="trigger_report" ),
    path('get_report/<rid>', get_report, name="get_report" ),
] 
