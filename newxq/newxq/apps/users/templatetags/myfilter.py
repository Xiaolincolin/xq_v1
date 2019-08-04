"""
author: Colin
@time: 2019-04-06 15:14
explain:

"""


from django import template
register = template.Library()

def isNone(value):
    if value:
        return "yes"
    else:
        return None

def replace_str(value):
    strs = value
    if type(value)==str:
        strs = strs.replace('"', '')
    return strs

register.filter("isNone",isNone)
register.filter("replace_str",replace_str)