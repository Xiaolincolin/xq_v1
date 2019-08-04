"""
author: Colin
@time: 2018-11-28 19:30
explain:

"""
import xadmin
from madmin.models import GraduateCheck
from .models import  Coursetable,StGgrade,StCredit,MajorSystem,LearnWarning,WarnRule


class MajorSystemXadmin(object):
    list_display = ['college', 'major', 'c_type', 'sum_credit']
    search_fields = ['college', 'major', 'c_type', 'sum_credit']
    list_filter = ['college', 'major', 'c_type', 'sum_credit']
    list_per_page = 20
    model_icon = 'fa fa-lightbulb-o'


class CoursetableXadmin(object):
    list_display = ['college', 'major', 'c_type', 'c_id', 'title','credit', 'period', 'semester']
    search_fields = ['college', 'major', 'c_type', 'c_id', 'title','credit', 'period', 'semester']
    list_filter= ['college', 'major', 'c_type', 'c_id', 'title','credit', 'period', 'semester']
    list_per_page = 20
    model_icon = 'fa fa-table'


class StCreditXadmin(object):
    list_display = ['st_id', 'name', 'accomplish', 'unfinshed', 'c_type']
    search_fields = ['st_id', 'name', 'accomplish', 'unfinshed', 'c_type']
    list_filter = ['st_id', 'name', 'accomplish', 'unfinshed', 'c_type']
    list_per_page = 20
    model_icon = 'fa fa-bars'


class StGgradeXadmin(object):
    list_display = ['st_id', 'title', 'credit', 'grade', 'year', 'semester', 'c_type']
    search_fields = ['st_id', 'title', 'credit', 'grade', 'year', 'semester', 'c_type']
    list_filter = ['st_id', 'title', 'credit', 'grade', 'year', 'semester', 'c_type']
    list_per_page = 20
    model_icon = 'fa fa-folder-open-o'


class LearnWarningXadmin(object):
    list_display = ['name','st_id','college','major','myclass', 'is_send','year','semester', 'level', 'message']
    search_fields = ['name','st_id','college','major','myclass', 'year', 'is_send','level','semester', 'message',]
    list_filter = ['name','st_id','college','major','myclass', 'year', 'is_send','level', 'semester','message']
    list_per_page = 20
    model_icon = 'fa fa-exclamation'


class WarnRuleXadmin(object):
    list_display = ['school_name', 'level', 'sum_credit', 'all_credit', 'truant', 'item']
    search_fields = ['school_name', 'level', 'sum_credit','all_credit', 'truant', 'item']
    list_filter = ['school_name', 'level', 'sum_credit', 'all_credit', 'truant', 'item']
    list_per_page = 20
    model_icon = 'fa fa-exclamation'




xadmin.site.register(MajorSystem,MajorSystemXadmin)
xadmin.site.register(Coursetable,CoursetableXadmin)
xadmin.site.register(StGgrade,StGgradeXadmin)
xadmin.site.register(StCredit,StCreditXadmin)
xadmin.site.register(LearnWarning,LearnWarningXadmin)
xadmin.site.register(WarnRule,WarnRuleXadmin)

