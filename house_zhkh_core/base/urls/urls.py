from django.urls import path

from house_zhkh.base.views.views import CalculatePaymentsView, TaskStatusView

urlpatterns = [
    path('calculate_payments/', CalculatePaymentsView.as_view(), name='calculate_payments'),
    path('task_status/<str:task_id>/', TaskStatusView.as_view(), name='task_status'),
]