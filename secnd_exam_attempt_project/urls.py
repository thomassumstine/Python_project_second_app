from django.conf.urls import url, include

urlpatterns = [
    url(r'^', include('apps.second_exam_attempt_app.urls')),
]