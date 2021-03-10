"""dj_learn URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from learn import views as learn_views  # new
from django.conf.urls import include, url
from learn import download, upload
from django.views.static import serve
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', learn_views.home, name="home"),  # new
    path('admin/', admin.site.urls),
    path('add/<int:a>/<int:b>/', learn_views.add, name='add'),
    url('help/', learn_views.index_add, name='add'),
    url('download/', download.download_file, name="download"),
    url('upload/', upload.upload, name="upload"),
    url('upload', upload.upload, name="upload"),
    url('static_pic/', serve, {'document_root': 'learn/upload'}),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
