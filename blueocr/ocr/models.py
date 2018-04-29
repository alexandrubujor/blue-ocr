from django.db import models
from django.contrib.postgres.fields import JSONField
from django_fsm import FSMField, transition, ConcurrentTransitionMixin
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from celery import current_app
import urllib.request
import os
import uuid
import logging

logger = logging.getLogger(__name__)


class OcrDocument(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    document_url = models.URLField(blank=False)
    callback_url = models.URLField(blank=True)
    priority = models.IntegerField(default=10, blank=False)
    state = FSMField(default='created')
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "OCR Document"
        verbose_name_plural = "OCR Documents"

    def __str__(self):
        return '{}'.format(self.id)

    def create_ocr_task(self):
        current_app.send_task('blueocr.ocr.tasks.scan_document', args=(self.id,))

    def download(self):
        download_dir = settings.TEMP_DOWNLOADS
        download_file, h = urllib.request.urlretrieve(self.document_url, os.path.join(download_dir, "temp-{}".format(self.id)))
        return download_file

    @transition(field=state, source='created', target='processed', on_error='error')
    def enter_processed(self):
        pass

    @transition(field=state, source='created', target='failed', on_error='error')
    def enter_failed(self):
        pass


@receiver(post_save, sender=OcrDocument)
def create_ocr_task(sender, instance, created, **kwargs):
    if created:
        doc = instance
        doc.create_ocr_task()


class OcrResult(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ocr_document = models.OneToOneField(OcrDocument, on_delete=models.CASCADE, blank=False)
    scanned_data = JSONField()
    state = FSMField(default='created')
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "OCR Result"
        verbose_name_plural = "OCR Results"

    def __str__(self):
        return '{}'.format(self.id)