from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count, Q
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, FormView

from projects.models import Project, Task


# Create your views here.

class ProjectListView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('users:login')
    model = Project
    context_object_name = 'projects'
    template_name = 'projects/list.html'

    def get_queryset(self):
        try:
            query = (Project.objects.filter(user=self.request.user)
                     .annotate(total_tasks=Count('tasks'))
                     .annotate(done_tasks=Count('tasks', filter=Q(tasks__is_completed = True))))
            return query
        except Exception as e:
            print(e)
            return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        projects = context.get('projects')
        for project in projects:
            if project.total_tasks > 0:
                project.progress = round((project.done_tasks / project.total_tasks) * 100, 2)
            else:
                project.progress = '0.0'

        return context

class ProjectDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    login_url = reverse_lazy('users:login')
    model = Project
    template_name = 'projects/detail.html'
    context_object_name = 'project'

    def test_func(self):
        """
        Test if the user is the owner of the project
        """
        project = get_object_or_404(Project,pk=self.kwargs['pk'])
        return project.user == self.request.user

    def get_queryset(self):
        try:
            result = (Project.objects.filter(pk=self.kwargs['pk'])
                      .annotate(total_tasks=Count('tasks'))
                      .annotate(done_tasks=Count('tasks', filter=Q(tasks__is_completed = True))))
            return result
        except Exception as e:
            print(e)
            return None


    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        #Add tasks related to this project
        project = get_object_or_404(Project, id=self.kwargs['pk'])
        tasks = project.tasks.all()
        context['tasks'] = tasks

        #Add tasks details
        project = context.get('project')
        if project.total_tasks > 0:
            project.progress = round(((project.done_tasks / project.total_tasks) * 100), 2)
        else:
            project.progress = 0

        return context

    def post(self, request, *args, **kwargs):
        dict_values = request.POST
        for k,v in dict_values.items():
            if k.isdigit():
                task = get_object_or_404(Task, pk=int(k))
                if task.project.user == self.request.user: # Verify if the task is owned by the current user
                    if dict_values.get(k) == 'on':
                        task.is_completed = True
                    else:
                        task.is_completed = False
                    task.save()
        return redirect(reverse_lazy('projects:detail', kwargs={'pk': self.kwargs.get('pk')}))

class CreateForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description']

class CreateProjectView(LoginRequiredMixin, FormView):
    model = Project
    form_class = CreateForm
    template_name = 'projects/create.html'
    login_url = reverse_lazy('users:login')

    def form_valid(self, form):
        form.instance.user = self.request.user #Assigning the current user to the new Project
        obj = form.save()
        print(obj)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("projects:list")


class UpdateProjectView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    fields = ['title', 'description']
    template_name = 'projects/update.html'
    login_url = reverse_lazy('users:login')

    def get_success_url(self):
        return reverse_lazy("projects:detail", kwargs={"pk": self.object.id})

    def test_func(self):
        """
        Test if the user is the owner of the project
        """
        project = get_object_or_404(Project,pk=self.kwargs['pk'])
        return project.user == self.request.user

class DeleteProjectView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Project
    template_name = 'projects/delete.html'
    success_url = reverse_lazy("projects:list")
    login_url = reverse_lazy('users:login')


    def test_func(self):
        """
        Test if the user is the owner of the project
        """
        project = get_object_or_404(Project,pk=self.kwargs['pk'])
        return project.user == self.request.user


# ==========================
# ======= TASK CRUD ========
# ==========================

class CreateTaskView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Task
    template_name = 'projects/create_task.html'
    fields = ['title', 'description']
    login_url = reverse_lazy('users:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = self.kwargs['pk']
        return context

    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.kwargs['pk'])
        form.instance.project = project
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        self.kwargs['pk'] = self.object.id
        return reverse_lazy("projects:detail", kwargs={"pk": self.object.project.pk})

    def test_func(self):
        project = get_object_or_404(Project, pk=self.kwargs['pk'])
        return project.user == self.request.user # Test if the user is owner of the project which the task is assigned

class DetailTaskView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Task
    template_name = 'projects/detail_task.html'
    context_object_name = 'task'
    login_url = reverse_lazy('users:login')

    def test_func(self):
        task = get_object_or_404(Task, pk=self.kwargs['pk'])
        project = task.project
        return project.user == self.request.user

class UpdateTaskView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    fields = ['title', 'description']
    template_name = 'projects/update_task.html'
    login_url = reverse_lazy('users:login')

    def get_success_url(self):
        return reverse_lazy("projects:detail", kwargs={"pk": self.object.project.pk})

    def test_func(self):
        task = get_object_or_404(Task, pk=self.kwargs['pk'])
        project = task.project
        return project.user == self.request.user

class DeleteTaskView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    template_name = 'projects/delete_task.html'
    login_url = reverse_lazy('users:login')

    def get_success_url(self):
        return reverse_lazy("projects:detail", kwargs={"pk": self.object.project.pk})

    def test_func(self):
        task = get_object_or_404(Task, pk=self.kwargs['pk'])
        project = task.project
        return project.user == self.request.user


