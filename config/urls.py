"""config URL Configuration

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
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
]

# 오로지 개발모드에서만 uploads 폴더에서 media 제공
# 배포시에는 볼수 없게 설정 >> 이유 : 디스크 용량을 소비...
if settings.DEBUG:
    # Return a URL pattern for serving files in debug mode. (static에 대한 설명)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
