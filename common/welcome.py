from django.shortcuts import render
import json
from .typeMethods import typeMethods
from django.contrib.auth.decorators import permission_required
from django.db import transaction
from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .models import engine_info,FTSI2IPS,ftsi_info,customized_type,historyrecord_engine_info
# Create your response here.
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
def engineInfo(request):
    qs=engine_info.objects.order_by("engine").values()
    retlist=list(qs)
    return JsonResponse({
        'data':retlist,
        'meta':{"msg":"obtain the engine information successfully",
        "status": 200}
    })

# Create your response here.
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
def obtainEngineInfoForEdit(request):
    engineNum = request.GET.get('engine', '')
    qs=list(engine_info.objects.filter(engine=engineNum).values())[0]
    return JsonResponse({
        'data':qs,
        'meta':{"msg":"obtain the engine information successfully",
        "status": 200}
    })

@api_view(['GET','PUT'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
@transaction.atomic
@permission_required('common.change_engine_info')
def submitEngineInfoEdit(request):
    info = json.loads(request.body)
    engineInfo=engine_info.objects.filter(engine=info['engine'])
    old_engineInfo=engineInfo.values()[0]
    engineInfo=engineInfo[0]
    #修改发动机信息
    for item in info.keys():
        new_value=info[item]
        exec('engineInfo.'+item+'=new_value')
    engineInfo.save()

    if info['FTSIchangeFlag']==True:
        #根据发动机信息，修改FTSI的target信息
        FTSIinfo=FTSI2IPS.objects.filter(engine_id=info['engine'],active_status=True)
        for item in FTSIinfo:
            #当为customize时
            if item.current_type in ['dep_type1','dep_type2','dep_type3']:
                type_used=customized_type.objects.filter(ftsi_id=item.ftsi_id).values()[0][item.current_type]
            elif item.current_type in ftsi_info.type_dict.keys():
                type_used=item.current_type
            else:
                type_used='OTHER'
            typeMethod=typeMethods(type_used)
            new_target=typeMethod.modify_for_engine_info(info,old_engineInfo,item.next_target)
            item.next_target=new_target
            item.save()
    return JsonResponse({
        'data':{},
        'meta':{
            "msg":"submit the engine modified information successfully",
            "status": 200}
    })

@api_view(['GET','PUT'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
@transaction.atomic
@permission_required('common.change_engine_info')
def submitEngineHistory(request):
    info = json.loads(request.body)
    date=info["submitDate"]
    engine_info1 = engine_info.objects.all()
    deleted_historyInfo = historyrecord_engine_info.objects.filter(date=date)
    deleted_historyInfo.delete()
    for item in engine_info1:
        history_info = historyrecord_engine_info.objects.create(
            date=date, engine=item.engine, aircraft=item.aircraft, left_right=item.left_right,
            flight_day=item.flight_day, flight_time=item.flight_time, run_time=item.run_time,
            c1_cycle=item.c1_cycle,
            flight_cycle=item.flight_cycle, engine_starts=item.engine_starts, reverse_cycle=item.reverse_cycle)
    return JsonResponse({
        'data':{},
        'meta':{
            "msg":"submit the engine modified information successfully",
            "status": 200}
    })