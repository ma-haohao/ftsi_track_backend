"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path,include
from apscheduler.schedulers.background import BackgroundScheduler
from django.views.generic import TemplateView
'''from django_apscheduler.jobstores import DjangoJobStore, register_job
from scheduler_task.tasks import activeDatecheck,historyEngineInfo

#定时任务
scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), 'default')
@register_job(scheduler, "cron",day_of_week='mon-sun',hour='5', minute='0',second='0',id='activeDatecheck',replace_existing=True)
#@register_job(scheduler, "cron",second='10',id='activeDatecheck',replace_existing=True)
def scheduler_task1():
    activeDatecheck()
@register_job(scheduler, "cron",day_of_week='mon-sun',hour='6', minute='0',second='0',id='historyEngineInfo',replace_existing=True)
#@register_job(scheduler, "cron", second='20', id='historyEngineInfo', replace_existing=True)
def scheduler_task2():
    historyEngineInfo()

scheduler.start()'''


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', include('login.urls')),
    path('common/',include('common.urls')),
    path('ftsiMgr/', include('ftsiMgr.urls')),
    path('ftsiOpt/', include('ftsiOpt.urls')),
    path('userOpt/', include('userOpt.urls')),
    path('historyRecord/', include('historyRecord.urls')),
    path('portalOpt/', include('portalOpt.urls')),
    path('', TemplateView.as_view(template_name="index.html"))
]
