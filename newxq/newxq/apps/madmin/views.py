import json
import random
import time
import operator
from django.contrib.auth.hashers import make_password
from django.db.models import Count, Sum
from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from courese.models import LearnWarning, StGgrade, MajorSystem
from madmin.models import GraduateCheck, Assiot, AssociateGrade, AssociateBook, Associateaward, Associate_native_place, \
    AssociateGender, AssociateCourseGrade, AssociateCourse, AssistTeacher, Assist
from madmin.sendmsg import tpl_send_sms
from xq_type.models import personal_type, Types
from users.models import UserProfile, MyMessage, AssitStudy
from django.db.models import Q
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from collections import Counter
import math
from collections import defaultdict, OrderedDict     # OrderedDict,实现了对字典对象中元素的排序
from itertools import combinations
# Create your views here.


#主页
class IndexView(View):
    def get(self,request):
        global dict_study_love
        if request.user.is_authenticated:
            # 获取学院名字
            sd = SendWarmMessage()
            sd.snedwarmmessage()

            user_name = request.user
            colleage_dict = UserProfile.objects.filter(username=user_name).values('colleage')
            if (len(colleage_dict) > 0):
                colleage = (colleage_dict[0])['colleage']
                # 获取整个学院的预警消息
                all_infos = LearnWarning.objects.filter(college=colleage).values_list('level').annotate(Count('level'))
                dict_warm = dict(all_infos)

                # 获取学院的学情分析
                study_love = MyMessage.objects.filter(~Q(favor=''),~Q(favor=None),college="计算机科学与工程学院").values_list('favor').annotate(
                    Count('favor'))[0:5]
                type_name = []
                count_type = []
                if len(study_love)>0:
                    for type_id in study_love:
                        count_type.append(type_id[1])
                        type_name.append(type_id[0])
                        dict_study_love = dict(zip(type_name, count_type))
                return render(request, 'adm/admin_index.html', {
                    'colleage': json.dumps(colleage),
                    'dict_warm': json.dumps(dict_warm),
                    'dict_study_love': json.dumps(dict_study_love),
                })
        else:
            return HttpResponseRedirect('/')


 #主页的图表，ajax异步加载
class MadminView(View):

    def post(self,request):
        if request.user.is_authenticated:
            strId = request.POST.get("choice", '')
            option = request.POST.get("options",'')
            jsondata = {}
            #学情预警
            if option=="option3":
                if strId=="major":

                    #专业统计
                    all_major_warm = LearnWarning.objects.filter(college="计算机科学与工程学院").values_list('major').annotate(Count('level'))[:5]
                    jsondata=dict(all_major_warm)
                elif strId=="colleage":
                    #学院
                    all_infos = LearnWarning.objects.filter(college="计算机科学与工程学院").values_list('level').annotate(Count('level'))[:5]

                    jsondata = dict(all_infos)

            #学情分析
            elif option=="option2":
                if strId == "major":
                    # 专业
                    major_list = []
                    count_list = []
                    all_major= personal_type.objects.filter(college="计算机科学与工程学院").values('major').distinct()[:5]
                    for major in all_major:
                        major_list.append(major['major'])
                        temp_count_result = personal_type.objects.filter(college="计算机科学与工程学院",major=major['major']).values_list('type_name').annotate(Count('type_name'))[:5]
                        count_list.append(dict(temp_count_result))
                    all_major_info = dict(zip(major_list,count_list))
                    jsondata = dict(all_major_info)

                elif  strId == "colleage":
                    study_love = personal_type.objects.filter(college="计算机科学与工程学院").values_list('type_name').annotate(Count('type_name'))[0:5]
                    type_name = []
                    count_type = []
                    for type_id in study_love:
                        count_type.append(type_id[1])
                        name = Types.objects.filter(id=type_id[0]).values('type_name')
                        type_name.append((name[0])['type_name'])
                    jsondata = dict(zip(type_name,count_type))

            return JsonResponse(jsondata)
        else:
            return HttpResponseRedirect('/')


#查看预警消息
class Admin_warmView(View):

    def get(selfs,request):
        if request.user.is_authenticated:
            admin_name = request.user
            colleage = UserProfile.objects.filter(username=admin_name).values('colleage')
            try:
                all_warm_data = LearnWarning.objects.filter(college=(colleage[0])['colleage']).all()
            except:
                all_warm_data=''



            return  render(request, 'adm/warm.html', {
                'all_warm_data':all_warm_data,
            })
        else:
            return HttpResponseRedirect('/')


#学生成绩详情页面
class Studenty_detailView(View):
    def get(self,request,st_id):
        if request.user.is_authenticated:
            admin_info = request.user
            study_info = MyMessage.objects.get(st_id=st_id)
            study_grade = StGgrade.objects.filter(st_id=st_id,grade__lt=60).all()

            return render(request, 'adm/warm_detail.html', {
                'admin_info':admin_info,
                'study_info':study_info,
                'study_grade':study_grade,
            })
        else:
            return HttpResponseRedirect('/')


#所有学分的专业方向
class Stududent_likeView(View):

    def get(self,request):
        if request.user.is_authenticated:
            colleage = UserProfile.objects.filter(username=request.user).values('colleage')
            std_likes = MyMessage.objects.filter(~Q(favor=''),~Q(favor=None),college=(colleage[0])['colleage']).all()

            # 获取学院的学情分析
            study_love = MyMessage.objects.filter(~Q(favor=''),~Q(favor=None), college="计算机科学与工程学院").values_list('favor').annotate(
                Count('favor'))[0:5]

            study_love_count = dict(study_love)

            #分页
            try:
                page = request.GET.get('page', 1)
            except PageNotAnInteger:
                page = 1
            p = Paginator(std_likes, 15, request=request)

            std_like = p.page(page)

            return render(request, 'adm/admin_interest.html', {
                'std_like':std_like,
                'study_love_count':study_love_count,
            })
        else:
            return HttpResponseRedirect('/')


#毕业审核页面
class CheckGraduateView(View):

    def get(self,request):
        if request.user.is_authenticated:
            # 更新年级
            now_time =time.strftime('%Y',time.localtime(time.time()))
            now_month = time.strftime('%m',time.localtime(time.time()))
            if eval(now_month[0])==0:
                month = eval(now_month[1])
            else:
                month = eval(now_month)
            all_st = MyMessage.objects.all()
            for st in all_st:
                st_year = str(st)[:4]
                grade = eval(now_time)-eval(st_year)
                #大一
                if grade==0:
                    MyMessage.objects.filter(st_id=st).update(grade='大一')
                #大二
                if grade==1 and month > 8:
                    MyMessage.objects.filter(st_id=st).update(grade='大二')
                else:
                    MyMessage.objects.filter(st_id=st).update(grade='大一')

                #大三
                if grade == 2 and month > 8:
                    MyMessage.objects.filter(st_id=st).update(grade='大三')
                else:
                    MyMessage.objects.filter(st_id=st).update(grade='大二')

                # 大四
                if grade == 3 and month > 8:
                    MyMessage.objects.filter(st_id=st).update(grade='大四')
                else:
                    MyMessage.objects.filter(st_id=st).update(grade='大三')

                # 大四
                if grade >= 4:
                    MyMessage.objects.filter(st_id=st).update(grade='大四')


            # 求已修总学分
            graudatecheck = GraduateCheck()
            graduate = MyMessage.objects.filter(grade='大四').all()
            for gradt in graduate:
                has = GraduateCheck.objects.filter(st_id=gradt).values('st_id')
                if len(has)<1:
                    st_major = MyMessage.objects.filter(st_id=gradt).get()
                    sum_require=(MajorSystem.objects.filter(major=st_major.major).aggregate(sums=Sum('sum_credit')))['sums']
                    sum_creadit=(StGgrade.objects.filter(st_id=st_major,grade__gte=60).aggregate(sums=Sum('credit')))['sums']
                    graudatecheck.name=st_major.name
                    graudatecheck.st_id = st_major.st_id
                    graudatecheck.major = st_major.major
                    graudatecheck.myclass = st_major.myclass
                    graudatecheck.sum_credit = sum_require
                    graudatecheck.finish_credit = sum_creadit
                    graudatecheck.need_credit = eval(str(sum_require))-eval(str(sum_creadit))
                    graudatecheck.save()

            #将毕业生信息展示也前端页面
            graudateck = GraduateCheck.objects.all()
            return render(request,'management.html',{
                'graudateck':graudateck,
            })
        else:
            return HttpResponseRedirect('/')


#毕业审核详情页面
class GraduateDetailView(View):

    def get(self,request,st_id):
        if request.user.is_authenticated:
            info = MyMessage.objects.get(st_id=st_id)
            # 所有个人成绩
            all_grade = StGgrade.objects.filter(st_id=info.st_id).all()

            # 专业培养方案所有
            all_creadit = MajorSystem.objects.filter(major=info.major).all()

            # 个人学分情况
            mycreadit_name = []
            mycreadit_grade = []

            for name in all_creadit:
                mycreadit_name.append(name)
                mygrade = StGgrade.objects.filter(st_id=info.st_id, c_type=name,grade__gte=60).aggregate(sums=Sum('credit'))
                if mygrade['sums']:
                    mycreadit_grade.append(mygrade['sums'])
                else:
                    mycreadit_grade.append(0)

            # 个人培养方案总学分
            sum_creadits = MajorSystem.objects.filter(major=info.major).aggregate(sums=Sum('sum_credit'))
            sum_creadit = sum_creadits['sums']

            # 已修学分
            finished = StGgrade.objects.filter(st_id=st_id, grade__gte=60).aggregate(finished_credit_sum=Sum('credit'))
            finished_credit = finished['finished_credit_sum']
            if (finished_credit == None):
                finished_credit = 0

            # 未修学分
            try:
                not_credit = sum_creadit - finished_credit
            except:
                not_credit = 0

            return render(request, 'adm/graduatecheck.html', {
                'info': info,
                'all_creadit': all_creadit,
                'sum_creadit': sum_creadit,
                'finished_credit': finished_credit,
                'not_credit': not_credit,
                'all_grade': all_grade,
                'mycreadit_name': mycreadit_name,
                'mycreadit_grade': mycreadit_grade,
            })
        else:
            return HttpResponseRedirect('/')


#预警点击图表加载
class WarmClickView(View):
    def get(self,request,id,parm):
        #0代表专业，1代表预警等级
        if id=="0":
            warm_count =  LearnWarning.objects.filter(major=parm).all()

            return render(request, 'adm/warm_table.html', {
                'warm_count':warm_count,
            })

        if id =="1":
            warm_count = LearnWarning.objects.filter(level=parm).all()
            return render(request, 'adm/warm_table.html', {
                'warm_count':warm_count,
            })

        return render(request, 'adm/warm_detail.html')


#学情点击图表加载
class XqClickView(View):

    def get(self,request,strId):
        if request.user.is_authenticated:
            interest_count = MyMessage.objects.filter(favor=strId).values_list('name','st_id','major','myclass')
            stu_count = []
            if len(interest_count) > 0:
                for stu in interest_count:
                    stu_one = list(stu)
                    stu_one.append(strId)
                    stu_count.append(stu_one)

            return render(request, 'adm/xq.html', {
                'strId':strId,
                'stu_count':stu_count,
            })
        else:
            return HttpResponseRedirect('/')


#学分管理
class CreditView(View):

    def get(self,request):
        if request.user.is_authenticated:
            # 专业培养方案
            major = '计算机科学与技术'
            all_creadit = MajorSystem.objects.filter(major=major).all()

            #培养方案总学分
            sum_creadits = MajorSystem.objects.filter(major=major).aggregate(sums=Sum('sum_credit'))
            sum_creadit = sum_creadits['sums']

            #指定专业的所有学生的学分情况
            all_student = MyMessage.objects.filter(major=major).values_list('name','st_id','major','myclass')
            student_info = []
            student_id = []
            if len(all_student)>0:
                for st in all_student:
                    student_once = list(st)
                    st_id = st[1]
                    student_id.append(st_id)

                    # 已修学分
                    finished = StGgrade.objects.filter(st_id=st_id, grade__gte=60).aggregate(finished_credit_sum=Sum('credit'))
                    finished_credit = finished['finished_credit_sum']
                    if (finished_credit == None):
                        finished_credit = 0

                    # 未修学分
                    try:
                        not_credit = sum_creadit - finished_credit
                    except:
                        not_credit = 0
                    student_once.append(sum_creadit)
                    student_once.append(finished_credit)
                    student_once.append(not_credit)
                    student_info.append(student_once)


            return render(request, 'adm/admin_credit.html', {
                'major':major,
                'sum_creadit':sum_creadit,
                'all_creadit':all_creadit,
                'student_info':student_info,
                'student_id':student_id,
            })
        else:
            return HttpResponseRedirect('/')


#学分管理详情页
class CreditdetailView(View):
    def get(self,request,st_id):
        if request.user.is_authenticated:
            info = MyMessage.objects.get(st_id=st_id)
            #所有个人成绩
            all_grade = StGgrade.objects.filter(st_id=st_id).all()

            #专业培养方案
            all_creadit = MajorSystem.objects.filter(major=info.major).all()

            #个人学分情况
            mycreadit_name = []
            mycreadit_grade = []

            for name in all_creadit:
                mycreadit_name.append(name)
                mygrade = StGgrade.objects.filter(st_id=st_id,c_type=name,grade__gte=60).aggregate(sums=Sum('credit'))
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

            return render(request, 'adm/admin_credit_detail.html', {
                'info':info,
                'all_creadit':all_creadit,
                'sum_creadit':sum_creadit,
                'finished_credit':finished_credit,
                'not_credit':not_credit,
                'all_grade':all_grade,
                'mycreadit_name':mycreadit_name,
                'mycreadit_grade':mycreadit_grade,
                })
        else:
            return HttpResponseRedirect('/')


#帮扶计划
class AssistView(View):
    def get(self,request):
        if request.user.is_authenticated:
            all_student = LearnWarning.objects.all()
            all_teacher = AssistTeacher.objects.all()

            return render(request, 'adm/assist.html', {
                'all_student':all_student,
                'all_teacher':all_teacher,

            })
        else:
            return HttpResponseRedirect('/')


#帮扶计划ajxa修改帮扶老师
class AddAssittch(View):
    def post(self,request):
        if request.user.is_authenticated:
            option = request.POST.get("option", '')

            if option=='0':
                strId = request.POST.get("st_id", '')
                teacher = request.POST.get("teacher", '')
                teacher = teacher.strip()
                st_id = MyMessage.objects.filter(st_id=strId).values('id')
                LearnWarning.objects.filter(st_id_id=(st_id[0])['id']).update(assit_teacher=teacher)
                job_id = AssistTeacher.objects.filter(name=teacher).get()
                Assist.objects.filter(st_id=strId).update(job_number=job_id)
                return JsonResponse({})
            elif option=='1':
                strId = request.POST.get("st_id", '')
                st_id = MyMessage.objects.filter(st_id=strId).values('id')
                LearnWarning.objects.filter(st_id_id=(st_id[0])['id']).update(assit_teacher='')
                Assist.objects.filter(st_id=strId).update(job_number='')
                return JsonResponse({})
            else:
                return HttpResponseRedirect('/')

        else:
            return HttpResponseRedirect('/')


#关联分析
class AssociationView():
    def get(self, request):
        if request.user.is_authenticated:

            return render(request, 'adm/assist.html', {

            })



        else:
            return HttpResponseRedirect('/')


#添加用户
class AdduserView(View):
    def get(self, request):
        if request.user.is_authenticated:

            return render(request, 'adm/adduser.html', {

            })
        else:
            return HttpResponseRedirect('/')


#上传文件
class AdduserdetailView(View):
    def post(self, request):
        if request.user.is_authenticated:
            msg = MyMessage()
            if request.method == "POST":
                    f = request.FILES.get("myfile", None)
                    querysetlist = []
                    for lines in f.readlines():
                        datas = (lines.decode('utf8'))
                        line = datas.split(',')
                        if len(line) > 0:
                            try:
                                st_id = line[0]
                                name = line[1]
                                college = line[10]
                                major = line[11]
                                gender = line[3]
                                is_indata = MyMessage.objects.filter(st_id=st_id).values('st_id')
                                if len(is_indata) == 0:
                                    if college == '计算机科学与工程学院':
                                        querysetlist.append(MyMessage(
                                            st_id = st_id,
                                            name = name,
                                            college = college,
                                            major = major,
                                            gender = gender,
                                            image = ''
                                                      ))
                            except Exception as e:
                                print(e)
                    MyMessage.objects.bulk_create(querysetlist)
                    self.add_user()

            return render(request, 'adm/adduser.html', {

            })

        else:
            return HttpResponseRedirect('/')

    def add_user(self):
        all_user = MyMessage.objects.all()
        querysetlist = []
        for info in all_user:
            user = info.st_id
            passwd = 'a'+str(user)
            password = make_password(passwd)
            is_admin = 'stu'
            is_have = UserProfile.objects.filter(username=user).values('username')
            if len(is_have)==0:
                querysetlist.append(UserProfile(
                    username=user,
                    password = password,
                    is_admin = is_admin,
                ))
        UserProfile.objects.bulk_create(querysetlist)


#发送预警消息
class SendWarmMessage(View):
    def snedwarmmessage(self):
        phone = []
        is_send = LearnWarning.objects.filter(is_send=0).values_list('st_id_id','level','name')
        st_id_id = []
        name = []
        level = []
        updata_st_id = []
        if len(is_send)>0:
            for st in is_send:
                st_id_index = st[0]
                if st_id_index not in st_id_id:
                    st_id_id.append(st_id_index)
                    mobile = MyMessage.objects.filter(~Q(phone_num=None), id=st_id_index).values('phone_num')
                    if len(mobile)>0:
                        phone.append((mobile[0])['phone_num'])
                        updata_st_id.append(st_id_index)
                        level.append(st[1])
                        name.append(st[2])

        tpl_value = {}
        if len(name)>0:
            for index,stname in enumerate(name):
                tpl_value['#stname#']=stname
                tpl_value['#level#'] = level[index]
                mobile_p = phone[index]
                msg = tpl_send_sms(tpl_value,mobile_p)
                msg = eval(msg)
                code = msg['code']
                # 获取code,如果为0成功，修改数据库信息标注成功
                if code==0:
                    LearnWarning.objects.filter(st_id_id=updata_st_id[index]).update(is_send=1)


#统计分析学校
class StatisticalView(View):
    def get(self,request):
        if request.user.is_authenticated:
            collage = []
            gender = []
            nation = []
            native_place = []
            major = []
            datas = Assiot.objects.values_list('id','collage','gender','minzu','jiguan','major')
            for line in datas:
                collage.append(line[1])
                gender.append(line[2])
                nation.append(line[3])
                native_place.append(line[4])
                major.append(line[5])

            #统计
            collage = Counter(collage)
            gender = Counter(gender)
            nation = Counter(nation)
            native_place = Counter(native_place)
            major = Counter(major)

            # 统计表
            collage_table = ['学校', '北方民族大学']
            nation_table = len(nation)
            native_place_table = len(native_place)
            major_table = len(major)
            gender_count_conn = []
            for dt in gender:
                gender_table =gender[dt]
                gender_count_conn.append(str(gender_table))
            gender_table = '/'.join(gender_count_conn)
            collage_count = list(collage)

            #排序
            collage =sorted(collage.items(), key=operator.itemgetter(1), reverse=True)
            gender = sorted(gender.items(), key=operator.itemgetter(1), reverse=True)
            nation = sorted(nation.items(), key=operator.itemgetter(1), reverse=True)
            native_place = sorted(native_place.items(), key=operator.itemgetter(1), reverse=True)
            major = sorted(major.items(), key=operator.itemgetter(1), reverse=True)

            #取前10个
            gender = dict(gender[0:10])
            nation = dict(nation[0:10])
            native_place = dict(native_place[0:10])
            major = dict(major[0:10])

            return render(request, 'adm/statistical.html', {
                'gender':json.dumps(gender),
                'nation':json.dumps(nation),
                'native_place':json.dumps(native_place),
                'major':json.dumps(major),

                'collage_count': collage_count,
                'collage_table':collage_table,
                'nation_table':nation_table,
                'native_place_table':native_place_table,
                'major_table':major_table,
                'gender_table':gender_table
            })
        else:
            return HttpResponseRedirect('/')


#统计分析专业
class StacollageView(View):
    def post(self,request):
        collage_get = request.POST.get('collage','')
        collage_get = str(collage_get).strip()
        data = {}
        collage = []
        gender = []
        nation = []
        native_place = []
        major = []
        datas = Assiot.objects.values_list('id', 'collage', 'gender', 'minzu', 'jiguan', 'major')
        for line in datas:
            if line[1]==collage_get:
                collage.append(line[1])
                gender.append(line[2])
                nation.append(line[3])
                native_place.append(line[4])
                major.append(line[5])

        # 统计
        collage = Counter(collage)
        gender = Counter(gender)
        nation = Counter(nation)
        native_place = Counter(native_place)
        major = Counter(major)

        # 统计表
        collage_table = ['学院']
        collage_table.append(collage_get)
        nation_table = len(nation)
        native_place_table = len(native_place)
        major_table = len(major)
        gender_count_conn = []
        for dt in gender:
            gender_table = gender[dt]
            gender_count_conn.append(str(gender_table))
        gender_table = '/'.join(gender_count_conn)

        # 排序
        collage = sorted(collage.items(), key=operator.itemgetter(1), reverse=True)
        gender = sorted(gender.items(), key=operator.itemgetter(1), reverse=True)
        nation = sorted(nation.items(), key=operator.itemgetter(1), reverse=True)
        native_place = sorted(native_place.items(), key=operator.itemgetter(1), reverse=True)
        major = sorted(major.items(), key=operator.itemgetter(1), reverse=True)

        # 取前10个
        gender = dict(gender[0:10])
        nation = dict(nation[0:10])
        native_place = dict(native_place[0:10])
        major = dict(major[0:10])


        #压缩成字典
        data['gender'] = gender
        data['nation'] = nation
        data['native_place'] = native_place
        data['major'] = major

        data['collage_table'] = collage_table
        data['nation_table'] = nation_table
        data['native_place_table'] = native_place_table
        data['major_table'] = major_table
        data['gender_table'] = gender_table

        return JsonResponse(data)


#关联分析
class AssociateView(View):
    def get(self,request):

        file = AssociateGrade.objects.values_list('id','student_id','grade')
        borrow = AssociateBook.objects.values_list('student_id','number')
        minimum_score = 90
        table = {}
        for line in file:
            line = list(line)
            if int(line[-1]) >= minimum_score:
                if line[1] not in table:
                    table[line[1]] = 1
                else:
                    table[line[1]] += 1
        result = []
        for line in borrow:
            line = list(line)
            line1 = []
            if line[0] in table:
                line1.append(line[1])
                line1.append(table[line[0]])
            result.append(line1)
        data = {'datas':result}

        #籍贯-成绩
        borrow = Associateaward.objects.values_list('id','student_id')
        file = Associate_native_place.objects.values_list('id','student_id','jiguan')
        table, number = self.getdata(file)
        aq, n = self.assdd(table, borrow)
        natice_place = []
        percent = []
        for k, v in aq.items():
            a = k
            b = v / number[k] * 100
            natice_place.append(a)
            percent.append(round(b))
        native_place_data = {'natice_place':natice_place,'percent':percent}

        #学院-性别-成绩
        file1 = AssociateGender.objects.values_list('id', 'student_id', 'gender','collage')
        borrow1 = Associateaward.objects.values_list('id','student_id')
        table, number = self.getdata1(file1)
        aq, n = self.assdd1(table,borrow1)
        datas = []
        for k, v in aq.items():
            lst = []
            a = k[0]
            c = k[1]
            b = v / number[k[1]] * 100
            # print('{},{},{:.2f}%'.format(c, a, b))
            per_collage = []
            per_collage.append(c)
            per_collage.append(a)
            per_collage.append(b)
            datas.append(per_collage)
        datas.sort()
        collage = []
        male_percent = []
        famale_percent = []
        for col in datas:
            if col[0] not in collage:
                collage.append(col[0])
            if col[1] == '男':
                male_percent.append(round(col[2]))
            if col[1] == '女':
                famale_percent.append(round(col[2]))

        collage_datas = {'collage': collage, 'male_percent': male_percent, 'famale_percent': famale_percent}


        #课程-课程
        # ts = time.time()
        score = 70

        file2 = AssociateCourseGrade.objects.values_list('id','student_id','course_id','grade')
        source = AssociateCourse.objects.values_list('course_id','course_name')
        score_table = self.getdata2(file2, score)
        min_support = math.ceil(len(score_table) * 0.4)  # 计算最小支持数，向上取整
        min_confident = 0.6
        # print('Number of Student:', len(score_table))
        # print('Min_Support:', min_support)
        # print('Min_Confident:', min_confident)
        c1, L1, table2, l = self.genl1(score_table, min_support)
        all_ls = []  # 所有频繁项集是列表形式
        all_ls.append(l)  # 将1频繁项集添加到所有的频繁项集中 # TODO
        L = list(L1.keys())  # 部分， 用于生成hash
        C2 = self.hash_l2(table2, L, min_support)
        C2s = self.calc_supportX(C2, score_table)
        mark = self.gen_mark(C2s, L,min_support,all_ls)
        l_next = C2s
        while (len(l_next)):
            for mk, v in mark.items():
                mark[mk] = v - 1
            nd = self.next_gen(l_next, mark, min_support)
            l_next = nd
            mark = self.update_mark(mark)
            if len(l_next) > 0:
                all_ls.append(l_next)
                # print('l_%d length:' % len(all_ls), len(l_next))
                ## 生成k+1项集
                c_next = self.combinationsX(list(mark.keys()), len(all_ls) + 1)
                # print('%%%%', len(c_next))
                l_next = self.calc_supportX(c_next, table2)
        l = all_ls[-1]
        result = []
        for item in l:
            r = self.generate_rules(source, list(item), all_ls, l[item], min_confident)
            result.append(r)
        # print(time.time() - ts)

        # for j in result:
        #     for k in j:
                #print(k)
            # print('-------------------------')

        return render(request, 'adm/associated.html', {
            'data_borrow':json.dumps(data),
            'native_place_data':json.dumps(native_place_data)

        })

    def getdata(self,file):
        table = defaultdict(list)
        number = {}
        for line in file:
            if line[2] not in number:
                number[line[2]] = 1
            else:
                number[line[2]] += 1

            if line[1] not in table:
                table[line[0]].append(line[1])
                table[line[1]].append(line[2])
        for key in table:
            table[key].sort()
        return table, number

    def assdd(self,table, borrow):
        aq = {}
        n = 0
        for line in borrow:
            if line[1] in table:
                n += 1
                if table[line[1]][0] not in aq:
                    aq[table[line[1]][0]] = 1
                else:
                    aq[table[line[1]][0]] += 1
        return aq, n

    def getdata1(self,file):
        table = defaultdict(list)
        number = {}
        for line in file:
            if line[1] not in table:
                table[line[1]].append(line[2])
                table[line[1]].append(line[3])

            if line[3] not in number:
                number[line[3]] = 1
            else:
                number[line[3]] += 1
        return table, number

    def assdd1(self,table,borrow):
        aq = {}
        n = 0
        for line in borrow:
            if line[1] in table:
                n += 1
                if tuple(table[line[1]]) not in aq:
                    aq[tuple(table[line[1]])] = 1
                else:
                    aq[tuple(table[line[1]])] += 1
        return aq, n

    def getdata2(self,file, minimum_score):
        """
        读取csv文件的数据，并根据给定的分数值筛选符合要求的数据，并以字典的形式返回
        :param file_path: 数据文件的存放路径
        :param minimum_score: 符合要求的最低分数值
        :return: 返回table，table的key是学生的学号，每个key对应的value是该学生符合要求的课程
        """
        # with open(file_path) as f:
        #     f_csv = csv.reader(f)
        table = defaultdict(list)  # defaultdict是指字典

        for line in file:  # 读取的是成绩的excel表
            # print(line)
            if int(line[3]) >= minimum_score and line[2] not in table[line[1]]:
                table[line[1]].append(line[2])
        for key in table:
            table[key].sort()
        return table

    #往下是课程-课程
    def genl1(self,table, min_support):
        """
        产生频繁一项集
        :param table: 数据表
        :param min_support: 最小支持度
        :return: 返回频繁一项集:所有: c1; > min_support :l1
        """
        c1 = {}
        keys = []
        table2 = defaultdict(list)
        for stu in table:  # 学号在Table表
            for course in table[stu]:  # 课程在table表中
                if course in c1:
                    c1[course] += 1
                else:
                    keys.append(course)
                    c1[course] = 1
        keys.sort()
        l1 = {}
        l = {}  # TODO
        for key in keys:
            if c1[key] >= min_support:
                l1[key] = c1[key]
                l[(key,)] = c1[key]  # TODO
        # 新table
        for stu in table:
            for course in table[stu]:
                if course in l1:
                    table2[stu].append(course)
        return c1, l1, table2, l

    # ## hash 二项频繁集
    def combination2(self,t0):
        c2 = []
        for tti in range(len(t0)):
            c2.append(list(combinations(t0[tti], 2)))
        # print('c2',c2)     #相当于把所有的分解的数据库展开
        return c2

    def hash_l2(self,table2, L, min_support):
        t = []
        for key, value in table2.items():
            t.append(value)
        t2 = self.combination2(t)
        hashr = [0 for i in range(997)]
        hashbit = [0 for i in range(997)]
        for t2t1 in t2:
            for X in t2t1:
                hash1 = 10 * L.index(X[0]) + L.index(X[1])
                hash1 %= 997
                hashr[hash1] += 1
                if hashr[hash1] > min_support:
                    hashbit[hash1] = 1

        # hash 二项集生成
        L1L1 = list(combinations(L, 2))
        C2 = []
        for y in L1L1:
            hash2 = 10 * L.index(y[0]) + L.index(y[0])
            hash2 %= 997
            if hashbit[hash2] > 0:
                C2.append(y)
        # print('~~~~',len(C2))
        return C2

    # ## 计算二项集支持度
    def calc_supportX(self,C2, table2):
        C2s = {}
        for key in C2:  # 在候选项集中找项集
            for stu in table2:  # table表中的学号
                if set(key).issubset(table2[stu]):  # set(key)是否包含在table[stu]中
                    if key in C2s:
                        C2s[key] += 1
                    else:
                        C2s[key] = 1
        return C2s

    # ## 二项集mark计算
    def gen_mark(self,C2s, L,min_support,all_ls):
        mark = dict(zip(L, [0 for i in range(len(L))]))
        for key, value in C2s.items():
            if value >= min_support:
                for item in key:
                    cnfd = value / all_ls[0][(item,)]  # TODO
                    if cnfd > 0.5:
                        mark[item] += 1
        return mark

    # ## 循环生成多项集
    def next_gen(self,l_next, mark, min_support):
        nd = {}
        for keys, v in l_next.items():
            if v > min_support:
                temp = list(set(keys))
                flag = 1
                for i in range(len(temp)):
                    if mark[temp[i]] < 1:
                        flag = 0
                        break
                if flag:
                    nd[keys] = v
        return nd

    def combinationsX(self,l, t):
        C = []
        C_next = []
        for l in list(combinations(l, t)):
            if set(l) not in C:
                C.append(set(l))
                C_next.append(l)
        return C_next

    # 更新 mark
    def update_mark(self,mark):
        mark_s = {}
        for mk, v in mark.items():
            if v > 0:
                mark_s[mk] = v
        return mark_s

    # ## 关联规则生成
    def generate_rules(self,source, l, all_ls, support, min_confident):
        """
        关联规则生成算法
        :param l: 频繁项集
        :param all_ls: 所有的频繁项集，记录了每个频繁项集的支持度
        :param support: 频繁项集l的支持度
        :param min_confident: 最小置信度

        """
        course = {}
        # with open(source_path) as f:
        #     course_csv = csv.reader(f)
        for line in source:
            course[line[0]] = line[1]
        subsets = []
        length = len(l)
        # print('!!!!!!',length)
        for i in range(1, length):
            subsets.append(list(combinations(l, i)))
        result = []
        for subset in subsets:
            for item in subset:
                tmp = list(set(l) - set(item))
                tmp.sort()
                if item in all_ls[len(item) - 1]:  # TODO
                    cnfd = support / all_ls[len(item) - 1][item]
                    if cnfd >= min_confident:
                        per_result = []
                        a = [course[i] for i in item]
                        b = [course[i] for i in tmp]
                        # print(a, '-->', b, ' 置信度:', cnfd, sep='')
                        per_result.append(a)
                        per_result.append(b)
                        per_result.append(cnfd)
                        result.append(per_result)
        return result

    def has_infrequent_subset(self,c, l_pre):
        """
        根据Apriori算法的先验性质，进行剪枝处理
        :param c: 新生成的候选项K集中的某一项
        :param l_pre: 频繁(k-1)项集
        :return:
        """
        for item in c:  # item是频繁项集中的项
            tmpsubset = list(c - {item})  # tmpsnbset是指频繁项集中的课程代码项
            tmpsubset.sort()  # l_pre.keys()频繁项集，如：odict_keys([('c0103810',), ('c1103001',), ('c1104001',), ('c1106001',)])
            if not {tuple(tmpsubset)}.issubset(
                    set(l_pre.keys())):  # issubset() 方法用于判断集合的所有元素是否都包含在指定集合中，如果是则返回 True，否则返回 False
                return True  # tuple(tmpsubset)}是否包含在l_pre.keys()
        return False

    def apriori_gen(self,l_pre):
        """
        生成候选K项集
        :param l_pre: 频繁K-1项集
        :return: 候选K项集c_next
        """
        keys = list()
        l_pre_key_list = list(l_pre.keys())
        l_pre_key_list.sort()  # 1频繁项集课程代码进行排序
        for idx, item1 in enumerate(
                l_pre_key_list):  # enumerate() 函数用于将一个可遍历的数据对象(如列表、元组或字符串)组合为一个索引序列，同时列出数据和数据下标，一般用在 for 循环当中
            for i in range(idx + 1, len(l_pre_key_list)):  # 在idx+1和1频繁集的长度之间
                item2 = l_pre_key_list[i]
                if item1[:-1] == item2[:-1] and \
                        not self.has_infrequent_subset(set(item1) | set(item2), l_pre):  # has_infrequent_subset调用进行了剪枝
                    item = list(set(item1) | set(item2))
                    item.sort()  # 对项集进行排序
                    keys.append(item)  # keys添加项集
        c_next = OrderedDict((tuple(key), 0) for key in keys)  # OrderedDict,实现了对字典对象中元素的排序，产生C2
        return c_next


#助学进度
class Helplan(View):
    def get(self,request):
        all_sure_student = MyMessage.objects.filter(~Q(favor=''),~Q(favor=None)).all()
        range_code = random.randint(10000, 99999)
        AssitStudy.objects.filter(number=request.user).update(rangeCode=range_code)

        return render(request,'adm/helptables.html',{
            "all_sure_student":all_sure_student,
            'range_code':range_code,
        })