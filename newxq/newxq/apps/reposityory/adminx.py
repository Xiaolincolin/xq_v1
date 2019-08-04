"""
author: Colin
@time: 2018-11-28 15:03
explain:

"""
import xadmin
from .models import HotProject, Artcle,HotJob,Banner,BorrowBook


class artcleXadmin(object):
    list_display = ['title', 'url',  'click_times', 'content', 'type_name', 'add_time']
    search_fields = ['title', 'url', 'content', 'type_name', 'click_times']
    list_filter = ['title', 'url', 'content', 'type_name', 'click_times', 'add_time']
    list_per_page = 20
    model_icon = 'fa fa-fire'


class HotJobXadmin(object):
    list_display = ['id', 'title', 'salary', 'type_name', 'click_times', 'url', 'content', 'add_time']
    search_fields = ['title', 'salary', 'type_name', 'click_times', 'url', 'content']
    list_filter = ['title', 'salary', 'type_name', 'click_times', 'url', 'content', 'add_time']
    list_per_page = 20
    model_icon = 'fa fa-gavel'


class HotProjectXadmin(object):
    list_display = ['title', 'url', 'type_name', 'click_times', 'content', 'add_time']
    search_fields = ['title', 'url', 'type_name', 'click_times', 'content']
    list_filter = ['title', 'url', 'type_name', 'click_times', 'content', 'add_time']
    list_per_page = 20
    model_icon = 'fa fa-tasks'


class BorrowBookXadmin(object):
    list_display = ['st_id', 'title', 'type_name', 'borrow_times', 'add_time']
    search_fields = ['st_id', 'title', 'type_name', 'borrow_times']
    list_filter = ['st_id', 'title', 'type_name', 'borrow_times', 'add_time']
    list_per_page = 20
    model_icon = 'fa fa-book'


# class BannerXadmin(object):
#     list_display = ['title', 'index', 'type_name','image', 'url', 'content', 'add_time']
#     search_fields = ['title', 'url','type_name', 'index', ]
#     list_filter = ['title', 'type_name', 'image', 'url', 'index', 'add_time']
#     list_per_page = 20
#     model_icon = 'fa fa-lightbulb-o'



xadmin.site.register(Artcle, artcleXadmin)
xadmin.site.register(HotJob, HotJobXadmin)
xadmin.site.register(HotProject, HotProjectXadmin)
# xadmin.site.register(Banner, BannerXadmin)
xadmin.site.register(BorrowBook, BorrowBookXadmin)