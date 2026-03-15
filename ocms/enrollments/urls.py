from django.urls import path
from .views import *

urlpatterns = [
    path('enrollments/my/', my_enrollments),
    path('enrollments/', enrollment_list),
    path('enrollments/<int:id>/', enrollment_detail),
    path('progress/', lectureprogress_list),
    path('progress/<int:id>/', lectureprogress_detail),
    path('progress/mark/<int:lecture_id>/', mark_lecture_completed),
]