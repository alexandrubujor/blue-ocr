from rest_framework import generics, permissions
from .models import OcrDocument, OcrResult
from .serializers import OcrDocumentSerializer, OcrResultSerializer


class OcrDocumentList(generics.ListCreateAPIView):
    model = OcrDocument
    serializer_class = OcrDocumentSerializer
    queryset = OcrDocument.objects.all()


class OcrDocumentDetail(generics.RetrieveDestroyAPIView):
    model = OcrDocument
    serializer_class = OcrDocumentSerializer
    queryset = OcrDocument.objects.all()


class OcrResultList(generics.ListAPIView):
    model = OcrResult
    serializer_class = OcrResultSerializer
    queryset = OcrResult.objects.all()


class OcrResultDetail(generics.RetrieveDestroyAPIView):
    model = OcrResult
    serializer_class = OcrResultSerializer
    queryset = OcrResult.objects.all()
