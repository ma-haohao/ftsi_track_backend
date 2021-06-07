from django.shortcuts import render
from common.models import historyrecord_task_submit,historyrecord_ftsi_modify,FTSI_implement_list,ftsi_info
from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage

# Create your views here.

def _obtain_history(request,table):
    # decode the request information
    select, input1, pagesize, pagenum = request.GET.get('select', ''), request.GET.get('input', ''), request.GET.get(
        'pagesize', ''), request.GET.get('pagenum', '')
    # query the data according to the input
    if select.strip() == '' or input1.strip() == '':
        query = table.objects.filter().order_by("-date")
    else:
        search_dict = {select + '__icontains': input1}
        query = table.objects.filter(**search_dict).order_by("-date")
    query_set = list(query.values())
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
            "response_info": relist},
        'meta': {"msg": "obtain history records successfully",
                 "status": 200}
    })

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
def obtain_submitHistory(request):
    res=_obtain_history(request,historyrecord_task_submit)
    return res

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
def obtain_ftsiHistory(request):
    res=_obtain_history(request,historyrecord_ftsi_modify)
    return res

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
def obtain_submitFailed(request):
    query=FTSI_implement_list.objects.filter(implement_status=False).order_by("-activity_date")
    query_list=list(query.values())
    for item in query_list:
        item["ftsi_info"]=item["document_no"]+" Rev."+item["document_revision"]
        try:
            s_FTSI=ftsi_info.objects.filter(ftsi_num=item["document_no"],active_status=True)[0]
            item["ftsi_title"]=s_FTSI.ftsi_title
        except IndexError:
            item["ftsi_title"] = "not found in the ftsi list."
    return JsonResponse({
        'data': {
            "totalitems": len(query_list),
            "query_info": query_list},
        'meta': {"msg": "obtain failed submit record successfully.",
                 "status": 200}
    })