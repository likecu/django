from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse
from django import forms
import os


class login_form(forms.Form):
    # 加入两个字符串，客户端的label名称定义，输入的最大值（指定后无法输入更多字符），输入的最小值（指定后若少于该值会提示），指定错误信息（这是一个字典类型）
    filename = forms.CharField(label='name', min_length=2, max_length=5, error_messages={"required": "文件名不能为空"});
    paths = forms.CharField(label="目录", min_length=2, )


def download_file(request):
    # do something
    if request.method == 'POST':  # 当提交表单时

        form = login_form(request.POST)  # form 包含提交的数据
        if form.is_valid():  # 如果提交的数据合法
            the_file_name = login_form.cleaned_data['filename']  # 显示在弹出对话框中的默认的下载文件名
            filename = login_form.cleaned_data['path']  # 要下载的文件路径

            for root, dirs, files in os.walk("."):
                for file in files:
                    if file == filename:
                        filename = root + "/" + filename
            response = StreamingHttpResponse(readFile(filename))
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)
            return response
    else:
        form = login_form()
    return render(request, 'download.html', {'form': form})


def readFile(filename, chunk_size=512):
    with open(filename, 'rb') as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break
