# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class FlightTestLog(models.Model):
    column = ('flight_day', 'msn', 'type', 'location', 'comment', 'squawks',
              'esn1', 'esn1_runtime', 'esn1_cycle', 'esn2', 'esn2_runtime', 'esn2_cycle',
              'summary', 'tr_deployed', 'comac_no', 'flight_hour', 'flight_cycle', 'test_date', 'flight_time')
    flight_day = models.TextField(blank=True, null=True)
    msn = models.TextField(blank=True, null=True)
    type = models.TextField(blank=True, null=True)
    location = models.TextField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    squawks = models.TextField(blank=True, null=True)
    esn1 = models.TextField(blank=True, null=True)
    esn1_runtime = models.TextField(blank=True, null=True)
    esn1_cycle = models.TextField(blank=True, null=True)
    esn2 = models.TextField(blank=True, null=True)
    esn2_runtime = models.TextField(blank=True, null=True)
    esn2_cycle = models.TextField(blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    tr_deployed = models.TextField(blank=True, null=True)
    comac_no = models.TextField(blank=True, null=True)
    flight_hour = models.TextField(blank=True, null=True)
    flight_cycle = models.TextField(blank=True, null=True)
    test_date = models.TextField(blank=True, null=True)
    flight_time = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'flight_test_log'
        app_label = "portalOpt"


class PoTracker(models.Model):
    column = ('index', 'po_field', 'po_version', 'status', 'description', 'part_number',
              'series_number', 'supplier', 'ms_information_gl_date', 'shipment_date', 'awb_no_field',
              'actually_arrived_date',
              'qty_required', 'gap', 'po_release_date', 'remarks', 'cfm_po_field')
    index = models.BigIntegerField(blank=True, null=True)
    po_field = models.FloatField(db_column='PO#', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    po_version = models.FloatField(db_column='PO version', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    status = models.TextField(db_column='Status', blank=True, null=True)  # Field name made lowercase.
    description = models.TextField(db_column='Description', blank=True, null=True)  # Field name made lowercase.
    part_number = models.TextField(db_column='Part number', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    series_number = models.TextField(db_column='Series number', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    supplier = models.TextField(db_column='Supplier', blank=True, null=True)  # Field name made lowercase.
    ms_information_gl_date = models.TextField(db_column='MS Information/GL Date', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    shipment_date = models.TextField(db_column='Shipment Date', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    awb_no_field = models.TextField(db_column='AWB No.', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    actually_arrived_date = models.TextField(db_column='Actually Arrived Date', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    qty_required = models.FloatField(db_column='Qty required', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    qty_received = models.FloatField(db_column='Qty Received', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    gap = models.FloatField(db_column='Gap', blank=True, null=True)  # Field name made lowercase.
    po_release_date = models.TextField(db_column='PO Release Date', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    remarks = models.TextField(db_column='Remarks', blank=True, null=True)  # Field name made lowercase.
    cfm_po_field = models.TextField(db_column='CFM PO#', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.

    class Meta:
        managed = True
        db_table = 'po_tracker'
        app_label = "portalOpt"


class ScDailyMiReport(models.Model):
    column = ('complete_date', 'activity_date', 'logged_date', 'ac_msn', 'mi_job_no', 'task_interval')
    complete_date = models.TextField(blank=True, null=True)
    activity_date = models.TextField(blank=True, null=True)
    logged_date = models.TextField(blank=True, null=True)
    ac_msn = models.TextField(blank=True, null=True)
    mi_job_no = models.TextField(blank=True, null=True)
    task_interval = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'sc_daily_mi_report'
        app_label = "portalOpt"


class ScFtsiTracking(models.Model):
    column = ('logged_date','ftsi_no', 'revision','ftsi_title', 'impact_ips','compliance', 'issue_date','entry_no')
    id = models.IntegerField(primary_key=True)
    logged_date = models.TextField(blank=True, null=True)
    ftsi_no = models.TextField(blank=True, null=True)
    revision = models.TextField(blank=True, null=True)
    ftsi_title = models.TextField(blank=True, null=True)
    impact_ips = models.TextField(blank=True, null=True)
    compliance = models.TextField(blank=True, null=True)
    issue_date = models.TextField(blank=True, null=True)
    entry_no = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'sc_ftsi_tracking'
        app_label = "portalOpt"


class ScIpsInformationOnly(models.Model):
    column = ('activity_date', 'logged_date', 'ac_msn', 'ac_position', 'identification', 'document_type',
              'document_no', 'document_revision')
    activity_date = models.TextField(blank=True, null=True)
    logged_date = models.TextField(blank=True, null=True)
    ac_msn = models.TextField(blank=True, null=True)
    ac_position = models.TextField(blank=True, null=True)
    identification = models.TextField(blank=True, null=True)
    document_type = models.TextField(blank=True, null=True)
    document_no = models.TextField(blank=True, null=True)
    document_revision = models.TextField(blank=True, null=True)
    id = models.IntegerField(primary_key=True)

    class Meta:
        managed = True
        db_table = 'sc_ips_information_only'
        app_label = "portalOpt"


class ToscTrackingEngine(models.Model):
    column = ('esn', 'flight_time', 'flight_cycle', 'flight_day', 'c1_cycle', 'run_time', 'starts', 'failed_starts',
              'inflight_c1_cycle', 'inflight_run_time', 'last_msn', 'last_position', 'last_test_type',
              'current_installation',
              'reverse_cycle', 'last_msn_time', 'last_msn_cycle', 'last_msn_day')
    esn = models.TextField(blank=True, null=True)
    flight_time = models.FloatField(blank=True, null=True)
    flight_cycle = models.FloatField(blank=True, null=True)
    flight_day = models.BigIntegerField(blank=True, null=True)
    c1_cycle = models.BigIntegerField(blank=True, null=True)
    run_time = models.FloatField(blank=True, null=True)
    starts = models.FloatField(blank=True, null=True)
    failed_starts = models.FloatField(blank=True, null=True)
    inflight_c1_cycle = models.BigIntegerField(blank=True, null=True)
    inflight_run_time = models.FloatField(blank=True, null=True)
    last_msn = models.TextField(blank=True, null=True)
    last_position = models.TextField(blank=True, null=True)
    last_test_type = models.TextField(blank=True, null=True)
    current_installation = models.TextField(blank=True, null=True)
    reverse_cycle = models.TextField(blank=True, null=True)
    last_msn_time = models.TextField(blank=True, null=True)
    last_msn_cycle = models.TextField(blank=True, null=True)
    last_msn_day = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tosc_tracking_engine'
        app_label = "portalOpt"
