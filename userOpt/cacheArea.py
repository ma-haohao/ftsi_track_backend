from django.shortcuts import render
import json
from common.models import FTSI2IPS, engine_info
from .models import userCacheEngineInfo, userCacheFTSI2IPS
from ftsiOpt.views import _obtainFTSI2IPSList,_obtainPredictInfo
from ftsiOpt.ftsiSubmit import _checkprocess,_submitprocess
from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from datetime import date
from django.db import transaction

def _obtain_aircraftlist(username):
    original_aircraftList = []
    infoInDB = userCacheEngineInfo.objects.filter(username=username).values('aircraft').distinct()
    for item in infoInDB:
        original_aircraftList.append(item['aircraft'])
    return original_aircraftList

# Create your views here.
@api_view(['GET', 'PUT'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
@transaction.atomic
def changeCachedArea(request):
    # 获得原来已经有的飞机信息
    username = request.user.username
    aircraftList = json.loads(request.body)['aircraftNum']
    aircraftList_old=_obtain_aircraftlist(username)
    add_list=list(set(aircraftList).difference(set(aircraftList_old)))
    delete_list=list(set(aircraftList_old).difference(set(aircraftList)))

    #添加操作
    for aircraft in add_list:
        original_info = list(engine_info.objects.filter(aircraft=aircraft).values())
        for engine in original_info:
            cache_info = userCacheEngineInfo.objects.create(username=username,
            cacheDate=date.today().strftime('%Y-%m-%d'),engine=engine['engine'],aircraft=engine['aircraft'],left_right=engine['left_right'],
            flight_day=engine['flight_day'],flight_time=engine['flight_time'],run_time=engine['run_time'],c1_cycle=engine['c1_cycle'],
            flight_cycle=engine['flight_cycle'],engine_starts=engine['engine_starts'],reverse_cycle=engine['reverse_cycle'])
            ftsi2ips_info=list(FTSI2IPS.objects.filter(engine_id=engine['engine'],active_status=True).values())
            for ftsi in ftsi2ips_info:
                cache_ftsi=userCacheFTSI2IPS.objects.create(ftsi_id=ftsi['ftsi_id'],
            last_date=ftsi['last_date'],current_type=ftsi['current_type'],next_target=ftsi['next_target'],residual_times=ftsi['residual_times'],
            active_status=ftsi['active_status'],cache_id=cache_info.id)
    #删除操作
    cache_info=userCacheEngineInfo.objects.filter(username=username,aircraft__in=delete_list)
    for item in cache_info:
        cache_ftsi=userCacheFTSI2IPS.objects.filter(cache_id=item.id)
        cache_ftsi.delete()
    cache_info.delete()
    return JsonResponse({
        'data': '',
        'meta':{
            'status':200,
            'msg':'update the cached information successfully!'
        }
    })

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
def obtainCachedAircraft(request):
    username = request.user.username
    aircraftList = _obtain_aircraftlist(username)
    return JsonResponse({
        'data': aircraftList,
        'meta':{
            'status':200,
            'msg':'obtain the cached aircraft list successfully!'
        }
    })

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
def cachedFTSI_for_aircraft(request):
    # decode the request information
    username=request.user.username
    aircraftMSN, type1 = request.GET.get('aircraftMSN', ''), request.GET.get('typeSelect', '')
    select,input1=request.GET.get('select', ''), request.GET.get('input', '')
    # query the specfic engine according to the aircraftMSN
    try:
        LHE_info = userCacheEngineInfo.objects.filter(username=username,left_right="L", aircraft=aircraftMSN).values()[0]
        RHE_info = userCacheEngineInfo.objects.filter(username=username,left_right="R", aircraft=aircraftMSN).values()[0]
    except IndexError:
        return JsonResponse({
            'data': {},
            'meta': {
                "msg": "Please choice MSN first.",
                "status": 404
            }
        })
    # query the effective ftsi for specific ips
    cachedate = \
    userCacheEngineInfo.objects.filter(username=username, aircraft=aircraftMSN).values('cacheDate').distinct()[0][
        'cacheDate']
    LFTSI_original=userCacheFTSI2IPS.objects.filter(cache_id=LHE_info['id'])
    RFTSI_original=userCacheFTSI2IPS.objects.filter(cache_id=RHE_info['id'])
    left_ftsi=_obtainFTSI2IPSList(LHE_info, LFTSI_original, select, input1,type1,username)
    right_ftsi=_obtainFTSI2IPSList(RHE_info, RFTSI_original, select, input1,type1,username)
    # 组合数据成total，一条FTSI显示一架飞机两个发动机的内容，若文件不适用于此发动机，则显示为NA
    total = {}
    for item in left_ftsi:
        total[item["ftsi_info"]["ftsi_num"]] = {"ftsi_info": item["ftsi_info"],
                                                "comments_LH": item["comments"], "reminds_LH": item["reminds"],
                                                "comments_RH": "NA", "reminds_RH": "NA"}
    keys = total.keys()
    for item in right_ftsi:
        if item["ftsi_info"]["ftsi_num"] in keys:
            total[item["ftsi_info"]["ftsi_num"]]["comments_RH"] = item["comments"]
            total[item["ftsi_info"]["ftsi_num"]]["reminds_RH"] = item["reminds"]
        else:
            total[item["ftsi_info"]["ftsi_num"]] = {"ftsi_info": item["ftsi_info"],
                                                    "comments_LH": "NA", "reminds_LH": "NA",
                                                    "comments_RH": item["comments"], "reminds_RH": item["reminds"]}

    total_final = list(total.values())
    return JsonResponse({
        'data': {
            "leftIPS": LHE_info,
            "rightIPS": RHE_info,
            'ftsiForLeft': left_ftsi,
            'amountLeft': len(left_ftsi),
            'ftsiForRight': right_ftsi,
            'amountRight': len(right_ftsi),
            'amountTotal':len(total_final),
            'ftsiForTotal':total_final,
            'cacheDate':cachedate
        },
        'meta': {
            "msg": "Obtain the FTSI info for the selected MSN successfully",
            "status": 200
        }
    })

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
def cachedFTSI_predict(request):
    # decode the request information
    username = request.user.username
    aircraftMSN = request.GET.get('aircraftMSN', '')
    flight_parameter = {'flightDay': request.GET.get('flightDay', ''), 'flightHour': request.GET.get('flightHour', ''),
                        'engineHour': request.GET.get('engineHour', ''),
                        'c1Cycle': request.GET.get('c1Cycle', '')}
    # query the specfic engine according to the aircraftMSN
    try:
        LHE_info = userCacheEngineInfo.objects.filter(username=username, left_right="L", aircraft=aircraftMSN).values()[0]
        RHE_info = userCacheEngineInfo.objects.filter(username=username, left_right="R", aircraft=aircraftMSN).values()[0]
    except IndexError:
        return JsonResponse({
            'data': {},
            'meta': {
                "msg": "Please choice MSN first.",
                "status": 404
            }
        })
    # query the specfic FTSI for different engine
    LFTSI_original = userCacheFTSI2IPS.objects.filter(cache_id=LHE_info['id'])
    RFTSI_original = userCacheFTSI2IPS.objects.filter(cache_id=RHE_info['id'])
    left_effective_ftsi=_obtainPredictInfo(LHE_info, LFTSI_original, flight_parameter,username)
    right_effective_ftsi=_obtainPredictInfo(RHE_info, RFTSI_original, flight_parameter,username)
    # create response data
    return JsonResponse({
        'data': {
             "leftIPS": LHE_info,
             "rightIPS": RHE_info,
             'ftsiForLeft': left_effective_ftsi,
             'ftsiForRight': right_effective_ftsi,
        },
        'meta': {
            "msg": "obtain the predict results successfully",
            "status": 200
        }
    })

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
def checkFTSIinfo_cache(request):
    #decode the request
    username=request.user.username
    engineNum,implementFTSI=request.GET.get('engineNum', ''),request.GET.get('implementFTSI', '')
    FTSI_list=implementFTSI.split('/')
    engine_info1 = userCacheEngineInfo.objects.filter(username=username,engine=engineNum).values()[0]
    FTSI_original=userCacheFTSI2IPS.objects.filter(cache_id=engine_info1['id'])
    FTSI_for_table,warning_info=_checkprocess(FTSI_original,engine_info1,FTSI_list)
    #return the response
    return JsonResponse({
        'data': {
        'FTSI_info': FTSI_for_table,
        'warning_info': warning_info},
        'meta': {
            "msg": "obtain the check result successfully",
            "status": 200
        }
    })

@api_view(['GET','PUT'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
@transaction.atomic
def submitFTSIinfo_cache(request):
    username=request.user.username
    info = json.loads(request.body)
    engineNum,implementFTSI=info['engineNum'],info['implementFTSI']
    implementDate=date.today().strftime('%Y-%m-%d')
    FTSI_list=implementFTSI.split('/')
    engine_info1 = userCacheEngineInfo.objects.filter(username=username, engine=engineNum).values()[0]
    FTSI_original = userCacheFTSI2IPS.objects.filter(cache_id=engine_info1['id'])
    warning_info = _submitprocess(FTSI_original, engine_info1, FTSI_list, implementDate,cachedOperation=True)
    # return the response
    return JsonResponse({
        'data': {
        'warning_info': warning_info},
        'meta': {
            "msg": "submit the implemented FTSI successfully",
            "status": 200
        }
    })

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
def cacheMSNinfoObtain(request):
    username=request.user.username
    aircraftMSN = request.GET.get('aircraftMSN', '')
    try:
        LHE_info = userCacheEngineInfo.objects.filter(username=username,left_right="L", aircraft=aircraftMSN).values()[0]
        RHE_info = userCacheEngineInfo.objects.filter(username=username,left_right="R", aircraft=aircraftMSN).values()[0]
    except IndexError:
        return JsonResponse({
            'data': {},
            'meta': {
                "msg": "Please choice MSN first.",
                "status": 404
            }
        })
    original_info={'FD':LHE_info['flight_day'],'FC':LHE_info['flight_cycle'],'FH':LHE_info['flight_time'],
                   'LHEH':LHE_info['run_time'],'LHCC':LHE_info['c1_cycle'],'LHES':LHE_info['engine_starts'],'LHRC':LHE_info['reverse_cycle'],
                   'RHEH':RHE_info['run_time'],'RHCC':RHE_info['c1_cycle'],'RHES':RHE_info['engine_starts'],'RHRC':RHE_info['reverse_cycle']}
    # return the response
    return JsonResponse({
        'data': original_info,
        'meta': {
            "msg": "obtain the MSN information successfully!",
            "status": 200
        }
    })

@api_view(['GET','PUT'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
@transaction.atomic
def cacheMSNinfoChange(request):
    username=request.user.username
    info = json.loads(request.body)
    aircraftMSN = info['aircraftMSN']
    try:
        LHE_info = userCacheEngineInfo.objects.filter(username=username,left_right="L", aircraft=aircraftMSN)[0]
        RHE_info = userCacheEngineInfo.objects.filter(username=username,left_right="R", aircraft=aircraftMSN)[0]
    except IndexError:
        return JsonResponse({
            'data': {},
            'meta': {
                "msg": "The MSN doesn't exist in cached area!",
                "status": 404
            }
        })
    #修改飞行数据
    LHE_info.flight_day,RHE_info.flight_day=LHE_info.flight_day+int(info['addFD']),RHE_info.flight_day+int(info['addFD'])
    LHE_info.flight_time, RHE_info.flight_time = round(LHE_info.flight_time + float(info['addFH']),2), round(RHE_info.flight_time + float(info['addFH']),2)
    LHE_info.flight_cycle, RHE_info.flight_cycle = LHE_info.flight_cycle + int(info['addFC']), RHE_info.flight_cycle + int(info['addFC'])
    LHE_info.run_time, RHE_info.run_time = round(LHE_info.run_time + float(info['addEH']), 2), round(RHE_info.run_time + float(info['addEH']), 2)
    LHE_info.c1_cycle, RHE_info.c1_cycle = LHE_info.c1_cycle + int(info['addCC']), RHE_info.c1_cycle + int(info['addCC'])
    LHE_info.engine_starts, RHE_info.engine_starts = LHE_info.engine_starts + int(info['addES']), RHE_info.engine_starts + int(info['addES'])
    LHE_info.reverse_cycle, RHE_info.reverse_cycle = LHE_info.reverse_cycle + int(info['addRC']), RHE_info.reverse_cycle + int(info['addRC'])
    LHE_info.save()
    RHE_info.save()
    # return the response
    return JsonResponse({
        'data': {},
        'meta': {
            "msg": "Change the MSN information successfully!",
            "status": 200
        }
    })