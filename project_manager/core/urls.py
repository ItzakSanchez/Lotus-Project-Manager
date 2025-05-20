from django.urls import path

from core.views import HomePage, AboutPage

app_name = 'core'

urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('about/', AboutPage.as_view(), name='about'),
]