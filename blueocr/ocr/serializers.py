from rest_framework import serializers
from blueocr.ocr.models import OcrDocument, OcrResult, OcrUploadedFile


class OcrDocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = OcrDocument
        fields = ('id', 'document_url', 'callback_url', 'method', 'priority', 'state', 'ocr_result', 'created', 'updated')
        read_only_fields = ('id', 'state', 'ocr_result', 'created', 'updated')


class OcrUploadedFileSerializer(serializers.ModelSerializer):

    class Meta:
        model = OcrUploadedFile
        fields = ('id', 'file', 'callback_url', 'priority', 'state', 'ocr_result', 'created', 'updated')
        read_only_fields = ('id', 'state', 'ocr_result', 'created', 'updated')



class OcrResultSerializer(serializers.ModelSerializer):

    class Meta:
        model = OcrResult
        fields = ('id', 'scanned_data', 'state', 'created', 'updated')
        read_only_fields = ('id', 'scanned_data', 'state', 'created', 'updated')
