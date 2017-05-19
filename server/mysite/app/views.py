# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import TemplateView

class HomePageView(TemplateView):
    template_name = "index.html"

class MyAccountView(TemplateView):
    template_name = "my_account.html"

class MyGroupsView(TemplateView):
    template_name = "my_groups.html"
