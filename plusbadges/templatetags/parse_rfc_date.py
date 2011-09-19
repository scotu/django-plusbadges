from django import template

from pyrfc3339 import parse

register = template.Library()

def parse_rfc_timestamp(value):
    return parse(value)
    
register.filter("parse_rfc_timestamp", parse_rfc_timestamp)
