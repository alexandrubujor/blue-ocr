from django.urls import path
from blueocr.ocr import views

urlpatterns = [
    path('ocrdocument/', views.OcrDocumentList.as_view(), name='ocrdocument-list'),
    path('ocrdocument/<uuid:pk>/', views.OcrDocumentDetail.as_view(), name='ocrdocument-detail'),
    path('ocrresult/', views.OcrResultList.as_view(), name='ocrresult-list'),
    path('ocrresult/<uuid:pk>/', views.OcrResultDetail.as_view(), name='ocrresult-detail'),
    ]