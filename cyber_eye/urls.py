from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('home.urls')),
    path('', include('users.urls')),
    path('', include('quiz.urls')),
    path('', include('social_media.main_urls')),

    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
]

handler400 = 'home.views.error_400'
handler403 = 'home.views.error_403'
handler404 = 'home.views.error_404'
handler500 = 'home.views.error_500'
