from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse
from django import forms
import os
import logging


class login_form(forms.Form):
    # 加入两个字符串，客户端的label名称定义，输入的最大值（指定后无法输入更多字符），输入的最小值（指定后若少于该值会提示），指定错误信息（这是一个字典类型）
    filename = forms.CharField(label='name', min_length=2, max_length=10000, error_messages={"required": "文件名不能为空"});
    paths = forms.CharField(label="目录", min_length=0, required=False)


def list_sys_path(current_dir="./learn/media/", deep=0):
    file_lists = []
    dir_list = os.listdir(current_dir)
    # traverse folder first.
    path_list, file_list = [], []
    for dir in dir_list:
        path = os.path.join(current_dir, dir)
        if os.path.isdir(path):
            path_list.append(dir)
        else:
            file_list.append(dir)
    dir_list = path_list + file_list

    # traverse all dir.
    for dir in dir_list:
        path = os.path.join(current_dir, dir)
        if os.path.isdir(path):
            # do something to this directory
            file_lists.append(" " * deep + dir)
            for i in list_sys_path(path, deep + 1):
                file_lists.append(i)
        if os.path.isfile(path):
            # do something to this file
            file_lists.append(" " * deep + "|--" + dir)
    return file_lists


def download_file(request):
    # do something
    if request.method == 'POST':  # 当提交表单时
        logging.debug("aaa")
        form = login_form(request.POST)  # form 包含提交的数据
        if form.is_valid():  # 如果提交的数据合法
            the_file_name = form.cleaned_data.get('filename')  # 显示在弹出对话框中的默认的下载文件名
            file_path = form.cleaned_data.get('paths')  # 要下载的文件路径
            t = 0  # 判断是否匹配到文件
            this_path = "./learn/media/"

            for root, dirs, files in os.walk(this_path):
                for file in files:
                    if file == the_file_name and file_path in root:
                        the_file_name = this_path + root + "/" + file
                        t = 1
            if t == 0:
                for root, dirs, files in os.walk("."):
                    for file in files:
                        if file == the_file_name:
                            the_file_name = this_path + root + "/" + file
                            t = 1
            if t == 0:
                for root, dirs, files in os.walk("."):
                    for file in files:
                        if str(the_file_name) in str(file):
                            the_file_name = this_path + root + "/" + file
                            t = 1
            if t == 1:
                response = StreamingHttpResponse(readFile(the_file_name))
                response['Content-Type'] = 'application/octet-stream'
                response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)
                return response
            else:
                return render(request, 'download.html', {'login_form': login_form(), 'list_sys_path': list_sys_path()})
    else:
        form = login_form()
    return render(request, 'download.html', {'login_form': form, 'list_sys_path': list_sys_path()})


def readFile(filename, chunk_size=512):
    with open(filename, 'rb') as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break
