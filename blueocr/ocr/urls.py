from django.urls import path
from blueocr.ocr import views

urlpatterns = [
    path('ocrdocument/', views.OcrDocumentList.as_view(), name='ocrdocument-list'),
    path('ocrdocument/<uuid:pk>/', views.OcrDocumentDetail.as_view(), name='ocrdocument-detail'),
    path('ocruploadfile/', views.OcrUploadedFileList.as_view(), name='ocruploadfile-list'),
    path('ocruploadfile/<uuid:pk>/', views.OcrUploadedFileDetail.as_view(), name='ocruploadfile-detail'),
    path('ocrfile/', views.OcrUploadedFileList.as_view(), name='ocruploadfile-list'),
    path('ocrfile/<uuid:pk>/', views.OcrUploadedFileDetail.as_view(), name='ocruploadfile-detail'),
    path('ocrresult/', views.OcrResultList.as_view(), name='ocrresult-list'),
    path('ocrresult/<uuid:pk>/', views.OcrResultDetail.as_view(), name='ocrresult-detail'),
    ]