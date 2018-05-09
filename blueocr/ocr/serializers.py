from rest_framework import serializers
from blueocr.ocr.models import OcrDocument, OcrResult, OcrFile


class OcrDocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = OcrDocument
        fields = ('id', 'document_url', 'callback_url', 'method', 'priority', 'state', 'ocr_result', 'created', 'updated')
        read_only_fields = ('id', 'state', 'ocr_result', 'created', 'updated')


class OcrFileSerializer(serializers.ModelSerializer):

    class Meta:
        model = OcrFile
        fields = ('id', 'document', 'callback_url', 'priority', 'state', 'ocr_result', 'created', 'updated')
        read_only_fields = ('id', 'state', 'ocr_result', 'created', 'updated')



class OcrResultSerializer(serializers.ModelSerializer):

    class Meta:
        model = OcrResult
        fields = ('id', 'scanned_data', 'state', 'created', 'updated')
        read_only_fields = ('id', 'scanned_data', 'state', 'created', 'updated')