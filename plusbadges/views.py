# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
from django.http import Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.conf import settings
from django.template import RequestContext

import httplib2

#from oauth2client.django_orm import Storage
#from oauth2client.client import OAuth2WebServerFlow
#from plusbadges.models import Credentials, Flow
from apiclient.discovery import build

from plusbadges.forms import GoogleIdForm #TODO: google plus library with this form, a generic view for badge and feed, oauth login (future)

#def plusbadge_auth(request, badge_index, google_profile_id):
    #if badge_index != 0:
        #raise Http404
    #storage = Storage(Credentials, 'id', request.user)
    #credential = storage.get()
    #if credential is None or credential.invalid == True:
        #flow = OAuth2WebServerFlow()
        #authorize_url = flow.step1_get_uthorize_url(settings.STEP2_URI)

        #flow_model = Flow(id=request.user, flow=flow)
        #flow_model.save()
        #return HttpResponseRedirect(authorize_url)
    #else:

        #http = httplib2.Http()
        #http = credential.authorize(http)

        ## init client object
        #service = build("plus", "v1", http=http)

        #people_resource = service.people()    
        #people_document = people_resource.get(userId='me').execute()

        #return render_to_response("plusbadges/badge.html", people_document)


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
    AFFIRMATIVE_TUPLE = ("yes", "yea", "yeah")
    if request.GET.get("embed", "no").lower() in AFFIRMATIVE_TUPLE:
        if request.GET.get("fragment","no").lower() in AFFIRMATIVE_TUPLE:
            # not a whole page, just the needed html, js and css (for the javascript badge)
            template = "plusbadges/embeddable_fragment_badge.html"
        else:
            # a whole page, to use in an iframe
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
    }, context_instance=RequestContext(request))

def plusbadges_home(request):
    if request.method == 'POST':
        form = GoogleIdForm(request.POST)
        if form.is_valid():
            google_profile_id = form.cleaned_data['google_profile_id']
            if not google_profile_id:# TODO check if id exists?
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
            

