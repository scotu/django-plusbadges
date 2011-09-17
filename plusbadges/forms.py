# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
from django import forms

class GoogleIdForm(forms.Form):
    google_profile_id = forms.RegexField(regex=r'\d+')
