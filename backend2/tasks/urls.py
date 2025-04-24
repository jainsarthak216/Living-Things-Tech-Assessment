from django.urls import path
from .views import TaskListCreateView, TaskDetailView, TaskExportExcelView

urlpatterns = [
    path('', TaskListCreateView.as_view()),
    path('<int:pk>/', TaskDetailView.as_view()),
    path('export/', TaskExportExcelView.as_view()),
]
