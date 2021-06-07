import json
from django.contrib.auth.decorators import permission_required
from django.db import transaction
from common.models import ftsi_info, FTSI2IPS, customized_type, engine_info
from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from common.typeMethods import typeMethods


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
def detail_ftsi(request):
    # decode the request information
    FTSIid = request.GET.get('id', '')
    # query the FTSI according to the input
    FTSI_query = ftsi_info.objects.filter(id=FTSIid).values()
    # query the details (including applied IPS information)
    AppliedIPS_query = FTSI2IPS.objects.filter(ftsi_id=FTSIid).order_by("engine").values()
    type_dict=ftsi_info.type_dict
    for i in range(0,len(AppliedIPS_query)):
        try:
            AppliedIPS_query[i]['current_type']=type_dict[AppliedIPS_query[i]['current_type']]
        except KeyError:
            pass
    # create response data
    return JsonResponse({
        'data': {
            "FTSI": list(FTSI_query)[0],
            "ipsDetail": list(AppliedIPS_query)
        },
        'meta': {"msg": "Obtain the IPS list for this FTSI successfully",
                 "status": 200}
    })

@api_view(['GET', 'PUT'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
@transaction.atomic
@permission_required('common.change_ftsi2ips')
def ips_status_change(request):
    # decode the request information
    info = json.loads(request.body)
    # change the status of the ips in the database
    try:
        ips = FTSI2IPS.objects.get(id=info['id'])
    except FTSI2IPS.DoesNotExist:
        return JsonResponse({
            'data': {},
            'meta': {"msg": "failed to update the status of the applied IPS",
                     "status": 404}
        })
    ips.active_status = info['active_status']
    ips.save()
    # create response data
    return JsonResponse({
        'data': {},
        'meta': {"msg": "update the status of the applied IPS successfully!",
                 "status": 200}
    })

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
@permission_required('common.change_ftsi2ips')
def getFTSI2IPS_info(request):
    # decode the request information
    info_id = request.GET.get('id', '')
    # obtain the related info
    type_dict=ftsi_info.type_dict
    res = {'id':info_id}
    info_query = list(FTSI2IPS.objects.filter(id=info_id).values())[0]
    relate_ftsi = list(ftsi_info.objects.filter(id=info_query['ftsi_id']).values())[0]
    res['ftsi_num'], res['ftsi_title'], res['statement'], res['dep_type'] = \
        relate_ftsi['ftsi_num'], relate_ftsi['ftsi_title'], relate_ftsi['statement'], type_dict[relate_ftsi['dep_type']]
    res['engine_id'], res['last_date'], res['current_type'], res['active_status'], res['next_target'], res['residual_times'] = \
        info_query['engine_id'], info_query['last_date'], info_query['current_type'], info_query['active_status'], \
        info_query['next_target'], info_query['residual_times']
    #获得next target的单位以及对应查询发动机参数所用的关键词
    if res['current_type'] in ['dep_type1','dep_type2','dep_type3']:
        real_type=customized_type.objects.filter(ftsi_id=info_query['ftsi_id']).values()[0][res['current_type']]
    elif res['current_type'] in list(type_dict.keys()):
        real_type = res['current_type']
    else:
        real_type = 'OTHER'
    typeMethod = typeMethods(real_type)
    res['DB_keyword'],res['unit']=typeMethod.queryword_unit()
    res['engine_info'] = list(engine_info.objects.filter(engine=info_query['engine_id']).values())[0]
    if relate_ftsi['dep_type'] == "CUS":
        parameter1 = list(customized_type.objects.filter(ftsi_id=info_query['ftsi_id']).values())[0]
        param_relate = customized_type.param_relate
        step_candidate = list(param_relate.keys())
        step_dict = {}
        for item in step_candidate:
            if parameter1[item] not in ['', 'NA']:
                step_dict[item] = {'type_label': parameter1[item],'type_value': item}
                for item2 in param_relate[item]:
                    step_dict[item][item2[0:-1]] = parameter1[item2]
                if item in ['dep_type1','dep_type2','dep_type3']:
                    typeMethod = typeMethods(step_dict[item]['type_label'])
                else:
                    typeMethod = typeMethods('OTHER')
                step_dict[item]['DB_keyword'], step_dict[item]['unit'] = typeMethod.queryword_unit()
        res['customize'] = step_dict
    else:
        res['customize'] = {}
    # create response data
    return JsonResponse({
        'data': res,
        'meta': {"msg": "Obtain the FTSI_IPS information successfully!",
                 "status": 200}
    })

@api_view(['GET', 'PUT'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
@transaction.atomic
def ips_info_change(request):
    # decode the request information
    info = json.loads(request.body)
    # change the status of the ips in the database
    try:
        ips = FTSI2IPS.objects.get(id=info['id'])
    except FTSI2IPS.DoesNotExist:
        return JsonResponse({
            'data': {},
            'meta': {"msg": "failed to edit the FTSI-IPS.",
                     "status": 404}
        })
    ips.active_status = info['active_status']
    ips.residual_times = info['residual_times']
    ips.last_date = info['last_date']
    ips.current_type = info['current_type']
    ips.next_target = info['next_target']
    ips.save()
    # create response data
    return JsonResponse({
        'data': {},
        'meta': {"msg": "Modify the FTSI-IPS information successfully!",
                 "status": 200}
    })

