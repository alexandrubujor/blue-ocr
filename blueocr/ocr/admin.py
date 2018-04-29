from django.contrib import admin
from .models import OcrDocument, OcrResult


class OcrDocumentAdmin(admin.ModelAdmin):
    list_display = ['id', 'created', 'state']
    ordering = ['-created']

class OcrResultAdmin(admin.ModelAdmin):
    list_display = ['id', 'ocr_document', 'created']
    ordering = ['-created']


admin.site.register(OcrDocument, OcrDocumentAdmin)
admin.site.register(OcrResult, OcrResultAdmin)
