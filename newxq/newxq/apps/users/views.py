import csv
import random
import string

from django.contrib.auth.handlers.modwsgi import check_password
from django.contrib.auth.hashers import make_password
from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q, Sum, F, Count
from django.views.generic import View

from madmin.models import Assist, AssistTeacher
from reposityory.models import HotJob, Artcle, HotProject
from .forms import LoginForm
from .models import MyMessage, AssitStudy
from courese.models import MajorSystem,StGgrade,LearnWarning
from xq_type.models import personal_type, Types, Technologys
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from courese.models import WarnRule
from users.models import UserProfile
import json
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
#配置登录名可以是邮箱
class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


#退出登录
class LogoutView(View):
    """
    用户退出
    """
    def get(self, request):
        logout(request)
        from django.urls import reverse
        return HttpResponseRedirect(reverse("login"))


#登录逻辑
class LoginView(View):
    def get(self,request):
        return render(request, "others/login.html", {})

    def post(self,request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            get_admin = request.POST.get("is_admin", "")

            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                dbadmin = UserProfile.objects.get(username=user_name)
                if get_admin == dbadmin.is_admin and get_admin == "stu":
                    login(request, user)
                    return HttpResponseRedirect('/main/')
                elif get_admin == dbadmin.is_admin and get_admin == "admin":
                    login(request,user)
                    return HttpResponseRedirect('/admindex/')
                else:
                    return render(request, 'others/login.html', {"msg": "用户名或密码错误！"})
            else:
                return render(request, "others/login.html", {"msg": "用户名或密码错误！"})

        else:
            return render(request, "others/login.html", {"login_form": "用户名或密码错误！"})


class MyMessageView(View):
    def get(self,request):
        if request.user.is_authenticated:
            student_number = request.user
            info = MyMessage.objects.get(st_id=request.user)
            #预警等级
            student_warm_leves = LearnWarning.objects.filter(st_id=info.id).order_by('add_time').values('level')
            if(len(student_warm_leves)>0):
                student_warm_leve = str((student_warm_leves[0])['level'])
            else:
                student_warm_leve = ''
            #总学分
            sum =MajorSystem.objects.filter(major=info.major).aggregate(sums=Sum('sum_credit'))
            sum_credit = sum['sums']
            #已修学分
            finished = StGgrade.objects.filter(st_id=info,grade__gte=60).aggregate(finished_credit_sum=Sum('credit'))
            finished_credit = finished['finished_credit_sum']
            if(finished_credit == None):
                finished_credit = 0
            #未修学分
            try:
                not_credit = sum_credit-finished_credit
            except:
                not_credit=0
            #挂科学分id __gt
            fail_exam = StGgrade.objects.filter(st_id=info,grade__lt=60).aggregate(grade_sum=Sum('credit'))
            fail_exam_sum = fail_exam['grade_sum']
            if fail_exam_sum == None:
                fail_exam_sum=0

            #查询的是所有成绩的学期和学分，加annotate以到达分组的目的，不然会有重复的学年出现
            once_year = StGgrade.objects.filter(st_id=info).values('year').annotate(year_Sum=Sum('credit'))
            once_semester = StGgrade.objects.filter(st_id=info).values_list('year','semester').annotate(year_Sum=Sum('credit'))
            # 反向查询，外键不能直接查询，获取个人信息表中学号的id
            #对应的学号
            st_id_info = info.id

            #获取制定的预警消息，并将每一学期，在校期间挂科学分加入列表，之后加入学生挂科的学分排序，获取前一个学分，再对应预警等级
            creadit_rule = WarnRule.objects.values_list('sum_credit','all_credit')
            once_semester_list = []
            all_year = []
            for index in creadit_rule:
                once_semester_list.append(index[0])
                all_year.append(index[1])


            #声明
            save_warm = LearnWarning()


            #(每一学期)首先统计每学期挂科的学分给出预警消息，分别查看每一学年的预警是否存在
            if(len(once_semester)>0):
                for semesters in once_semester:
                    #查看预警消息是否存在
                    has = LearnWarning.objects.filter(st_id_id=st_id_info, year=semesters[0],semester=semesters[1])

                    #查询这一学年是否有挂科
                    creadit_list = StGgrade.objects.filter(st_id=info,year=semesters[0], semester=semesters[1],grade__lt=60).values('year').annotate(sem_Sum=Sum('credit'))

                    #如果有挂科
                    if (len(creadit_list)>0):
                        # 如果不存在则添加一条预警消息
                        if (len(has) == 0):
                            sem_sum_creadit = (creadit_list[0])['sem_Sum']
                            sem_sum = (creadit_list[0])['sem_Sum']+0.0005  #加小数是为了防止数据的临界值
                            once_semester_list.append(sem_sum)
                            once_semester_list.sort()
                            sem_index = once_semester_list.index(sem_sum)
                            #获取到对应预警学分
                            if sem_index != 0:
                                warm_level_creadit = once_semester_list[sem_index-1]
                                #对应的预警等级
                                get_warm_level = WarnRule.objects.get(sum_credit=warm_level_creadit)
                                #将预警消息保存到数据库
                                save_warm.st_id_id=st_id_info
                                save_warm.name = info.name
                                save_warm.level =str(get_warm_level)
                                save_warm.warm_creadit = sem_sum_creadit
                                save_warm.college = info.college
                                save_warm.major = info.major
                                save_warm.myclass = info.myclass
                                save_warm.year = semesters[0]
                                save_warm.semester = semesters[1]
                                save_warm.message = str(semesters[0])+str(semesters[1])+"挂科学分为"+str(sem_sum_creadit)+"达到"+str(get_warm_level)
                                save_warm.save()

                    elif len(creadit_list)==0 and len(has) > 0:
                        #预警消息存在，又没有挂科，说明补考过了，删除预警等级
                        LearnWarning.objects.filter(st_id_id=st_id_info,year=semesters[0],semester=semesters[1]).delete()

            #在校期间是预警消息是否存在
            has_exist = LearnWarning.objects.filter(st_id_id=st_id_info,year='在校期间',warm_creadit = fail_exam_sum).all()

            #(在校期间)挂科总学分
            if(len(fail_exam)>0):
                if len(has_exist)==0:
                    fail_creadit = fail_exam_sum+0.005
                    all_year.append(fail_creadit)
                    all_year.sort()
                    creadit_index = all_year.index(fail_creadit)
                    # 获取到对应预警学分
                    if creadit_index != 0:
                        warm_level_creadit = all_year[creadit_index-1]
                        # 对应的预警等级
                        get_warm_level = WarnRule.objects.filter(all_credit=warm_level_creadit).values('level')
                        get_warm_level_name = (get_warm_level[0])['level']

                        #将数据保存入数据库
                        save_warm.st_id_id = st_id_info
                        save_warm.name = info.name
                        save_warm.level = get_warm_level_name
                        save_warm.warm_creadit = fail_exam_sum
                        save_warm.college = info.college
                        save_warm.major = info.major
                        save_warm.myclass = info.myclass
                        save_warm.year = '在校期间'
                        save_warm.semester = '在校期间'
                        save_warm.message = '在校期间' + "挂科学分为" + str(fail_exam_sum) + "达到" + str(get_warm_level_name)
                        save_warm.save()
            elif len(fail_exam) ==0 and len(has_exist)>0:
                LearnWarning.objects.filter(st_id_id=st_id_info,year='在校期间',warm_creadit = fail_exam_sum ).delete()

            #将预警消息推送到前端页面
            all_warn = LearnWarning.objects.all()

            #学情分析结果
            sum_result = personal_type.objects.filter(st_id=request.user).values('click_times').aggregate(sum=Sum('click_times'))
            max_f = personal_type.objects.all().filter(st_id=request.user)
            try:
                max_list = max_f.order_by('-click_times')[:4].values('click_times')
                max_names = max_f.order_by('-click_times')[:4].values('type_name')
                max_name = []
                for name in max_names:
                    tp_name = Types.objects.filter(id=name['type_name']).values('type_name')
                    max_name.append(tp_name[0])

                list_value = [1,1,1,1]
                list_key = ['暂无','暂无','暂无','暂无']
                if(len(max_list) and len(sum_result) != 0):
                    for r_item in range(4):
                        list_key[r_item] = max_name[r_item]['type_name']
                        list_value[r_item] = (float(max_list[r_item]['click_times'])/float(sum_result['sum']))
                else:
                    list_result=[1,1,1,1]
                for p in range(4):
                    list_value[p] = round(list_value[p] * 100, 2)
            except:
                list_value = [1, 1, 1, 1]
                list_key = ['暂无', '暂无', '暂无', '暂无']

            #所有挂科科目详情
            all_faile_courese = []
            fail_courese = StGgrade.objects.filter(st_id=request.user,grade__lt=60).values_list('year','semester','title','credit','grade')
            for cor in fail_courese:
                all_faile_courese.append(list(cor))

            #帮扶计划
            assist = Assist.objects.filter(st_id=request.user).values('job_number_id')
            #帮扶老师信息
            assist_teacher_info=[]
            if(len(assist)>0):
                assist_teacher = AssistTeacher.objects.filter(id=(assist[0])['job_number_id']).values_list('name','phone','major','assist_address')
                if(len(assist_teacher)>0):
                    assist_teacher_info = list(assist_teacher[0])

            s = string.ascii_letters
            code = random.choice(s)
            AssitStudy.objects.filter(number=request.user).update(rangeCode=code)

            #资讯，招聘推荐
            all_job=[]
            all_artcle=[]
            all_types = []
            # 如果已经确定方向，根据选择的类随机推荐
            sure_interest = MyMessage.objects.filter(st_id=request.user).values('favor')
            #没确定方向
            try:
                if (sure_interest[0])['favor']=='':
                    sure_interest = personal_type.objects.filter(st_id=request.user).values('type_name')
                    #如果没确定方向，也没点击过任何文章
                    if (sure_interest[0])['type_name']=='':
                        all_job = HotJob.objects.all().order_by('click_times')[0:15]
                        all_artcle = Artcle.objects.all().order_by('click_times')[0:15]
                        all_types = Types.objects.all().order_by('click_times')[0:15]
                    #如果点击过，根据点击过得类随机推荐
                    else:

                        type_id = []
                        for i in sure_interest:
                            type_id.append(i['type_name'])
                        range_id = random.choice(type_id)
                        all_job = HotJob.objects.filter(type_name_id=range_id).all().order_by('click_times')[0:15]
                        all_artcle = Artcle.objects.filter(type_name_id=range_id).all().order_by('click_times')[0:15]
                        all_types = Types.objects.all().order_by('click_times')[0:15]

                else:
                    tp_name = Types.objects.filter(type_name=(sure_interest[0])['favor']).values('id')
                    range_id = (tp_name[0])['id']
                    all_job = HotJob.objects.filter(type_name_id=range_id).all().order_by('click_times')[0:15]
                    all_artcle = Artcle.objects.filter(type_name_id=range_id).all().order_by('click_times')[0:15]
                    all_types = Types.objects.all().order_by('click_times')[0:15]
            except:
                all_job = HotJob.objects.all().order_by('click_times')[0:15]
                all_artcle = Artcle.objects.all().order_by('click_times')[0:15]
                all_types = Types.objects.all().order_by('click_times')[0:15]
            key1 = list_key[0]
            key2 = list_key[1]
            key3 = list_key[2]
            key4 = list_key[3]
            #生成随机码
            range_code = random.randint(10000, 99999)
            AssitStudy.objects.filter(number=request.user).update(rangeCode=range_code)

            #涉及技能
            tc_List = ''
            type_id = Types.objects.filter(type_name=info.favor).values('id')
            try:
                tc = Technologys.objects.filter(type_name_id=(type_id[0])['id']).values('name')
                for i in tc:
                    tc_List += i['name'] + '\t'
            except:
                tc_List=''
            #涉及招聘
            try:
                tc = HotJob.objects.filter(type_name_id=(type_id[0])['id'])[0]
                job_List = tc
            except:
                job_List=''



            return render(request, 'stu/main.html',{
                'info':info,
                'sum_credit':json.dumps(sum_credit),
                'finished_credit':json.dumps(finished_credit),
                'not_credit':json.dumps(not_credit),
                'fail_exam_sum':json.dumps(fail_exam_sum),
                'all_warn':all_warn,
                'key1':key1 ,
                'value1':list_value[0],
                'key2': key2,
                'value2': list_value[1],
                'key3': key3,
                'value3': list_value[2],
                'key4': key4,
                'value4': list_value[3],
                'student_number':json.dumps(str(student_number),ensure_ascii=False),
                'student_warm_leve':json.dumps(str(student_warm_leve),ensure_ascii=False),
                'all_faile_courese': json.dumps(all_faile_courese),
                'assist_teacher_info':json.dumps(assist_teacher_info),
                'code':code,
                "all_job": all_job,
                "all_artcle": all_artcle,
                'all_types': all_types,
                'range_code':range_code,
                'tc_List':tc_List,
                'job_List':job_List,
                })
        else:
            return HttpResponseRedirect('/')

#确定方向
class ConfirmInterestView(View):

    def post(self,request):
        if request.user.is_authenticated:
            mychoice = request.POST.get('choice','')
            student_number = request.POST.get('student_number','')
            MyMessage.objects.filter(st_id=student_number).update(favor=mychoice)
            json_data = {'message':'成功'}

            return JsonResponse(json_data)
        else:
            return HttpResponseRedirect('/')


#助学到学情自动登录实现
class AutoLogin(View):

    def get(self,request,id,username,code):
        if code!=0:
            result = AssitStudy.objects.filter(number=username,rangeCode=code)
            if len(result)>0:
                AssitStudy.objects.filter(number=username).update(rangeCode=0)

            id = str(id)
            if len(result)>0:
                pd = AssitStudy.objects.filter(number=username).values('password')
                password = (list(pd)[0])['password']
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request,user)
                    if id==str(1):
                        return HttpResponseRedirect('/main/')
                    elif id==str(2):
                        return HttpResponseRedirect('/stcred/')
                    elif id==str(3):
                        return HttpResponseRedirect('/course/')
                    elif id==str(4):
                        return HttpResponseRedirect('/inst/')
                    else:
                        return HttpResponseRedirect('/')
                else:
                    return HttpResponseRedirect('/')
            else:
                return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/')


#重新确定方向
class ReconfirmIterestView(View):
    def post(self,request):
        if request.user.is_authenticated:
            student_number = request.POST.get('student_number','')
            mychoice = request.POST.get('choice')
            MyMessage.objects.filter(st_id=student_number).update(favor=mychoice)
            json_data = {'message':'成功'}

            return JsonResponse(json_data)
        else:
            return HttpResponseRedirect('/')


#涉及技能
class AboutTc(View):
    def post(self,request):
        if request.user.is_authenticated:
            mychoice = request.POST.get('choice')

            type_id = Types.objects.filter(type_name=mychoice).values('id')
            tc = Technologys.objects.filter(type_name_id=(type_id[0])['id']).values('name')
            tc_List = ''
            for i in tc:
                tc_List+=i['name']+'\t'

            tc = HotJob.objects.filter(type_name_id=(type_id[0])['id']).values('title')
            job_List = ''
            for i in tc:
                job_List += i['title'] + '\t'


            json_data = {'tc':tc_List,'job':job_List}

            return JsonResponse(json_data)
        else:
            return HttpResponseRedirect('/')


def page_not_found(request):
    #全局404
    from django.shortcuts import render_to_response
    response = render_to_response('others/404.html', {})
    response.status_code = 404
    return response


def page_error(request):
    #全局404
    from django.shortcuts import render_to_response
    response = render_to_response('others/500.html', {})
    response.status_code = 500
    return response


def page_reject(request):
    #全局404
    from django.shortcuts import render_to_response
    response = render_to_response('others/403.html', {})
    response.status_code = 403
    return response