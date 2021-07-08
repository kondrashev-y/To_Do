from django.urls import path
from . import views
urlpatterns = [
    path('', views.apiOverview, name="api-overview"),
    path('task-list/', views.TaskListApiViews.as_view(), name="task-list"),
    path('task-detail/<int:pk>/', views.TaskDetailApiViews.as_view(), name="task-Detail"),
    path('task-update/<int:pk>/', views.TaskUpdateApiViews.as_view(), name="task-update"),
    path('task-create/', views.TaskCreateApiViews.as_view(), name="task-Create"),
    path('task-delete/<int:pk>/', views.TaskDestroy.as_view(), name="task-delete"),
    path('task-download/', views.CSVviewSet.as_view(), name="task-download"),
    path('task-upload/', views.FileUploadView.as_view(), name="task-upload"),

  ]