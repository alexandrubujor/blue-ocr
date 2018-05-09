from rest_framework import generics, permissions
from .models import OcrDocument, OcrResult, OcrFile
from .serializers import OcrDocumentSerializer, OcrResultSerializer, OcrFileSerializer
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


class OcrFileList(generics.ListCreateAPIView):
    model = OcrFile
    serializer_class = OcrFileSerializer
    queryset = OcrFile.objects.all()
    permission_classes = (AllowAny,)


class OcrFileDetail(generics.RetrieveDestroyAPIView):
    model = OcrFile
    serializer_class = OcrFileSerializer
    queryset = OcrFile.objects.all()
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
