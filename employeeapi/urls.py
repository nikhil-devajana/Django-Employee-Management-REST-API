from django.urls import path
from .import views

urlpatterns=[
    path('api/employee/',views.employee_list_view),
    path('api/employee/<int:employee_id>',views.employee_details_view),
]