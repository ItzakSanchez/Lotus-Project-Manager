from django.urls import path

from projects.views import ProjectListView, ProjectDetailView, CreateProjectView, UpdateProjectView, DeleteProjectView, \
    CreateTaskView, DetailTaskView, UpdateTaskView, DeleteTaskView

app_name = 'projects'

urlpatterns = [
    path('list', ProjectListView.as_view(), name='list'),
    path('detail/<int:pk>', ProjectDetailView.as_view(), name='detail'),
    path('create', CreateProjectView.as_view(), name='create'),
    path('update/<int:pk>', UpdateProjectView.as_view(), name='update'),
    path('delete/<int:pk>', DeleteProjectView.as_view(), name='delete'),
    path('<int:pk>/task/create', CreateTaskView.as_view(), name='create_task'),
    path('task/<int:pk>', DetailTaskView.as_view(), name='detail_task'),
    path('task/update/<int:pk>', UpdateTaskView.as_view(), name='update_task'),
    path('task/delete/<int:pk>', DeleteTaskView.as_view(), name='delete_task'),

]