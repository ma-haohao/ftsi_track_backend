from django.db import models

# Create your models here.
# 建立engine信息表
class engine_info(models.Model):
    engine = models.IntegerField(primary_key=True)
    aircraft = models.CharField(max_length=8)
    left_right = models.CharField(max_length=5, blank=True)
    flight_day = models.IntegerField(blank=True, null=True)
    flight_time = models.FloatField(blank=True, null=True)
    run_time = models.FloatField(blank=True, null=True)
    c1_cycle = models.IntegerField(blank=True, null=True)
    flight_cycle = models.IntegerField(blank=True, null=True)
    engine_starts = models.IntegerField(blank=True, null=True)
    reverse_cycle = models.IntegerField(blank=True, null=True)

# 建立FTSI文件信息表
class ftsi_info(models.Model):
    type_choice = (
        ('OTHER','On condition'),
        ('FD','Up to flight day'),
        ('FH','Up to flight hour'),
        ('EH','Up to engine hour'),
        ('CC','Up to C1 cycle'),
        ('DATE','Up to date'),
        ('FC','Up to flight cycle'),
        ('ES','Up to engine starts'),
        ('RC','Up to reverse cycle'),
        ('CUS','Customize'))
    type_dict={}
    for i in range(0, len(type_choice)):
        type_dict[type_choice[i][0]]=type_choice[i][1]
    ftsi_num = models.CharField(max_length=20)
    rev = models.CharField(max_length=5)
    ftsi_title = models.CharField(max_length=200, blank=True)
    statement = models.CharField(max_length=500, blank=True)
    active_status = models.BooleanField()
    dep_type = models.CharField(max_length=30,choices=type_choice)
    period = models.CharField(blank=True, max_length=30)
    total_times=models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'common_ftsi_info'
        unique_together = ("ftsi_num", "rev")
        app_label = "common"

    ips = models.ManyToManyField(to='engine_info',
                                 through='FTSI2IPS',
                                 through_fields=('ftsi', 'engine'))

# 当FTSI_info的类型为customize的情况，FTSI的子属性
class customized_type(models.Model):
    type_choice = ftsi_info.type_choice
    trigger_type = (
        ('NA','No active item'),
        ('TDATE','Active by date'),
        ('TFTSI','Active by FTSI'))
    param_relate = {'trigger_factor': ['trigger_para'], 'dep_type1': ['period1', 'total_times1'],
                    'dep_type2': ['period2', 'total_times2'], 'dep_type3': ['period3', 'total_times3']}
    ftsi = models.OneToOneField(to='ftsi_info', on_delete=models.CASCADE, primary_key=True)
    trigger_factor = models.CharField(max_length=30, blank=True,choices=trigger_type)
    trigger_para = models.CharField(max_length=30, blank=True)
    dep_type1 = models.CharField(max_length=30)
    period1 = models.CharField(blank=True, max_length=30)
    total_times1 = models.IntegerField(blank=True, null=True)
    dep_type2 = models.CharField(max_length=30)
    period2 = models.CharField(blank=True, max_length=30)
    total_times2 = models.IntegerField(blank=True, null=True)
    dep_type3 = models.CharField(max_length=30)
    period3 = models.CharField(blank=True, max_length=30)
    total_times3 = models.IntegerField(blank=True, null=True)
    class Meta:
        app_label = "common"

# 建立engine 与 FTSI文件之间的关联关系
class FTSI2IPS(models.Model):
    ftsi = models.ForeignKey(to='ftsi_info', on_delete=models.CASCADE)
    engine = models.ForeignKey(to='engine_info', on_delete=models.CASCADE)
    last_date = models.CharField(max_length=100, blank=True)
    current_type = models.CharField(max_length=30, blank=True)
    next_target = models.CharField(max_length=30, blank=True)
    residual_times = models.IntegerField(blank=True, null=True)
    active_status = models.BooleanField()
    class Meta:
        app_label = "common"

class trigger_relationship(models.Model):
    exciter_FTSI=models.CharField(max_length=20)
    response_FTSI=models.CharField(max_length=20,primary_key=True)
    class Meta:
        app_label = "common"

class historyrecord_engine_info(models.Model):
    date=models.CharField(max_length=20)
    engine = models.IntegerField()
    aircraft = models.CharField(max_length=8)
    left_right = models.CharField(max_length=5, blank=True)
    flight_day = models.IntegerField(blank=True, null=True)
    flight_time = models.FloatField(blank=True, null=True)
    run_time = models.FloatField(blank=True, null=True)
    c1_cycle = models.IntegerField(blank=True, null=True)
    flight_cycle = models.IntegerField(blank=True, null=True)
    engine_starts = models.IntegerField(blank=True, null=True)
    reverse_cycle = models.IntegerField(blank=True, null=True)
    class Meta:
        db_table = 'historyrecord_engineInfo'
        unique_together = ("date", "engine")
        app_label = "common"

class historyrecord_task_submit(models.Model):
    date=models.CharField(max_length=20)
    aircraft=models.CharField(max_length=8)
    engine=models.IntegerField()
    ftsi_info=models.CharField(max_length=200, blank=True)
    implement_info=models.CharField(max_length=100, blank=True)
    next_step=models.CharField(max_length=100, blank=True)
    class Meta:
        db_table = 'historyrecord_taskSubmit'
        app_label = "common"

class historyrecord_ftsi_modify(models.Model):
    date=models.CharField(max_length=20)
    modify_type=models.CharField(max_length=20)
    ftsi_num = models.CharField(max_length=20)
    rev = models.CharField(max_length=5)
    ftsi_title = models.CharField(max_length=200, blank=True)
    statement = models.CharField(max_length=500, blank=True)
    effect_change=models.BooleanField(blank=True, null=True)
    monitor_change = models.BooleanField(blank=True, null=True)
    class Meta:
        db_table = 'historyrecord_ftsiModify'
        app_label = "common"

class FTSI_implement_list(models.Model):
    activity_date = models.TextField(max_length=40, blank=True)
    logged_date = models.TextField(max_length=40, blank=True)
    identification = models.IntegerField(blank=True,null=True)
    document_type = models.TextField(max_length=20, blank=True)
    document_no = models.TextField(max_length=10, blank=True)
    document_revision = models.TextField(max_length=5, blank=True)
    implement_status = models.BooleanField()
    class Meta:
        unique_together = ("activity_date", "identification","document_no")
        db_table = 'common_ftsi_implement_list'
        app_label = "common"

class ftsi_number_issue(models.Model):
    entry_no=models.TextField(max_length=20, blank=True)
    logged_date = models.TextField(max_length=40, blank=True)
    type = models.TextField(null=True, blank=True)
    ftsi_no = models.CharField(max_length=10, blank=True)
    revision = models.CharField(max_length=5, blank=True)
    ftsi_title = models.CharField(max_length=200, blank=True)
    statement = models.CharField(max_length=500, blank=True)
    impact_ips = models.TextField(max_length=100, blank=True)
    issue_date=models.TextField(max_length=40, blank=True)
    action_type=models.TextField(max_length=10,blank=True)
    status=models.BooleanField(default=False)
    class Meta:
        unique_together = ("ftsi_no", "revision")
        db_table = 'common_ftsi_number_issue'
        app_label = "common"

from django.contrib import admin

admin.site.register(engine_info)

admin.site.register(ftsi_info)
