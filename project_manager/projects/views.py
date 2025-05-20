from django.shortcuts import render
from django.views.generic import ListView

from projects.models import Project


# Create your views here.
class ProjectListView(ListView):
    model = Project
    context_object_name = 'projects'
    template_name = 'projects/list.html'
    paginate_by = 10

    # def get_queryset(self):
    #     return Project.objects.filter(user=self.request.user)
