from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView
from django.views import defaults as default_views


urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='dashboard/index.html'), name='index'),

    url(settings.ADMIN_URL, admin.site.urls),
    url(r'^accounts/login/$', LoginView.as_view(), name="login"),
    url(r'^accounts/logout/$', LogoutView.as_view(), name="logout"),

    url(r'^api/', include('apps.api.urls')),

    url(r'^accounts/', include('apps.profile_app.urls')),
    url(r'^orders/', include('apps.order.urls')),
    url(r'^strategy/', include('apps.strategy.urls')),
]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', default_views.bad_request, kwargs={'exception': Exception('Bad Request!')}),
        url(r'^403/$', default_views.permission_denied, kwargs={'exception': Exception('Permission Denied')}),
        url(r'^404/$', default_views.page_not_found, kwargs={'exception': Exception('Page not Found')}),
        url(r'^500/$', default_views.server_error),
    ]
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns = [
            url(r'^__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
