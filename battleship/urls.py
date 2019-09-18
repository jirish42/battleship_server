"""jawsirish URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home),
    url(r'^download/$', views.download),
    url(r'^message/$', views.message),
    url(r'^login/$', views.login),
    url(r'^createAccount/$', views.createAccount),
    url(r'^logout/$', views.logout),
    url(r'^profile/$', views.profile),
    url(r'^leaderboard/$', views.leaderboard),
    url(r'^admin/$', views.admin),
    url(r'^clearStats/$', views.clearStats),
    url(r'^app/login/$', views.appLogin),
    url(r'^app/game/$', views.game),
    url(r'^app/clearqueue/$', views.clearQueue)

]
