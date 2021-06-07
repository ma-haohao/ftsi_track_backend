import json
from django.contrib.auth.decorators import permission_required
from django.db import transaction
from common.models import ftsi_info, FTSI2IPS, customized_type, trigger_relationship,historyrecord_ftsi_modify
from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
from common.typeMethods import typeMethods
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from datetime import date,datetime
# Create your views here.
#finished

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
def get_ftsi(request):
    # decode the request information
    select, input, pagesize, pagenum = request.GET.get('select', ''), request.GET.get('input', ''), request.GET.get(
        'pagesize'), request.GET.get('pagenum')
    # query the data according to the input
    if select.strip() == '' or input.strip() == '':
        query = ftsi_info.objects.filter(active_status=True).order_by("id")
        print(query[0].get_dep_type_display())
    else:
        search_dict = _select_filter(select,input)
        query = ftsi_info.objects.filter(**search_dict).order_by("id")
    #将dep_type显示为display的值
    query_set = list(query.values())
    for i in range(0,len(query_set)):
        query_set[i]['dep_type'] = query[i].get_dep_type_display()
    # return the data in the page that requested
    paginator = Paginator(query_set, int(pagesize))
    try:
        # 获取查询页数的接口数据列表，page()函数会判断page实参是否是有效数字。
        qs_list = paginator.page(pagenum)
    except PageNotAnInteger:
        qs_list = paginator.page(1)
    except (EmptyPage, InvalidPage):
        # paginator.num_pages
        qs_list = paginator.page(paginator.num_pages)
    relist = list(qs_list)
    # create response data
    return JsonResponse({
        'data': {
            "totalitems": len(query_set),
            "pagenum": pagenum,
            "ftsi_info": relist},
        'meta': {"msg": "obtain the ftsi information successfully",
                 "status": 200}
    })
#finished
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
@permission_required('common.add_ftsi_info')
def para_for_addftsi(request):
    # create response data
    return JsonResponse({
        'data': {
            "monitorType": ftsi_info.type_choice,
            "triggerType": customized_type.trigger_type
        },
        'meta': {"msg": "obtain the types successfully",
                 "status": 200}
    })
#finished
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
def ftsi_num_check(request):
    ftsi_num1= request.GET.get('ftsi_num', '')
    try:
        res=ftsi_info.objects.filter(ftsi_num=ftsi_num1).values()[0]
    except:
        return JsonResponse({
            'data': {},
            'meta': {"msg": "validation pass",
                     "status": 200}
        })
    return JsonResponse({
        'data': {},
        'meta': {"msg": 'This FTSI num has already exist.',
                 "status": 400}
    })
#finished
@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
@transaction.atomic
@permission_required('common.add_ftsi_info')
def add_ftsi(request):
    # decode the request information
    info = json.loads(request.body)
    # add into the database
    new_ftsi = ftsi_info.objects.create(ftsi_num=info['ftsi_num'], rev=info['rev'], ftsi_title=info['ftsi_title'],
                                        statement=info['statement'], dep_type=info['dep_type'],
                                        total_times=info['total_times'],
                                        period=info['period'], active_status=True)
    _CustomizeCreate(info, new_ftsi)
    _FTSI2IPSadd(info, new_ftsi, info['appliedIPS'])
    _historyFTSI_record('New FTSI',new_ftsi,issue_date=info['issueDate'])
    # create response data
    return JsonResponse({
        'data': {},
        'meta': {"msg": "Add a new FTSI successfully!",
                 "status": 201}
    })
#finished
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
def getFTSIinfo(request):
    # decode the request information
    info_id = request.GET.get('id', '')
    # query the data according to the input
    # original part
    item_info = ftsi_info.objects.filter(id=info_id)
    # obatain the applied IPS number
    appliedIPS = _IPSList(item_info)
    item_info = item_info.values()[0]
    item_info['appliedIPS'] = appliedIPS
    # customize_part
    monitorParam = []
    if item_info['dep_type'] != 'CUS':
        trigger = {"type": 'NA', 'parameter': ''}
        monitorParam.append({'type': '', 'period': '', 'times': ''})
    else:
        customize_info = customized_type.objects.filter(ftsi_id=info_id).values()[0]
        trigger = {"type": customize_info['trigger_factor'],
                   'parameter': customize_info['trigger_para']}
        for i in range(1, 4):
            if customize_info['dep_type' + str(i)] != '':
                monitorParam.append({'type': customize_info['dep_type' + str(i)],
                                     'period': customize_info['period' + str(i)],
                                     'times': customize_info['total_times' + str(i)]})
            else:
                break
    item_info['customizePara'] = {'trigger': trigger, 'monitorParam': monitorParam}
    # return the data in the page that requested
    # create response data
    return JsonResponse({
        'data': item_info,
        'meta': {"msg": "obtain the ftsi information successfully",
                 "status": 200}
    })
#finished
@api_view(['GET', 'PUT'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
@transaction.atomic
@permission_required('common.change_ftsi_info')
def editFTSI(request):
    # decode the request information
    info = json.loads(request.body)
    # 处理适用范围发生改变的情况
    FTSI_info = ftsi_info.objects.filter(id=info['id'])
    if info['modifyRange'] == True:
        appliedIPS_old = _IPSList(FTSI_info)
        intersection_IPS = list(set(info['appliedIPS']).intersection(set(appliedIPS_old)))
        delete_IPS = list(set(appliedIPS_old).difference(set(info['appliedIPS'])))
        add_IPS = list(set(info['appliedIPS']).difference(set(appliedIPS_old)))
    else:
        intersection_IPS = info['appliedIPS']
        delete_IPS = []
        add_IPS = []

    ftsi_ips = FTSI2IPS.objects.filter(ftsi_id=info['id'])
    FTSI_obj = FTSI_info.first()
    # 处理compliance statement改变的情况
    if info['modifyType'] == True:
        FTSI_info_old = FTSI_info.values()[0]
        # 更新FTSI_info表中的内容
        FTSI_obj.dep_type, FTSI_obj.total_times, FTSI_obj.period=info['dep_type'], info['total_times'],info['period']
        if FTSI_info_old['dep_type'] == 'CUS':
            customize_atribute = customized_type.objects.filter(ftsi_id=FTSI_info_old['id'])
            customize_atribute_old = customize_atribute.values()[0]
            customize_atribute.delete()
            try:
                trigger_item = trigger_relationship.objects.get(response_FTSI=FTSI_info_old['ftsi_num'])
                trigger_item.delete()
            except trigger_relationship.DoesNotExist:
                pass
        _CustomizeCreate(info, FTSI_obj)
        #更新FTSI_IPS中的内容
        if info['dep_type'] == FTSI_info_old['dep_type']:
            #当新的类型为CUS时
            if info['dep_type'] == 'CUS':
                # 对比新旧dep_type的数量
                new_amount = len(info['customizePara']['monitorParam'])
                old_amount = 3
                for i in range(1, 4):
                    if customize_atribute_old['dep_type' + str(i)] == '':
                        old_amount = i - 1
                        break
                customize_atribute = customized_type.objects.filter(ftsi_id=info['id']).values()[0]
                for engine_num in intersection_IPS:
                    item = ftsi_ips.get(engine_id=engine_num)
                    if item.next_target=='Closed':
                        continue
                    if item.current_type=="trigger_factor":
                        if customize_atribute['trigger_factor']=='No active item':
                            _target_times_reset(info,1,engine_num,item)
                            item.current_type = 'dep_type1'
                            item.save()
                            continue
                        else:
                            continue
                    index1 = int(item.current_type[-1])
                    index2 = index1 if new_amount==old_amount else 1
                    new_type = info['customizePara']['monitorParam'][index2 - 1]['type']
                    old_type = customize_atribute_old[item.current_type]
                    item.current_type = 'dep_type1' if new_amount!=old_amount else item.current_type
                    item.save()
                    if new_type == old_type:
                        dep_type = new_type
                        _target_times_modify(dep_type, item, customize_atribute_old, customize_atribute,
                                                index1=str(index1),index2=str(index2))
                    else:
                        _target_times_reset(info,index2,engine_num,item)

            #当新的类型不是CUS时
            else:
                for engine_num in intersection_IPS:
                    # next target更新
                    item = ftsi_ips.get(engine_id=engine_num)
                    if item.next_target=='Closed':
                        continue
                    dep_type = info['dep_type']
                    _target_times_modify(dep_type, item, FTSI_info_old, info)
        #当新的type与老的不一致时，直接重置
        else:
            _FTSI2IPSmodify(info, intersection_IPS, ftsi_ips)

    # 只改变文字性描述的处理
    FTSI_obj.ftsi_title = info['ftsi_title']
    FTSI_obj.statement = info['statement']
    FTSI_obj.save()
    # 对删除的Effective_engine的处理
    _FTSI2IPSdelete(delete_IPS, ftsi_ips)
    # 对添加的Effective_engine的处理
    _FTSI2IPSadd(info, FTSI_obj, add_IPS)
    _historyFTSI_record('Edited', FTSI_obj,info['modifyRange'],info['modifyType'])
    # create response data
    return JsonResponse({
        'data': {},
        'meta': {"msg": "Modify the FTSI information successfully",
                 "status": 200}
    })

@api_view(['GET', 'PUT'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
@transaction.atomic
@permission_required('common.change_ftsi_info')
def updateFTSI(request):
    # decode the request information
    info = json.loads(request.body)
    # 处理适用范围发生改变的情况
    FTSI_info = ftsi_info.objects.filter(id=info['id'])
    if info['modifyRange'] == True:
        appliedIPS_old = _IPSList(FTSI_info)
        intersection_IPS = list(set(info['appliedIPS']).intersection(set(appliedIPS_old)))
        delete_IPS = list(set(appliedIPS_old).difference(set(info['appliedIPS'])))
        add_IPS = list(set(info['appliedIPS']).difference(set(appliedIPS_old)))
    else:
        intersection_IPS = info['appliedIPS']
        delete_IPS = []
        add_IPS = []
    ftsi_ips = FTSI2IPS.objects.filter(ftsi_id=info['id'])
    FTSI_obj = FTSI_info.first()
    #创建新版的FTSI条目
    FTSI_obj.active_status=False
    FTSI_obj.save()
    new_ftsi = ftsi_info.objects.create(ftsi_num=info['ftsi_num'], rev=info['rev'], ftsi_title=info['ftsi_title'],
                                        statement=info['statement'], dep_type=info['dep_type'],
                                        total_times=info['total_times'],
                                        period=info['period'], active_status=True)
    try:
        trigger_item = trigger_relationship.objects.get(response_FTSI=info['ftsi_num'])
        trigger_item.delete()
    except trigger_relationship.DoesNotExist:
        pass
    _CustomizeCreate(info, new_ftsi)
    #改变ips指向的FTSI的id
    for item in ftsi_ips:
        item.ftsi_id=new_ftsi.id
        item.save()
    ftsi_ips = FTSI2IPS.objects.filter(ftsi_id=new_ftsi.id)

    # 处理compliance statement改变的情况
    if info['modifyType'] == True:
        FTSI_info_old = FTSI_info.values()[0]
        if FTSI_info_old['dep_type'] == 'CUS':
            customize_atribute_old = customized_type.objects.filter(ftsi_id=FTSI_info_old['id']).values()[0]
        # 更新FTSI_IPS中的内容
        if info['dep_type'] == FTSI_info_old['dep_type']:
            # 当新的类型为CUS时
            if info['dep_type'] == 'CUS':
                # 对比新旧dep_type的数量
                new_amount = len(info['customizePara']['monitorParam'])
                old_amount = 3
                for i in range(1, 4):
                    if customize_atribute_old['dep_type' + str(i)] == '':
                        old_amount = i - 1
                        break
                customize_atribute = customized_type.objects.filter(ftsi_id=new_ftsi.id).values()[0]
                for engine_num in intersection_IPS:
                    item = ftsi_ips.get(engine_id=engine_num)
                    if item.next_target == 'Closed':
                        continue
                    if item.current_type == "trigger_factor":
                        if customize_atribute['trigger_factor'] == 'No active item':
                            _target_times_reset(info, 1, engine_num, item)
                            item.current_type = 'dep_type1'
                            item.save()
                            continue
                        else:
                            continue
                    index1 = int(item.current_type[-1])
                    index2 = index1 if new_amount == old_amount else 1
                    new_type = info['customizePara']['monitorParam'][index2 - 1]['type']
                    old_type = customize_atribute_old[item.current_type]
                    item.current_type = 'dep_type1' if new_amount != old_amount else item.current_type
                    item.save()
                    if new_type == old_type:
                        dep_type = new_type
                        _target_times_modify(dep_type, item, customize_atribute_old, customize_atribute,
                                             index1=str(index1), index2=str(index2))
                    else:
                        _target_times_reset(info, index2, engine_num, item)

            # 当新的类型不是CUS时
            else:
                for engine_num in intersection_IPS:
                    # next target更新
                    item = ftsi_ips.get(engine_id=engine_num)
                    if item.next_target == 'Closed':
                        continue
                    dep_type = info['dep_type']
                    _target_times_modify(dep_type, item, FTSI_info_old, info)
        # 当新的type与老的不一致时，直接重置
        else:
            _FTSI2IPSmodify(info, intersection_IPS, ftsi_ips)
    # 对删除的Effective_engine的处理
    _FTSI2IPSdelete(delete_IPS, ftsi_ips)
    # 对添加的Effective_engine的处理
    _FTSI2IPSadd(info, FTSI_obj, add_IPS)
    #处理文件升级到Z版的情况
    _condition_revZ(new_ftsi, ftsi_ips)
    #保存历史添加、升版信息
    _historyFTSI_record('Updated', new_ftsi, info['modifyRange'], info['modifyType'],issue_date=info['issueDate'])
    # create response data
    return JsonResponse({
        'data': info,
        'meta': {"msg": "Update the FTSI version successfully",
                 "status": 200}
    })

def _select_filter(select,input):
    if select=='dep_type':
        type_dict=ftsi_info.type_dict
        candidate_type=[]
        for item in type_dict:
            if input.upper() in type_dict[item].upper():
                candidate_type.append(item)
        search_dict = {select + '__in': candidate_type, "active_status": True}
    else:
        search_dict = {select + '__icontains': input, "active_status": True}
    return search_dict

def _IPSList(item_info):
    IPSinfo = list(item_info.first().ips.all().values('engine'))
    appliedIPS = []
    for item in IPSinfo:
        appliedIPS.append(item['engine'])
    return appliedIPS

def _CustomizeCreate(info, new_ftsi):
    if info['dep_type'] == 'CUS':
        customize_atribute = customized_type.objects.create(ftsi=new_ftsi,
                                                            trigger_factor=info['customizePara']['trigger']['type'],
                                                            trigger_para=info['customizePara']['trigger']['parameter'])
        if info['customizePara']['trigger']['type'] == 'TFTSI':
            trigger_relationship.objects.create(
                exciter_FTSI=info['customizePara']['trigger']['parameter'], response_FTSI=info['ftsi_num'])
        for i in range(0, len(info['customizePara']['monitorParam'])):
            exec("customize_atribute.dep_type" + str(
                i + 1) + "=info['customizePara']['monitorParam'][i]['type']")
            exec("customize_atribute.period" + str(i + 1) + "=info['customizePara']['monitorParam'][i]['period']")
            exec("customize_atribute.total_times" + str(i + 1) + "=info['customizePara']['monitorParam'][i]['times']")
            customize_atribute.save()
    else:
        return

def _FTSI2IPSadd(info, ftsi, effective_range):
    if info['dep_type'] == 'CUS':
        for item in effective_range:
            if info['customizePara']['trigger']['type'] != 'NA':
                ftsi.ips.add(item,
                             through_defaults={'active_status': True,
                                               'last_date': 'new created',
                                               'current_type': 'trigger_factor',
                                               'next_target': 'After ' + info['customizePara']['trigger']['parameter']})
            else:
                typeMethod = typeMethods(info['customizePara']['monitorParam'][0]['type'])
                next_target = typeMethod.update_next_target(item, info['customizePara']['monitorParam'][0]['period'])
                ftsi.ips.add(item,
                             through_defaults={'active_status': True,
                                               'residual_times': info['customizePara']['monitorParam'][0]['times'],
                                               'next_target': next_target,
                                               'last_date': 'new created', 'current_type': 'dep_type1'})
    else:
        typeMethod = typeMethods(info['dep_type'])
        for item in effective_range:
            next_target = typeMethod.update_next_target(item, info['period'],info['issueDate'])
            ftsi.ips.add(item,
                         through_defaults={'active_status': True, 'residual_times': info['total_times'],
                                           'next_target': next_target,
                                           'last_date': 'new created', 'current_type': info['dep_type']})

def _FTSI2IPSdelete(delete_IPS, ftsi_ips):
    for item in delete_IPS:
        single_ips = ftsi_ips.get(engine_id=item)
        single_ips.delete()

def _FTSI2IPSmodify(info, intersection_IPS, ftsi_ips):
    if info['dep_type'] == 'CUS':
        for engine_num in intersection_IPS:
            item = ftsi_ips.get(engine_id=engine_num)
            if item.active_status == False:
                continue
            if info['customizePara']['trigger']['type'] != 'NA':
                item.current_type = 'trigger_factor'
                item.next_target = 'After ' + info['customizePara']['trigger']['parameter']
                item.save()
            else:
                typeMethod = typeMethods(info['customizePara']['monitorParam'][0]['type'])
                next_target = typeMethod.update_next_target(engine_num,
                                                            info['customizePara']['monitorParam'][0]['period'],info['issueDate'])
                item.current_type = 'dep_type1'
                item.next_target = next_target
                item.residual_times = info['customizePara']['monitorParam'][0]['times']
                item.save()
    else:
        typeMethod = typeMethods(info['dep_type'])
        for engine_num in intersection_IPS:
            item = ftsi_ips.get(engine_id=engine_num)
            if item.next_target=='Closed':
                continue
            next_target = typeMethod.update_next_target(engine_num, info['period'],info['issueDate'])
            item.current_type = info['dep_type']
            item.next_target = next_target
            item.residual_times = info['total_times']
            item.save()

def _target_times_modify(dep_type, item, FTSI_info_old, info, index1='',index2=''):
    typeMethod = typeMethods(dep_type)
    current_value = item.next_target
    old_target = FTSI_info_old['period' + index1]
    new_target = info['period' + index2]
    item.next_target = typeMethod.next_target_edit(current_value, old_target, new_target)
    # residual times更新
    item.residual_times = item.residual_times - FTSI_info_old['total_times' + index1] + int(info['total_times' + index2])
    item.save()

def _target_times_reset(info,index2,engine_num,item):
    typeMethod = typeMethods(info['customizePara']['monitorParam'][index2 - 1]['type'])
    next_target = typeMethod.update_next_target(engine_num, info['customizePara']['monitorParam'][index2 - 1]['period'],info['issueDate'])
    item.next_target = next_target
    item.residual_times = info['customizePara']['monitorParam'][index2 - 1]['times']
    item.save()

def _condition_revZ(new_ftsi,ftsi_ips):
    if new_ftsi.rev == 'Z':
        new_ftsi.active_status = False
        new_ftsi.save()
        for item in ftsi_ips:
            item.delete()

def _historyFTSI_record(modify_type,ftsi_info,effect_change='',monitor_change='',issue_date=date.today().strftime("%Y-%m-%d")):
    pass
    ftsi_history = historyrecord_ftsi_modify.objects.create(date=issue_date, modify_type=modify_type,
                                                    effect_change=effect_change,monitor_change=monitor_change)
    ftsi_history.ftsi_num = ftsi_info.ftsi_num
    ftsi_history.rev = ftsi_info.rev
    ftsi_history.ftsi_title = ftsi_info.ftsi_title
    ftsi_history.statement = ftsi_info.statement
    ftsi_history.save()