from django.shortcuts import render
from .models import engine_info
from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
# Create your views here.

def _dictzip(attributes, values):
    return [dict(zip(attributes, value)) for value in values]

#token vadiation
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
#return the menus
def menus(request):
    attrubutes = ["id", "authName","path", "children"]
    # second-class navigation
    sec_FTSIMgr = [[102, 'FTSI List','ftsilist', []],[103, 'Pending List','pendinglist', []]]
    sec_FTSIOpt = [[202, 'Task Query','taskquery', []], [203, 'Task Submit','tasksubmit', []],
                   [204, 'Cache Area','cachearea', []],[205, 'Cached Task Submit','cachesubmit', []]]
    sec_History = [[302, 'FTSI Record', 'ftsirecord', []], [303, 'Submit Record', 'submitrecord', []],
                   [304, 'Submit Failed', 'submitfailed', []]]
    # first-class navigation
    first_class = [[101, 'FTSI Manage','', _dictzip(attrubutes, sec_FTSIMgr)],
                   [201, 'FTSI Operation','', _dictzip(attrubutes, sec_FTSIOpt)],
                   [301, 'History', '', _dictzip(attrubutes, sec_History)]]
    # create response data
    return JsonResponse({
        "data":_dictzip(attrubutes,first_class),
        "meta":{
            "msg":"Obtain the menus successfully.",
            "status":200
        }
    })

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
def engineInfo(request):
    qs=engine_info.objects.values()
    retlist=list(qs)
    return JsonResponse({'ret':0,'retlist':retlist})
