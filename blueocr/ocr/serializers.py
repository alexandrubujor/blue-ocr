from rest_framework import serializers
from blueocr.ocr.models import OcrDocument, OcrResult


class OcrDocumentSerializer(serializers.ModelSerializer):
    result = serializers.SerializerMethodField()

    class Meta:
        model = OcrDocument
        fields = ('id', 'document_url', 'callback_url', 'priority', 'state', 'result', 'created', 'updated')
        read_only_fields = ('id', 'state', 'result', 'created', 'updated')

    def get_result(self, obj):
        try:
            result = OcrResult.objects.get(ocr_document=obj)
            return result.id
        except OcrResult.DoesNotExist:
            return None


class OcrResultSerializer(serializers.ModelSerializer):

    class Meta:
        model = OcrResult
        fields = ('id', 'ocr_document', 'scanned_data', 'state', 'created', 'updated')
        read_only_fields = ('id', 'ocr_document', 'scanned_data', 'state', 'created', 'updated')