# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('plusbadges.views',
    url(r'^$', 'plusbadges_home', name='plusbadges_home'),
    url(r'^(?P<badge_index>\d+)/(?P<google_profile_id>\d+)/$', 'plusbadge', name='plusbadges_badge'),
)

