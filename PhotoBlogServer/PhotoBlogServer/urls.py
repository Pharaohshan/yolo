from django.urls import path
from api.views import yolo_stream_view, capture_and_segment

urlpatterns = [
    path('', yolo_stream_view, name='yolo_stream'), 
    path('capture/', capture_and_segment, name='capture_and_segment'), 
]
