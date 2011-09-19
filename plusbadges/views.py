# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.conf import settings
from django.template import RequestContext

import httplib2

from apiclient.discovery import build

from plusbadges.forms import GoogleIdForm



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
    
    template = "plusbadges/badge.html"
    if request.GET.get("embed", "no") == "yes":
        template = "plusbadges/embeddable_badge.html"
    
    people_document = people_resource.get(userId=google_profile_id).execute(http)
    
    activities_document = activities_resource.list(userId=google_profile_id, collection="public", maxResults=1).execute()
    post_list = None
    if 'items' in activities_document:
        post_list = activities_document["items"]
        
    return render_to_response(template, {
        "person": {
            "id": people_document["id"],
            "displayName": people_document["displayName"],
            "image":{"url": people_document.get("image", {"url":""}).get("url")},
            "tagline": people_document.get("tagline", ""),
            "post_list": post_list
        }
        })

def plusbadges_home(request):
    if request.method == 'POST':
        form = GoogleIdForm(request.POST)
        if form.is_valid():
            google_profile_id = form.cleaned_data['google_profile_id']
            if not google_profile_id:
                return HttpResponseRedirect(reverse("plusbadges_home"))
            return HttpResponseRedirect(reverse("plusbadges_badge", kwargs={"badge_index": 0,"google_profile_id":google_profile_id}))
        else:
            return render_to_response("plusbadges/create_badge.html",
                {"form": form},
                context_instance=RequestContext(request))
    else:
        form = GoogleIdForm()
        return render_to_response("plusbadges/create_badge.html",
            {"form": form},
            context_instance=RequestContext(request))
            

