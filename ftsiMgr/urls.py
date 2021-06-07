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
from django.urls import path
from . import ftsi_operation,ftsi2ips_opt,pendingMgr

urlpatterns = [
    path('getFTSI/', ftsi_operation.get_ftsi),
    path('paraforAddFTSI/', ftsi_operation.para_for_addftsi),
    path('FTSInumExistCheck/', ftsi_operation.ftsi_num_check),
    path('addFTSI/', ftsi_operation.add_ftsi),
    path('getFTSIInfo/', ftsi_operation.getFTSIinfo),
    path('editFTSI/', ftsi_operation.editFTSI),
    path('updateFTSI/', ftsi_operation.updateFTSI),
    path('detailFTSI/', ftsi2ips_opt.detail_ftsi),
    path('detailFTSI/statusChange/', ftsi2ips_opt.ips_status_change),
    path('detailFTSI/getInfo/', ftsi2ips_opt.getFTSI2IPS_info),
    path('detailFTSI/infoChange/', ftsi2ips_opt.ips_info_change),
    path('getPendingList/',pendingMgr.pending_info),
    path('PendingClose/',pendingMgr.PendingClose),
]
