from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from .models import AddForm


def home(request):
    h = {'a': "你好", 'b': {"你好嗷嗷", "hahaha", "士大夫撒旦法"}}
    return render(request, 'home.html', {'h': h})


def add(request, a, b):
    c = int(a) + int(b)
    return HttpResponse(str(c))


def index_add(request):
    if request.method == 'POST':  # 当提交表单时

        form = AddForm(request.POST)  # form 包含提交的数据

        if form.is_valid():  # 如果提交的数据合法
            a = form.cleaned_data['a']
            b = form.cleaned_data['b']
            return HttpResponse(str(int(a) + int(b)))

    else:  # 当正常访问时
        form = AddForm()
    return render(request, 'post_form.html', {'form': form})
