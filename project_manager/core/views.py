from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.
class HomePage(TemplateView):
    template_name = 'core/home.html'

class AboutPage(TemplateView):
    template_name = 'core/about.html'