from django.urls import path

from base.views.views import (
    CalculatePaymentsView,
    TaskStatusView,
    PaymentCalculationView,
)

urlpatterns = [
    path('calculate_payment/', PaymentCalculationView.as_view(), name='calculate_payment'),
    path('calculate_payments/', CalculatePaymentsView.as_view(), name='calculate_payments'),
    path('task_status/<str:task_id>/', TaskStatusView.as_view(), name='task_status'),
]