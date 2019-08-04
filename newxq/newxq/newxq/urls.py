"""xqfx URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib.staticfiles.views import serve
from django.views.decorators.csrf import csrf_exempt

import xadmin
from users.views import MyMessageView, LogoutView, LoginView, ConfirmInterestView, ReconfirmIterestView, AutoLogin, \
    AboutTc
from reposityory.views import JobDetailView,ReposityoryView,ArtcleDetailView,ProjectDetailView
from courese.views import CoursetableView, StudentCreaditView, WarmMessageView, CourseAjaxView
from madmin.views import MadminView, Admin_warmView, Studenty_detailView, IndexView, Stududent_likeView, \
    CheckGraduateView, GraduateDetailView, WarmClickView, XqClickView, \
    CreditView, CreditdetailView, AssistView, AdduserView, AdduserdetailView, StatisticalView, StacollageView, \
    AssociateView, AddAssittch, Helplan
from xq_type.views import InterestView
from newxq import settings

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    #管理员学分管理
    url(r'^admcred/$', CreditView.as_view(), name='admcred'),
    # 学生学分管理详情页
    url(r'^admcredetail/(\d+)/$', CreditdetailView.as_view(), name='admcredetail'),
    # 个人中心
    url(r'^main/$', MyMessageView.as_view(), name='main'),
    # 配置login登录
    url(r'^$', LoginView.as_view(), name="login"),
    # 配置退出登录
    url(r'^logout/$', LogoutView.as_view(), name="logout"),
    # 招聘详情页面
    url(r'^jobdetail/(\d+)', JobDetailView.as_view(), name='jobdetail'),
    # 主页面
    url(r'^study/$', ReposityoryView.as_view(), name='study'),
    # 文章的详情页面
    url(r'^artcledetail/(\d+)', ArtcleDetailView.as_view(), name='artcledetail'),
    # 开源项目详情页面
    url(r'^projectdetail/(\d+)', ProjectDetailView.as_view(), name='projectdetail'),
    # 课程中心
    url(r'^course/$', CoursetableView.as_view(), name='course'),
    # 管理员主页面配置
    url(r'^admindex/$', IndexView.as_view(), name='admindex'),
    #ajax配置
    url(r'^index/$',MadminView.as_view(),name='index'),
    #配置预警消息页面
    url(r'^warm/$',Admin_warmView.as_view(),name='warm'),
    #配置预警消息详情页面
    url(r'^warm_detail/(\d+)/$',Studenty_detailView.as_view(),name='warm_detail'),
    #配置兴趣方向
    url(r'^st_like/$',Stududent_likeView.as_view(),name='st_like'),
    #配置毕业审核页面
    url(r'^ckgraduate/$', CheckGraduateView.as_view(), name='ckgraduate'),
    #确定方向
    url(r'^ensuer/$', ConfirmInterestView.as_view(), name='ensuer'),
    #重新选择方向
    url(r'^rechoice/$', ReconfirmIterestView.as_view(), name='rechoice'),
    #个人兴趣展示
    url(r'^inst/$', InterestView.as_view(), name='inst'),
    #学生学分管理
    url(r'^stcred/$', StudentCreaditView.as_view(), name='stcred'),
    #预警消息
    url(r'^warmsg/$', WarmMessageView.as_view(), name='warmsg'),
    #毕业审核详情页面
    url(r'^checkgd/(\d+)/$', GraduateDetailView.as_view(), name='checkgd'),
    #图标的点击ajax请求
    url(r'^stcreditaj/$', CourseAjaxView.as_view(), name='stcreditaj'),

    #管理员页面预警图点击显示详情
    url(r'^warmdet/(\d+)/(.*)/$', WarmClickView.as_view(), name='warmdet'),
    #学情分析图点击详情
    url(r'^xqdetail/(.*)$', XqClickView.as_view(), name='xqdetail'),
    #帮扶计划
    url(r'^assit/$', AssistView.as_view(), name='assit'),
    #修改帮扶老师 AddAssittch
    url(r'^assitch/$', AddAssittch.as_view(), name='assitch'),
    #添加用户
    url(r'^adduser/$', AdduserView.as_view(), name='adduser'),
    #文件上传 AdduserdetailView
    url(r'^adduserdet/$', AdduserdetailView.as_view(), name='adduserdet'),
    #配置media文件缓存
    url(r'^media/(?P<path>.*)$',serve,{'document_root':settings.MEDIA_ROOT}),
    #统计分析
    url(r'^tj/$', StatisticalView.as_view(), name='tj'),
    #统计分析学院
    url(r'^tjcollage/$', StacollageView.as_view(), name='tjcollage'),
    # 关联分析
    url(r'^associate/$', AssociateView.as_view(), name='associate'),

    #助学到学情自动登录
    url(r'^autologin/(\d+)/(.*)/(.*)$', csrf_exempt(AutoLogin.as_view()), name='autologin'),

    #涉及技能
    url(r'^AboutTc/$', AboutTc.as_view(), name='AboutTc'),

    #助学进度
    url(r'^hplan/$', Helplan.as_view(), name='hplan'),

    #插入信息
    # url(r'^insertmsg/$', InsertStudnetMSG.as_view(), name='insertmsg'),

]
# #全局404配置
# handler404 = 'users.views.page_not_found'
# handler500 = 'users.views.page_error'
# handler503 = 'users.views.page_reject'
