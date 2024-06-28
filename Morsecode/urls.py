from django.contrib import admin
from django.urls import path
from home import views as homeview
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('noadminsallowed/', admin.site.urls),
    path('', homeview.index, name='index'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
