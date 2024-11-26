from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import torch
import os
from pathlib import Path
from ultralytics import YOLO
from django.http import StreamingHttpResponse
from ultralytics import YOLO
from rest_framework.viewsets import ModelViewSet
from .models import Post
from .serializers import PostSerializer
import cv2
from django.http import StreamingHttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import numpy as np
from django.http import HttpResponse

class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

def yolo_stream_view(request):
    return StreamingHttpResponse(generate_frames(), content_type='multipart/x-mixed-replace; boundary=frame')

def process_frame(frame):

    height, width = frame.shape[:2]
    result_frame = cv2.rectangle(frame, (50, 50), (width - 50, height - 50), (0, 255, 0), 2) 
    return result_frame

# 摄像头流生成器
def generate_frames():
    cap = cv2.VideoCapture(0)  # 打开摄像头
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        processed_frame = process_frame(frame)

        ret, buffer = cv2.imencode('.jpg', processed_frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()

# 实时摄像头流视图
def live_feed(request):
    return StreamingHttpResponse(generate_frames(), content_type='multipart/x-mixed-replace; boundary=frame')

@csrf_exempt
def capture_and_segment(request):
    if request.method == 'POST':
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        if not ret:
            cap.release()
            return JsonResponse({'error': 'Failed to capture frame'})

        # 模拟分割处理（替换为您的分割逻辑）
        processed_frame = process_frame(frame)

        # 保存分割结果
        save_path = 'static/captured_segment.jpg'
        cv2.imwrite(save_path, processed_frame)

        cap.release()
        return JsonResponse({'status': 'success', 'path': f'/{save_path}'})

    return JsonResponse({'error': 'Invalid request method'})