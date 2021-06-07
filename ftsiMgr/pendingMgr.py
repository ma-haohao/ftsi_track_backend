import json
from django.contrib.auth.decorators import permission_required
from django.db import transaction
from common.models import ftsi_number_issue,ftsi_info, FTSI2IPS, customized_type, trigger_relationship,historyrecord_ftsi_modify
from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
from common.typeMethods import typeMethods
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from datetime import date,datetime
from .ftsi_operation import _CustomizeCreate,_FTSI2IPSadd,_historyFTSI_record
# Create your views here.
#finished

#finished
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
def pending_info(request):
    # create response data
    pending_list=list(ftsi_number_issue.objects.filter(status=False).values())
    for item in pending_list:
        item['impact_ips']=[int(i) for i in item['impact_ips'].split(",")]
        if item['action_type']=='update':
            item['pending_id']=item['id']
            try:
                item['id']=ftsi_info.objects.filter(ftsi_num=item['ftsi_no'],active_status=True)[0].id
            except IndexError:
                continue
    return JsonResponse({
        'data': {
            "pending_info": pending_list,
        },
        'meta': {"msg": "obtain the pending list successfully",
                 "status": 200}
    })

def PendingClose(request):
    # decode the request information
    info = json.loads(request.body)
    #修改pending表中的status状态
    pending_item=ftsi_number_issue.objects.filter(id=info['pending_id'])[0]
    pending_item.status=True
    pending_item.save()
    # create response data
    return JsonResponse({
        'data': {},
        'meta': {"msg": "Close the pending item successfully!",
                 "status": 200}
    })