from common.models import engine_info,customized_type,ftsi_info,historyrecord_engine_info
from datetime import date,timedelta,datetime
from configparser import ConfigParser
from ftsiOpt.CachedmonitorFlag import single_para
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class typeMethods():
    def __init__(self, count_type,username="common"):
        self.username = username
        self.method_dict = {
            'OTHER': self.on_condition(self.username),
            'FD':self.up2FD(self.username),
            'FH':self.up2FH(self.username),
            'EH':self.up2EH(self.username),
            'CC':self.up2CC(self.username),
            'DATE':self.up2DATE(self.username),
            'FC':self.up2FC(self.username),
            'ES':self.up2ES(self.username),
            'RC':self.up2RC(self.username),
            'CUS':self.up2CUS(self.username)}
        self.count_type = count_type

        self.type_used = self.method_dict[self.count_type]

    def update_next_target(self, engine_num, period,issue_date=None):
        if issue_date in [None,'']:
            query_info = engine_info.objects.filter(engine=engine_num).values()[0]
            query_info['issue_date']=date.today().strftime('%Y-%m-%d')
        else:
            try:
                query_info = historyrecord_engine_info.objects.filter(engine=engine_num,date=issue_date).values()[0]
                query_info['issue_date']=issue_date
            except:
                query_info = engine_info.objects.filter(engine=engine_num).values()[0]
                query_info['issue_date'] = date.today().strftime('%Y-%m-%d')
        return self.type_used.target_update(query_info,period)

    def generate_comments(self, engine_info, next_target,monitor_para):
        return self.type_used.comments_generate(engine_info,next_target,monitor_para)

    def queryword_unit(self):
        DB_keyword,unit=self.type_used.DB_keyword,self.type_used.unit
        return DB_keyword,unit

    def predict_implement(self,engine_info,next_target,flight_parameter,monitor_para):
        return self.type_used.predict(engine_info,next_target,flight_parameter,monitor_para)

    def submit_check_comments(self,engine_info,ftsi_instance):
        if ftsi_instance['dep_type']=='CUS':
            customized_types = customized_type.objects.filter(ftsi_id=ftsi_instance['id']).values()[0]
            if self._residual_times_check(ftsi_instance):
                new_types=self._customize_type_change(ftsi_instance,customized_types)
                if new_types==False:
                    return "Next: Closed"
                else:
                    type_change_content=customized_types[ftsi_instance['ips_info']['current_type']]+' => '+customized_types[new_types['new_type']]
                    type_used=self.method_dict[customized_types[new_types['new_type']]]
                    next_target=type_used.target_update(engine_info,new_types['period'])
                    return type_change_content+', '+'Next target: '+str(next_target)+' '+type_used.unit
            else:
                current_type=customized_types[ftsi_instance['ips_info']['current_type']]
                type_used = self.method_dict[current_type]
                next_target = type_used.target_update(engine_info, customized_types['period'+ftsi_instance['ips_info']['current_type'][-1]])
                return 'Next target: ' + str(next_target)+' '+type_used.unit
        else:
            if self._residual_times_check(ftsi_instance):
                return "Next: Closed"
            else:
                next_target=self.type_used.target_update(engine_info, ftsi_instance['period'])
                return 'Next target: ' + str(next_target)+' '+self.type_used.unit

    def history_implement(self,engine_info,ftsi_instance):
        type_dict=ftsi_info.type_dict
        if ftsi_instance['dep_type']=='CUS':
            customized_types = customized_type.objects.filter(ftsi_id=ftsi_instance['id']).values()[0]
            current_type=customized_types[ftsi_instance['ips_info']['current_type']]
            type_used = self.method_dict[current_type]
            implement_info = type_used.history_implement(engine_info)
            return type_dict[current_type]+': '+str(implement_info)
        else:
            implement_info = self.type_used.history_implement(engine_info)
            return type_dict[self.count_type]+': '+str(implement_info)

    def submit_ftsi(self,engine_info,ftsi_instance,FTSI_original,implementDate):
        ips=FTSI_original.get(id=ftsi_instance['ips_info']['id'])
        if ftsi_instance['dep_type']=='CUS':
            customized_types = customized_type.objects.filter(ftsi_id=ftsi_instance['id']).values()[0]
            if self._residual_times_check(ftsi_instance):
                new_types=self._customize_type_change(ftsi_instance,customized_types)
                if new_types==False:
                    ips.last_date=implementDate
                    ips.residual_times=ftsi_instance['ips_info']['residual_times']-1
                    ips.active_status=False
                    ips.next_target='Closed'
                    ips.save()
                    return True
                else:
                    type_used=self.method_dict[customized_types[new_types['new_type']]]
                    next_target=type_used.target_update(engine_info,new_types['period'])
                    ips.current_type = new_types['new_type']
                    ips.last_date = implementDate
                    ips.residual_times = new_types['total_times']
                    ips.next_target = next_target
                    ips.save()
                    return True
            else:
                current_type=customized_types[ftsi_instance['ips_info']['current_type']]
                type_used = self.method_dict[current_type]
                next_target = type_used.target_update(engine_info, customized_types['period'+ftsi_instance['ips_info']['current_type'][-1]])
                ips.last_date = implementDate
                ips.residual_times = ftsi_instance['ips_info']['residual_times'] - 1
                ips.next_target = next_target
                ips.save()
                return True
        else:
            if self._residual_times_check(ftsi_instance):
                ips.last_date = implementDate
                ips.residual_times = ftsi_instance['ips_info']['residual_times'] - 1
                ips.active_status = False
                ips.next_target = 'Closed'
                ips.save()
                return True
            else:
                next_target=self.type_used.target_update(engine_info, ftsi_instance['period'])
                ips.last_date = implementDate
                ips.residual_times = ftsi_instance['ips_info']['residual_times'] - 1
                ips.next_target = next_target
                ips.save()
                return True

    def _residual_times_check(self,ftsi_instance):
        return True if ftsi_instance['ips_info']['residual_times']-1<=0 else False

    def _customize_type_change(self,ftsi_instance,types):
        current_type=int(ftsi_instance['ips_info']['current_type'][-1])
        if current_type==3:
            return False
        else:
            next_type='dep_type'+str(current_type+1)
            if types[next_type]=='':
                return False
            else:
                return {'new_type':next_type,'period':types['period'+str(current_type+1)],'total_times':types['total_times'+str(current_type+1)]}

    def next_target_edit(self,current_value,old_target,new_target):
        return self.type_used.next_target_modify(current_value,old_target,new_target)

    def modify_for_engine_info(self,new_engine_info,old_engine_info,next_target):
        return self.type_used.engine_parameter_change(new_engine_info,old_engine_info,next_target)

    #不同类型下的对应处理方法
    class on_condition():
        def __init__(self,username):
            self.DB_keyword = ''
            self.unit = ''
            self.username=username
        def target_update(self,query_info,period):
            return ''
        def comments_generate(self,engine_info,next_target,monitor_para):
            return 'On Condition','safe'
        def predict(self,engine_info,next_target,flight_parameter,monitor_para):
            return 'On condition',False
        def next_target_modify(self,current_value,old_target,new_target):
            return ''
        def history_implement(self,engineInfo):
            return ''
        def engine_parameter_change(self,new_engine_info,old_engine_info,next_target):
            return ''

    class up2FD():
        def __init__(self,username):
            self.DB_keyword='flight_day'
            self.unit='FD'
            self.username = username
        def target_update(self,query_info,period):
            return query_info[self.DB_keyword]+int(period)

        def comments_generate(self,engine_info,next_target,monitor_para):
            res=int(next_target)-engine_info[self.DB_keyword]
            content=str(res)+' '+self.unit+' left, \nnext '+str(next_target)+' '+self.unit
            #获得remind—flag来判断是否需要把该项标注出来
            if res>single_para(monitor_para,'warning',self.unit):remind_flag='safe'
            elif res<=single_para(monitor_para,'warning',self.unit) and res>single_para(monitor_para,'attention',self.unit):remind_flag='warning'
            else: remind_flag='attention'
            return content,remind_flag

        def predict(self,engine_info,next_target,flight_parameter,monitor_para):
            res = int(next_target) - engine_info[self.DB_keyword]-int(flight_parameter['flightDay'])
            flag=True if res<=single_para(monitor_para,'predict',self.unit) else False
            content=str(res)+' '+self.unit
            return content,flag

        def next_target_modify(self,current_value,old_target,new_target):
            return int(current_value)-int(old_target)+int(new_target)

        def history_implement(self,engineInfo):
            return str(engineInfo[self.DB_keyword])+' '+self.unit

        def engine_parameter_change(self,new_engine_info,old_engine_info,next_target):
            return str(int(next_target)+int(new_engine_info[self.DB_keyword])-int(old_engine_info[self.DB_keyword]))

    class up2FH():
        def __init__(self,username):
            self.DB_keyword='flight_time'
            self.unit='FH'
            self.username=username
        def target_update(self,query_info,period):
            res=query_info[self.DB_keyword] + int(period)
            return round(res,2)
        def comments_generate(self,engine_info,next_target,monitor_para):
            res=float(next_target)-engine_info[self.DB_keyword]
            content=str(round(res,2))+' '+self.unit+' left, \nnext '+next_target+' '+self.unit
            if res>single_para(monitor_para,'warning',self.unit):remind_flag='safe'
            elif res<=single_para(monitor_para,'warning',self.unit) and res>single_para(monitor_para,'attention',self.unit):remind_flag='warning'
            else: remind_flag='attention'
            return content,remind_flag
        def predict(self,engine_info,next_target,flight_parameter,monitor_para):
            res = float(next_target) - engine_info[self.DB_keyword]-float(flight_parameter['flightHour'])
            flag=True if res<=single_para(monitor_para,'predict',self.unit) else False
            content=str(round(res,2))+' '+self.unit
            return content,flag
        def next_target_modify(self,current_value,old_target,new_target):
            res=float(current_value)-float(old_target)+float(new_target)
            return round(res,2)
        def history_implement(self,engineInfo):
            return str(engineInfo[self.DB_keyword])+' '+self.unit

        def engine_parameter_change(self,new_engine_info,old_engine_info,next_target):
            return round(float(next_target)+float(new_engine_info[self.DB_keyword])-float(old_engine_info[self.DB_keyword]),2)

    class up2EH(up2FH):
        def __init__(self,username):
            self.DB_keyword = 'run_time'
            self.unit = 'EH'
            self.username=username
        def predict(self,engine_info,next_target,flight_parameter,monitor_para):
            res = float(next_target) - engine_info[self.DB_keyword]-float(flight_parameter['engineHour'])
            flag=True if res<=single_para(monitor_para,'predict',self.unit) else False
            content=str(round(res,2))+' '+self.unit
            return content,flag

    class up2CC(up2FD):
        def __init__(self,username):
            self.DB_keyword = 'c1_cycle'
            self.unit = 'C1 cycle'
            self.username = username
        def predict(self,engine_info,next_target,flight_parameter,monitor_para):
            res = int(next_target) - engine_info[self.DB_keyword]-int(flight_parameter['c1Cycle'])
            flag=True if res<=single_para(monitor_para,'predict',self.unit) else False
            content=str(res)+' '+self.unit
            return content,flag

    class up2FC(up2FD):
        def __init__(self,username):
            self.DB_keyword = 'flight_cycle'
            self.unit = 'FC'
            self.username = username
        def predict(self,engine_info,next_target,flight_parameter,monitor_para):
            res = int(next_target) - engine_info[self.DB_keyword]-int(flight_parameter['flightCycle'])
            flag=True if res<=single_para(monitor_para,'predict',self.unit) else False
            content=str(res)+' '+self.unit
            return content,flag

    class up2ES(up2FD):
        def __init__(self,username):
            self.DB_keyword = 'engine_starts'
            self.unit = 'ES'
            self.username = username
        def predict(self,engine_info,next_target,flight_parameter,monitor_para):
            res = int(next_target) - engine_info[self.DB_keyword]-1
            flag=True if res<=single_para(monitor_para,'predict',self.unit) else False
            content=str(res)+' '+self.unit
            return content,flag

    class up2RC(up2FD):
        def __init__(self,username):
            self.DB_keyword = 'reverse_cycle'
            self.unit = 'RC'
            self.username = username
        def predict(self,engine_info,next_target,flight_parameter,monitor_para):
            res = int(next_target) - engine_info[self.DB_keyword]-int(flight_parameter['TRCycle'])
            flag=True if res<=single_para(monitor_para,'predict',self.unit) else False
            content=str(res)+' '+self.unit
            return content,flag

    class up2DATE():
        def __init__(self,username):
            self.DB_keyword = ''
            self.unit = ''
            self.username = username
        def target_update(self,query_info,period):
            issue_date=datetime.strptime(query_info['issue_date'], '%Y-%m-%d').date()
            return (issue_date+timedelta(days=int(period))).strftime('%Y-%m-%d')
        def comments_generate(self,engine_info,next_target,monitor_para):
            res=(datetime.strptime(next_target,'%Y-%m-%d').date()-date.today()).days
            if res>single_para(monitor_para,'warning','DATE'):remind_flag='safe'
            elif res<=single_para(monitor_para,'warning','DATE') and res>single_para(monitor_para,'attention','DATE'):remind_flag='warning'
            else: remind_flag='attention'
            content = str(res)+' day left, next ' + next_target
            return content,remind_flag
        def predict(self,engine_info,next_target,flight_parameter,monitor_para):
            res = (datetime.strptime(next_target,'%Y-%m-%d').date()-date.today()).days-int(flight_parameter['flightDay'])
            flag=True if res<=single_para(monitor_para,'predict','DATE') else False
            content=str(res)+' days'
            return content,flag
        def next_target_modify(self, current_value, old_target, new_target):
            res = datetime.strptime(current_value,'%Y-%m-%d').date() - timedelta(days=int(old_target)) + timedelta(days=int(new_target))
            return res.strftime('%Y-%m-%d')
        def history_implement(self,engineInfo):
            return ''
        def engine_parameter_change(self,new_engine_info,old_engine_info,next_target):
            return next_target

    class up2CUS():
        def __init__(self,username):
            pass
        def target_update(self,query_info,period):
            return ''



