# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.conf import settings

import httplib2

from apiclient.discovery import build



def plusbadge(request, badge_index, google_profile_id):
    try:
        badge_index = int(badge_index)
    except:
        raise Http404

    if badge_index != 0:
        raise Http404

    http = httplib2.Http()

    # init client object
    service = build("plus", "v1", http=http, developerKey=settings.GOOGLE_API_KEY)

    people_resource = service.people()
    
    activities_resource = service.activities()
    
    try:
        people_document = people_resource.get(userId=google_profile_id).execute(http)
        
        activities_document = activities_resource.list(userId=google_profile_id, collection="public", maxResults=1).execute()
        post_list = None
        if 'items' in activities_document:
            post_list = activities_document["items"]

        return render_to_response("plusbadges/badge.html", {
            "person": {
                "displayName": people_document["displayName"],
                "image":{"url": people_document["image"]["url"]},
                "tagline": people_document["tagline"],
                "post_list": post_list
            }
            })
    except:
        return HttpResponse("Error trying to display id %s." % google_profile_id)

