"""
author: Colin
@time: 2019-03-12 16:06
explain:

"""
from django import forms



class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)
    is_admin = forms.CharField(required=True)