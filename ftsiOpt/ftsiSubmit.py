from django.shortcuts import render
import json
from common.models import ftsi_info, FTSI2IPS, engine_info, customized_type, trigger_relationship, \
    historyrecord_task_submit, historyrecord_engine_info
from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from common.typeMethods import typeMethods
from django.db import transaction


def _Special_FTSI_filter(special_FTSI, ftsi_num):
    res = []
    for item in special_FTSI:
        if item['ftsi_num'].split('_')[0] == ftsi_num:
            res.append(item)
    return res


def _checkprocess(FTSI_original, engine_info1, FTSI_list):
    FTSI_info = []
    special_FTSI = list(ftsi_info.objects.filter(active_status=True, ftsi_num__icontains='_').values())
    for item in FTSI_list:
        FTSI_info1 = list(ftsi_info.objects.filter(active_status=True, ftsi_num=item).values())
        FTSI_info = FTSI_info + FTSI_info1 + _Special_FTSI_filter(special_FTSI, item)
    obtained_FTSI_num = []
    not_triggered_FTSI = []
    FTSI_for_table = []
    for item in FTSI_info:
        try:
            item['ips_info'] = FTSI_original.filter(ftsi_id=item['id']).values()[0]
        except:
            continue
        if item['ips_info']['active_status'] == True:
            obtained_FTSI_num.append(item['ftsi_num'].split('_')[0])
            try:
                type_used = typeMethods(item['dep_type'])
                item['comments'] = type_used.submit_check_comments(engine_info1, item)
                FTSI_for_table.append(item)
                trigger_info = _FTSI_trigger(FTSI_original, item['ftsi_num'])
                if trigger_info != False:
                    name = [i['ftsi_num'] for i in trigger_info]
                    item['comments'] = 'activate ' + str(name)[1:-1] + '. ' + item['comments']
            except TypeError:
                not_triggered_FTSI.append(item['ftsi_num'])
    # 检查请求中是否存在不存在或者已经关闭的FTSI
    FTSI_not_found = list(set(FTSI_list).difference(set(obtained_FTSI_num)))
    # 构建弹窗信息（当有不存在/已关闭、未激活的FTSI时）
    exist_info = '' if len(FTSI_not_found) == 0 else 'FTSI: ' + str(FTSI_not_found)[
                                                                1:-1] + ' is closed or not applied for this engine.<br/>'
    trigger_info = '' if len(not_triggered_FTSI) == 0 else 'FTSI: ' + str(not_triggered_FTSI)[
                                                                      1:-1] + ' is not triggered yet.'
    return FTSI_for_table, exist_info + trigger_info


def _submitprocess(FTSI_original, engine_info1, FTSI_list, implementDate,cachedOperation=False):
    FTSI_info = []
    special_FTSI = list(ftsi_info.objects.filter(active_status=True, ftsi_num__icontains='_').values())
    for item in FTSI_list:
        FTSI_info1 = list(ftsi_info.objects.filter(active_status=True, ftsi_num=item).values())
        FTSI_info = FTSI_info + FTSI_info1 + _Special_FTSI_filter(special_FTSI, item)
    obtained_FTSI_num = []
    not_triggered_FTSI = []
    FTSI_for_table = []
    for item in FTSI_info:
        try:
            item['ips_info'] = FTSI_original.filter(ftsi_id=item['id']).values()[0]
        except:
            continue
        if item['ips_info']['active_status'] == True:
            obtained_FTSI_num.append(item['ftsi_num'].split('_')[0])
            try:
                type_used = typeMethods(item['dep_type'])
                type_used.submit_ftsi(engine_info1, item, FTSI_original, implementDate)
                FTSI_for_table.append(item)
                trigger_info = _FTSI_trigger(FTSI_original, item['ftsi_num'])
                _historyInfo_save(engine_info1, item, implementDate, trigger_info,cachedOperation)
                if trigger_info != False:
                    for item in trigger_info:
                        ips = FTSI_original.get(id=item['id'])
                        ips.current_type = 'dep_type1'
                        ips.last_date = 'Activate on ' + implementDate
                        customized_info = customized_type.objects.filter(ftsi_id=item['ftsi_id']).values()[0]
                        ips.residual_times = customized_info['total_times1']
                        type_used = typeMethods(customized_info['dep_type1'])
                        ips.next_target = type_used.update_next_target(engine_info1['engine'],
                                                                       customized_info['period1'], implementDate)
                        ips.save()
            except TypeError:
                not_triggered_FTSI.append(item['ftsi_num'])
    # 检查请求中是否存在不存在或者已经关闭的FTSI
    FTSI_not_found = list(set(FTSI_list).difference(set(obtained_FTSI_num)))
    # 构建弹窗信息（当有不存在/已关闭、未激活的FTSI时）
    exist_info = '' if len(FTSI_not_found) == 0 else 'FTSI: ' + str(FTSI_not_found)[
                                                                1:-1] + ' is closed or not applied for this engine.<br/>'
    trigger_info = '' if len(not_triggered_FTSI) == 0 else 'FTSI: ' + str(not_triggered_FTSI)[
                                                                      1:-1] + ' is not triggered yet.'
    return exist_info + trigger_info


def _FTSI_trigger(FTSI_original, FTSINum):
    info = list(trigger_relationship.objects.filter(exciter_FTSI=FTSINum).values())
    if len(info) == 0:
        return False
    else:
        response_FTSI = []
        for item in info:
            key1 = ftsi_info.objects.filter(active_status=True, ftsi_num=item['response_FTSI']).values()[0]
            try:
                candidate_FTSI = FTSI_original.filter(ftsi_id=key1['id']).values()[0]
                if candidate_FTSI['current_type'] == 'trigger_factor':
                    candidate_FTSI['ftsi_num'] = key1['ftsi_num']
                    response_FTSI.append(candidate_FTSI)
            except:
                continue
        if len(response_FTSI) == 0:
            return False
        else:
            return response_FTSI


def _historyInfo_save(engineInfo, FTSI_info, implementDate, trigger_info,cachedOperation):
    if cachedOperation==True:
        return
    task = historyrecord_task_submit.objects.create(date=implementDate, engine=engineInfo['engine'],
                                                    aircraft=engineInfo['aircraft'])
    task.ftsi_info = FTSI_info['ftsi_num'] + ' Rev. ' + FTSI_info['rev'] + ' ' + FTSI_info['ftsi_title']
    type_used = typeMethods(FTSI_info['dep_type'])
    next_step = type_used.submit_check_comments(engineInfo, FTSI_info)
    if trigger_info != False:
        name = [i['ftsi_num'] for i in trigger_info]
        next_step = 'activate ' + str(name)[1:-1] + '. ' + next_step
    task.next_step = next_step
    task.implement_info = type_used.history_implement(engineInfo, FTSI_info)
    task.save()


# Create your views here.
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
def getEngineNum(request):
    aircraftMSN = request.GET.get('aircraftMSN', '')
    left_engine_info = engine_info.objects.filter(left_right="L", aircraft=aircraftMSN).values()[0]
    right_engine_info = engine_info.objects.filter(left_right="R", aircraft=aircraftMSN).values()[0]
    return JsonResponse({
        'data': {
            'left_engine': left_engine_info['engine'],
            'right_engine': right_engine_info['engine'],
        },
        'meta': {
            "msg": "obtain the related engines successfully",
            "status": 200
        }
    })


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
def checkFTSIinfo(request):
    engineNum, implementFTSI,implementDate = request.GET.get('engineNum', ''), request.GET.get('implementFTSI', ''),request.GET.get('implementDate','')
    FTSI_list = implementFTSI.split('/')
    try:
        engine_info1 = historyrecord_engine_info.objects.filter(engine=engineNum,date=implementDate).values()[0]
    except IndexError:
        return JsonResponse({
            'data': {},
            'meta': {
                "msg": "can not find the engine info record for this day.",
                "status": 404
            }
        })
    FTSI_original = FTSI2IPS.objects.filter(engine_id=engineNum)
    FTSI_for_table, warning_info = _checkprocess(FTSI_original, engine_info1, FTSI_list)
    # return response
    return JsonResponse({
        'data': {
            'FTSI_info': FTSI_for_table,
            'warning_info': warning_info},
        'meta': {
            "msg": "obtain the check result successfully",
            "status": 200
        }
    })


@api_view(['GET', 'PUT'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
@transaction.atomic
def submitFTSIinfo(request):
    info = json.loads(request.body)
    engineNum, implementFTSI, implementDate = info['engineNum'], info['implementFTSI'], info['implementDate']
    FTSI_list = implementFTSI.split('/')
    try:
        engine_info1 = historyrecord_engine_info.objects.filter(engine=engineNum,date=implementDate).values()[0]
    except IndexError:
        return JsonResponse ({
            'data':{},
            'meta':{
                "msg":"can not find the engine info record for this day.",
                "status":404
            }
        })
    FTSI_original = FTSI2IPS.objects.filter(engine_id=engineNum)
    warning_info = _submitprocess(FTSI_original, engine_info1, FTSI_list, implementDate)
    # return response
    return JsonResponse({
        'data': {
            'warning_info': warning_info},
        'meta': {
            "msg": "submit the implemented FTSI successfully",
            "status": 200
        }
    })
