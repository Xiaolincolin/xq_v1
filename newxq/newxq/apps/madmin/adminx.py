"""
author: Colin
@time: 2019-04-07 18:57
explain:

"""
import xadmin
from madmin.models import GraduateCheck, StudenCreditManage, Assist, AssistTeacher, AssociateBook, AssociateGrade, \
    BorrowAssociate, Associateaward, Associate_native_place, AssociateGender, AssociateCourseGrade, AssociateCourse, \
    Assiot


class GraduateCheckXadmin(object):
    list_display = ['name', 'st_id', 'major', 'myclass', 'sum_credit', 'finish_credit', 'need_credit','add_time']
    search_fields = ['name', 'st_id', 'major', 'myclass', 'sum_credit', 'finish_credit', 'need_credit']
    list_filter = ['name', 'st_id', 'major', 'myclass', 'sum_credit', 'finish_credit', 'need_credit', 'add_time']
    list_per_page = 20
    model_icon = 'fa fa-exclamation'


class StudenCreditManageXadmin(object):
    list_display = ['name', 'st_id', 'major', 'myclass', 'sum_credit', 'finish_credit', 'need_credit','add_time']
    search_fields = ['name', 'st_id', 'major', 'myclass', 'sum_credit', 'finish_credit', 'need_credit']
    list_filter = ['name', 'st_id', 'major', 'myclass', 'sum_credit', 'finish_credit', 'need_credit', 'add_time']
    list_per_page = 20
    model_icon = 'fa fa-id-card-o'


class AssistXadmin(object):
    list_display = ['name', 'st_id', 'major', 'myclass', 'warm_leve', 'job_number','assist_teacher']
    search_fields = ['name', 'st_id', 'major', 'myclass', 'warm_leve', 'job_number','assist_teacher']
    list_filter = ['name', 'st_id', 'major', 'myclass', 'warm_leve', 'job_number', 'assist_teacher']
    list_per_page = 20
    model_icon = 'fa fa-lightbulb-o'


class AssistTeacherXadmin(object):
    list_display = ['name', 'job_number', 'college', 'major', 'phone', 'assist_address', 'add_time']
    search_fields = ['name', 'job_number', 'college', 'major', 'phone', 'assist_address']
    list_filter = ['name', 'job_number', 'college', 'major', 'phone', 'assist_address', 'add_time']
    list_per_page = 20
    model_icon = 'fa fa-lightbulb-o'


class AssociateBookXadmin(object):
    list_display = ['student_id', 'number']
    search_fields = ['student_id', 'number']
    list_filter = ['student_id', 'number']
    list_per_page = 20
    model_icon = 'fa fa-lightbulb-o'


class AssociateGradeXadmin(object):
    list_display = ['student_id', 'grade']
    search_fields = ['student_id', 'grade']
    list_filter = ['student_id', 'grade']
    list_per_page = 20
    model_icon = 'fa fa-lightbulb-o'


class BorrowAssociateXadmin(object):
    list_display = ['student_id', 'frequency', 'number']
    search_fields = ['student_id', 'frequency', 'number']
    list_filter = ['student_id', 'frequency', 'number']
    list_per_page = 20
    model_icon = 'fa fa-lightbulb-o'


class AssociateawardXadmin(object):
    list_display = ['student_id']
    search_fields = ['student_id']
    list_filter = ['student_id']
    list_per_page = 20
    model_icon = 'fa fa-lightbulb-o'


class Associate_native_placeXadmin(object):
    list_display = ['student_id', 'jiguan']
    search_fields = ['student_id', 'jiguan']
    list_filter = ['student_id', 'jiguan']
    list_per_page = 20
    model_icon = 'fa fa-lightbulb-o'


class AssociateGenderXadmin(object):
    list_display = ['student_id', 'gender','collage']
    search_fields = ['student_id', 'gender','collage']
    list_filter = ['student_id', 'gender','collage']
    list_per_page = 20
    model_icon = 'fa fa-lightbulb-o'


class AssociateCourseGradeXadmin(object):
    list_display = ['student_id', 'course_id','grade']
    search_fields = ['student_id', 'course_id','grade']
    list_filter = ['student_id', 'course_id','grade']
    list_per_page = 20
    model_icon = 'fa fa-lightbulb-o'


class AssociateCourseXadmin(object):
    list_display = ['course_id', 'course_name']
    search_fields = ['course_id', 'course_name']
    list_filter = ['course_id', 'course_name']
    list_per_page = 20
    model_icon = 'fa fa-lightbulb-o'


class AssiotXadmin(object):
    list_display = ['collage', 'gender', 'minzu', 'jiguan', 'major']
    search_fields = ['collage', 'gender', 'minzu', 'jiguan', 'major']
    list_filter = ['collage', 'gender', 'minzu', 'jiguan', 'major']
    list_per_page = 20
    model_icon = 'fa fa-lightbulb-o'


xadmin.site.register(Assiot,AssiotXadmin)
xadmin.site.register(GraduateCheck,GraduateCheckXadmin)
xadmin.site.register(StudenCreditManage,StudenCreditManageXadmin)
xadmin.site.register(Assist,AssistXadmin)
xadmin.site.register(AssistTeacher,AssistTeacherXadmin)
xadmin.site.register(AssociateBook,AssociateBookXadmin)
xadmin.site.register(AssociateGrade,AssociateGradeXadmin)
xadmin.site.register(BorrowAssociate,BorrowAssociateXadmin)
xadmin.site.register(Associateaward,AssociateawardXadmin)
xadmin.site.register(Associate_native_place,Associate_native_placeXadmin)
xadmin.site.register(AssociateGender,AssociateGenderXadmin)
xadmin.site.register(AssociateCourseGrade,AssociateCourseGradeXadmin)
xadmin.site.register(AssociateCourse,AssociateCourseXadmin)