from datetime import datetime

from django import forms
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, FormView

from projects.models import Project, Task


# Create your views here.
class ProjectListView(ListView):
    model = Project
    context_object_name = 'projects'
    template_name = 'projects/list.html'

    # def get_queryset(self):
    #     return Project.objects.filter(user=self.request.user)

class ProjectDetailView(DetailView):
    model = Project
    template_name = 'projects/detail.html'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['tasks'] = get_list_or_404(Task, project=self.get_object())
        return context

class CreateForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description']

class CreateProjectView(FormView):
    model = Project
    form_class = CreateForm
    template_name = 'projects/create.html'

    def form_valid(self, form):
        #form.instance.user = self.request.user
        obj = form.save()
        print(obj)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("projects:list")

class UpdateProjectView(UpdateView):
    model = Project
    fields = ['title', 'description']
    template_name = 'projects/update.html'

    def get_success_url(self):
        return reverse_lazy("projects:detail", kwargs={"pk": self.object.id})

class DeleteProjectView(DeleteView):
    model = Project
    template_name = 'projects/delete.html'
    success_url = reverse_lazy("projects:list")


# ==========================
# ======= TASK CRUD ========
# ==========================

class CreateTaskView(CreateView):
    model = Task
    template_name = 'projects/create_task.html'
    fields = ['title', 'description']

    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.kwargs['pk'])
        form.instance.project = project
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        self.kwargs['pk'] = self.object.id
        return reverse_lazy("projects:detail", kwargs={"pk": self.object.project.pk})

class DetailTaskView(DetailView):
    model = Task
    template_name = 'projects/detail_task.html'
    context_object_name = 'task'


class UpdateTaskView(UpdateView):
    model = Task
    fields = ['title', 'description']
    template_name = 'projects/update_task.html'

    def get_success_url(self):
        return reverse_lazy("projects:detail", kwargs={"pk": self.object.project.pk})

class DeleteTaskView(DeleteView):
    model = Task
    template_name = 'projects/delete_task.html'

    def get_success_url(self):
        return reverse_lazy("projects:detail", kwargs={"pk": self.object.project.pk})
