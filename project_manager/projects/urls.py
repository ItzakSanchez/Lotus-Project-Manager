from django.urls import path

from projects.views import ProjectListView

app_name = 'projects'

urlpatterns = [
    path('list', ProjectListView.as_view(), name='list_projects'),
]