from django.contrib import admin
from .models import OcrDocument, OcrResult, OcrFile


class OcrDocumentAdmin(admin.ModelAdmin):
    list_display = ['id', 'created', 'state']
    ordering = ['-created']


class OcrResultAdmin(admin.ModelAdmin):
    list_display = ['id', 'created']
    ordering = ['-created']


admin.site.register(OcrDocument, OcrDocumentAdmin)
admin.site.register(OcrFile)
admin.site.register(OcrResult, OcrResultAdmin)

