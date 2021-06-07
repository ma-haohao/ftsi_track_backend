from django.shortcuts import render
# Create your views here.
import json
from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django_redis import get_redis_connection
from userOpt.models import monitor_para
from django.db import transaction
from django.forms import model_to_dict

def _obtain_from_db(username):
    # 去数据库中查找相关参数
    try:
        data = monitor_para.objects.filter(owner=username).values()[0]
    except IndexError:  # 未找到则为此用户建立一个新条目，所有值与common项一样
        origianldata = monitor_para.objects.filter(owner="common").values()[0]
        origianldata['owner'] = username
        data = monitor_para.objects.create(**origianldata)
        data = model_to_dict(data)
    return data

def _get_monitor_para(username):
    address = "monitor_para"
    dict_name = address + ":" + username
    try:
        conn = get_redis_connection('default')
        # 查找在redis缓存数据库中是否存在，存在则直接返回，不存在则去数据库中查找数据
        if conn.exists(dict_name) == 1:
            data = conn.hgetall(dict_name)
        else:
            data=_obtain_from_db(username)
            # 将数据保存到redis缓存中去
            conn.hmset(dict_name, data)
    except:#若访问缓存数据库失败，则直接从数据库中取数据
        data=_obtain_from_db(username)
    return data

def single_para(monitor_para,type1,keywords):
    match_map={'warning':'w_','attention':'a_','predict':'p_'}
    keywords="CC" if keywords=="C1 cycle" else keywords
    key=match_map[type1]+keywords
    return int(monitor_para[key])

def _set_monitor_para(username,data):
    address = "monitor_para"
    dict_name = address + ":" + username
    try:
        conn = get_redis_connection('default')
        conn.hmset(dict_name, data)
    except:
        pass
    #同步到数据库中去
    para_db=monitor_para.objects.filter(owner=username)[0]
    for key in data:
        exec('para_db.'+key+'=data[key]')
    para_db.save()

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
def obtain_monitor_para(request):
    #获取用户名称
    username = request.user.username
    data=_get_monitor_para(username)
    return JsonResponse({
        "data":data,
        "meta":{
            "status":200,
            "msg":"Obtain the monitor parameters successfully!"
        }
    })

@api_view(['GET','PUT'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
@transaction.atomic
def change_monitor_para(request):
    #获取用户名称
    username = request.user.username
    info = json.loads(request.body)
    _set_monitor_para(username,info)
    return JsonResponse({
        "data":{},
        "meta":{
            "status":200,
            "msg":"change the monitor parameters successfully!"
        }
    })