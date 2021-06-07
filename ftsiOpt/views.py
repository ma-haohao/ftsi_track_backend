from django.shortcuts import render
# Create your views here.
from common.models import ftsi_info, FTSI2IPS, engine_info, customized_type
from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from common.typeMethods import typeMethods
from ftsiOpt.CachedmonitorFlag import _get_monitor_para

def _obtainFTSI2IPSList(engine_info, FTSI_original, select, input1, type1,username):
    #获取用于监控和预测的数据
    monitor_para=_get_monitor_para(username)
    # query the effective ftsi for specific ips
    if type1 in ['All', '']:
        ftsi = FTSI_original.filter(active_status=True).exclude(
            current_type='trigger_factor')
    elif type1 == 'On condition':
        ftsi = FTSI_original.filter(current_type='OTHER', active_status=True)
    elif type1 == 'Parameter dependence':
        ftsi = FTSI_original.filter(active_status=True).exclude(current_type='OTHER').exclude(
            current_type='trigger_factor')
    else:
        # trigger_type = list(customized_type.trigger_type.values())[1:]
        ftsi = FTSI_original.filter(current_type='trigger_factor', active_status=True)
    if select != '' and input1 != '':
        search_dict = {'ftsi_id__' + select + '__icontains': input1}
        ftsi = list(ftsi.filter(**search_dict).values())
    else:
        ftsi = list(ftsi.values())

    type_dict = ftsi_info.type_dict
    for item in ftsi:
        item['ftsi_info'] = ftsi_info.objects.filter(id=item['ftsi_id']).values()[0]
        if item['current_type'] not in list(type_dict.keys()):
            item['current_type'] = customized_type.objects.filter(ftsi_id=item['ftsi_id']).values()[0][
                item['current_type']]
        if item['current_type'] in list(type_dict.keys())[1:-1]:
            typeMethod = typeMethods(item['current_type'],username)
            item['comments'], item['reminds'] = typeMethod.generate_comments(engine_info, item['next_target'],monitor_para)
        else:
            item['comments'], item['reminds'] = item['ftsi_info']['statement'], 'safe'
    # create response data
    return ftsi

def _obtainPredictInfo(engine_info, FTSI_original, flight_parameter,username):
    # 获取用于监控和预测的数据
    monitor_para = _get_monitor_para(username)
    # query the specfic FTSI for different engine
    ftsi = list(FTSI_original.filter(active_status=True).exclude(
        current_type='OTHER').exclude(current_type='trigger_factor').values())
    type_dict = ftsi_info.type_dict
    effective_ftsi = []
    for item in ftsi:
        item['ftsi_info'] = ftsi_info.objects.filter(id=item['ftsi_id']).values()[0]
        if item['current_type'] not in list(type_dict.keys()):
            item['current_type'] = customized_type.objects.filter(ftsi_id=item['ftsi_id']).values()[0][
                item['current_type']]
        typeMethod = typeMethods(item['current_type'],username)
        item['content'], flag = typeMethod.predict_implement(engine_info, item['next_target'], flight_parameter,monitor_para)
        if flag == True: effective_ftsi.append(item)
    return effective_ftsi

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
def select_bar(request):
    aircraft_list = ['AC10101', 'AC10102', 'AC10103', 'AC10104', 'AC10105', 'AC10106']
    type_list = ['All', 'Parameter dependence', 'On condition', 'Unactive']
    offWing_query = engine_info.objects.filter(aircraft='off-wing').order_by('engine')
    offWing_list = []
    for item in offWing_query:
        offWing_list.append(item.engine)
    return JsonResponse({
        'data': {
            'aircraft_list': aircraft_list,
            'type_list': type_list,
            'offWing_list': offWing_list
        },
        'meta': {
            "msg": "obtain the select bar successfully",
            "status": 200
        }
    })

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
def ftsi_for_aircraft(request):
    # decode the request information
    username=request.user.username
    onWing, aircraftMSN, engineIPS, type1 = \
        request.GET.get('onWing', ''), request.GET.get('aircraftMSN',''), \
        request.GET.get('engineIPS', ''), request.GET.get('typeSelect', '')
    select, input1 = request.GET.get('select', ''), request.GET.get('input', '')
    # query the specfic engine according to the aircraftMSN
    try:
        if onWing == 'true':
            LHE_info = engine_info.objects.filter(left_right="L", aircraft=aircraftMSN).values()[0]
            RHE_info = engine_info.objects.filter(left_right="R", aircraft=aircraftMSN).values()[0]
            LFTSI_original = FTSI2IPS.objects.filter(engine_id=LHE_info['engine'])
            RFTSI_original = FTSI2IPS.objects.filter(engine_id=RHE_info['engine'])
            left_ftsi = _obtainFTSI2IPSList(LHE_info, LFTSI_original, select, input1, type1,username)
            right_ftsi = _obtainFTSI2IPSList(RHE_info, RFTSI_original, select, input1, type1,username)
            #组合数据成total，一条FTSI显示一架飞机两个发动机的内容，若文件不适用于此发动机，则显示为NA
            total={}
            for item in left_ftsi:
                total[item["ftsi_info"]["ftsi_num"]]={"ftsi_info":item["ftsi_info"],
                                                      "comments_LH":item["comments"],"reminds_LH":item["reminds"],
                                                      "comments_RH":"NA","reminds_RH":"NA"}
            keys=total.keys()
            for item in right_ftsi:
                if item["ftsi_info"]["ftsi_num"] in keys:
                    total[item["ftsi_info"]["ftsi_num"]]["comments_RH"]=item["comments"]
                    total[item["ftsi_info"]["ftsi_num"]]["reminds_RH"]=item["reminds"]
                else:
                    total[item["ftsi_info"]["ftsi_num"]] = {"ftsi_info": item["ftsi_info"],
                                                            "comments_LH": "NA","reminds_LH": "NA",
                                                            "comments_RH": item["comments"], "reminds_RH": item["reminds"]}

            total_final=list(total.values())
        else:
            LHE_info = engine_info.objects.filter(engine=engineIPS).values()[0]
            RHE_info = {'engine':'NA'}
            LFTSI_original = FTSI2IPS.objects.filter(engine_id=LHE_info['engine'])
            left_ftsi = _obtainFTSI2IPSList(LHE_info, LFTSI_original, select, input1, type1,username)
            right_ftsi = []
            total_final=[]
    except:
        return JsonResponse({
            'data': {},
            'meta': {
                "msg": "Please choice MSN first.",
                "status": 404
            }
        })
# query the effective ftsi for specific ips
    return JsonResponse({
        'data': {
            "leftIPS": LHE_info,
            "rightIPS": RHE_info,
            'ftsiForLeft': left_ftsi,
            'amountLeft': len(left_ftsi),
            'ftsiForRight': right_ftsi,
            'amountRight': len(right_ftsi),
            'ftsiForTotal':total_final,
            'amountTotal':len(total_final)
        },
        'meta': {
            "msg": "Obtain the FTSI info for the selected MSN successfully",
            "status": 200
        }
    })

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
def ftsi_predict(request):
    # decode the request information
    username=request.user.username
    aircraftMSN,engineIPS,onWing = request.GET.get('aircraftMSN', ''),request.GET.get('engineIPS',''),request.GET.get('onWing','')
    flight_parameter = {'flightDay': request.GET.get('flightDay', ''), 'flightHour': request.GET.get('flightHour', ''),
                        'engineHour': request.GET.get('engineHour', ''),
                        'c1Cycle': request.GET.get('c1Cycle', '')}
    # query the specfic engine according to the aircraftMSN
    try:
        if onWing=='true':
            LHE_info = engine_info.objects.filter(left_right="L", aircraft=aircraftMSN).values()[0]
            RHE_info = engine_info.objects.filter(left_right="R", aircraft=aircraftMSN).values()[0]
            LFTSI_original = FTSI2IPS.objects.filter(engine_id=LHE_info['engine'])
            RFTSI_original = FTSI2IPS.objects.filter(engine_id=RHE_info['engine'])
            left_effective_ftsi = _obtainPredictInfo(LHE_info, LFTSI_original, flight_parameter,username)
            right_effective_ftsi = _obtainPredictInfo(RHE_info, RFTSI_original, flight_parameter,username)
        else:
            LHE_info = engine_info.objects.filter(engine=engineIPS).values()[0]
            RHE_info = {'engine':'NA'}
            LFTSI_original = FTSI2IPS.objects.filter(engine_id=LHE_info['engine'])
            left_effective_ftsi = _obtainPredictInfo(LHE_info, LFTSI_original, flight_parameter,username)
            right_effective_ftsi = []
    except IndexError:
        return JsonResponse({
            'data': {},
            'meta': {
                "msg": "Please choice MSN first.",
                "status": 404
            }
        })
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
