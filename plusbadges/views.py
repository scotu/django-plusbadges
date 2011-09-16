# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
from django.http import HttpResponse, Http404

def plusbadge(request, badge_index, google_profile_id):
    if badge_index != 0:
        raise Http404

    return HttpResponse("")
