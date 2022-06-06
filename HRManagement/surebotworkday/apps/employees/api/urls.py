from django.urls import path


from surebotworkday.apps.employees.api.views import *


urlpatterns = [
    path('details', employeeDetails.as_view()),
    path('list', employeeList.as_view()),
]