# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, url
from django.conf import settings


urlpatterns = patterns('solver.views',
    url(r'^$', 'solve', name='solve'),
)


if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
            }),
    )
