import json
import random

from django.db.models import Sum
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render

from madmin.models import Assist, AssistTeacher
from users.models import MyMessage, AssitStudy
from .models import Coursetable, LearnWarning, MajorSystem, StCredit
from django.views.generic import View
from .models import StGgrade


# Create your views here.
class CoursetableView(View):

    def get(self, request):
        if request.user.is_authenticated:
            info = MyMessage.objects.get(st_id=request.user)
            mycourse = Coursetable.objects.all()
            fail_courese = StGgrade.objects.filter(st_id=request.user,grade__lt=60).all()
            complet_course = StGgrade.objects.filter(st_id=request.user,grade__gte=60).all()

            # 预警等级
            student_warm_leves = LearnWarning.objects.filter(st_id=info.id).order_by('add_time').values('level')
            if (len(student_warm_leves) > 0):
                student_warm_leve = str((student_warm_leves[0])['level'])
            else:
                student_warm_leve = '正常'

            # 帮扶计划
            assist = Assist.objects.filter(st_id=request.user).values('job_number_id')
            # 帮扶老师信息
            assist_teacher_info = []
            if (len(assist) > 0):
                assist_teacher = AssistTeacher.objects.filter(id=(assist[0])['job_number_id']).values_list('name','phone','major','assist_address')
                if (len(assist_teacher) > 0):
                    assist_teacher_info = list(assist_teacher[0])

            # 帮扶计划
            assist = Assist.objects.filter(st_id=request.user).values('job_number_id')
            # 帮扶老师信息
            assist_teacher_info = []
            if (len(assist) > 0):
                assist_teacher = AssistTeacher.objects.filter(id=(assist[0])['job_number_id']).values_list(
                    'name', 'phone', 'major', 'assist_address')
                if (len(assist_teacher) > 0):
                    assist_teacher_info = list(assist_teacher[0])
            # 挂科学分id __gt
            fail_exam = StGgrade.objects.filter(st_id=info, grade__lt=60).aggregate(grade_sum=Sum('credit'))
            fail_exam_sum = fail_exam['grade_sum']

            # 生成随机码
            range_code = random.randint(10000, 99999)
            AssitStudy.objects.filter(number=request.user).update(rangeCode=range_code)

            return render(request, 'stu/stu_course.html', {
                'mycourse':mycourse,
                'info':info,
                'fail_course':fail_courese,
                'complet_course':complet_course,
                'student_warm_leve': json.dumps(str(student_warm_leve), ensure_ascii=False),
                'assist_teacher_info': json.dumps(assist_teacher_info),
                'fail_exam_sum': json.dumps(fail_exam_sum),
                'fail_courese':fail_courese,
                'range_code':range_code,

            })
        else:
            return HttpResponseRedirect('/')


class CourseAjaxView(View):

    def post(self,request):
        global datas
        if request.user.is_authenticated:
            req_type = request.POST.get('req_type','')
            #个人信息
            info = MyMessage.objects.get(st_id=request.user)
            # 专业培养方案
            all_creadit = MajorSystem.objects.filter(major=info.major).all()
            #返回数据声明
            datas = {}

            course_info = {}
            if req_type=='fail':
                fail_courese = StGgrade.objects.filter(st_id=request.user, grade__lt=60).values_list('year','semester','title','credit','grade')
                i=1
                for cor in fail_courese:
                    course_info[str(i)]=','.join([str(x) for x in list(cor)])
                    i+=1
                datas = json.dumps(course_info,ensure_ascii=False)

            elif req_type=='final':
                complet_course = StGgrade.objects.filter(st_id=request.user, grade__gte=60).values_list('year','semester','title','credit','grade')
                i = 1
                for cor in complet_course:
                    course_info[str(i)] = ','.join([str(x) for x in list(cor)])
                    i+=1
                datas = json.dumps(course_info, ensure_ascii=False)
            elif req_type=='all':
                #培养方案要求
                all_creadit_grade = []

                # 个人学分情况
                mycreadit_name = []
                mycreadit_grade = []

                #培养方案统计
                for name in all_creadit:
                    all_creadit_grade.append(name.sum_credit)

                #个人学分统计
                for name in all_creadit:
                    mycreadit_name.append(str(name))
                    mygrade = StGgrade.objects.filter(st_id=request.user, c_type=name, grade__gte=60).aggregate(sums=Sum('credit'))
                    mycreadit_grade.append(mygrade['sums'])

                #浮点型转字符型
                back_all = []
                back_person = []
                for i in all_creadit_grade:
                    back_all.append(str(i))

                for j in mycreadit_grade:
                    back_person.append(str(j))

                datas = {'name':','.join(mycreadit_name),'all':','.join(back_all),'my':','.join(back_person)}
            elif req_type=='req_credit':
                datas={}

            return JsonResponse(datas,safe=False)
        else:
            return HttpResponseRedirect('/')


class StudentCreaditView(View):
    def get(self,request):
        if request.user.is_authenticated:
            info = MyMessage.objects.get(st_id=request.user)

            #所有个人成绩
            all_grade = StGgrade.objects.filter(st_id=request.user).all()

            #专业培养方案
            all_creadit = MajorSystem.objects.filter(major=info.major).all()

            #个人学分情况
            mycreadit_name = []
            mycreadit_grade = []

            for name in all_creadit:
                mycreadit_name.append(name)
                mygrade = StGgrade.objects.filter(st_id=request.user,c_type=name,grade__gte=60).aggregate(sums=Sum('credit'))
                if mygrade['sums']:
                    mycreadit_grade.append(mygrade['sums'])
                else:
                    mycreadit_grade.append(0)

            #总学分
            sum_creadits = MajorSystem.objects.filter(major=info.major).aggregate(sums=Sum('sum_credit'))
            sum_creadit = sum_creadits['sums']

            # 已修学分
            finished = StGgrade.objects.filter(st_id=info, grade__gte=60).aggregate(finished_credit_sum=Sum('credit'))
            finished_credit = finished['finished_credit_sum']
            if (finished_credit == None):
                finished_credit = 0

            # 未修学分
            try:
                not_credit = sum_creadit - finished_credit
            except:
                not_credit = 0

            # 预警等级
            student_warm_leves = LearnWarning.objects.filter(st_id=info.id).order_by('add_time').values('level')
            if (len(student_warm_leves) > 0):
                student_warm_leve = str((student_warm_leves[0])['level'])
            else:
                student_warm_leve = ''
            # 帮扶计划
            assist = Assist.objects.filter(st_id=request.user).values('job_number_id')
            # 帮扶老师信息
            assist_teacher_info = []
            if (len(assist) > 0):
                assist_teacher = AssistTeacher.objects.filter(id=(assist[0])['job_number_id']).values_list(
                    'name', 'phone', 'major', 'assist_address')
                if (len(assist_teacher) > 0):
                    assist_teacher_info = list(assist_teacher[0])

            # 所有挂科科目详情
            all_faile_courese = []
            fail_courese = StGgrade.objects.filter(st_id=request.user, grade__lt=60).values_list('year','semester','title','credit','grade')
            for cor in fail_courese:
                all_faile_courese.append(list(cor))

            # 挂科学分id __gt
            fail_exam = StGgrade.objects.filter(st_id=info, grade__lt=60).aggregate(grade_sum=Sum('credit'))
            fail_exam_sum = fail_exam['grade_sum']
            if fail_exam_sum == None:
                fail_exam_sum = 0

            # 生成随机码
            range_code = random.randint(10000, 99999)
            AssitStudy.objects.filter(number=request.user).update(rangeCode=range_code)

            return render(request, 'stu/xuefen.html', {
                'info':info,
                'student_warm_leve':json.dumps(str(student_warm_leve),ensure_ascii=False),
                'all_creadit':all_creadit,
                'sum_creadit':sum_creadit,
                'finished_credit':finished_credit,
                'not_credit':not_credit,
                'assist_teacher_info': json.dumps(assist_teacher_info),
                'all_grade':all_grade,
                'mycreadit_name':mycreadit_name,
                'mycreadit_grade':mycreadit_grade,
                'all_faile_courese': json.dumps(all_faile_courese),
                'fail_exam_sum': json.dumps(fail_exam_sum),
                'range_code':range_code,
                })
        else:
            return HttpResponseRedirect('/')


class WarmMessageView(View):
    def get(self,request):

        return render(request, 'stu/warmmessage.html')


