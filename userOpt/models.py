from django.db import models

# Create your models here.
class userCacheEngineInfo(models.Model):
    username=models.CharField(max_length=30)
    cacheDate=models.CharField(max_length=20)
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
        db_table = 'userOpt_engineInfo'
        unique_together = ("username", "engine")
        app_label = "userOpt"

class userCacheFTSI2IPS(models.Model):
    cache = models.ForeignKey(to='userCacheEngineInfo', on_delete=models.CASCADE)
    ftsi_id = models.IntegerField()
    last_date = models.CharField(max_length=100, blank=True)
    current_type = models.CharField(max_length=30, blank=True)
    next_target = models.CharField(max_length=300, blank=True)
    residual_times = models.IntegerField(blank=True, null=True)
    active_status = models.BooleanField()
    class Meta:
        db_table = 'userOpt_ftsi2ips'
        app_label = "userOpt"

class monitor_para(models.Model):
    owner=models.CharField(max_length=50, blank=True,primary_key=True)
    w_FD = models.IntegerField()
    w_FH = models.IntegerField()
    w_EH = models.IntegerField()
    w_CC = models.IntegerField()
    w_FC = models.IntegerField()
    w_ES = models.IntegerField()
    w_RC = models.IntegerField()
    w_DATE = models.IntegerField()
    a_FD = models.IntegerField()
    a_FH = models.IntegerField()
    a_EH = models.IntegerField()
    a_CC = models.IntegerField()
    a_FC = models.IntegerField()
    a_ES = models.IntegerField()
    a_RC = models.IntegerField()
    a_DATE = models.IntegerField()
    p_FD = models.IntegerField()
    p_FH = models.IntegerField()
    p_EH = models.IntegerField()
    p_CC = models.IntegerField()
    p_FC = models.IntegerField()
    p_ES = models.IntegerField()
    p_RC = models.IntegerField()
    p_DATE = models.IntegerField()
    class Meta:
        db_table = 'userOpt_monitor_para'
        app_label = "userOpt"
