from django.shortcuts import render
from datetime import datetime
import os
from django.shortcuts import redirect
from .download import login_form, list_sys_path
from django import template

register = template.Library()

def upload(request):
    if request.method == 'GET':
        return render(request, 'upload.html')
    else:
        pic = request.FILES.get('pic_file')
        paths = 'upload/{}_{}_{}_'.format(datetime.now().year, '{:02d}'.format(datetime.now().month),
                                          '{:02d}'.format(datetime.now().day))
        path = "learn/static/media/" + paths
        if "png" or "jpg" or "gif" in pic.name:
            if os.path.isfile(path + pic.name):
                os.remove(path + pic.name)
            #     return render(request, 'upload.html')
            with open(path + pic.name, 'wb') as f:
                for c in pic.chunks():  # 相当于切片
                    f.write(c)

        path = "learn/" + paths
        if os.path.isfile(path + pic.name):
            os.remove(path + pic.name)
        #     return render(request, 'upload.html')
        with open(path + pic.name, 'wb') as f:
            for c in pic.chunks():  # 相当于切片
                f.write(c)

        if "png" in pic.name:
            return render(request, 'upload.html',
                          {"img_all": {"imgs": {"url": str('media/' + paths + pic.name)}}})

    return render(request, 'download.html',
                  {'login_form': login_form(), 'list_sys_path': list_sys_path("./learn/upload")})
