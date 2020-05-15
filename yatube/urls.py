from django.conf import settings
from django.contrib import admin
from django.contrib.flatpages import views
from django.urls import include, path
from django.views.defaults import page_not_found

urlpatterns = [
    path('auth/', include('users.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('about/', include('django.contrib.flatpages.urls')),
]

urlpatterns += [
    path('about-us/', views.flatpage, {'url': '/about-us/'}, name='about'),
    path('terms/', views.flatpage, {'url': '/terms/'}, name='terms'),
    path('about-author/', views.flatpage,
         {'url': '/about-author/'}, name='about-author'),
    path('about-spec/', views.flatpage,
         {'url': '/about-spec/'}, name='about-spec'),
    path('', include('posts.urls')),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns


def error404(request, exception):
    return page_not_found(request, exception,
                          template_name='errors/404.html')


handler404 = error404
