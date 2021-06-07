from django.shortcuts import render
import json
from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.db import connections
from common.models import historyrecord_engine_info,FTSI_implement_list,FTSI2IPS
from ftsiOpt.ftsiSubmit import _submitprocess
# Create your views here.

def _unique_operation(db_name,table_name):
    with connections[db_name].cursor() as cursor:
        SQL='''select distinct * into public.temp_%s from public.%s;
        delete from public.%s;
        insert into public.%s select * from public.temp_%s;
        drop table public.temp_%s;'''
        para_list=(table_name,table_name,table_name,table_name,table_name,table_name)
        cursor.execute(SQL%para_list)
    return 0

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
def test(request):
    '''自动提交ftsi_implement_list中的任务，同时将还未提交飞行数据的情况进行暂时的缓存'''
    submit_list = FTSI_implement_list.objects.filter(implement_status=False)
    for item in submit_list:
        try:
            engineNum = item.identification
        except ValueError:
            continue
        implementDate = item.activity_date
        FTSI_list = [item.document_no]
        try:
            engine_info1 = historyrecord_engine_info.objects.filter(engine=engineNum,date=implementDate).values()[0]  # 修改为engine history后更新
            FTSI_original = FTSI2IPS.objects.filter(engine_id=engineNum)
            warning_info = _submitprocess(FTSI_original, engine_info1, FTSI_list, implementDate)
        except:
            continue
        if warning_info != "":
            print(warning_info)
        else:
            item.implement_status = True
            item.save()
    return JsonResponse({
        'data':'sucess'
    })

