from django.shortcuts import render
from common.models import FTSI2IPS, customized_type, historyrecord_engine_info, engine_info, FTSI_implement_list, \
    ftsi_info, ftsi_number_issue
from portalOpt.models import ToscTrackingEngine, ScIpsInformationOnly, ScFtsiTracking
from datetime import datetime, date, timedelta
from common.typeMethods import typeMethods
from django.db import transaction
from ftsiOpt.ftsiSubmit import _submitprocess
from django.db import connections
from django.db.models import Q

# Create your views here.
@transaction.atomic
def activeDatecheck():
    '''查看customize类FTSI中日期激活项是否到达相关时间'''
    customized_info = list(customized_type.objects.filter(trigger_factor='TDATE').values())
    for item in customized_info:
        active_date = item['trigger_para']
        active_date = datetime.strptime(active_date, '%Y-%m-%d')
        flag = (active_date.date() - date.today()).days
        if flag <= 0:
            ftsi_ips = FTSI2IPS.objects.filter(ftsi_id=item['ftsi_id'])
            for ips in ftsi_ips:
                if ips.current_type!='trigger_factor':
                    continue
                ips.current_type = 'dep_type1'
                ips.last_date = 'Activate on ' + date.today().strftime('%Y-%m-%d')
                ips.residual_times = item['total_times1']
                type_used = typeMethods(item['dep_type1'])
                ips.next_target = type_used.update_next_target(ips.engine_id, item['period1'])
                ips.save()

@transaction.atomic
def historyEngineInfo():
    dateInfo_saved = (date.today() + timedelta(days=-1)).strftime('%Y-%m-%d')
    dateInfo_delete = date.today() + timedelta(days=-30)
    engine_info1 = engine_info.objects.all()
    try:
        for item in engine_info1:
            history_info = historyrecord_engine_info.objects.create(
                date=dateInfo_saved, engine=item.engine, aircraft=item.aircraft, left_right=item.left_right,
                flight_day=item.flight_day, flight_time=item.flight_time, run_time=item.run_time,
                c1_cycle=item.c1_cycle,
                flight_cycle=item.flight_cycle, engine_starts=item.engine_starts, reverse_cycle=item.reverse_cycle)
    except:
        print('already existed')
    deleted_historyInfo = historyrecord_engine_info.objects.filter(date=dateInfo_delete)
    deleted_historyInfo.delete()

@transaction.atomic
def updateEngineInfo():
    '''根据tosc_tracking_engine中的数据对发动机表中的数据进行自动更新'''
    new_engineInfo = ToscTrackingEngine.objects.all().values(*ToscTrackingEngine.column)
    engine_table = engine_info.onjects.all()
    for item in new_engineInfo:
        try:
            engine = engine_table.filter(engine=item['esn'])
            engine.flight_day = item['last_msn_day']
            engine.flight_time = item['last_msn_time']
            engine.flight_cycle = item['last_msn_cycle']
            engine.run_time = item['run_time']
            engine.c1_cycle = item['c1_cycle']
            engine.engine_starts = item['starts']
            engine.reverse_cycle = item['reverse_cycle']
            engine.save()
        except:
            pass

#checked
def implement_list_query():
    '''提取sc_ips_information_only中的数据，并放入到待处理队列中'''
    # 获取logged_time为3天内的所有数据
    today = date.today().strftime('%Y-%m-%d')
    yesterday = (date.today() + timedelta(days=-1)).strftime('%Y-%m-%d')
    # 过滤条件，logged_date是今天或者昨天，activity date, identification，document no这三个参数都不为null
    ftsi_info = ScIpsInformationOnly.objects.filter(
        Q(logged_date__icontains=today) | Q(logged_date__icontains=yesterday)).filter(
        activity_date__isnull=False).filter(identification__isnull=False).filter(document_no__isnull=False).values(
        *ScIpsInformationOnly.column)
    for item in ftsi_info:
        if item['identification'][0:3] != 'IPS' or item['document_type']!='LEAP-1C-FTSI-':
            continue
        try:
            # 利用unique条件来加入新添加的文件，try失败表示该份信息已经加入到list中,同时对其中存在问题的数据进行修正
            item['identification'] = '600' + item['identification'][3:6]
            item['activity_date'] = item['activity_date'].split(' ')[0]
            new_ftsi = FTSI_implement_list.objects.create(activity_date=item['activity_date'],
                                                          identification=item['identification'],
                                                          document_no=item['document_no'], implement_status=False)
            new_ftsi.logged_date = item['logged_date']
            new_ftsi.document_type = item['document_type']
            new_ftsi.document_revision = item['document_revision']
            new_ftsi.save()
        except:
            pass

#checked
def ftsi_tracking_query():
    '''提取sc_ftsi_tracking中的数据，进行处理后放入到待处理队列中
    1.时间格式的转换
    2. update or add类型的判断...'''
    today = date.today().strftime('%Y-%m-%d')
    yesterday = (date.today() + timedelta(days=-1)).strftime('%Y-%m-%d')
    ftsi_list = ScFtsiTracking.objects.filter(
        Q(logged_date__icontains=today) | Q(logged_date__icontains=yesterday)).filter(
        ftsi_no__isnull=False).filter(revision__isnull=False).exclude(impact_ips="Off Engine").\
        values(*ScFtsiTracking.column).distinct()
    for item in ftsi_list:
        # 格式转换
        internal_format = item['issue_date'].split('/')
        issue_date = internal_format[2] + '-' + str('%02d'%int(internal_format[0])) + '-' + str('%02d'%int(internal_format[1]))
        logged_date = item['logged_date'].split(' ')[0]
        # 判断数据库中是否存在此FTSI号
        try:
            query_res1 = ftsi_info.objects.filter(ftsi_num=item['ftsi_no']).values()[0]
            actiontype = 'update'
        except:
            actiontype = 'add'
        # 判断缓冲表里是否有相同FTSI号的项目，有则仅保留其中高版本的文件
        try:
            query_res2 = ftsi_number_issue.objects.filter(ftsi_no=item['ftsi_no'], status=False)[0]
            revision_old = query_res2.revision
            revision_new = item['revision']
            if revision_old < revision_new:
                actiontype = query_res2.action_type
                query_res2.delete()
            else:
                continue
        except:
            pass
        # 将数据加入到ftsi_num_issue表中,try失败表明在其中已经存在同名文件
        try:
            new_item = ftsi_number_issue.objects.create(entry_no=item['entry_no'], logged_date=logged_date, type=item['type'],
                                                        ftsi_no=item['ftsi_no'], revision=item['revision'],
                                                        ftsi_title=item['ftsi_title'],statement=item['compliance'],
                                                        impact_ips=item['impact_ips'],issue_date=issue_date,
                                                        status=False, action_type=actiontype)
        except:
            pass

@transaction.atomic
def AutoTaskSubmit():
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
            pass
        else:
            item.implement_status = True
            item.save()

# 数据库重新更新
def _unique_operation(db_name, table_name):
    with connections[db_name].cursor() as cursor:
        SQL = '''select distinct * into public.temp_%s from public.%s;
        delete from public.%s;
        insert into public.%s select * from public.temp_%s;
        drop table public.temp_%s;'''
        para_list = (table_name, table_name, table_name, table_name, table_name, table_name)
        cursor.execute(SQL % para_list)
    return 0

@transaction.atomic
def ips_table_opt():
    _unique_operation('ReData', 'sc_ips_information_only')
    return None

@transaction.atomic
def mi_table_opt():
    _unique_operation('ReData', 'sc_daily_mi_report')
    return None

@transaction.atomic
def ftsi_table_opt():
    _unique_operation('ReData', 'sc_ftsi_tracking')
    return None
