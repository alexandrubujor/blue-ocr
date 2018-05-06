from rest_framework import generics, permissions
from .models import OcrDocument, OcrResult
from .serializers import OcrDocumentSerializer, OcrResultSerializer
from rest_framework.permissions import AllowAny


class OcrDocumentList(generics.ListCreateAPIView):
    model = OcrDocument
    serializer_class = OcrDocumentSerializer
    queryset = OcrDocument.objects.all()
    permission_classes = (AllowAny,)


class OcrDocumentDetail(generics.RetrieveDestroyAPIView):
    model = OcrDocument
    serializer_class = OcrDocumentSerializer
    queryset = OcrDocument.objects.all()
    permission_classes = (AllowAny,)


class OcrResultList(generics.ListAPIView):
    model = OcrResult
    serializer_class = OcrResultSerializer
    queryset = OcrResult.objects.all()
    permission_classes = (AllowAny,)


class OcrResultDetail(generics.RetrieveDestroyAPIView):
    model = OcrResult
    serializer_class = OcrResultSerializer
    queryset = OcrResult.objects.all()
    permission_classes = (AllowAny,)
