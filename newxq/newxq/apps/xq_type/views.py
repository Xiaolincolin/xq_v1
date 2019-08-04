import json
import random

from django.db.models import Sum, Count
from django.shortcuts import render

# Create your views here.
#个人兴趣管理
from django.views.generic import View

from courese.models import LearnWarning, StGgrade
from madmin.models import Assist, AssistTeacher
from reposityory.models import HotJob
from users.models import MyMessage, AssitStudy
from xq_type.models import personal_type, Types, Technologys


class InterestView(View):
    def get(self,request):
        global assist_teacher_info, all_faile_courese, fail_exam_sum
        if request.user.is_authenticated:
            info = MyMessage.objects.get(st_id=request.user)

            #我选择的专业方向
            favor = MyMessage.objects.filter(st_id=request.user).values('favor')
            favor = (favor[0])['favor']
            print(favor)
            #我可能喜欢的所有岗位
            all_interest = personal_type.objects.filter(st_id=request.user).all().order_by('click_times')[0:6]

            #获取外检类型的id
            type_name_id = all_interest.values_list('type_name')
            type_name_id_list = []
            for tp_id in type_name_id:
                type_name_id_list.append(tp_id[0])
            type_name_id_list = list(set(type_name_id_list))
            #通过类型id查找对应的类型
            all_type = []
            for types in type_name_id_list:
                med_list = []
                result = Types.objects.filter(id=types).values_list('type_name')
                tc_List = ''
                try:
                    type_id = Types.objects.filter(type_name=list(result[0])[0]).values('id')
                    tc = Technologys.objects.filter(type_name_id=(type_id[0])['id']).values('name')
                    for i in tc:
                        tc_List += i['name'] + '\t'
                except:
                    tc_List = ''

                try:
                    type_id = Types.objects.filter(type_name=list(result[0])[0]).values('id')
                    tc = HotJob.objects.filter(type_name_id=(type_id[0])['id'])[0]
                    job_List = tc
                except:
                    job_List = ''
                med_list.append(list(result[0])[0])
                med_list.append(tc_List)
                med_list.append(job_List)
                if list(result[0])[0]!=favor:
                    all_type.append(med_list)
            print(all_type)

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

            # 所有挂科科目详情
            all_faile_courese = []
            fail_courese = StGgrade.objects.filter(st_id=request.user, grade__lt=60).values_list('year','semester','title','credit','grade')
            for cor in fail_courese:
                all_faile_courese.append(list(cor))

            # 挂科学分id __gt
            fail_exam = StGgrade.objects.filter(st_id=info, grade__lt=60).aggregate(grade_sum=Sum('credit'))
            fail_exam_sum = fail_exam['grade_sum']

            # #我确定的专业方向
            # ensure_interest = Types.objects.filter(type_name=info.favor).values('technology','recommend_job')
            # if(len(ensure_interest)>0):
            #     technology = (ensure_interest[0])['technology']
            #     recommend_job = (ensure_interest[0])['recommend_job']
            # else:
            #     technology = ''
            #     recommend_job = ''
            my_inst = MyMessage.objects.filter(st_id=request.user).values('favor')
            favor = (my_inst[0])['favor']
            type_id = Types.objects.filter(type_name=favor).values('id')
            try:
                tc = Technologys.objects.filter(type_name_id=(type_id[0])['id']).values('name')
                tc_List = ''
                for i in tc:
                    tc_List += i['name'] + '\t'
            except:
                tc_List=''

            try:
                tc = HotJob.objects.filter(type_name_id=(type_id[0])['id']).values('title')
                job_List = ''
                for i in tc:
                    job_List += i['title'] + '\t'
            except:
                job_List=''

            #统计招聘个数
            jobs = Types.objects.filter(type_name=favor).values('id')
            med_id = (jobs[0])['id']
            count_job = HotJob.objects.filter(type_name_id=med_id).annotate(count_j=Count('title'))
            count_job=len(count_job)
            # 生成随机码
            range_code = random.randint(10000, 99999)
            AssitStudy.objects.filter(number=request.user).update(rangeCode=range_code)

            return render(request, 'stu/inst.html', {
                "all_interest":all_interest,
                'info':info,
                'student_warm_leve': json.dumps(str(student_warm_leve), ensure_ascii=False),
                'assist_teacher_info': json.dumps(assist_teacher_info),
                'all_faile_courese': json.dumps(all_faile_courese),
                'fail_exam_sum': json.dumps(fail_exam_sum),
                'tc_List':tc_List,
                # 'technology':technology,
                # 'recommend_job':recommend_job,
                'all_type':all_type,
                'favor':favor,
                'job_List':job_List,
                'count_job':count_job,
                'range_code':range_code,

            })
        else:
            return render(request, 'others/login.html')